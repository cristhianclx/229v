from flask import Flask
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)


@app.route("/")
def index():
    return {
        "status": "healthy"
    }


@app.route("/exchange-sunat")
def exchange_from_sunat():
    data = requests.get("https://cuantoestaeldolar.pe/")
    soup = BeautifulSoup(data.text, 'html.parser')
    all_elements = soup.find_all("div", class_= "ValueQuotation_valueContainer__eH4KL")
    results = {
        "compra": all_elements[2].text,
        "venta": all_elements[3].text,
    }
    return results