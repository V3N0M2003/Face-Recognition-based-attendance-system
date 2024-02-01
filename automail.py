import os
import yagmail

receiver = "abhishekghorpade07@gmail.com"  # receiver email address
body = "Attendence File"                    # email body
filename = r"C:\Users\Abhi Ghorpade\Desktop\it f\Face-Recognition-Attendance-System\FRAS\Attendance\Attendance.csv" 

# mail information
yag = yagmail.SMTP("senderabhi07@gmail.com", "bejgcsxezqwabajj")

# sent the mail
yag.send(
    to=receiver,
    subject="Attendance Report",  # email subject
    contents=body,                # email body
    attachments=filename,         # file attached
)
