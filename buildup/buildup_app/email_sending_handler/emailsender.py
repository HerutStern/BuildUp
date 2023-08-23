from rest_framework import status
from email.message import EmailMessage
import ssl
import smtplib
from rest_framework.response import Response


# - Sending an Email Function -
def send_an_email(email_receiver, building_permit_id, building_permit_new_status):

    # Email Information:
    email_sender = ''
    email_password = ''
    # email_receiver = 'herutstern@outlook.com'  # temporary
    # building_id = 2  # temporary
    # building_new_status = 'PENDING'  # temporary

    # Email context:
    subject = f'Building Permit Status Has Been Changed - {building_permit_id}'
    body = f"""
        Building number - {building_permit_id}
        is now on {building_permit_new_status}.
        
        
        BUILDUP | Your Building Permits Manager
        buildupbuildingpermits@gmail.com
        link
        """

    # Setting the Email message with EmailMessage()
    emailmessage = EmailMessage()
    emailmessage['From'] = email_sender
    emailmessage['To'] = email_receiver
    emailmessage['Subject'] = subject
    emailmessage.set_content(body)

    context = ssl.create_default_context()

    # Sending the Email
    success = False
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        try:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, emailmessage.as_string())
        except smtplib.SMTPException as e:
            # return 'error'
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # return 'sent'
        return Response(status=status.HTTP_202_ACCEPTED)

# print(send_an_email())
