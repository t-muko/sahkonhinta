from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from html import unescape
import io
import csv
import json
from flask import Flask
app = Flask(__name__)

def palautaDataSarakkeesta(jsondata, sarake=0):
    sarakeArvot={}

    for row in jsondata["data"]["Rows"]:
        if not (row.get("IsExtraRow", True)):
            hours = (unescape(row.get("Name", "no rows available")))
            hour = hours.split()[0]
            sarakeArvot[hour]={}
            sarakeArvot[hour]['hours']=hours
            sarakeArvot[hour]['date'] = (row.get("Columns")[sarake].get("CombinedName", "no name available"))
            sarakeArvot[hour]['spotprice'] = (row.get("Columns")[sarake].get("DisplayNameOrDominatingDirection", "no value available"))
    return sarakeArvot

def csvHinnat(jsondata):
    hinnat = {}  # hinnat laitetaan dictionaryyn
    csvoutput = io.StringIO()  # CSV-file kootaan iostringiin
    fieldnames = ['date', 'hours', 'spotprice']
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
    fieldnames = ['date', 'hours', 'spotprice']

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
        #with urlopen(reg) as response:
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        return('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        return('Reason: ', e.reason)
    else:
        # everything is fine

        jsondata=json.loads(response.read().decode())   # haetaan URLista JSON ja ladataan se dictionaryyn

        return(json.dumps(palautaDataSarakkeesta(jsondata, 0)))
        #print(dictToCsv(palautaDataSarakkeesta(jsondata, 0)))

        #return(csvHinnat(jsondata))

        # Haetaan datasta rivit, rivin metatieto ja sarakkeista tarvittavaa dataa

if __name__ == "__main__":
    app.run()
    #main()
