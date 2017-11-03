from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from html import unescape
import io
import csv
import json
from flask import Flask, Response
from dateutil.parser import parse
from dateutil.parser import parserinfo
from datetime import date, datetime
from pytz import timezone

source_tz = timezone('CET')
output_tz = timezone('Europe/Helsinki')

app = Flask(__name__)


def datetime_serial(obj):
    """JSON serializer for objects not serializable by default json code.
    Returning times as in Europe/Helsinki timezone"""

    if isinstance(obj, (datetime, date)):
        return obj.astimezone(output_tz).isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def palautaDataSarakkeista(jsondata, sarakkeet=(0,)):
    """Hakee JSON-lähdedatasta yhden päivän tiedot"""

    sarakeArvot = {}
    rivilaskuri = 1

    for sarake in sarakkeet:
        for row in jsondata["data"]["Rows"]:
            if not (row.get("IsExtraRow", True)) and (row.get("Columns")[sarake].get("Value", "-")) != '-':
                hours = (unescape(row.get("Name", "no rows available")))
                hour = hours.split()[0]
                riviId=str(rivilaskuri).zfill(2)
                # Tehdään aikavyöhykekäsittely: Alkuperäiset ajat ovat CET.
                sarakeArvot[riviId] = {}
                sarakeArvot[riviId]['starttime'] = source_tz.localize(
                    parse(row.get("Columns")[sarake].get("CombinedName", "no name available") + "T" + hour,
                          parserinfo(dayfirst=True)))
                sarakeArvot[riviId]['CET_hours'] = hours
                # sarakeArvot[hour]['starttime'] =
                sarakeArvot[riviId]['spotprice'] = (row.get("Columns")[sarake].get("Value", "no value available"))
                rivilaskuri = rivilaskuri + 1

    return sarakeArvot


def csvHinnat(jsondata):
    hinnat = {}  # hinnat laitetaan dictionaryyn
    csvoutput = io.StringIO()  # CSV-file kootaan iostringiin
    fieldnames = ['starttime', 'hours', 'spotprice']
    writer = csv.DictWriter(csvoutput, fieldnames=fieldnames)
    writer.writeheader()

    # Haetaan datasta rivit, rivin metatieto ja sarakkeista tarvittavaa dataa
    for row in jsondata["data"]["Rows"]:
        if not (row.get("IsExtraRow", True)):
            hinnat['date'] = (row.get("Columns")[0].get("CombinedName", "no name available"))
            hinnat['hours'] = (unescape(row.get("Name", "no rows available")))
            hinnat['spotprice'] = (row.get("Columns")[0].get("DisplayNameOrDominatingDirection", "no value available"))
            writer.writerow(hinnat)
    return csvoutput.getvalue()


def dictToCsv(data):
    csvoutput = io.StringIO()  # CSV-file kootaan iostringiin
    fieldnames = ['starttime', 'hours', 'spotprice']

    writer = csv.DictWriter(csvoutput, fieldnames=fieldnames)
    writer.writeheader()

    for row in data:
        writer.writerow(row)
    return csvoutput.getvalue()


@app.route('/hello')
def hello():
    return 'Hello vaan ja nyt Windowsista\n'


@app.route('/')
def main():
    req = Request("http://www.nordpoolspot.com/api/marketdata/page/35?currency=,,,EUR")

    try:
        response = urlopen(req)
        # with urlopen(reg) as response:
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        return ('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        return ('Reason: ', e.reason)
    else:
        # everything is fine

        jsondata = json.loads(response.read().decode())  # haetaan URLista JSON ja ladataan se dictionaryyn

        return (Response(
            json.dumps(palautaDataSarakkeista(jsondata, (1,0)), indent=4, sort_keys=True, default=datetime_serial),
            # json.dumps(jsondata, indent=4, sort_keys=True),
            mimetype='application/json'))
        # print(dictToCsv(palautaDataSarakkeesta(jsondata, 0)))

        # return(csvHinnat(jsondata))

        # Haetaan datasta rivit, rivin metatieto ja sarakkeista tarvittavaa dataa


if __name__ == "__main__":
    app.run()
    # main()
