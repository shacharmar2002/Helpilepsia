'''
1) Create new gmail account
2) Login with your gmail account and find "Allow less secure apps:" from here: https://myaccount.google.com/security#activity
'''

import smtplib, ssl

sender_email = "testpythonemails316@gmail.com"
passward = "hFK7Rq8EbBit"


def send_email(receiver_email, message):
    context = ssl.create_default_context()

    # Send the message via our own SMTP server.
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("testpythonemails316@gmail.com", passward)
        server.sendmail(sender_email, receiver_email, message)


receiver_email = "shacharmar2002@gmail.com"
message = """\
Subject: Hi there
This message is sent from Python."""
send_email(receiver_email, message)