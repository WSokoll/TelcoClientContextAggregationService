import smtplib
from jinja2 import Environment, FileSystemLoader
from app.email.email_config import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_SALT, EMAIL_SECRET
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer


# This class build as Singleton is responsible for sending email verifications
class MailService:
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # This method sends the verification link for a new user
    @staticmethod
    def send_ticket_status_changed(email, firstname, ticket_id, new_status):
        msg = EmailMessage()
        msg['Subject'] = f'New status of {ticket_id} ticket'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email

        # Construct the email body with html file content
        file_loader = FileSystemLoader('app/templates/email')
        env = Environment(loader=file_loader)
        template = env.get_template('ticket_status_changed.html')
        output = template.render(firstname=firstname, ticket_id=ticket_id, new_status=new_status)
        msg.add_alternative(output, subtype='html')

        # Construct the email body with plain text content
        # email_body = f"Hello {firstname},\n\nYour reported problem with id {ticket_id}:\n\n has now new status:\n\n{new_status}"
        # msg.set_content(email_body)

        MailService.smtpObj.send_message(msg)
