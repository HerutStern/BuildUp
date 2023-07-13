from email.message import EmailMessage
import ssl
import smtplib

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, request
from rest_framework.decorators import api_view, permission_classes

from buildup_app.serializers import SignupSerializer, CreateCompanySerializer


# - Sign-Up Function -
@api_view(['POST'])
def signup_new_company(request):
    new_user = SignupSerializer(data=request.data)
    new_user.is_valid(raise_exception=True)
    print(new_user.validated_data)

    new_user.save()

    return Response(data=new_user.data)


# - Getting User Information Function -
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_information(request):
    serializer = SignupSerializer(instance=request.user)
    return Response(serializer.data)


# - Sending an Email Function -
@api_view(['POST'])
def send_an_email(request):

        # buildup Email password - ***
        # buildup Email - ***

    # Email Information:
    email_sender = '***'
    email_password = '***'
    email_receiver = 'herutstern@outlook.com' # temporary
    building_number_id = 2 # temporary
    building_new_status = 'QUALITY_CHECKER' # temporary

    # Email context:
    subject = f'Building Permit Status Has Been Changed - {building_number_id}'
    body = f"""
        Building number - {building_number_id}
        is now on {building_new_status}.
        
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
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_202_ACCEPTED)

