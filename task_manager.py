# ===== Importing Libraries ===========
from datetime import date, datetime
date.today()

# === Functions ===


def get_users(user_file):
    user_data = {}  # stores usernames and passwords as dictionary

    # reads through every line in user.txt and returns this data as a dictionary
    with open(user_file, "r+") as f:
        for line in f:
            data = line.strip().split(", ")
            user = data[0]
            user_password = data[1]
            user_data[user] = user_password

    return user_data


def reg_user(user_file):
    # requests username, password and password confirmation
    print("\n+++++++++++ NEW USER +++++++++++")
    new_user = input(">> Enter username: ")
    new_pass = input(">> Enter password: ")
    confirm_pass = input(">> Confirm password: ")

    # gets list of all currently in use usernames
    used_names = get_users(user_file).keys()

    # adds new user to user file if password confirmation matches and username not in use
    if new_pass == confirm_pass and new_user not in used_names:
        with open(user_file, "a") as f:
            f.write(f"\n{new_user}, {new_pass}")
        print(f">> {new_user} has been successfully registered.")

    # presents error message if username already used
    elif new_user in used_names:
        print(f">> The username {new_user} is currently in use. Please try again.")

    # presents error message if password confirmation does not match
    else:
        print(">> The password confirmation did not match. Please try again.")


def add_task(task_file):
    # requests username, title, description and due date
    print("\n+++++++++++ NEW TASK +++++++++++")
    task_user = input(">> Enter username: ")
    title = input(">> Enter title: ")
    desc = input(">> Enter description: ")
    due_date = input(">> Enter due date: ")

    # gets current date
    today = date.today()
    full_date = today.strftime("%d %b %Y")

    # adds new task to tasks.txt file
    task = f"\n{task_user}, {title}, {desc}, {full_date}, {due_date}, No"
    with open(task_file, "a") as f:
        f.write(task)

    print(">> Task added.")


def view_all(task_file):
    # opens tasks file and iterates through each line in the file
    with open(task_file, "r+") as f:
        for line in f:
            # splits line where there are commas
            task_data = line.strip().split(", ")
            # prints formatted task data
            print(f'''────────────────────────────────────────────
    Task:                 {task_data[1]}
    Assigned To:          {task_data[0]}
    Date Assigned:        {task_data[3]}
    Due Date:             {task_data[4]}
    Task Complete?        {task_data[5]}
    Task Description:
    {task_data[2]}''')
    print("────────────────────────────────────────────")


def view_mine(task_file):
    # creates list to store data of all tasks
    all_tasks = []

    # opens tasks file and iterates through each line in the file
    with open(task_file, "r+") as f:
        tasks = 0
        for line in f:
            tasks += 1
            # splits line where there are commas
            task_data = line.strip().split(", ")
            # adds task to all_tasks
            all_tasks.append(task_data)

            # prints task only if assigned to current user
            if task_data[0] == current_user:
                # prints formatted task data
                print(f'''──────────────────────────────────────────── {tasks} ─
    Task:                 {task_data[1]}
    Assigned To:          {task_data[0]}
    Date Assigned:        {task_data[3]}
    Due Date:             {task_data[4]}
    Task Complete?        {task_data[5]}
    Task Description:
    {task_data[2]}''')
    print("─────────────────────────────────────────────────")

    # presents task management menu and asks user for task number
    task_no = int(input('''\n++++++++++++ MARK/EDIT ++++++++++++
>> You can enter '-1' to exit this section.
>> Enter the number of the task you wish to mark as complete/edit: '''))

    # proceeds with editing/marking task if user hasn't entered -1 or task hasn't been completed
    if task_no != -1:
        action = int(input('''\n>> 1. Mark task as complete
>> 2. Edit task

>> Choose your option: '''))

        # marks task as complete if user chooses '1'
        if action == 1:
            # edits completion tag in all_tasks list
            all_tasks[task_no-1][5] = "Yes"

            # rewrites task file with new task data
            with open(task_file, "w+") as f:
                for task in all_tasks:
                    data = ", ".join(task)
                    f.write(f"{data}\n")

        # edits task if user chooses '2'
        elif action == 2:
            # allows user to edit task if task is not yet complete
            if all_tasks[task_no-1][5] != "Yes":
                new_username = input("\n>> Enter new username: ")
                new_date = input(">> Enter new date: ")

                # edits username and date assigned to task in all_tasks list
                all_tasks[task_no-1][0] = new_username
                all_tasks[task_no-1][4] = new_date

                # rewrites task file with new task data
                with open(task_file, "w+") as f:
                    for task in all_tasks:
                        data = ", ".join(task)
                        f.write(f"{data}\n")

            # displays error message if task is complete already
            else:
                print(">> This task has already been completed and cannot be edited.")

        # displays error message if user enters wrong option
        else:
            print(">> That was an invalid option. Please try again.")


