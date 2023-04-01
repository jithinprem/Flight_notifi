import smtplib
from email.message import EmailMessage

class NotificationManager:
    def __init__(self, start_city, dest_city, price):
        self.start_city = start_city
        self.dest_city = dest_city
        self.price = price

    def sendmail(self):
        # Set up SMTP server connection
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'notus1v@gmail.com'
        smtp_password = 'APP_Password' # TODO: add app password
        with smtplib.SMTP(smtp_server, smtp_port) as smtpObj:
            smtpObj.starttls()  # enable TLS encryption
            smtpObj.ehlo()  # identify yourself to the SMTP server
            smtpObj.login(smtp_user, smtp_password)  # log in to the SMTP server

            # Create email message
            msg = EmailMessage()
            msg.set_content(f"current price from {self.start_city} to {self.dest_city} : {self.price} \n")
            msg['Subject'] = 'notifi travel'
            msg['From'] = smtp_user
            msg['To'] = '@gmail.com' # TODO: add customer email

            # Send email message
            smtpObj.send_message(msg)

            # Close SMTP server connection
            smtpObj.quit()




