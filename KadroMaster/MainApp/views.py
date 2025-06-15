from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from MainApp.models import *
from MainApp.forms import *
from django.db.models import Q, F, Count, Sum
from django.http import JsonResponse
import random, datetime, calendar
from passlib.hash import django_pbkdf2_sha256
from django.utils import timezone
from django.db import connection
from datetime import date, datetime, timedelta, time
from collections import defaultdict

def profile_hr(request):
    departments = Departments.objects.all()
    if not request.user.is_authenticated:
        return redirect("login")
    
    try:
        if request.user.group.access_for_emplyees == 1 or request.user.is_superuser == 1:
            employeers = Employees.objects.all()
        else:
            employeers = Employees.objects.filter(job__departament_id=request.user.employee.job.departament.id)
            departments = Departments.objects.filter(id=request.user.employee.job.departament.id)
    except:
        employeers = Employees.objects.all()
    if request.method == 'POST':
        if request.GET.get("delete") is not None:
            Employees.objects.filter(id=request.GET.get("delete")).delete()
            return redirect("profile")
        try:
            if request.POST.get('fullname') and request.POST.get('p_number'):
                employeers = Employees.objects.filter(Q(fullname__contains=request.POST.get('fullname')) & Q(personnel_number__contains=request.POST.get('p_number')))
            elif request.POST.get('fullname'):
                employeers = Employees.objects.filter(fullname__contains=request.POST.get('fullname'))
            elif request.POST.get('departament_id'):
                employeers = Employees.objects.filter(job__departament_id=request.POST.get('departament_id'))
            else:
                employeers = Employees.objects.filter(personnel_number__contains=request.POST.get('p_number'))
        except:
            pass

    return render(request, 'MainApp/main.html', {'employeers': employeers, 'departments': departments})

def auth_hr(request):
    if request.user.is_authenticated:
        return redirect('profile')

    users = User.objects.filter(password__isnull=False)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                error_message = "Неправильный пароль!"
                return render(request, 'MainApp/login.html', {'error_message': error_message, 'users': users})

    return render(request, 'MainApp/login.html', {'users': users})

def department_hr(request):
    departments = Departments.objects.annotate(employee_count=Count('jobs__employees')).prefetch_related('jobs_set')
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == 'POST':
        if 'add' in request.POST:
            department_new = Departments()
            department_new.title = request.POST.get('title')
            try:
                department_new.save()
            except:
                return render(request, 'MainApp/department.html', {'departments': departments, 'error': 'Данный отдел уже существует'})
        elif 'find' in request.POST:
            departments = Departments.objects.filter(title__contains=request.POST.get('title')).annotate(employee_count=Count('jobs__employees')).prefetch_related('jobs_set')
        elif 'delete' in request.GET:
            count_of_jobs = Jobs.objects.filter(departament=Departments.objects.filter(id=request.GET.get("delete")).first()).count()
            if count_of_jobs == 0:
                Departments.objects.filter(id=request.GET.get("delete")).delete()
            else:
                return render(request, 'MainApp/department.html', {'departments': departments, 'error': 'Необходимо удалить все должности'})
    return render(request, 'MainApp/department.html', {'departments': departments})

def job_hr(request):
    departments = Departments.objects.all()
    jobs = Jobs.objects.all().prefetch_related('employees_set')
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == 'POST':
        if 'add' in request.POST:
            job_new = Jobs()
            job_new.title = request.POST.get('title')
            job_new.salary_per_hour = request.POST.get('salary_per_hour')
            job_new.departament = Departments.objects.filter(id=request.POST.get('departament_id')).first()
            try:
                job_new.save()
            except:
                pass
        elif 'find' in request.POST:
            filter_params = {
            'title__contains': request.POST.get('title'),
            'salary_per_hour__contains': request.POST.get('salary_per_hour'),
            'departament_id': request.POST.get('departament_id'),
            }
            filter_params = {k: v for k, v in filter_params.items() if v is not None}
            jobs = Jobs.objects.filter(**filter_params).prefetch_related('employees_set')
        elif 'delete' in request.GET:
            try:
                Jobs.objects.filter(Q(id=request.GET.get("delete"))).delete()
            except:
                return render(request, 'MainApp/job.html', {'departments': departments, 'jobs': jobs, 'error': 'Необходимо уволить всех сотрудников на должности'})
    return render(request, 'MainApp/job.html', {'departments': departments, 'jobs': jobs})

def password_hr(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'MainApp/password.html', {'form': form})

