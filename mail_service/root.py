import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from authentication.admin import ADMIN_SENDER_MAIL, ADMIN_SENDER_LOGIN_PASSWORD


def send_message_to_admin_about_publishing_new_product(publisher_email, product_id):
    message = build_message_with_subject(ADMIN_SENDER_MAIL, ADMIN_SENDER_MAIL, "New Product")
    link_to_approve = "http://127.0.0.1:5000/modify_product/change_product_status/approve"
    link_to_decline = "http://127.0.0.1:5000/modify_product/change_product_status/decline"
    body = f"Dear Admin, \nA new product by {product_id} id has been sent to the review.\nThe owner is {publisher_email}." \
           f"\nYou can approve it via {link_to_approve} \nor decline via {link_to_decline}"
    message.attach(MIMEText(body, "plain"))

    send(ADMIN_SENDER_MAIL, message)


def send_message_to_user_about_approving_or_declining_the_product(owner, product, is_approved):
    result = "Approved" if is_approved else "Declined"
    (title, desc) = product

    message = build_message_with_subject(ADMIN_SENDER_MAIL, owner, f"Product {title}'s status")

    body = f"Dear {owner}, \nProduct \"{title}\" has been {result}"
    message.attach(MIMEText(body, "plain"))
    send(owner, message=message)


def build_message_with_subject(from_email, to_email, subject):
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    return message


def send(receiver, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(ADMIN_SENDER_MAIL, ADMIN_SENDER_LOGIN_PASSWORD)
        server.sendmail(ADMIN_SENDER_MAIL, receiver, message.as_string())
