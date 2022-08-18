from django.http import HttpResponse
from django.shortcuts import render
from collections import OrderedDict
from fusioncharts import FusionCharts
import requests
import json

RELEVANCE_CHOICES = (
    (1, "KYC onboarding"),
    (2, "Funding features"),
    (3, "Trading features"),
    (4, "Custody features"),
    (5, "Fee schedule"),
    (6, "Security"),
    (7, "Others"),
)
COUNTRY_MAP = {
		"China": "101",
		"Singapore": "119",
		"United Kingdom": "170",
		"United States": "23",
    }

# Create your views here.
def request_questions():
    try:
        r = requests.get('https://simple-faq-collector.herokuapp.com/chatbotFAQ/question/')
        return r.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def get_geolocation_data(data):
    geoloc = {}
    for elem in data:
        country = COUNTRY_MAP[elem["country"]]
        if country in geoloc:
            geoloc[country] += 1
        else: geoloc[country] = 1
    return geoloc

def myFirstMap(request):
    raw_data = request_questions()
    geo_dict = get_geolocation_data(raw_data)
    dataSource = OrderedDict()
    mapConfig = OrderedDict()
    mapConfig["caption"] = "Geographic Location Population"
    mapConfig["subcaption"] = ""
    mapConfig["numbersuffix"] = ""
    mapConfig["includevalueinlabels"] = "1"
    mapConfig["labelsepchar"] = ":"
    mapConfig["entityFillHoverColor"] = "#FFF9C4"
    mapConfig["theme"] = "fusion"
    colorDataObj = {
        "minvalue": "0",
        "code": "#FFE0B2",
        "gradient": "1",
        "color": [{
                "minValue": "0.5",
                "maxValue": "3",
                "code": "#FFD74D"
            },
            {
                "minValue": "3.0",
                "maxValue": "6.0",
                "code": "#FB8C00"
            },
            {
                "minValue": "6.0",
                "maxValue": "9.0",
                "code": "#E65100"
            }
        ]
    }
    dataSource["chart"] = mapConfig
    dataSource["colorrange"] = colorDataObj
    dataSource["data"] = []
    for k,v in geo_dict.items():
        dataSource["data"].append({
			"id": k,
			"value": str(v),
			"showLabel": "1"
		})
    fusionMap = FusionCharts("maps/worldwithcountries", "myFirstMap", "590", "440", "myFirstmap-container", "json", dataSource)
    print(dataSource["data"])
    return render(request, 'index.html', {'output': fusionMap.render()})

