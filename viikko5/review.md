## Copilotin tekemä pull requestin katselmointi (tennis_refactoring > main)

### Mitä huomioita Copilot teki koodistasi
Huomioita oli melko paljon ja liittyivät esimerkiksi tällaisiin asioihin:
1. `Score.ADVANTAGE` enumia ei käytetä semanttisesti oikein, vaan ainoastaan ylitettävänä arvona ehtolauseessa. Copilot ehdotti poistamista tai erillistä vakiota, tai enumin nimeämisti paremmin, esim. `ADVANTAGE_THRESHOLD`.
2. Muuttujat `self.player1` ja `self.player2` ovat liian epäselvästi nimettyjä, joten niissä olisi parempi käyttää esim. `self.player1_name`.
3. Muuttuja `temp_score` määritelty liian aikaisin, olisi parempi määritellä loopin sisällä.
4. Metodi `call_score()` on epäselvä, koska se käyttää looppia ja iteroi pelaajien välillä numeroiden avulla. 

### Olivatko ehdotetut muutokset hyviä
Yleisesti ottaen kyllä, ainakin omaan silmääni. Erityisesti muutama muutosehdotus oli toimiva ja tarpeeksi pieni, joten ne oli helppo lisätä PR:ään heti mukaan batch committina.
* Muuttuja `minus_result` oli harhaanjohtavasti nimetty, Copilot nimesi sen toimivasti uudelleen.
* Copilot myös korjasi pitkän ehtolauseen paremmalla tyylillä kahdelle riville.

Muutkin ehdotuksista olivat ainakin osittain hyviä, mutta tuntuivat liian isoilta otettavaksi ”varomamattomasti” ja hallitsemattomasti mukaan Copilotin tekeminä. Esim. kommentti metodista `call_score()` oli todella hyvä, mutta tekisin korjauksen mieluummin itse ja tavalla, jonka varmasti ymmärrän ja voin testata.

### Kuinka hyödylliseksi koit Copilotin tekemän katselmoinnin
Copilotin katselmointi on tähän mennessä tuntunut melko hyödylliseltä. Olemme jonkin verran käyttäneet sitä myös miniprojektissa ja usein sieltä löytyy esimerkiksi tyyliin liittyviä tarpeeksi pieniä korjausehdotuksia kuten tässäkin tapauksessa, jotka on kätevää lisätä PR:ään mukaan saman tien.

Jotkut ehdotetut muutokset ovat kuitenkin sellaisia, että niiden tietää hajottavan ohjelman toiminta muualla jos muutoksia ei viedä moneen eri paikkaan. Copilot tuntuu huomioivan vain yhden kontekstin ja juuri kyseisessä PR:ssä muuttuneet tiedostot, joten näiden muutosten ottaminen mukaan suoraan olisi hankalaa. Jos ehdotukset kuitenkin ovat hyviä, otan ne mieluummin itselleni erikseen ylös ja tutkin asiaa koko ohjelman koodia katsoen. Esim. tässä tapauksessa tein itse muutamat hyvät muutosehdotukset muuttujien nimiin. Lisäksi ottamalla mukaan sokkona paljon muutoksia Copilotilta voisi nopeasti menettää ymmärryksen ja kokonaiskuvan ohjelmasta, ainakin näin vielä hyvin aloittelevana koodarina.
