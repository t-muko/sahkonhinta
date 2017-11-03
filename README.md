# sahkonhinta
Hakeepi Norpoolin spottihinnat ja palauttaa ne siistimmässä muodossa.

Apuna on käytetty [Flask mikroframeworkkia](https://www.fullstackpython.com/flask.html) ja AWS lambda deployment on automatisoitu [Zappalla](https://www.zappa.io/).

- TODO: Kuluvan tunnin hinta
- TODO: Laskentaa kalleimmista tunneista
- TODO: Ohjauslogiikkaparametrit lämmityksen ohjaukseen niin että lämmitys kytketään takaisin päälle 
      vasta kun hinta on oikeasti laskenut, eli tunti-pari hintapiikin jälkeen.
      
# Forkkaus / asennus
1. Kloonaa gittirepo
2. Perusta projektille virtualenv python 3.6:lla
3. Asenna tarvittavat paketit virtualenviin: `pip install -r requirements.txt`
4. Varmista että AWS:n profiili ja access keyt löytyy [~/.aws/config tiedostosta](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
5. Jos forkkaat oman versiosi: 
      - editoi zappa_settings.json:iin uniikki S3 bucketin nimi ja tarvittaessa AWS-profiilisi nimi
      - Aja `zappa deploy`
6. Jos taas jatkat aiempaa työtä riittää `zappa update` aiemmin deployatun lambdafuntion päivittämiseksi


      
