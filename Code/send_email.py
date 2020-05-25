import smtplib, ssl

sender_email = "testpythonemails316@gmail.com"
passward = "hFK7Rq8EbBit"

def send_email(receiver_email, message):
    context = ssl.create_default_context()

    # Send the message via our own SMTP server.
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, passward)
        server.sendmail(sender_email, receiver_email, message)
