import xmltodict
import requests


def rtojson(url):
    return xmltodict.parse(requests.get(url).content)