import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin._messaging_utils import Notification

cred = credentials.Certificate("config/credentials.json")


firebase = firebase_admin.initialize_app(cred)

message = messaging.Message(
    # token="d98SnykNQW6oO6hQsbwcPW:APA91bEcMVvV7usgzRW59YyMWB5XNi7ubpxR14okOM5bst_crG308DJZELRSkveeNFw_A9jjEcZKq1_uNpX3TqBifC5MM14NMdgsGoM4IXZj9-zeZDfTItylfUkR52Dpmu5cpqVBvKs3",
    notification=Notification(
        title="Test",
        body="Hello",
    ),
    topic="/topics/allUsers",
)
print(message.notification)
response = messaging.send(message)

# Response is a message ID string.
print("Successfully sent message:", response)
