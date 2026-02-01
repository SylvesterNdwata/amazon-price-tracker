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
live_url = "https://www.amazon.de/-/en/Ninja-FlexDrawer-Compartments-Dishwasher-AF500EUCP/dp/B0CJVNGMFL/?_encoding=UTF8&pd_rd_w=ebgGP&content-id=amzn1.sym.79d1f343-1e12-4a57-8f6f-6e5712b5effc&pf_rd_p=79d1f343-1e12-4a57-8f6f-6e5712b5effc&pf_rd_r=KEQ97BDC1MJVDKV7MMYE&pd_rd_wg=JiE5G&pd_rd_r=5a84f461-b571-4e29-aba4-445759ec333d&ref_=pd_hp_d_atf_unk&th=1"

header = {
    "Accept-Language": "de-DE,de;q=0.9,en-DE;q=0.8,en-US;q=0.7,en;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}

response = requests.get(live_url, headers=header)

web_content = response.text

soup = BeautifulSoup(web_content, "html.parser")

price_element = soup.find("div", class_="a-section a-spacing-none a-spacing-top-micro _p13n-desktop-sims-fbt_fbt-desktop_display-flex__1gorZ")
actual_span = price_element.select_one("div span")

price = actual_span.find("span", class_="a-offscreen").get_text().strip("€")

title_element = soup.find("div", id="titleSection")
product_name = title_element.find("h1", id="title").get_text()

msg = MIMEText(f"{product_name} is now €{price}\nFind it here: {live_url}", "plain", "utf-8")
msg["Subject"] = "Amazon Price Alert"
msg["From"] = email
msg["To"] = to_addr


if float(price) < 200:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(email, to_addr, msg.as_string())