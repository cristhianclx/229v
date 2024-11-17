from flask import Flask
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
api = Api(app)


class PINGResource(Resource):
    def get(self):
        return {
            'status': 'healthy',
        }


class IPResource(Resource):
    def get(self):
        data = requests.get('https://ipinfo.io/json').json()
        return {
            "IP": data["ip"],
            "country": data["country"],
            "region": data["region"],
            "city": data["city"]
        }


class ExchangeRatePENUSDSunatResource(Resource):
    def get(self):
        data = requests.get("https://cuantoestaeldolar.pe/")
        soup = BeautifulSoup(data.text, 'html.parser')
        all_elements = soup.find_all("div", class_= "ValueQuotation_valueContainer__eH4KL")
        results = {
            "compra": all_elements[2].text,
            "venta": all_elements[3].text,
        }
        return results


class PokemonInfoResource(Resource):
    def get(self, id):
        data = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(id)).json()
        print(data)
        return {
            "id": id,
            "abilities": [], # ["static", "lightning-rod"]
            "forms": [], # ["pikachu"]
            "height": "", # 4
            "weight": "" # 60
        }


api.add_resource(PINGResource, '/')
api.add_resource(IPResource, '/ip')
api.add_resource(ExchangeRatePENUSDSunatResource, '/exchange-rate/PEN-USD/sunat')
api.add_resource(PokemonInfoResource, "/pokemon/info/<id>")