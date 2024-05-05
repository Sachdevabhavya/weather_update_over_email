# Weather Update Over Email

This Python script fetches current weather information for a specified city and sends it to a recipient via email. Additionally, it generates a graph depicting the weather forecast for the next 5 days and attaches it to the email.

## Environment Variables
- **EMAIL**: Email address from which the weather updates will be sent.
- **PASSWORD**: Password for the email account.
- **WEATHER_API_KEY**: API key for accessing weather data.
- **RECEIVER_EMAIL**: Email address of the recipient.

## Dependencies
- `schedule`
- `smtplib`
- `requests`
- `os`
- `datetime`
- `matplotlib.pyplot`
- `email.mime.multipart`
- `email.mime.text`
- `email.mime.base`
- `email.encoders`

## How to Run
To run the script, simply execute `python filename.py`. Ensure that the necessary environment variables are set correctly in the `.env` file.

## Note
Currently, the city name is hardcoded within the script. If you wish to change the city, modify the respective variable in the script.
