import serial
import time
from math import radians, cos, sin, asin, sqrt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


ser = serial.Serial('COM3', 9800, timeout=1)
time.sleep(2)
coordinates = [0.0, 0.0]
j = 0
t1 = 300
lat1 = radians(13.13681)
lon1 = radians(77.56753)


def send_mail(latitude, longitude, to = "to-address", emg=0):

    first_mail_body = "\nThe user has gone outside the 5km mark radius from home.\n\nCurrent user locations\nLatitude : " + str(latitude) + "\nLongitude : " + str(longitude) + "\n\nLocation will be sent every 5 mins from now on, until user is inside the safe zone."

    second_mail_body = "\nThe user is currently inside the 5km radius.\n\nCurrent user locations\nLatitude : " + str(latitude) + "\nLongitude : " + str(longitude)

    sender_address = 'sender-mail'
    sender_pass = 'sender-password'
    receiver_address = to

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'ALERT! ALERT! ALERT!'

    if emg:
        message.attach(MIMEText(first_mail_body, 'plain'))
    else:
        message.attach(MIMEText(second_mail_body, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def calc_distance(lat2, lon2):
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371

    return c * r


while True:
    line = ser.readline()
    if line:
        string = line.decode()

        if (isfloat(string)):
            num = float(string)
            coordinates[j] = num
            print(num, end="")
            j += 1

        elif (not(string.isdigit())):
            print(string)

        if j == 2:
            lat2 = radians(coordinates[0])
            lon2 = radians(coordinates[1])
            
            distance = calc_distance(lat2, lon2)

            if (distance > 5 and time.time()-t1 >= 300):
                t1 = time.time()
                send_mail(latitude=lat2, longitude=lon2, emg=1)
            elif (distance <= 5):
                send_mail(latitude=lat2, longitude=lon2)

            print("Distance is ", distance)
            j = 0
        
        time.sleep(2)

ser.close()
