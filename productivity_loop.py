import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import time
import random
import pandas as pd

class notify:
    def __init__(self,base):
        self.base=base
    def send_email(self,rec, message,files=[]):
        msg = MIMEMultipart()




        # Send the message via our own SMTP server.

        #msg.attach(MIMEText(msg, 'plain'))
        if len(files)>0:

            for file in files:
                with open(file, 'rb') as f:
                    img_data = f.read()


                image = MIMEImage(img_data, name=os.path.basename(file))
                msg.attach(image)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("mikebell180@gmail.com", "felblbqjqihploho")
        text = msg.as_string()
        server.sendmail("mikebell180@gmail.com", rec, message)
        server.quit()
    def start_text(self):
        message=f"Productivity Time Starts Now!\nView tasks at {self.base}/tasks"
        self.send_email("8609298636@txt.att.net",message)
    def end_text(self):
        message = f"Productivity Time Ends Now!\nLog your activity at {self.base}/logs"
        self.send_email("8609298636@txt.att.net", message)
def main(base):
    text = notify(base)
    while 1:

        t = time.localtime()
        if t.tm_hour==9:
            minute_interval=random.randrange(0,59)
            schedule=[x for x in range(9,22,1)]
            i=0
            while i<len(schedule)-1:
                t=time.localtime()
                if t.tm_hour == schedule[i] and t.tm_min == minute_interval:
                    df=pd.read_csv("activity_logs.csv", index_col=0)
                    pd.concat([df,pd.DataFrame([[datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"Nothing"]],columns=df.columns,index=[len(df)])]).to_csv("activity_logs.csv")
                    text.start_text()
                    time.sleep(360)
                    text.end_text()
                    i+=1
                time.sleep(60)
            time.sleep(43200)
main("https://54.198.186.121:8080")