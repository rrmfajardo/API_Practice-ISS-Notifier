import requests, smtplib
from datetime import datetime
import config # contains my user pass etc...
import time

MY_LAT = -49.222 #testing purposes
MY_LONG = 30.222 #testing purposes

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])
print(iss_latitude)
print(iss_longitude)

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) - 7
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) - 7 + 24

time_now = datetime.now()
hour_now = 19
# time_now.hour

while True:
    if hour_now >= sunrise or hour_now <= sunset:
        if iss_latitude - 5 <= config.MYLAT <= iss_latitude + 5:
            if iss_longitude - 5 <= config.MYLONG <= iss_longitude + 5:
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=config.MYEMAIL, password=config.PASSWORD)
                    connection.sendmail(from_addr=config.MYEMAIL,
                                        to_addrs=config.TO_EMAIL,
                                        msg=f"Subject:ISS IS ABOVE!\n\nQuickly, look up!")
    time.sleep(10)