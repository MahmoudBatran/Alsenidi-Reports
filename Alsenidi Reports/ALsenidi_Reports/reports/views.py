from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Report, ReportSection, SectionPermission
from .forms import ReportForm
from django.core.mail import send_mail
from django.conf import settings

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('report_list')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    return render(request, 'reports/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'اسم المستخدم موجود بالفعل.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'البريد الإلكتروني مستخدم من قبل.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False  # حساب غير مفعل حتى يتم تفعيله من الأدمن
            user.save()

            admin_email = settings.ADMINS[0][1] if settings.ADMINS else None
            if admin_email:
                send_mail(
                    subject='مستخدم جديد يحتاج تفعيل',
                    message=f'تم تسجيل مستخدم جديد: {username} ({email}). الرجاء تفعيل الحساب.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin_email],
                    fail_silently=True,
                )

            messages.success(request, 'تم التسجيل بنجاح. سيتم تفعيل حسابك من قبل الأدمن.')
            return redirect('login')

    return render(request, 'reports/register.html')

@login_required
def report_list(request):
    user = request.user
    section_code = request.GET.get('section', 'all')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # لو المستخدم سوبر يوزر، يشوف كل الأقسام
    if user.is_superuser:
        allowed_sections = ReportSection.objects.all()
    else:
        allowed_sections = ReportSection.objects.filter(
            sectionpermission__user=user
        ).distinct()

    reports = Report.objects.filter(section__in=allowed_sections)

    if section_code != 'all':
        reports = reports.filter(section__code=section_code)

    if date_from:
        reports = reports.filter(created_at__date__gte=date_from)
    if date_to:
        reports = reports.filter(created_at__date__lte=date_to)

    context = {
        'reports': reports.order_by('-created_at'),
        'sections': allowed_sections,
        'selected_section': section_code,
        'date_from': date_from or '',
        'date_to': date_to or '',
    }
    return render(request, 'reports/report_list.html', context)

@login_required
def upload_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            # يمكن ربط التقرير بالمستخدم إذا أردت:
            # report.uploaded_by = request.user
            report.save()
            messages.success(request, 'تم رفع التقرير بنجاح')
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'reports/upload_report.html', {'form': form})

@login_required
def manage_permissions(request):
    user = request.user

    # السماح فقط للـ superuser بالدخول لصفحة إدارة الصلاحيات
    if not user.is_superuser:
        messages.error(request, 'ليس لديك صلاحية الدخول لهذه الصفحة.')
        return redirect('report_list')

    users = User.objects.exclude(is_superuser=True)
    sections = ReportSection.objects.all()

    if request.method == 'POST':
        # حفظ الصلاحيات
        for u in users:
            for s in sections:
                checkbox_name = f'user_{u.id}_section_{s.id}'
                has_permission = checkbox_name in request.POST

                permission_qs = SectionPermission.objects.filter(user=u, section=s)

                if has_permission and not permission_qs.exists():
                    SectionPermission.objects.create(user=u, section=s)
                elif not has_permission and permission_qs.exists():
                    permission_qs.delete()

        messages.success(request, 'تم تحديث صلاحيات الأقسام بنجاح.')
        return redirect('manage_permissions')

    # تجهيز بيانات الصلاحيات للعرض
    permissions = {
        u.id: set(
            SectionPermission.objects.filter(user=u).values_list('section_id', flat=True)
        ) for u in users
    }

    context = {
        'users': users,
        'sections': sections,
        'permissions': permissions,
    }
    return render(request, 'reports/manage_permissions.html', context)
