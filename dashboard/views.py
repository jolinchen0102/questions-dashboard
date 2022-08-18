from django.http import JsonResponse
from json2html import *
from django.shortcuts import render
from collections import OrderedDict
from fusioncharts import FusionCharts
import requests
from django.template.loader import render_to_string

RELEVANCE_CHOICES = {
    "1": "KYC onboarding",
    "2": "Funding features",
    "3": "Trading features",
    "4": "Custody features",
    "5": "Fee schedule",
    "6": "Security",
    "7": "Others",
}
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

raw_data = request_questions()

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
    return render(request, 'index.html', {'output': fusionMap.render()})

def get_category_data(data):
    category = {}
    for elem in data:
        cat = RELEVANCE_CHOICES[elem["category"][0]]
        if cat in category:
            category[cat] += 1
        else: category[cat] = 1
    return category

def draw_treeMap(request):
    cat_dict = get_category_data(raw_data)
    total = 0
    for value in cat_dict.values():
        total += value
    dataSource = OrderedDict()
    dataSource["chart"] = OrderedDict(
		{
			"animation": "0",
			"hideTitle": "1",
			"plotToolText": "<div><b>$label</b><br/> <b>Count: </b>$value<br/><b>Percentage: </b>$svalue%</div>",
			"spacex": "0",
			"spacey": "0",
			"horizontalPadding": "1",
			"verticalPadding": "1",
			"hoveronallsiblingleaves": "1",
			"plotborderthickness": ".5",
			"plotbordercolor": "666666",
			"legendpadding": "0",
			"legendItemFontSize": "10",
			"legendItemFontBold": "1",
			"showLegend": "1",
			"legendPointerWidth": "8",
			"legenditemfontcolor": "3d5c5c",
			"algorithm": "squarified",
			"caption": "Tree Map of Questions Categories",
			"legendScaleLineThickness": "0",
			"legendCaptionFontSize": "10",
			"legendaxisbordercolor": "bfbfbf",
			"subcaption": "",
			"legendCaption": "",
			"theme": "zune"
		}
	)
    dataSource["colorrange"] = OrderedDict(
		{
			"mapbypercent": "1",
			"gradient": "1",
			"minvalue": "0",
			"code": "6da81e",
			"startlabel": "",
			"endlabel": "",
			"color": [
				{
					"code": "ffffff",
					"maxvalue": "50",
					"label": ""
				},
				{
					"code": "e24b1a",
					"maxvalue": "100",
					"label": ""
				}
			]
		}
	)
    dataSource["data"] = [
		{
            "label": "Question Categories",
            "value": str(total),
            "data": []
		}
	]
    
    for k, v in cat_dict.items():
        dataSource["data"][0]["data"].append({
			"label": k,
			"value": str(v),
			"sValue": str(round(v/total*100, 2))
		})
        total += v
    treeMap = FusionCharts("treemap", "draw_treeMap", "590", "440", "treemap-container", "json", dataSource)
    return render(request, 'treemap.html', {'output': treeMap.render()})

def get_all_question(request):
    data = raw_data.copy()
    for i in range(len(data)):
        data[i]["category"] = RELEVANCE_CHOICES[data[i]["category"][0]]
    done = json2html.convert(json=data)
    with open("dashboard/templates/dataview.html",'w') as f:
        f.writelines(done)
    return render(request, 'dataview.html')

def base(request):
    return render(request, 'base.html')