def personal_hr(request):
    if not request.user.is_authenticated:
        return redirect("login")
    departments = Departments.objects.all()

    if request.method == 'POST':
        form = AddEmployee(request.POST)
        if form.is_valid():
            db = form.save(commit=False)
            if request.POST['military_ticket']:
                db.military_ticket = request.POST['military_ticket']
            db.personnel_number = random.randint(100000,999999)
            db.save()
    return render(request, 'MainApp/personal.html', {'departments': departments})

def get_job_titles(request):
    department_id = request.GET.get('department')
    if department_id:
        jobs = Jobs.objects.filter(departament_id=department_id)
    else:
        jobs = Jobs.objects.none()
    
    data = [{'id': job.id, 'title': job.title} for job in jobs]
    return JsonResponse(data, safe=False)

def time_tracking_hr(request):
    if not request.user.is_authenticated:
        return redirect("login")
    employeers = Employees.objects.filter(job__departament_id=request.user.employee.job.departament.id)
    time_tracking = TimeTraking.objects.filter(employee__job__departament_id=request.user.employee.job.departament.id).order_by('-date')
    if request.method == 'POST':
        if 'add' in request.POST:
            time_tracking_new = TimeTraking()
            time_tracking_new.date = request.POST.get('date')
            time_tracking_new.amount = request.POST.get('amount')
            time_tracking_new.employee = Employees.objects.filter(id=request.POST.get('employee')).first()
            try:
                time_tracking_new.save()
            except:
                pass
        elif 'find' in request.POST:
            filter_params = {
            'date': request.POST.get('date'),
            'amount': request.POST.get('amount'),
            'employee_id': request.POST.get('employee'),
            }
            filter_params = {k: v for k, v in filter_params.items() if v is not None and v != ''}
            time_tracking = TimeTraking.objects.filter(**filter_params).filter(employee__job__departament_id=request.user.employee.job.departament.id).order_by('-date')
        elif 'delete' in request.GET:
            TimeTraking.objects.filter(id=request.GET.get("delete")).delete()
    return render(request, 'MainApp/time_tracking.html', {'employeers': employeers, 'time_tracking': time_tracking})

def info_personal_hr(request, id):
    if not request.user.is_authenticated:
        return redirect("login")
    departments = Departments.objects.all()
    employee = Employees.objects.filter(id=id).first()
    if request.method == 'POST':
        if 'new' in request.POST:
            if request.POST.get('job') is not None:
                employee.job = Jobs.objects.filter(id=request.POST.get('job')).first()
            employee.fullname = request.POST.get('fullname')
            employee.birthday = request.POST.get('birthday')
            employee.gender = request.POST.get('gender')
            employee.phone = request.POST.get('phone')
            employee.residence_address = request.POST.get('residence_address')
            employee.passport = request.POST.get('passport')
            employee.insurance_number = request.POST.get('insurance_number')
            employee.individual_tax_number = request.POST.get('individual_tax_number')
            employee.work_book_number = request.POST.get('work_book_number')
            employee.military_ticket = request.POST.get('military_ticket')
            employee.email = request.POST.get('email')
            employee.employment_date = request.POST.get('employment_date')
            employee.save()
            return redirect("info-personal", id=id)
    return render(request, 'MainApp/info_personal.html', {'departments': departments, 'employee': employee})

def salary_hr(request, id):
    if not request.user.is_authenticated:
        return redirect("login")
    salaries = Salary.objects.filter(employee=id)
    if request.POST:
        if 'add' in request.POST:
            if request.POST.get('from') > request.POST.get('before'):
                return render(request, 'MainApp/report_salary.html', {'salaries': salaries, 'error': 'Период с не должен превышать периода до'})
            else:
                employee_salary_hour = Employees.objects.filter(id=id).first().job.salary_per_hour
                employee_amount_hours = TimeTraking.objects.filter(employee=id, date__range=(request.POST.get('from'), request.POST.get('before'))).aggregate(Sum('amount'))['amount__sum']
                employee_final_salary = employee_salary_hour * employee_amount_hours
                current_date = datetime.now().strftime('%Y-%m-%d')
                Salary.objects.create(salary_date=current_date, number_of_hours_worked=employee_amount_hours, final_salary=employee_final_salary, employee=Employees.objects.filter(id=id).first())
    return render(request, 'MainApp/report_salary.html', {'salaries': salaries})

