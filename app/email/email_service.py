import smtplib
from jinja2 import Environment, FileSystemLoader
from email.message import EmailMessage


# This class build as Singleton is responsible for sending email verifications
class MailService:
    EMAIL_ADDRESS = ''
    EMAIL_PASSWORD = ''

    smtp_obj = smtplib.SMTP("smtp.gmail.com", 587)

    def init_app(self, app):

        self.EMAIL_ADDRESS = app.config['EMAIL_ADDRESS']
        self.EMAIL_PASSWORD = app.config['EMAIL_PASSWORD']

        self.smtp_obj.ehlo()
        self.smtp_obj.starttls()
        self.smtp_obj.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)

    # Sending email with status changed info
    def send_ticket_status_changed(self, email, firstname, ticket_id, new_status, feedback):
        msg = EmailMessage()
        msg['Subject'] = f'New status of {ticket_id} ticket'
        msg['From'] = self.EMAIL_ADDRESS
        msg['To'] = email

        # Construct the email body with html file content
        file_loader = FileSystemLoader('app/templates/email')
        env = Environment(loader=file_loader)
        template = env.get_template('ticket_status_changed.html')
        output = template.render(firstname=firstname, ticket_id=ticket_id, new_status=new_status, feedback=feedback)
        msg.add_alternative(output, subtype='html')

        # Construct the email body with plain text content
        # email_body = f"Hello {firstname},\n\nYour reported problem with id {ticket_id}:\n\n has now new status:\n\n{new_status}"
        # msg.set_content(email_body)

        self.smtp_obj.send_message(msg)

    # Sending email with status changed info
    def send_service_status_changed(self, email, firstname, service_name, new_status):
        msg = EmailMessage()
        msg['Subject'] = f'New status of {service_name}'
        msg['From'] = self.EMAIL_ADDRESS
        msg['To'] = email

        # Construct the email body with html file content
        file_loader = FileSystemLoader('app/templates/email')
        env = Environment(loader=file_loader)
        template = env.get_template('service_status_changed.html')
        output = template.render(firstname=firstname, service_name=service_name, new_status=new_status)
        msg.add_alternative(output, subtype='html')

        # Construct the email body with plain text content
        # email_body = f"Hello {firstname},\n\n{ service_name }\n\n has changed at your location its status to:\n\n{new_status}"
        # msg.set_content(email_body)

        self.smtp_obj.send_message(msg)

    # Sending email with temporal credentials
    def send_credentials(self, email, password, firstname):
        msg = EmailMessage()
        msg['Subject'] = f'Your new credentials'
        msg['From'] = self.EMAIL_ADDRESS
        msg['To'] = email

        # Construct the email body with html file content
        file_loader = FileSystemLoader('app/templates/email')
        env = Environment(loader=file_loader)
        template = env.get_template('temporal_credentials.html')
        output = template.render(firstname=firstname, email=email, password=password)
        msg.add_alternative(output, subtype='html')

        self.smtp_obj.send_message(msg)
