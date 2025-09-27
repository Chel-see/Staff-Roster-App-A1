import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from sqlalchemy import table

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.models import staff
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

    time = datetime.strptime("1:00 PM", "%I:%M %p")

    for i in range(4):
       
        new_time = time + timedelta(hours=2, minutes=30)

        start_str = time.strftime("%I:%M %p")
        end_str = new_time.strftime("%I:%M %p")
        monday = Available(day='Monday', start_time=start_str, end_time=end_str)
        db.session.add(monday)

        time = new_time
        db.session.add(monday)

    time = datetime.strptime("1:00 PM", "%I:%M %p")
    for i in range(4):
        new_time = time + timedelta(hours=2, minutes=30)

        start_str = time.strftime("%I:%M %p")
        end_str = new_time.strftime("%I:%M %p")
        tuesday = Available(day='Tuesday', start_time=start_str, end_time=end_str)
        db.session.add(tuesday)

        time = new_time
        db.session.add(tuesday)

    time = datetime.strptime("11:00 AM", "%I:%M %p")
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





@app.cli.command("view-slots", help="displays time slots for the week")
def view_slots():

    all_admins=Admin.query.all()
    print(f"\nThe following are our admins : \n{all_admins}\n")

    ad_ID=int(input("Enter your admin ID : "))
    admin=Admin.query.get(ad_ID)
    
    if not admin:
        print("Invalid Admin ID")
        return
    
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



@app.cli.command("schedule-staff",help="allocates a staff to a certain time ")
def staff_times():

    all_admins=Admin.query.all()
    print(f"\nThe following are our admins : \n{all_admins}\n")

    ad_ID=int(input("Enter your admin ID : "))
    admin=Admin.query.get(ad_ID)

    if not admin:
        print("Invalid Admin ID")
        return

    print("\n Admins , assign the following staff members to this weeks timeslots ...")
    print("Use the staff and the Days/Time ID to allocate a staff to a time slot \n")

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
     if time_day.status=="available":
        newschedule=Schedule(staff_id=member.id,available_id=time_day.id)
        time_day.set_status("closed")
        db.session.add(newschedule)
        db.session.commit()    
        print(f"{member.firstname} {member.lastname} has been scheduled for {time_day.day} from {time_day.start_time} to {time_day.end_time}")
     else:
        print("Time slot is taken ") 





@app.cli.command("view-schedule",help="view the schedule for the week ")
def view_schedule():
    schedules = Schedule.query.all()
    table = Table(title="Weekly Schedule")
    table.add_column("Staff", justify="left",style="green")
    table.add_column("Day", justify="left",style="red")
    table.add_column("Start Time", justify="left" )
    table.add_column("End Time", justify="left")
#fix
    for s in schedules:
        # staff = Staff.query.get(s.staff_id)
        # available = Available.query.get(s.available_id)
        table.add_row(f"{s.staff.firstname} {s.staff.lastname}", s.available.day, s.available.start_time, s.available.end_time)

    console.print(table)




@app.cli.command("clock-in", help="logs the beginning of a staff member's shift")
def check_in():

    staff_id=int(input("Enter your employee ID :"))

    staff_times=Schedule.query.filter_by(staff_id=staff_id).all() # validates that this employee has been scheduled

   

    if staff_times:  

        ongoing=Shift.query.filter(Shift.staff_id==staff_id,Shift.complete==False).first()

        if ongoing:
            print (f"You have an ongoing shift : \n{ongoing.schedule.available.day} from {ongoing.schedule.available.start_time} to {ongoing.schedule.available.end_time} \n ")
            print("Please clock out of this shift before clocking into another.")
            return


        
        print("\n Your scheduled times are as follows . \n")

        table=Table(title=f"{staff_times[0].staff.firstname}'s Weekly Schedule") # because they can have multiple entries in the list
        table.add_column("Schedule ID", justify="center",style="cyan")
        table.add_column("Day", justify="center")
        table.add_column("Start Time", justify="center")
        table.add_column("End Time", justify="center")

        for s in staff_times:
                table.add_row(f"{s.id}",f"{s.available.day}", f"{s.available.start_time}", f"{s.available.end_time}")
        console.print(table)

       
        schedule_id=int(input("Enter the Schedule ID of the shift you are clocking in for : "))  # since any number can be entered that may correspond to someone else's schedule


        completed=Shift.query.filter_by(staff_id=staff_id, schedule_id=schedule_id,complete=True).first()

        if completed:
            print("You have COMPLETED this shift for THIS WEEK.")
            return
        
        if schedule_id:

                check_in=input("\n Enter the current time hh:mm: AM/PM -   ")
                try:
                    time_in=datetime.strptime(check_in,"%I:%M %p")

                except ValueError:
                    print("Invalid date/time format. Must be hh:mm AM/PM") 
                    return
                
                schedule=Schedule.query.get(schedule_id)

                start_time=datetime.strptime(schedule.available.start_time,"%I:%M %p")
                end_time=datetime.strptime(schedule.available.end_time,"%I:%M %p")


                if(start_time <= time_in <= end_time): # check if the time in is within the scheduled time
                        time_in=datetime.strftime(time_in,"%I:%M %p")
                        s1=Shift(staff_id=staff_id,schedule_id=schedule_id,timeIn=time_in,timeOut=None)
                        db.session.add(s1)
                        db.session.commit()
                        print(f"You have been clocked in")
                else:
                    print(f" You cannot clock in at this time.")
                  
                
        else:
            print("Invalid Schedule ID")

    else:
         print("Schedule not found")




