import frappe
from frappe.utils import now_datetime, add_to_date, get_datetime

def send_event_reminders():
    print(">>> send_event_reminders function started")
    now = now_datetime()
    print("Current time:", now)

    time_frames = {
        "1_hour": add_to_date(now, hours=1),
        "1_day": add_to_date(now, days=1),
        "1_week": add_to_date(now, weeks=1),
    }

    for label, reminder_time in time_frames.items():
        events = frappe.get_all("Event",
            filters={
                "custom_enable_reminders": 1,
                "starts_on": ["between", [reminder_time, add_to_date(reminder_time, minutes=1)]],
                "status": "Open"
            },
            fields=["name", "subject", "starts_on", "owner"]
        )

        for event in events:
            user = frappe.get_doc("User", event.owner)
            subject = f"[Reminder: {label.replace('_', ' ')}] Upcoming Event: {event.subject}"
            message = f"Your event <b>{event.subject}</b> is scheduled on {event.starts_on}. (Reminder set for {label.replace('_', ' ')})"

            # Send Email Notification
            frappe.sendmail(
                recipients=[user.email],
                subject=subject,
                message=message
            )

            # Send In-App Notification
            frappe.publish_realtime(
                event='eval_js',
                message=f'frappe.show_alert("Reminder: {event.subject} in {label.replace("_", " ")}")',
                user=user.name
            )