def groups_admin(request):
    if not request.user.is_authenticated:
        return redirect("login")
    groups = Groups.objects.all().prefetch_related('user_set')
    if request.POST:
        if 'add' in request.POST:
            group_new = Groups()
            if request.POST.get('role-name') is not None:
                group_new.title = request.POST.get('role-name')
            if request.POST.get('personal') is not None:
                group_new.access_for_emplyees = request.POST.get('personal')
            if request.POST.get('department') is not None:
                group_new.access_for_departments = request.POST.get('department')
            if request.POST.get('job') is not None:
                group_new.access_for_jobs = request.POST.get('job')
            if request.POST.get('reports') is not None:
                group_new.access_for_reports = request.POST.get('reports')
            if request.POST.get('time') is not None:
                group_new.access_for_time = request.POST.get('time')
            group_new.save()
        elif 'delete' in request.GET:
            try:
                Groups.objects.filter(id=request.GET.get("delete")).delete()
                return redirect("groups")
            except:
                return render(request, 'MainApp/groups_for_users.html', {'groups': groups, 'error': 'Необходимо удалить всех пользователей из группы'})
    return render(request, 'MainApp/groups_for_users.html', {'groups': groups})

def users_admin(request):
    if not request.user.is_authenticated:
        return redirect("login")
    groups = Groups.objects.all()
    employees = Employees.objects.all()
    users = User.objects.all()
    if request.POST:
        if 'create_user' in request.POST:
            user_new = User()
            user_new.password = django_pbkdf2_sha256.hash(request.POST.get('password'), rounds=320000)
            user_new.username = Employees.objects.filter(id=request.POST.get('employee')).first().fullname
            user_new.group = Groups.objects.filter(id=request.POST.get('role')).first()
            user_new.employee = Employees.objects.filter(id=request.POST.get('employee')).first()
            try:
                user_new.save()
            except:
                pass
        elif 'delete' in request.GET:
            User.objects.filter(id=request.GET.get("delete")).delete()
            return redirect("users")
    return render(request, 'MainApp/add_user.html', {'groups': groups, 'employees': employees, 'users': users})

def count_work_days(year, month):
    # Получаем количество дней в месяце
    _, days_in_month = calendar.monthrange(year, month)

    work_days = 0
    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)
        # Проверяем, не является ли день субботой (5) или воскресеньем (6)
        if current_date.weekday() < 5:  # 0-4 — понедельник-пятница
            work_days += 1

    return work_days

def calculate_work_time(employee_id, year, month):
    """
    Возвращает отформатированное рабочее время для сотрудника за указанный месяц.
    Учитывает возможные перерывы (например, обед) в течение дня.
    Формат: "чч:мм:сс"
    """

    # Определяем временной диапазон месяца
    start_date = timezone.make_aware(datetime(year, month, 1))
    end_date = timezone.make_aware(datetime(
        year + 1 if month == 12 else year,
        1 if month == 12 else month + 1,
        1, 23, 59, 59
    ))

    # Получаем и сортируем все записи за период
    records = AccessControl.objects.filter(
        employee_id=employee_id,
        date__range=(start_date, end_date)
    ).order_by('date')

    total_time = timedelta()
    pending_ins = []  # Необработанные отметки входа
    last_date = None  # Для контроля смены дня

    for record in records:
        current_date = record.date.date()
        
        # Если день сменился, сбрасываем необработанные входы
        if last_date is not None and current_date != last_date:
            pending_ins = []
        
        last_date = current_date
        
        if record.state == 'in':
            pending_ins.append(record.date)
        elif record.state == 'out' and pending_ins:
            # Берем последний необработанный вход
            in_time = pending_ins.pop(0)
            # Учитываем только если выход после входа
            if record.date > in_time:
                total_time += record.date - in_time

    # Форматируем результат
    total_seconds = int(total_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_attendance_stats(employee_id, year, month):
    """
    Возвращает количество опозданий и ранних уходов за месяц.
    Опоздание - приход после 9:00, ранний уход - уход до 18:00.
    Возвращает: {'total_late': X, 'total_early': Y}
    """
    # Определяем временной диапазон месяца
    start_date = timezone.make_aware(datetime(year, month, 1))
    end_date = timezone.make_aware(datetime(
        year + 1 if month == 12 else year,
        1 if month == 12 else month + 1,
        1, 23, 59, 59
    ))

    # Получаем все отметки за период
    records = AccessControl.objects.filter(
        employee_id=employee_id,
        date__range=(start_date, end_date)
    ).order_by('date')

    result = {'total_late': 0, 'total_early': 0}
    current_day = None
    first_in = None
    last_out = None

    for record in records:
        record_day = record.date.date()
        
        # Если день сменился, анализируем предыдущий день
        if current_day is not None and record_day != current_day:
            if first_in and first_in.time() > time(9, 0):
                result['total_late'] += 1
            if last_out and last_out.time() < time(18, 0):
                result['total_early'] += 1
            first_in, last_out = None, None
        
        current_day = record_day
        
        # Обновляем первый приход/последний уход
        if record.state == 'in':
            if first_in is None or record.date < first_in:
                first_in = record.date
        elif record.state == 'out':
            if last_out is None or record.date > last_out:
                last_out = record.date

    # Анализируем последний день
    if current_day:
        if first_in and first_in.time() > time(9, 0):
            result['total_late'] += 1
        if last_out and last_out.time() < time(18, 0):
            result['total_early'] += 1

    return result

def stats_hr(request):
    employees = None
    department = 'Отдел'
    month = 'Месяц'
    hours = ''
    MONTH_NAMES = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
    }
    if not request.user.is_authenticated:
        return redirect("login")
    departments = Departments.objects.all()
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT EXTRACT(MONTH FROM date) AS month FROM mainapp_accesscontrol")
        rows = cursor.fetchall()
    months = [{'id': mid, 'name': MONTH_NAMES.get(mid, 'Неизвестный месяц')} for mid in sorted([row[0] for row in rows])]
    if request.POST:
        if 'find' in request.POST:
            employees_tmp = Employees.objects.filter(job__departament_id=request.POST.get('department'))
            department = Departments.objects.filter(id=request.POST.get('department')).first()
            month = MONTH_NAMES.get(int(request.POST.get('month')))
            hours = count_work_days(2025, int(request.POST.get('month'))) * 8
            employees = []
            for emp in employees_tmp:
                total_time = calculate_work_time(int(emp.id), 2025, int(request.POST.get('month')))
                stats = get_attendance_stats(int(emp.id), 2025, int(request.POST.get('month')))
                warning_var = None
                if int(hours) > int(total_time.split(':')[:-2][0]):
                    warning_var = 'warning'
                employees.append({
                    'id': emp.id,
                    'fullname': emp.fullname,
                    'job_title': emp.job.title,
                    'total_time': total_time,
                    'total_late': stats['total_late'],
                    'total_early': stats['total_early'],
                    'warning_var': warning_var,
                })
    return render(request, 'MainApp/stats.html',  {'departments': departments, 'months': months, 'employees': employees, 'department': department, 'month': month, 'hours': hours})

