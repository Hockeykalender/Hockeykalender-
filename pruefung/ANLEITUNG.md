# Tägliche Prüfung Hockeykalender

Diese Anleitung wird von der geplanten Aufgabe „Hockeykalender: tägliche Prüfung“ jeden Tag um 09:15 (Europe/Berlin) gelesen und Schritt für Schritt ausgeführt. Wenn sich die Vorgaben ändern, wird nur diese Datei angepasst.

## Regeln (immer gültig)
- Berichte an Christian auf Deutsch, kurz und einfach, ohne Fachwörter.
- Suche KEINE neuen Anbieter. Neue Termine von bekannten Anbietern dürfen eingetragen werden.
- Ändere niemals die `id` eines Eintrags.
- Nichts löschen außer vergangenen Einträgen, kein force-push.
- Impressum/Datenschutz (`<details id="impressum">` in index.html) nie ändern.
- Keine fremden Skripte, Schriften oder Bilder einbauen. Einzige Ausnahme ist das vorhandene Umami-Skript.
- Kein `window.claude`, keine Datenbank, keine Nutzerkennung, kein GoatCounter.
- superturnaje.cz bleibt ausgeschlossen.
- Mitock-Einträge `deN010402` und `deN020801` stammen von einem Flyer. Nicht ändern, nur entfernen, wenn sie vorbei sind.
- Länder: nur DE, AT, CH, CZ.
- Eine Seite nicht lesbar? Nicht umgehen, sondern im Bericht nennen.

## Dateien
- `daten.js`: `DATA` (Termine mit `id`), `LAUFEND` (laufende Kurse, ohne id, per `url` finden), `OHNE` (ohne Termin, per `url` finden), `const STAND="JJJJ-MM-TT";`.
- `pruefung/anbieter.json`: Liste `[Name, Land, Domain, Termine, Laufend, OhneTermin, Status, URL]`. Index i entspricht Sheet-Zeile i+2.
- `pruefung/laufschulen_woche.json`: Schlüssel Mo, Di, Mi, Do, Fr, Sa, So mit je ca. 56 Einträgen `[Sheet-Zeile, Name, URL]`.
- `pruefung/nicht_lesbar.json`: Seiten, die bisher nicht lesbar waren.
- Helfer: `python3 pruefung/set.py <id> <feld> <wert>`, `python3 pruefung/add.py '<json>'`, `sh pruefung/version.sh`.
- Test: `python3 pruefung/test.py <repo-pfad>`. Nur Umami-Ladefehler (ERR_TUNNEL_CONNECTION_FAILED) sind ok. Vorher alte `http.server` beenden (`pkill -f http.server`).

## Seiten finden über die Websuche
Christian möchte bei den automatischen Läufen nichts bestätigen müssen. Gespeicherte Adressen direkt abzurufen löst jedes Mal eine Freigabe aus. Darum gilt:
- Für jeden Anbieter steht in `pruefung/suche.json` (Schlüssel = Sheet-Zeile) ein fester Suchbegriff, z. B. `site:nxtmove.de campsmore`. Damit zuerst WebSearch ausführen. Trifft er nicht, einmal mit `site:<domain>` plus Anbietername oder Stichwort (Camp/kemp, Laufschule/bruslení) nachsuchen. Ein Suchbegriff, der besser trifft, wird in `suche.json` gespeichert.
- Dann nur Seiten mit WebFetch öffnen, die die Suche geliefert hat, am besten die Seite, die der gespeicherten Adresse entspricht.
- Gespeicherte Adressen nicht direkt abrufen und keine anderen Umwege nutzen. Taucht doch eine Freigabe-Abfrage auf, sie stehen lassen und weitermachen.
- Findet die Suche einen Anbieter nicht oder lässt die Seite den Abruf nicht zu: `[Sheet-Zeile, Name, URL]` in `pruefung/nur_mit_christian.json` eintragen, falls noch nicht drin. Diese Anbieter werden montags um 10 Uhr gemeinsam mit Christian geprüft.
- Ist ein Anbieter aus `nur_mit_christian.json` per Suche wieder gut auffindbar, ihn dort entfernen.
- Im Bericht zählen: geprüft, nicht prüfbar, Freigaben ausgelöst.

## Zwei Läufe pro Tag
Die Nachricht der geplanten Aufgabe sagt, welcher Lauf dran ist.
- **Lauf A (09:15):** Schritt 3 und 4.
- **Lauf B (15:15):** Schritt 5, 6 und 7.
Beide Läufe machen Schritt 1, 2 und 8 bis 11. Was der andere Lauf heute schon geprüft hat (Status „geprüft TT.MM.“ von heute in `anbieter.json`), nicht nochmal prüfen.

