#this file will contain all the utillity functions that will be used in the main file
from datetime import date, timedelta
from flask import current_app


from flask_mail import Message
import schedule
import time
import threading

from .models import User


stop_scheduler = threading.Event()


def schedule_email_job():
    schedule_time = current_app.config.get('SCHEDULE_TIME', "08:00")
    schedule.every().day.at(schedule_time).do(send_upcoming_birthday_emails)


# find all the birthdays that are today (upcoming)
# # upcoming_birthdayes = today + 1 # to add option to choose the delta dayes (+ timedelta(deys=1))
def find_upcoming_birthdays(days_ahead):
    """מחזיר רשימת אנשי קשר שאצלם יום הולדת במרחק days_ahead ימים."""
    target_date = date.today() + timedelta(days=days_ahead)
    from website.models import db
    month = target_date.month
    day = target_date.day

    from .models import Contact, User
    return Contact.query.filter(
        db.extract('month', Contact.date) == month,
        db.extract('day', Contact.date) == day
    ).all()

    # today = date.today()
    # upcoming_birthdays = []

    # try:
    #     contacts = Contact.query.all()
    #     if not contacts:
    #         print("No contacts found.")
    #         return upcoming_birthdays
        
    #     for contact in contacts:
    #         if contact.date and contact.date == today:
    #             upcoming_birthdays.append(contact)
    # except Exception as e:
    #     print(f"Error fetching contacts: {e}")    
                
    # return upcoming_birthdays



def send_upcoming_birthday_emails(days_ahead: int = 1):
    contacts_list = find_upcoming_birthdays(days_ahead)
    for contact in contacts_list:
        user = User.query.get(contact.user_id)
        if not user:
            print(f"User with ID {contact.user_id} not found.")
            continue

        user_email = user.email
        if not user_email:
            print(f"User with ID {contact.user_id} has no email address.")
            continue

        contact_age = calculate_age(contact.date + timedelta(days=days_ahead))
        if contact_age < 0:
            print(f"Contact {contact.name} has an invalid age.")
            continue
        msg = Message(
            subject='Birthday Alert',
            recipients=[user_email],
        )
        msg.body = (
                    f'שלום {user.name},\n\n'
                    f'רק רצינו להזכיר לך של{contact.name}  יש מחר יומהולדת-{contact_age}!\n\n'
                    f'אל תשכחי לאחל לה/לו יומהולדת שמח!🎉'
                    )
        print({msg.body})
        #from . import mail
        # mail.send(msg)

def calculate_age(birth_date):
    today = date.today()
    age = today.year -  birth_date.year
    return age


# def start_scheduler():
#     """הפעלת מתזמן לשליחת מיילים על ימי הולדת קרובים."""
#     schedule.every().day.at(SCHEDULE_TIME).do(send_upcoming_birthday_emails)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)



def start_scheduler():
    while not stop_scheduler.is_set():
        schedule.run_pending()
        time.sleep(1)
              
