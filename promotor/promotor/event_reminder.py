import frappe
from frappe.utils import now_datetime, add_to_date

def send_event_reminders():
    current_time = now_datetime()

    time_windows = {
        '1 hour': add_to_date(current_time, hours=1),
        '1 day': add_to_date(current_time, days=1),
        '1 week': add_to_date(current_time, weeks=1)
    }

    for label, notify_time in time_windows.items():
        events = frappe.get_all("Event",
            filters={
                "starts_on": ("between", [notify_time, add_to_date(notify_time, minutes=1)]),
                "custom_enable_reminders": 1
            },
            fields=["name", "subject", "owner", "starts_on"]
        )

        print(f"[{label}] Total matching events: {len(events)}")
        for event in events:
            print("Sending notification for:", event)
            send_notification(event, label)

def send_notification(event, label):
    user = event.get("owner")
    subject = f"Reminder: {event.get('subject')} - {label} remaining"
    message = f"Your event '{event.get('subject')}' is scheduled to start at {event.get('starts_on')}.\nThis is a reminder {label} before the event."

    try:
        # Send Email
        user_email = frappe.db.get_value("User", user, "email")
        if user_email:
            frappe.sendmail(
                recipients=[user_email],
                subject=subject,
                message=message
            )

        # Create Notification Log (Frappe in-app notification)
        doc = frappe.new_doc("Notification Log")
        doc.subject = subject
        doc.email_content = message
        doc.for_user = user
        doc.type = "Alert"
        doc.document_type = "Event"
        doc.document_name = event.get("name")
        doc.seen = 0
        doc.insert(ignore_permissions=True)

        frappe.db.commit()
        print(f"Notification sent to: {user} ({user_email})")

    except Exception as e:
        frappe.log_error(message=str(e), title="Send Notification Failed")
