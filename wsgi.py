import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.models.admin import Admin 
from App.models.staff import Staff
from App.models.available import Available
from App.models.schedule import Schedule
from App.models.shift import Shift

from rich.console import Console
from rich.table import Table
from datetime import datetime , timedelta , time

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)
console=Console()

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    Aria=Staff(firstname='Aria',lastname='Dianna',password='ariapass',role='staff')
    Bob=Staff(firstname='Boblin',lastname='Bobbins',password='boblinpass',role='staff')
    Charmon=Staff(firstname='Charmona',lastname='Charm',password='charmonapass',role='staff')

    Ian=Admin(firstname='Ian',lastname='Ianna',password='ianpass',role='admin')
    Dyan=Admin(firstname='Dyan',lastname='Dyed',password='dyanpass',role='admin')

    time = datetime.strptime("13:00", "%H:%M")

    for i in range(4):
       
        new_time = time + timedelta(hours=2, minutes=30)

        start_str = time.strftime("%I:%M %p")
        end_str = new_time.strftime("%I:%M %p")
        monday = Available(day='Monday', start_time=start_str, end_time=end_str)
        db.session.add(monday)

        time = new_time
        db.session.add(monday)
    time = datetime.strptime("13:00", "%H:%M")
    for i in range(4):
        new_time = time + timedelta(hours=2, minutes=30)

        start_str = time.strftime("%I:%M %p")
        end_str = new_time.strftime("%I:%M %p")
        tuesday = Available(day='Tuesday', start_time=start_str, end_time=end_str)
        db.session.add(tuesday)

        time = new_time
        db.session.add(tuesday)

    for i in range(3):
        new_time = time + timedelta(hours=2, minutes=30)

        start_str = time.strftime("%I:%M %p")
        end_str = new_time.strftime("%I:%M %p")
        wednesday = Available(day='Wednesday', start_time=start_str, end_time=end_str)
        db.session.add(wednesday)

        time = new_time
        db.session.add(wednesday)
    
    db.session.add_all([Aria,Bob,Charmon,Ian,Dyan])
    db.session.commit()
    print('database intialized')




admin=AppGroup('admin', help='Admin object commands')
@admin.command("view-slots", help="displays time slots for the week")
def view_slots():
    timeslots=Available.query.all()

    table=Table(title="Days & Times")
    table.add_column("ID",justify="left")
    table.add_column("Days",justify="left")
    table.add_column("Start times",justify="center")
    table.add_column("End times",justify="center")
    table.add_column("Status",justify="center",style="yellow")

    for t in timeslots:
        table.add_row(str(t.id),t.day,t.start_time,t.end_time,t.status)

    console.print(table)

@admin.command("schedule-staff",help="allocates a staff to a certain time ")
def staff_times():

    print("Admins , assign the following staff members to this weeks timeslots ...")
    print("Use the staff and the Days/Time ID to allocate a staff to a time slot")

    staff=Staff.query.all()
    table=Table(title="Staff List")
    table.add_column("ID",justify="right")
    table.add_column("First Name",justify="left")
    table.add_column("Last Name",justify="left")
    for s in staff:
       table.add_row(str(s.id),s.firstname,s.lastname)

    console.print(table)

    staff_id=int(input("Enter a staff ID : "))
    time_day_id=int(input("Enter a time slot ID : "))

    member=Staff.query.get(staff_id)

    time_day=Available.query.get(time_day_id)

    if member and time_day:
        newschedule=Schedule(staff_id=member.id,available_id=time_day.id)
        time_day.set_status("closed")


        db.session.add(newschedule)
        db.session.commit()

        
        print(f"{member.firstname} {member.lastname} has been scheduled for {time_day.day} from {time_day.start_time} to {time_day.end_time} {time_day.status}")



app.cli.add_command(admin)





# this shoudl be within 1 week 
# admins should seee that dates and time available and set a date and time for staff? 

# @app.cli.command("list-staff",help="testing if this works ")
# def list_staff():
#     staff=Staff.query.all()
#     table=Table(title="Staff List")
#     table.add_column("ID",justify="right")
#     table.add_column("First Name",justify="left")
#     table.add_column("Last Name",justify="left")
#     for s in staff:
#        table.add_row(str(s.id),s.firstname,s.lastname)

#     console.print(table)



























# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("firstname", default="rob")
@click.argument("lastname", default="rob")
@click.argument("password", default="robpass")
def create_user_command(firstname, lastname, password):
    create_user(firstname, lastname, password)
    print(f'{firstname} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
