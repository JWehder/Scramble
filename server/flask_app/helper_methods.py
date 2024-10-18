from flask_mailman import EmailMessage
from bson import ObjectId
import pytz

# Add this line to ensure the correct path
import sys
import os
sys.path.append(os.path.dirname(__file__))

from config import db

def send_email(subject, recipient, body_html):
    """Send an email."""
    msg = EmailMessage(
        subject=subject,
        to=[recipient],
        body=body_html,
    )
    try:
        msg.send()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_all_tournament_ids():
    tournaments_collection = db.tournaments
    tournament_ids = tournaments_collection.distinct('_id')
    return [ObjectId(tid) for tid in tournament_ids]

def get_day_number(day_name: str) -> int:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days.index(day_name)

def convert_utc_to_local(utc_dt, user_tz):
    local_tz = pytz.timezone(user_tz)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_dt