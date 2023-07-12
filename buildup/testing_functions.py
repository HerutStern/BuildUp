from email.message import EmailMessage
import ssl
import smtplib

# buildup - rqqrozpfeilayrbq
# buildup - buildupbuildingpermits@gmail.com

email_sender = 'buildupbuildingpermits@gmail.com'
email_password = 'rqqrozpfeilayrbq'
email_receiver = 'herutstern@outlook.com'

subject = 'yeeeeeessssssss'
body = """
I did it!!
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
