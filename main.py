from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

email = os.environ.get("email")
password = os.environ.get("password")
to_addr = os.environ.get("recipient")

url = "https://appbrewery.github.io/instant_pot/"

header = {
    "Accept-Language": "de-DE,de;q=0.9,en-DE;q=0.8,en-US;q=0.7,en;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}

response = requests.get("https://appbrewery.github.io/instant_pot/", headers=header)

web_content = response.text

soup = BeautifulSoup(web_content, "html.parser")

price_element = soup.find("div", class_="a-section a-spacing-none a-spacing-top-micro _p13n-desktop-sims-fbt_fbt-desktop_display-flex__1gorZ")

actual_span = price_element.select_one("div span")

price = actual_span.find("span", class_="a-offscreen").get_text().strip("$")

title_element = soup.find("div", id="titleSection")
product_name = title_element.find("h1", id="title").get_text()

msg = MIMEText(f"{product_name} is now €{price}\nFind it here: {url}", "plain", "utf-8")
msg["Subject"] = "Amazon Price Alert"
msg["From"] = email
msg["To"] = to_addr


if float(price) < 101:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(email, to_addr, msg.as_string())