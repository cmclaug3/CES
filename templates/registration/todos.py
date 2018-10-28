'''

* go through the built in auth URLs and Views and implement (password update, forgot password, etc)
* need to figure out how to handle fuel receipts!!!

---MODELS---

User
    email, first_name, last_name, timestamp, account_setup_code, is_active, is_staff, is_admin

Employee
    pin,

Job
    name, job_num(XX-XXXX), type(ongoing, one-time), status, WorkDays(M2M)

WorkDay
     location, date, completed, timesheet(FK), **other paper work linked here


Employee_Work
    Employee(FK), time_start, time_finish, lunch, injured, signature
        total_hours()

Timesheet
    date, supervisor, supervisor_signature, Employee_Works(M2M), status(incomplete, pending, approved, complete), receipts(M2M)
        week_ending()

Receipt
    image


---VIEWS---

LOGIN
    email and password
    new users need to be able to set a password

HOME PAGE

Employee (links)
    new job, miscellanous timesheet, incomplete jobs, incomplete timesheets, settings, work history (only signed in employee)
    jobs list

    new job
        form to create new job, (list of last 8 job names and numbers will be visible)
            buttons-->submit, submit and start timesheet (both immediatly post to jobs list so numbers can be correct)

    incomplete jobs
        list of incomplete jobs created

    settings
        set first_name, last_name, pin
        change pin, password

    work history
        week by week of work history
            total hours per job, total hours per week

    jobs list
        job numbers of jobs starting from most recent


Admin (links)
    new job, miscellanous timesheet, jobs, timesheets, settings, work history (all employees), jobs list

'''