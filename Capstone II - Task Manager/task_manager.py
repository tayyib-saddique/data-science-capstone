# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", "r") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t["username"] = task_components[0]
    curr_t["title"] = task_components[1]
    curr_t["description"] = task_components[2]
    curr_t["due_date"] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t["assigned_date"] = datetime.strptime(
        task_components[4], DATETIME_STRING_FORMAT
    )
    curr_t["completed"] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


# ====Login Section====
"""This code reads usernames and password from the user.txt file to 
    allow a user to login.
"""
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", "r") as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(";")
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login successful!")
        logged_in = True


def reg_user():
    """Add a new user to the user.txt file"""
    # - Request input of a new username
    new_username = input("New Username: ")
    if new_username in username_password:
        print("Username is taken, please try again")

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w+") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do not match")


def add_task():
    while True:
        """Allow a user to add a new task to task.txt file
        Prompt a user for the following:
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and
            - the due date of the task."""
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue

        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Then get the current date.
        curr_date = date.today()
        """ Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete."""
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False,
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t["username"],
                    t["title"],
                    t["description"],
                    t["due_date"].strftime(DATETIME_STRING_FORMAT),
                    t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t["completed"] == True else "No",
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")
        break


def view_all():
    """Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    """
    for idx, t in enumerate(task_list):
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Task No: \t {idx}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += (
            f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        )
        disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \t {t['description']}\n"

        print(disp_str)


def view_mine():
    """Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    """
    for idx, t in enumerate(task_list):
        if t["username"] == curr_user:
            disp_str = f"Task: \t\t {t['title']}\n"
            # added task no based on index of t in task_list
            disp_str += f"Task No.: \t {idx}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += (
                f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            )
            disp_str += f"Task Description: {t['description']}\n"
            disp_str += f"Task Completion: {t['completed']}\n"

            print(disp_str)

    # user is requested to provide input which is transformed into an int variable
    input_task = int(input("Please select a task number "))
    if input_task != -1:
        # enumerate is used to index tasks in task_list
        for idx, t in enumerate(task_list):
            # if input_task is equal to idx
            if input_task == idx:
                # user is requested to provide further information
                completion = input(
                    "Do you wish to mark this task as complete (Yes/No) "
                ).lower()
                if completion in ["y", "yes"]:
                    t["completed"] = True
                # if user responds to above with no or n, then user has the option to edit the task
                elif completion in ["n", "no"]:
                    edit_task = input(
                        "Do you wish to edit this task? (Yes/No) "
                    ).lower()
                    t["completed"] = False
                    # t['completed'] is converted to False (as user responded saying task is not complete)
                    # if the above question is answered by user with yes or y,
                    # user is requested to provide further information
                    if edit_task in ["yes", "y"]:
                        assignment_change = input(
                            "Who do you wish to assign the task to? "
                        )
                        due_date_change = input(
                            "What is the new due date for this task? (YYYY-MM-DD)"
                        )
                        due_date_change = datetime.strptime(
                            due_date_change, DATETIME_STRING_FORMAT
                        )
                        t["username"] = assignment_change
                        t["due_date"] = due_date_change
                # file is opened and amendments are written to based
                with open("tasks.txt", "w+") as task_file:
                    task_list_to_write = []
                    for t in task_list:
                        str_attrs = [
                            t["username"],
                            t["title"],
                            t["description"],
                            t["due_date"].strftime(DATETIME_STRING_FORMAT),
                            t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                            "Yes" if t["completed"] == True else "No",
                        ]
                        task_list_to_write.append(";".join(str_attrs))

                    task_file.write("\n".join(task_list_to_write))