def generate_reports(user_file, tasks_file):
    user_data = []
    task_data = []

    # gets current date
    date_now = datetime.today()

    # reads user file and adds each user to user_data
    with open(user_file, "r+") as f:
        for line in f:
            user_data.append(line.strip().split(", "))

    # reads tasks file and adds each task to task_data
    with open(tasks_file, "r+") as f:
        for line in f:
            task_data.append(line.strip().split(", "))

    # generates and adds data to user_overview.txt file
    with open("user_overview.txt", "w+") as f:
        # iterates through and generates data for each user in user_data
        for user in user_data:
            user_name = user[0]
            # gets list of all tasks which are assigned to user
            user_tasks = [task for task in task_data if task[0] == user_name]
            # number of tasks assigned to user
            total_tasks = len(user_tasks)
            # percentage of total tasks assigned to user
            total_percentage = round((len(user_tasks)/len(task_data))*100, 2)
            # gets list of all tasks completed by user
            completed = [task for task in user_tasks if task[5] == "Yes"]
            # gets percentage of tasks that have been completed by user
            percentage_complete = round((len(completed)/len(user_tasks))*100, 2)
            # gets percentage of tasks yet to be completed
            percentage_incomplete = 100 - percentage_complete
            # gets list of all overdue tasks
            overdue = [task for task in user_tasks if task[5] == "No" and date_now > datetime.strptime(task[4], "%d %b %Y")]
            # gets percentage of overdue tasks
            percentage_overdue = round((len(overdue)/len(user_tasks))*100, 2)

            # formats data as a string
            data_user = f"{user_name}, {total_tasks}, {total_percentage}, {percentage_complete}, {percentage_incomplete}, {percentage_overdue}\n"

            # adds data to file
            f.write(data_user)

    # generates and adds data to task_overview.txt file
    with open("task_overview.txt", "w+") as f:
        # gets total number of tasks
        no_tasks = len(task_data)
        # gets total number of incomplete and completed tasks
        complete_tasks = [task for task in task_data if task[5] == "Yes"]  # list of complete tasks
        no_complete = len(complete_tasks)
        no_incomplete = no_tasks - no_complete
        # gets list of overdue tasks
        overdue_tasks = [task for task in task_data if task[5] == "No" and date_now > datetime.strptime(task[4], "%d %b %Y")]
        # gets number of overdue tasks
        no_overdue = len(overdue_tasks)
        # calculates percentage of incomplete and overdue tasks
        percent_incomplete = round((no_incomplete/no_tasks)*100, 2)
        percent_overdue = round((no_overdue/no_tasks)*100, 2)

        # formats data as a string
        data_task = f"{no_tasks}, {no_complete}, {no_incomplete}, {no_overdue}, {percent_incomplete}, {percent_overdue}\n"

        # adds data to file
        f.write(data_task)


def statistics(user_file, tasks_file):
    # initialise variables
    user_data = []
    task_data = []

    # generates latest report data
    generate_reports(user_file, tasks_file)

    # adds data from user_overview.txt file to user_data
    with open("user_overview.txt", "r+") as f:
        for line in f:
            user = line.strip().split(", ")
            user_data.append(user)

    # adds data from task_overview.txt file to task_data
    with open("task_overview.txt", "r+") as f:
        task_data = f.read().strip().split(", ")

    # prints general statistics
    print("\n+++++++++++ STATISTICS +++++++++++\n")
    print(f'''─────────────────────────────────────────────
    Total Users:       {len(user_data)}
    Total Tasks:       {task_data[0]}
───────────────────────────────────────────────''')

    # prints formatted task overview data
    print("\n+++++++++++ TASK OVERVIEW +++++++++++\n")
    print(f'''──────────────────────────────────────────── Tasks ─
    Total Tasks:          {task_data[0]}
    Complete Tasks:       {task_data[1]}
    Incomplete Tasks:     {task_data[2]}
    Overdue Tasks:        {task_data[3]}
    % Incomplete:         {task_data[4]}%
    % Overdue: :          {task_data[5]}
─────────────────────────────────────────────────────''')

    # prints formatted user overview data for each user
    print("\n+++++++++++ USER OVERVIEW +++++++++++\n")
    for user in user_data:
        print(f'''──────────────────────────────────────────── {user[0]} ─
        Tasks Assigned:       {user[1]}
        % Assigned:           {user[2]}%
        % Complete:           {user[3]}%
        % Incomplete:         {user[4]}%
        % Overdue: :          {user[5]}%''')
    print("───────────────────────────────────────────────────")


# ==== Login Section ====
users = get_users("user.txt")  # gets dictionary of all current users and their passwords
current_user = None

# displays login menu and validates username and password
while True:
    username = input('''++++++++++++ LOGIN ++++++++++++
    
>> Username: ''')

    password = input(">> Password: ")

    if users[username] == password:
        print(">> Login successful!")
        current_user = username  # sets current user if login successful
        break

    else:
        print(">> Your username or password is incorrect. Please try again.\n")
        continue

# === Menu Section ===
while True:
    # changes menu text depending on whether user is admin or not
    if current_user == "admin":
        menu_text = '''\n+++++++++++ OPTIONS +++++++++++
>> r - Registering a user
>> a - Adding a task
>> va - View all tasks
>> vm - View my tasks
>> gr - Generate reports
>> ds - Display statistics
>> e - Exit

>> Enter an option: '''

    else:
        menu_text = '''\n+++++++++++ OPTIONS +++++++++++
>> r - Registering a user
>> a - Adding a task
>> va - View all tasks
>> vm - View my tasks
>> e - Exit

>> Enter an option: '''

    # presenting the menu to the user and converts user input to lower case
    menu = input(menu_text).lower()

    if menu == 'r' and current_user == "admin":
        reg_user("user.txt")

    elif menu == 'r' and current_user != "admin":
        print(">> You do not have admin permissions.")

    elif menu == 'a':
        add_task("tasks.txt")

    elif menu == 'va':
        view_all("tasks.txt")

    elif menu == 'vm':
        view_mine("tasks.txt")

    elif menu == 'gr' and current_user == "admin":
        generate_reports("user.txt", "tasks.txt")
        print("\n>> Reports generated.")

    elif menu == 'gr' and current_user != "admin":
        print(">> You do not have admin permissions.")

    elif menu == 'ds' and current_user == "admin":
        statistics("user.txt", "tasks.txt")

    elif menu == 'ds' and current_user != "admin":
        print(">> You do not have admin permissions.")

    elif menu == 'e':
        print('>> Goodbye!')
        exit()

    else:
        print(">> You have made a wrong choice, please try again.")
