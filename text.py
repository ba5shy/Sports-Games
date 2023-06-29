from twilio.rest import Client
import sports
from datetime import datetime

def main():
    sendMessage("whatsapp:+966512345678")


def sendMessage(contact):
    text = createMessage()
    message = client.messages.create(
    from_="whatsapp:+123456789",
    body=text,
    to=contact
    )
    return message.sid

def createMessage():
    header = "Todays Games (" + str(datetime.now().strftime('%x')) + "):\n"
    header += sports.main()
    return header

    
account_sid = "yourSID"
auth_token = "yourToken"
# initiate client
client = Client(account_sid, auth_token)

