from rest_framework import status
from email.message import EmailMessage
import ssl
import smtplib
from rest_framework.response import Response


# - Sending an Email Function -
def send_an_email(email_receiver, building_permit_id, building_permit_new_status):

    # buildup Email password - rqqrozpfeilayrbq
    # buildup Email - buildupbuildingpermits@gmail.com

    # Email Information:
    email_sender = 'buildupbuildingpermits@gmail.com'
    email_password = 'rqqrozpfeilayrbq'
    # email_receiver = 'herutstern@outlook.com'  # temporary
    # building_id = 2  # temporary
    # building_new_status = 'PENDING'  # temporary

    # Email context:
    subject = f'Building Permit Status Has Been Changed - {building_permit_id}'
    body = f"""
        Building number - {building_permit_id}
        is now on {building_permit_new_status}.
        Go check it out on BuildUp http://buildupbuildingpermits.com/
        
        BUILDUP | Your Building Permits Manager
        buildupbuildingpermits@gmail.com
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
    with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=context) as smtp:
        try:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, emailmessage.as_string())
        except smtplib.SMTPException as e:
            # Return 'error'
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)

        # Return
        return Response(status=status.HTTP_200_OK)

# print(send_an_email())
