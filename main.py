import requests
from datetime import datetime
import smtplib
import time


MY_LAT = 58.594719 # Your latitude
MY_LONG = 16.183630 # Your longitude
my_email = "senderemailservice23.1@gmail.com"
password = "kqprjgdsjnfzxtsu"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    iss_position = (iss_latitude, iss_longitude)
    my_location = (MY_LAT,  MY_LONG)

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-53 <= iss_latitude <= MY_LAT+63 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtb.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="dawood.rizwan@outlook.com",
                                msg=f"Subject:Iss Notification!\n\n Iss is here look up")


# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



