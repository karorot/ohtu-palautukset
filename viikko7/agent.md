# Viikko 7: AI Agent in Action

## Päätyikö agentti toimivaan ratkaisuun?
Ei päätynyt (heti)! Tappelin aikani sen kanssa miksi sovellus ei käynnistynyt virtuaaliympäristössä sen jälkeen, kun agentti ilmoitti sen valmiiksi. Virheeni oli, että en käynyt heti tutkimassa agentin tekeleitä - sen luoma sovelluksen uusi käynnistystiedosto oli nimittäin kokonaan tyhjä. No, pienellä lisäpromptailulla agentti täytti tiedoston koodilla ja pääsin ihmettelemään itse sovellusta, mutta jo ensimmäinen peliyritys kaatui bugiin. Korjailujen jälkeen sovellus toimi ja myös lisäpyyntöjen jälkeen agentti osasi seurata testien kautta paremmin ettei vastaavaa käynyt uudestaan.

Eräs hieman hassu yksityiskohta oli se, että agentti teki tai jätti koodiin paljon Pylint-virheitä. Esimerkiksi "trailing whitespace"-virheitä on koodissa solkenaan.

## Miten varmistuit, että ratkaisu toimii? Oletko ihan varma, että ratkaisu toimii oikein?
Testasin ensin kaikkia pelimoodeja lyhyesti manuaalisesti ja niistä löytyikin heti bugeja. En tehnyt valtavan perusteellisia testejä, vaan lähinnä kokeilin että kaikki pelimoodit vaikuttivat toimivan oikein. Sitten kun sovellus vaikutti toimivalta, pyysin agentilta yksikkötestit, jotka se loi ja jotka myös menivät muutaman korjauskierroksen jälkeen läpi. Koska kyse on agenttikoodista, pitäisi koodi käydä varmasti vieläkin tarkemmin läpi, jotta voisi varmistua sen toimivan aina oikein. Nythän myös testit ovat agentin käsialaa, joten ne eivät lopulta anna täydellistä turvallisuuden tunnetta.

## Kuinka paljon jouduit antamaan agentille komentoja matkan varrella?
Yhteistyö agentin kanssa alkoi hyvin ja se ryhtyi toteuttamaan web-käyttöliittymää ohjeideni mukaan, pitäen mielessä että olemassaolevaa koodia tulisi varjella mahdollisimman paljon. Lisäksi agentti kyseli innokkaasti haluaisinko esim. lisää animaatioita tai äänitehosteita. Ongelmia tuli kuitenkin paljon, kun pyysin agenttia suorittamaan ohjelman, eikä se saanut Poetryä jostain syystä toimimaan. Pitkällisen säätämisen jälkeen agentti varmistui mielestään siitä, että ohjelma toimii muutosten jälkeen ja pääsin itsekin sitä testailemaan. Agentti osasi käsitellä bugit varsin nohevasti kunhan niistä vain ensin ilmoitti sille ja loppua kohti se suoritti myös testit itsenäisesti aina muutosten jälkeen.

## Kuinka hyvät agentit tekemät testit olivat?
Pyysin agenttia kirjoittamaan automaattiset testit "kaikille tarvittaville perustoiminnoille", jotta ne voisi aina ajaa muokkausten jälkeen. Näin agentti sitten jatkossa tekikin ja jos se huomasi testien epäonnistuvan, se ryhtyi heti korjaamaan tilannetta. Lisäksi agentti teki omatoimisesti dokumentaatiota testeistä.

Ikävämpi juttu oli, että agentti kirjoitti kaikki testit yhteen ja samaan tiedostoon, josta tuli yli 30 testin kanssa melkoinen litania. Agentti kirjoitti testit aivan kaikelle alkaen aloitussivun latautumisesta oikein, mikä lienee aivan liian iso määrä. Lisäksi se käytti testeissä pohjana itselleni tuntematonta tyyliä ja loi ensin testi-clientin ja session. Esimerkiksi kurssilla esiteltyjä Mock-olioita se ei käyttänyt.

Testit siis vaikuttavat ensisilmäyksellä kattavilta, mutta takaraivossa nakertaa tunne siitä, että tuskin ne lopulta ovatkaan niin hyödyllisiä, koska tästä on kurssillakin paljon puhuttu.

## Onko agentin tekemä koodi ymmärrettävää?
Käyttöliittymän toiminnallisuudet on kaikki kasattu tiedostoon web_app.py, joka vaikuttaakin alkuun melko samanlaiselta kuin mitä itsekin olemme nyt tehneet parilla kurssilla. Toisaalta, ehkä siinä piileekin suurin ongelma, että aloittelija tunnistaa agentin koodin samanlaiseksi kuin omansa. Esimerkiksi jotkin funktiot ovat hyvin pitkiä ja niissä on paljon sekalaista toiminnallisuutta, mitä yritimme juuri omassakin miniprojektissamme korjailla kurssin oppien mukaan.

Varsinkin html-sivut vaikuttivat hyvin selkeiltä ja samankaltaisilta kuin esim. Tikawessa opeteltiin. Toisaalta agentin kirjoittamasta JavaScriptistä en ymmärtänyt ensin juuri mitään, koska en myöskään osaa JavaScriptiä lainkaan. Selittäviä kommentteja on toki tekoälyn tyyliin paljon sielläkin ja selityksen sai lyhyellä promptilla.

## Miten agentti on muuttanut edellisessä tehtävässä tekemääsi koodia?
Agentti ei itse asiassa tehnyt juuri mitään muutoksia alkuperäiseen koodiin, joten se ehkä noudatti pyyntöäni turhankin tarkasti välittämättä koko ohjelman selkeydestä ja isosta rakenteesta. Se ei edes esimerkiksi muokannut index.py, vaan loi kokonaan uuden tiedoston web_app.py, jonka kautta web-sovelluksen saa käynnistettyä. Ratkaisu ei tunnu kovin ideaalilta ja olisi varmastikin ollut selkeämpää muokata index.pytä tai vastaavasti poistaa se kokonaan.

## Mitä uutta opit?
Että tekoälyn ja olemassaolevan koodin yhdistäminen voi olla melko hankalaa! Olin pyöritellyt ajatusta jo edellinen vibe-tehtävän jälkeen, että esimerkiksi juuri käyttöliittymän luomiseen vibeily voisi sopia. Tämä oli ensimmäinen kerta kun kokeilin agenttia ja vaikka siinä oli puolensa, en pitänyt hallitsemattomuuden tunteesta ja siitä, että joutuisin jälkikäteen käymään agentin tuottaman koodin läpi erityisen tiheällä kammalla ja mahdollisesti korjailemaan sitä. Toisaalta esimerkiksi agentin luoma styles.css oli mielenkiintoista luettavaa ja sai pohdiskelemaan, että olisiko kunnollinen tyylitiedosto paras rakentaa juuri tähän malliin, koska en ollut aiemmin ihan samanlaista pidempää ja kattavaa esimerkkiä nähnytkään.
