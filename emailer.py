import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def sendmail(
        sender_email = "trishubhshukla@gmail.com",
        sender_password = "ihgialgblmnceozi",
        receiver_email = "ryanagent007@gmail.com",
        userid="1"):

    subject = "Detected Obscenity Screenshot"+userid

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    #Load the PNG image file and attach it to the email:

    with open("pic.png", "rb") as f:
        image_data = f.read()
    image = MIMEImage(image_data)
    image.add_header('Content-Disposition', 'attachment', filename="pic.png")
    msg.attach(image)

    #Add the message content to the email body:

    message = "Notification content"
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
sendmail()