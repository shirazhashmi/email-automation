import SendTo
import SendFrom
import time
import smtplib
import mimetypes
from email.message import EmailMessage

# variables
max_emails_per_email = 500
total_email_send = 0

if max_emails_per_email > len(SendTo.emailsTo):
    new_max_emails_per_email = len(SendTo.emailsTo)
else:
    new_max_emails_per_email = max_emails_per_email

s = smtplib.SMTP('smtp.mail.me.com', 587)  # empty constructor
s.ehlo()
s.starttls()
s.set_debuglevel(False)

message = EmailMessage()
message['Subject'] = "Customer Care"
for sender in SendFrom.fromEmail:
    s.login(sender["Email"], sender["Password"])
    for index in range(new_max_emails_per_email):
        try:
            body = "email body"
            message.set_content(body)
            mime_type, _ = mimetypes.guess_type('sample.pdf')
            mime_type, mime_subtype = mime_type.split('/')
            with open('sample.pdf', 'rb') as file:
                message.add_attachment(file.read(),maintype=mime_type,subtype=mime_subtype,filename='sample.pdf')

            message['From'] = "Shiraz"
            message['To'] = SendTo.emailsTo[index]["Email"]
            # s.send_message(message)
            s.sendmail(sender["Email"], message['To'], message)
            total_email_send = index + 1
            info = {"Index No.": index, "Send to.": message['To'],"From .": sender["Email"],"At Time.": time.asctime(time.localtime(time.time())), "Total.": total_email_send}
            history_info = "***** Last Email History *****\n\nIndex No : " + str(index) + "\nSend to : " + message['TO'] + "\nFrom : "+sender["Email"] + "\nAt Time : " + time.asctime(time.localtime(time.time())) + "\nTotal : " + str(total_email_send)
            with open("history.txt","w") as file:
                file.write(history_info)
            print(info)
        except smtplib.SMTPServerDisconnected as e:
            print(e.args)
        except smtplib.SMTPRecipientsRefused as msg:
            print(str(msg))

    s.quit()

