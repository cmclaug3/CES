from time_sheet.models import TimeSheet, WorkDay, EmployeeWork, Job
from accounts.models import Employee, User
import random
from datetime import datetime, date, time, timedelta






###############################
#     DELETION FUNCTIONS      #
###############################



def clear_all_but_jobs_employees():
    '''
    Only used for erasing all editable content to softly clear database
    '''
    TimeSheet.objects.all().delete()
    WorkDay.objects.all().delete()
    EmployeeWork.objects.all().delete()
    print('just deleted all timesheets, workdays, and employeeworks')





###############################
#     CREATION FUNCTIONS      #
###############################


def _get_group_sizes():
    '''
    Returns list of a random #s 1-5 that sum is equal to total employees
    Used to create accurate groups of employees for a given day
    THIS IS BLOODY HORRIBLE NOW BUT IT WORKS
    '''
    NUMBER_OF_EMPLOYEES = Employee.objects.all().count()
    limit = [1,2,3,4,5]
    order = []
    group_size = NUMBER_OF_EMPLOYEES

    while group_size > 0:
        choice = random.choice(limit)
        if group_size - choice < 0:
            # print('supposedly wasnt enough ppl for this choice')
            continue
        group_size -= choice
        order.append(choice)

    return order



def random_employee_list():
    '''
    Creates groups of employees for a given timesheet/worday
        returns a list of employee group lists
    '''
    all_employees = list(Employee.objects.all())
    random.shuffle(all_employees)
    list_of_lists = []
    for amount in _get_group_sizes():
        individual_list = []
        for i in range(amount):
            individual_list.append(all_employees.pop())
        list_of_lists.append(individual_list)
    return list_of_lists



def get_all_days():
    START_DATE = date(2018, 12, 1)
    END_DATE = date(2019, 3, 1)

    all_days = []

    while START_DATE < END_DATE:
        all_days.append(START_DATE)
        START_DATE += timedelta(days=1)

    return all_days



def create_workday(date, job, created_by):
    # create workday with logic to make them believable and slightly unique


    if job.address == '':
        address = 'missing address'
    else:
        address = job.address

    completed = True
    status = 'Complete'

    new_workday = WorkDay.objects.create(date=date, address=address, job=job, created_by=created_by, completed=completed, status=status)
    new_workday.save()
    return new_workday



def create_timesheet(workday):
    completed = True
    new_timesheet = TimeSheet.objects.create(work_day=workday, completed=completed)
    new_timesheet.save()
    return new_timesheet



def random_shift_time():
    START_TIME_CHOICES = [time(6, 0), time(6, 30), time(7, 0), time(7, 30), time(8, 0), time(8, 30)]

    END_TIME_CHOICES = [time(15, 0), time(15, 30), time(16, 0), time(16, 30), time(17, 0), time(17, 30),
                        time(18, 0), time(18, 30), time(19, 0), time(19, 30), time(20, 0), time(20, 30)]

    shift = [random.choice(START_TIME_CHOICES), random.choice(END_TIME_CHOICES)]
    return shift



def create_employee_work(employee, timesheet, start, end, lunch):

    injured = False
    comment = ''
    signature = True

    new_emp_work = EmployeeWork.objects.create(employee=employee, time_sheet=timesheet, start_time=start, end_time=end,
                                               lunch=lunch, injured=injured, comment=comment, signature=signature)
    new_emp_work.save()




#######################
#######################



def data_injection():
    '''



    '''

    wd_ts_count = 0
    emp_work_count = 0

    for day in get_all_days():
        JOB_CHOICES_LIST = list(Job.objects.all())
        random.shuffle(JOB_CHOICES_LIST)
        for group in random_employee_list():
            job = JOB_CHOICES_LIST.pop()
            workday = create_workday(date=day, job=job, created_by=group[0])
            timesheet = create_timesheet(workday=workday)
            wd_ts_count += 1
            shift = random_shift_time()
            lunch = random.choice(['half-hour', 'hour', 'none'])
            for emp in group:
                create_employee_work(employee=emp, timesheet=timesheet, start=shift[0], end=shift[1], lunch=lunch)
                emp_work_count += 1
    print('just created {} WorkDays/TimeSheets and {} EmployeeWorks'.format(wd_ts_count, emp_work_count))





def get_present_week(other_date=None):
    '''
    return list of 7 day week of current pay period (friday-thursday)
    optional argument other_date is a datetime day and will give the pay period that day falls in
    '''
    if other_date == None:
        today = datetime.today()
    else:
        today = other_date
    formatted_day = datetime(today.year, today.month, today.day)
    today_num = formatted_day.weekday()

    # Get Monday of the given week (first day of pay period)

    starting_monday = formatted_day - timedelta(days=today_num)

    # Get full Pay Period of that week

    week = []

    for week_days in range(7):
        week.append(starting_monday)
        starting_monday += timedelta(days=1)

    return week




def get_all_weeks():
    '''

    list of days in particular week (pay period) for each week from earliest to most recent session

    '''


    earliest_session = WorkDay.objects.all().order_by('date').first()
    latest_session = WorkDay.objects.all().order_by('date').last()

    first_week = get_present_week(other_date=earliest_session.date)
    last_week = get_present_week(other_date=latest_session.date)

    monday_first_week = first_week[0]
    monday_last_week = last_week[0]

    weeks_list = []

    while (monday_first_week.year, monday_first_week.month, monday_first_week.day) \
            <= (monday_last_week.year, monday_last_week.month, monday_last_week.day):

        end_sunday = monday_first_week + timedelta(days=6)
        weeks_list.append([monday_first_week, end_sunday])
        monday_first_week += timedelta(days=7)

    weeks_list.reverse()

    return weeks_list



# MyModel.objects.filter(date__range=(range_start, range_end))