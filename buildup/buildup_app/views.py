from email.message import EmailMessage
import ssl
import smtplib
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['POST'])
def send_an_email(request):

    # buildup Email password - rqqrozpfeilayrbq
    # buildup Email - buildupbuildingpermits@gmail.com

    email_sender = 'buildupbuildingpermits@gmail.com'
    email_password = 'rqqrozpfeilayrbq'
    email_receiver = 'herutstern@outlook.com' # temporary
    building_number_id = 2 # temporary
    building_new_status = 'QUALITY_CHECKER' # temporary

    subject = f'Building Permit Status Has Been Changed - {building_number_id}'
    body = f"""
        Building number - {building_number_id}
        is now on {building_new_status}.
        
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
    return Response(status=status.HTTP_202_ACCEPTED)

