import smtplib
import requests
import os
import datetime
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if None in [EMAIL, PASSWORD, WEATHER_API_KEY]:
    print("Error: Please set all required environment variables.")
    exit(1)


def send_email(subject, body, to_email, attachment=None):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment:
        with open(attachment, "rb") as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment}")
        msg.attach(part)

    try:
        smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_object.starttls()
        smtp_object.login(EMAIL, PASSWORD)
        smtp_object.send_message(msg)
        smtp_object.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", str(e))


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            current_weather = weather_data['list'][0]
            current_temperature = current_weather['main']['temp']
            current_weather_description = current_weather['weather'][0]['description']
            current_time = current_weather['dt_txt']
            past_and_next_days_data = [(item['dt_txt'], item['main']['temp']) for item in weather_data['list'][1:]]
            return current_temperature, current_weather_description, current_time, past_and_next_days_data
        else:
            print("Failed to fetch weather data:", response.status_code)
            return None, None, None, None
    except Exception as e:
        print("Error fetching weather data:", str(e))
        return None, None, None, None


def send_temperature_graph_email(to_email , city):
    current_temperature, current_weather_description, current_time, past_and_next_days_data = get_weather(city)
    if current_temperature is not None and current_weather_description is not None and current_time is not None and past_and_next_days_data:
        times = [item[0] for item in past_and_next_days_data]
        temperatures = [item[1] for item in past_and_next_days_data]

        plt.figure(figsize=(10, 5))
        plt.plot(times, temperatures, marker='o', linestyle='-')
        plt.title('Temperature vs Time')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        try:
            plt.savefig('temperature_vs_time.png')
            plt.close()
            print("Temperature graph saved successfully.")

            subject = "Temperature Graph and Current Weather Update"
            body = (f"Current weather in {city}:\nTemperature: {current_temperature}°C\n"
                    f"Weather: {current_weather_description}\nTime: {current_time}\n\n"
                    "Temperature graph for the past and next 7 days attached.")

            send_email(subject, body, to_email, "temperature_vs_time.png")
            os.remove("temperature_vs_time.png")
            print("PNG file deleted.")
        except Exception as e:
            print("Error saving temperature graph or sending email:", str(e))
    else:
        print("Failed to send email: Weather data not available")