def get_stats_employee(request):
    employee_id = request.GET.get('employee')
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    
    start_date = timezone.make_aware(datetime(year, month, 1))
    end_date = timezone.make_aware(datetime(
        year + 1 if month == 12 else year,
        1 if month == 12 else month + 1,
        1, 23, 59, 59
    ))
    
    # Get employee details
    try:
        employee = Employees.objects.get(id=employee_id)
        employee_info = {
            'fullname': employee.fullname,
            'department': employee.job.departament.title,
            'job': employee.job.title
        }
    except Employees.DoesNotExist:
        employee_info = {
            'fullname': None,
            'department': None,
            'job': None
        }
    
    records = AccessControl.objects.filter(
        employee_id=employee_id,
        date__range=(start_date, end_date)
    ).order_by('date')

    daily_records = defaultdict(list)
    for record in records:
        day_key = record.date.date()
        daily_records[day_key].append(record)

    data = []
    for day, day_records in sorted(daily_records.items()):
        day_records.sort(key=lambda x: x.date)
        
        current_entry = None
        total_work_time = timedelta()
        is_late = False
        is_early_exit = False
        
        # Получаем первое время входа и последнее время выхода
        first_entry_time = next((r.date.time() for r in day_records if r.state.lower() == 'in'), None)
        last_exit_time = next((r.date.time() for r in reversed(day_records) if r.state.lower() == 'out'), None)
        
        # Проверка опоздания (только если пришел после 9:00)
        if first_entry_time and first_entry_time > time(9, 0):
            is_late = True
        
        # Проверка раннего ухода (только если ушел до 18:00)
        if last_exit_time and last_exit_time < time(18, 0):
            is_early_exit = True
        
        # Расчет общего времени работы
        for record in day_records:
            if record.state.lower() == 'in' and current_entry is None:
                current_entry = record.date
            elif record.state.lower() == 'out' and current_entry is not None:
                total_work_time += record.date - current_entry
                current_entry = None
        
        total_hours = total_work_time.total_seconds() // 3600
        total_minutes = (total_work_time.total_seconds() % 3600) // 60
        work_duration = f"{int(total_hours)}ч {int(total_minutes)}м" if total_work_time else None

        data.append({
            'date': day.strftime("%Y.%m.%d"),
            'first_entry': first_entry_time.strftime("%H:%M:%S") if first_entry_time else None,
            'last_exit': last_exit_time.strftime("%H:%M:%S") if last_exit_time else None,
            'work_duration': work_duration,
            'is_late': is_late,
            'is_early_exit': is_early_exit
        })

    response_data = {
        'employee_info': employee_info,
        'attendance_data': data
    }

    return JsonResponse(
        response_data, 
        safe=False, 
        json_dumps_params={'ensure_ascii': False}
    )