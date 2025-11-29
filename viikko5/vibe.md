## Copilot luo ohtuvarastolle käyttöliittymän
Sovellus uudella vibe-UI:lla löytyy täältä: [ohtuvarasto](https://github.com/karorot/ohtuvarasto)

### Päätyikö Copilot toimivaan ja hyvään ratkaisuun
Päätyihän se, ainakin toimivaan! Copilotin luoma sovellus vastasi hyvin tarkasti juuri niitä toiminnallisuuksia, jotka olin kirjoittanut ohjenuoraksi issueen. Sovellus myös toimi pienen manuaalisen testailun perusteella hyvin ja unittestit näyttivät vihreää kuten olin myös pyynnössä painottanut. Kun katsoo pellin alle, löytyi sovelluksen rakenteesta kuitenkin ehdottomasti myös paranneltavaa. Positiivisin yllätys itselleni oli sovelluksen ulkoasu, johon liittyen annoin vain muutamia avainsanoja (tailwind css, selkeys) mutta josta tuli kuitenkin valmiissa sovelluksessa varsin mallikas.

### Oliko koodi selkeää
Hyvät puolet
* Pienet toiminnallisuudet oli jaettu omiin metodeihinsa ja funktioihinsa, jotka vastasivat selkeästi omasta tontistaan.
* Yleisellä tasolla koodi oli melko selkeää ja erityisesti html-sivut oli rakennettu helposti ymmärrettävällä tavalla ja samalla tyylillä, kuin mitä olen itse oppinut.

Ja sitten ne ongelmat
* Lähes kaikki toiminnallisuus vaikutti olevan alunperin tiedostossa `app.py` sen sijaan, että se toimisi eräänlaisena ”pääohjelmana” kuten tikawen ja tämän kurssin esimerkeissä. Lisäksi eri sivupyynnöt oli laitettu erillisten funktioiden sisään, jolloin `app.py` olikin kasvanut melko valtavaksi ja siellä oli paljon erilaista ja erityyppistä toiminnallisuutta. Ohjelman kulkua, eri reittejä ja riippuvuuksia oli tämän takia myös paljon hankalampi hahmottaa.
* Uuen luokan `WarehouseManager` olisi voinut heti eriyttää omaan tiedostoonsa selkeyden parantamiseksi. Pyysin tähän korjausta katselmoinnissani ja Copilot korjasikin sitten tilanteen nohevasti.
* Lisätyt varastot tallennettiin sanakirjaan `WarehouseManager`-luokkaan. Ratkaisu toimi tässä esimerkissä kyllä, enkä myöskään erikseen pyynnössä spesifioinut että käyttöön tulisi ottaa vaikkapa tietokanta, mutta pidemmän päälle täytyisi ohjelmaa laajentaa paremmalla tavalla varastoida dataa.

### Opitko jotain uutta Copilotin tekemää koodia lukiessasi
* Tailwind ei ole minulle ennestään tuttu, joten oli mielenkiintoista pytää Copilotia käyttämään sitä, nähdä tulos ja tutustua sitten siihen kuinka html-sivut oli tyylitelty. Toki nyt täytyy tarkistaa itse muista lähteistä, kuinka hyvin Copilot oikeastaan suoriutui hommasta. :)
* Pyysin Copilotia myös kirjoittamaan uusille toiminnallisuuksille tarpeen mukaan uusia unittestejä ihan jo siksikin, että kurssin aikana on ollut paljon puhetta tekiälyn tekemistä testeistä. Testeissä oli ehdottomasti myös hyviä testitapauksia ja perustoiminnallisuudet oli katettu, mutta niitä oli myös melkoisen paljon. Copilot oli lisäksi mielenkiintoisesti käyttänyt sivukutsujen vastauskoodeja testien tarkistuksissa, en tiedä onko tämä hyvä vai huono tyyli?
