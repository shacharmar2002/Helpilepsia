import smtplib
sender = "shacharmar2002@gmail.com"
receivers = ["shahar.schneider25198@gmail.com"]

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

smtpObj = smtplib.SMTP('smtp.gmail.com', 25)
smtpObj.sendmail(sender, receivers, message)
print ("Successfully sent email")
