import imaplib
import email
import smtplib
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    account = 'pythonemailtestbot@gmail.com'
    password = 'gvmqsoyhnlusnvrx'
    # Connect to the email account
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(account, password)
    
    # Select the inbox
    mail.select("inbox")
    
    # Search for new messages
    status, messages = mail.search(None, 'UNSEEN')
    
    
    # Loop through the messages
    # Loop through the messages
    for message in messages[0].split():
        # Get the message
        status, data = mail.fetch(message, '(RFC822)')
    
        # Parse the message
        msg = email.message_from_bytes(data[0][1])
    
        # Get the sender's email address
        sender = msg['From']
        words = sender.split('<')
        sender = words[1][:-1]
        print(sender)
        # Get the message subject
        subject = msg['Subject']
        print(subject)
    
        # Check if the message is multipart
        if msg.is_multipart():
            # Loop through each part of the message
            for part in msg.get_payload():
                # Check if the part is of type text/plain
                if part.get_content_type() == 'text/plain':
                    # Get the contents of the body as a string
                    body = part.get_payload(decode=True)
                    print(body)
        else:
            # Get the contents of the body as a string
            body = msg.get_payload(decode=True)
            print(body)
    
        body = body.decode()
        send_email(sender, body)
        
        
def send_email(RECIPIENT, body):
    SENDER = "pythonemailtestbot@gmail.com"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-west-2"

    SUBJECT = "This is test email for testing purpose..!!"

    BODY_TEXT = (f"Replied body sent from {RECIPIENT} to {SENDER}...\r\n {body}"
                )
                
    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    Replied body sent from <b>{RECIPIENT}</b> to <b>{SENDER}</b>...\r\n {body}
    </body>
    </html>
                """            

    CHARSET = "UTF-8"

    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
        
                        'Data': BODY_HTML
                    },
                    'Text': {
        
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {

                    'Data': SUBJECT
                },
            },
            Source=SENDER
        )
        
    # Catch Error
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