# new function added to generate reports
def generate_reports():

    num_tasks = len(task_list)
    num_users = len(username_password.keys())
    # declared variables are used later in for loop
    overdue_tasks = 0
    incomplete_tasks = 0
    complete_tasks = 0
    # for loop is used to determine figures for the above variables based on dictionary
    for t in task_list:
        if t["completed"] == False:
            incomplete_tasks += 1
            present = datetime.today()
            if t["assigned_date"] < present:
                overdue_tasks += 1
        elif t["completed"] == True:
            complete_tasks += 1

    percent_overdue = (overdue_tasks / len(task_list)) * 100
    percent_incomplete = (incomplete_tasks / len(task_list)) * 100

    task_overview_string = "{0} task(s) have been generated and tracked. \n \n{1} task(s) have been completed. \n\n{2} task(s) are currently incomplete. \n\n{3} task(s) are overdue and currently incomplete. \n\n{4:.2f}% task(s) are incomplete. \n\n{5:.2f}% task(s) are overdue".format(
        num_tasks,
        complete_tasks,
        incomplete_tasks,
        overdue_tasks,
        percent_overdue,
        percent_incomplete,
    )
    print(task_overview_string)

    # file opened and string above written to file
    with open("task_overview.txt", "w+") as file1:
        file1.write(task_overview_string)

    # declare empty strings as seperate variables
    total_user_assignment = ""
    percent_assignment = ""
    completed_assignment = ""
    incompleted_assignment = ""
    overdue_assignment = ""
    # declare empty dict
    assigned_tasks = {}
    # for each task in task_list, append information to assigned_tasks
    for t in task_list:
        assigned_tasks.setdefault(t["username"], []).append(
            [
                {"title": t["title"]},
                {"completed": t["completed"]},
                {"assigned_date": t["assigned_date"]},
            ]
        )

    print(str(assigned_tasks) + "\n")
    # the previously declared dictionary was structured where the user is the outermost key allowing us to differentiate users
    for user in assigned_tasks:
        print(user)
        # len(assigned_tasks[user]) pulls out the number of tasks per user
        total_user_assignment += "{0} has been assigned {1} tasks. \n".format(
            user, len(assigned_tasks[user])
        )

        assignment_percentage = len(assigned_tasks[user]) / len(task_list) * 100
        percent_assignment += "{0:.2f}% tasks have been assigned to {1}. \n".format(
            assignment_percentage, user
        )

        # declare variables as 0
        user_complete_task = 0
        user_incomplete_task = 0
        user_overdue_task = 0
        # a temp_dict is used to simplify things
        temp_dict = assigned_tasks[user]
        # temp_dict as an example is now the following:
        # [[{'title': 'Create template'}, {'completed': False}, {'assigned_date': datetime.datetime(2022, 12, 28, 0, 0)}]]
        # not in the most ideal structure due to nested structure so accessing variables is a bit complicated
        # for loop is used to differentiate tasks for the same user, further simplifying things for us
        for i in temp_dict:
            print(i)
            # print(i) for admin user which has two tasks below:
            # [{'title': 'Add functionality to task manager'}, {'completed': True}, {'assigned_date': datetime.datetime(2022, 11, 22, 0, 0)}]
            # [{'title': 'Add files to system '}, {'completed': False}, {'assigned_date': datetime.datetime(2022, 12, 28, 0, 0)}]
            # [1] is used to call the 2nd dictionary in the list (index starts at 0 for 1st item) i.e. {'completed': True}
            # ['completed'] is used to call the value of the associated key
            if i[1]["completed"] == True:
                user_complete_task += 1
                completed_assignment += (
                    "{0} has completed {1} assigned tasks. \n".format(
                        user, user_complete_task
                    )
                )

            if i[1]["completed"] == False:
                user_incomplete_task += 1
                incompleted_assignment += (
                    "{0} has yet to complete {1} assigned tasks. \n".format(
                        user, user_incomplete_task
                    )
                )

                present = datetime.today()
                if i[2]["assigned_date"] < present:
                    user_overdue_task += 1
                    overdue_assignment += "{0} has {1} assigned tasks which are yet to be complete and are overdue. \n".format(
                        user, user_overdue_task
                    )

    user_overview_string = (
        str(total_user_assignment)
        + "\n"
        + str(percent_assignment)
        + "\n"
        + str(completed_assignment)
        + "\n"
        + str(incompleted_assignment)
        + "\n"
        + overdue_assignment
    )
    print(user_overview_string)

    # file opened and string above is written to file
    with open("user_overview.txt", "w+") as file2:
        file2.write(user_overview_string)


while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input(
        """Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
gr - Generate reports
e - Exit
: """
        # gr is added above
    ).lower()

    if menu == "r":
        reg_user()

    elif menu == "a":
        add_task()

    elif menu == "va":
        view_all()

    elif menu == "vm":
        view_mine()

    elif menu == "ds" and curr_user == "admin":
        """If the user is an admin they can display statistics about number of users
        and tasks."""
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")
    # added function is called upon if user responds with gr (generate reports)
    elif menu == "gr":
        generate_reports()

    elif menu == "e":
        print("Goodbye!!!")
        exit()

    else:
        print("This is not an option, please try again")
