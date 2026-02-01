from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.amazon.de/-/en/Ninja-FlexDrawer-Compartments-Dishwasher-AF500EUCP/dp/B0CJVNGMFL/?_encoding=UTF8&pd_rd_w=V1wT4&content-id=amzn1.sym.79d1f343-1e12-4a57-8f6f-6e5712b5effc&pf_rd_p=79d1f343-1e12-4a57-8f6f-6e5712b5effc&pf_rd_r=2X6DG7AJHK7Y48BGQJN9&pd_rd_wg=ZbKqQ&pd_rd_r=6de754c2-a184-4b72-ae1f-75c1372d820e&ref_=pd_hp_d_atf_unk&th=1")

content = response.text

soup = BeautifulSoup(content, "html.parser")

print(soup.title)

price = soup.find("div", id="twisterPlusPriceSubtotalWWDesktop_feature_div")
print(price)