## Ablauf
1. Christian per SendUserMessage kurz sagen, dass die Prüfung startet: Lauf A oder B, Wochentag und was heute dran ist.
2. Repository holen und aktualisieren (`git pull`). Vergangene Einträge entfernen, also Einträge in `DATA` mit `bis` vor heute.
3. Alle Camps, Turniere und freien Trainings mit Termin in den nächsten 6 Wochen auf der Anbieterseite prüfen: ausgebucht, abgesagt, verschoben, freie Plätze, neue Termine. Gibt es eine Übersichtsseite für viele Termine, diese nutzen statt jede Einzelseite.
4. Fest jeden Tag: nxtmove (Sheet-Zeile 606), auf Wunsch von Christian, egal wie weit die Termine entfernt sind.
4b. Fest jeden Tag: TCC sportovní služby (Sheet-Zeile 411), auf Wunsch von Christian (28.11.2026). Die Websuche findet TCC nicht. Darum gilt NUR für TCC eine Ausnahme von „Seiten finden über die Websuche“: Diese vier Übersichtsseiten direkt mit WebFetch öffnen.
   - https://www.tcc-sportovnisluzby.cz/de/rezervace/kempy/ (Wochenend-Skills-Camps)
   - https://www.tcc-sportovnisluzby.cz/de/rezervace/eishockeycamp-wochentlich/ (Mehrtagescamps)
   - https://www.tcc-sportovnisluzby.cz/de/rezervace/trainings/ (Einzeltrainings)
   - https://www.tcc-sportovnisluzby.cz/de/rezervace/torwart-wochenende-skills-eishockey-camp/ (Torwart-Camps)
   Dabei kann eine Freigabe-Abfrage kommen. Christian bestätigt sie selbst mit „Immer erlauben“. Wird eine Seite nicht freigegeben oder kommt eine Sperre (z. B. PROVENANCE_REQUIRED), diese Seite überspringen, keinen anderen Weg versuchen und es im Bericht nennen. Neue Termine eintragen (Einzeltrainings als typ "Training", Camps als typ "Camp", Land CZ, Ort Plzeň, Halle Studentská 2143/117, Plzeň-Bolevec), geänderte Termine anpassen. Einzelne Termin-Seiten nur öffnen, wenn die Übersicht etwas Wichtiges nicht zeigt.
5. Laufschulen des heutigen Wochentags aus `laufschulen_woche.json`. Änderungen in `LAUFEND` per URL bearbeiten.
6. NUR MONTAG und DONNERSTAG: alle Camp- und Turnier-Anbieter mit Terminen später als 6 Wochen sowie die Anbieter ohne Termin (OhneTermin > 0).
7. AM 1. JEDES MONATS: `nicht_lesbar.json` erneut versuchen.
8. Bei Änderungen Notizen mit „Stand TT.MM.JJJJ“ versehen. Freie Plätze wie bisher schreiben, zum Beispiel „5 frei (7/12) – Stand 28.11.2026“.
9. Status setzen, an ZWEI Stellen:
   a) In `pruefung/anbieter.json` Spalte Status (Index 6) der geprüften Anbieter auf „geprüft TT.MM.“.
   b) Im Sheet https://claude.ai/artifact/Fa78fFbdSGTtuignm93wo1 Spalte C derselben Zeilen (Sheet-Zeile = Index + 2). Werkzeug `mcp__Claude_Docs__update` (Schema per ToolSearch laden), `ref {"object":"node","id":"cd8db97c-e817"}`, `container {"kind":"project","id":"75ff43c1-2dc6-40b0-973b-afebc134f414"}`, `engine "workbook"`. Vorher mit `mcp__Claude_Docs__read` und `payload {"kind":"readCells","sheet":"Anbieter","range":"C2:C2"}` die Revision und die Dropdown-Optionen lesen. Schreiben mit `payload {"kind":"applyEdits","base":<Revision>,"edits":[…]}`. Spalte C ist ein Dropdown mit der id aus dem readCells-Ergebnis: Fehlt die Option „geprüft TT.MM.“, als erstes Edit `{"kind":"setDropdownOptions","sheet":"Anbieter","dropdownId":"<id>","options":[alle bisherigen Optionen unverändert, {"optionId":null,"label":"geprüft TT.MM.","color":{"kind":"standard","hue":"green","shade":200}}]}`. Danach je Zeile `{"kind":"writeCells","sheet":"Anbieter","topLeft":"C<Zeile>","rows":[["geprüft TT.MM."]]}`. Höchstens 64 Edits pro Aufruf. Klappt das Sheet nicht, im Bericht sagen.
10. Immer zuerst `python3 pruefung/geprueft.py` ausführen: Das schreibt die Prüfdaten aus `anbieter.json` als `GEPRUEFT` in daten.js (Anzeige „Vom Hockeykalender geprüft“ an jedem Termin). Wenn sich `daten.js` oder Dateien in `pruefung/` geändert haben: bei daten.js `STAND` auf heute setzen und `sh pruefung/version.sh` ausführen, node-Check und Test laufen lassen. Commit-Nachricht endet mit:
    ```
    Co-Authored-By: Claude <noreply@anthropic.com>
    ```
    Danach `git pull --rebase`, `git push`, mit `git ls-remote origin main` prüfen.
11. Kurzer Bericht an Christian per SendUserMessage, auf Deutsch: was geändert wurde, wie viele geprüft, nicht prüfbar, Freigaben. Wenn nichts geändert wurde, reicht ein Satz.
