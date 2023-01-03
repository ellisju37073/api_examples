import requests
import json
import webbrowser
from datetime import date
from datetime import timedelta

def rover():
    today = date.today()
    print(today)
    threedays = today - timedelta(days=3)
    params = {"earth_date": threedays, "api_key": "ekzhH2EN2c076XH54seXButHeyXM8MPAMXj2NahP"}
    f = r"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?"
    #https://holypython.com/api-2-mars-weather/
    data = requests.get(f, params=params)
    a = json.loads(data.text)
    print(a)

    for i in a["photos"]:
        print(i, "\n\n\n")

        b = a["photos"][10]["img_src"]
        print(a["photos"][1]["img_src"])

    webbrowser.open(b)



rover()