@app.cli.command("clock-out", help=" Logs the end time of a staff member's shift")
def check_out():

    staff_id=int(input("Enter your employee ID :")) 
    open=Shift.query.filter(Shift.staff_id==staff_id, Shift.complete==False).first() # checks if there is an open shift for this staff member
   
    if open:
        print(open)
        table=Table()
        
        table.add_column("Day",justify="center")
        table.add_column("Began",justify="center")
        table.add_column("Ended",justify="center")

        table.add_row(f"{open.schedule.available.day}",f"{open.timeIn}",f"{open.timeOut}")
        console.print(table)
        

        check_out=(input("Enter your current time hh:mm am/pm -"))
        try:
             
             time_out=datetime.strptime(check_out,"%I:%M %p")
             end_time=datetime.strptime(open.schedule.available.end_time,"%I:%M %p")
             time_in=datetime.strptime(open.timeIn,"%I:%M %p")

        except ValueError:
             print("Invalid date/time format. Must be hh:mm AM/PM")
             return

        if(time_in<=time_out<=end_time):

            time_out=datetime.strftime(time_out,"%I:%M %p")
            open.set_timeOut(time_out)
            open.set_complete(True)   
            db.session.commit()
        else:
            print("You cannot clock out at this time")
            return
        

        table=Table()
        table.add_column("Day",justify="center")
        table.add_column("Began",justify="center")
        table.add_column("Ended",justify="center")
        table.add_row(f"{open.schedule.available.day}",f"{open.timeIn}",f"{open.timeOut}")


        console.print(table)
        print("You have been clocked out")

    else: 
        print("No open shifts found")



@app.cli.command("weekly-report", help="Generates a report for admins to asses the working hours completed of staff")
def report():
    all_admins=Admin.query.all()
    print(f"\nThe following are our admins : \n{all_admins}\n")

    ad_ID=int(input("Enter your admin ID : "))

    admin=Admin.query.get(ad_ID)
    
    if not admin:
        print("Invalid Admin ID")
        return

    staff=Staff.query.all()
    # print(staff)

    table=Table(title=" \nStaff Weekly Report")
    table.add_column("ID ",justify="center",style="purple")
    table.add_column("NAME ",justify="center",style="yellow")
    table.add_column("HOURS ASSIGNED",justify="center",style="green")
    table.add_column("HOURS WORKED",justify="center",style="red")

    if staff:
        for s in staff:
            total_assigned=timedelta()  # so i can add the intervals
            total_worked=timedelta()
            assigned_hours=0
            worked_hours=0

            staff_shift=Shift.query.filter_by(staff_id=s.id).all() # all shifts for 1 staff

            for sh in staff_shift:
                if sh.complete:

                    In=datetime.strptime(sh.timeIn,"%I:%M %p")
                    Out=datetime.strptime(sh.timeOut,"%I:%M %p")

                    
                    total_worked+=(Out-In)
                    worked_hours=total_worked.total_seconds()/3600


            staff_schedule=Schedule.query.filter_by(staff_id=s.id).all() # all the times assiged to 1 staff
            
            for sc in staff_schedule:

                start=datetime.strptime(sc.available.start_time,"%I:%M %p")
                end=datetime.strptime(sc.available.end_time,"%I:%M %p")

                total_assigned+=(end-start)
                assigned_hours=total_assigned.total_seconds()/3600

           

            table.add_row(f"{s.id}",f"{s.firstname} {s.lastname}", f"{assigned_hours:.1f}", f"{worked_hours:.1f}")
        console.print(table)

    else:
        print("No staff found")
    
    mid=int(input("Enter a staff ID to view detailed report : "))

    scheduled_shift=Schedule.query.filter_by(staff_id=mid).all()

    if scheduled_shift:

        table=Table(title=f"{scheduled_shift[0].staff.firstname} {scheduled_shift[0].staff.lastname}'s Report")
        table.add_column("Day",justify="center")

        table.add_column("Starts ",justify="center", style="yellow")
        table.add_column("Ends ",justify="center", style="yellow")

        table.add_column("Checked-in",justify="center", style="green")
        table.add_column("Checked-out",justify="center", style="green")

        table.add_column("Status",justify="center", style="magenta")

        for s in scheduled_shift:
            if s.shift==None:
                table.add_row(f"{s.available.day}",f"{s.available.start_time}",f"{s.available.end_time}","-","-","Incomplete")
            else:
                if s.shift.complete:
                    status="Completed"
                else:
                    status="Ongoing"
                table.add_row(f"{s.available.day}",f"{s.available.start_time}",f"{s.available.end_time}",f"{s.shift.timeIn}",f"{s.shift.timeOut}",f"{status}")
        console.print(table)
    else:
        print(" You did not schedule this staff member")
    


               

















# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
# user_cli = AppGroup('user', help='User object commands') 

# # Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("firstname", default="rob")
# @click.argument("lastname", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(firstname, lastname, password):
#     create_user(firstname, lastname, password)
#     print(f'{firstname} created!')

# # this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())

# app.cli.add_command(user_cli) # add the group to the cli

# '''
# Test Commands
# '''

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
