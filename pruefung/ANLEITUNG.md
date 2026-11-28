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
Christian möchte bei der Prüfung nichts bestätigen müssen. Gespeicherte Adressen direkt abzurufen löst jedes Mal eine Freigabe aus. Darum gilt: Jeden Anbieter zuerst über WebSearch suchen (Name plus Stichwort, zum Beispiel „nxtmove Camps 2027“ oder „EHC Waldkraiburg Eislaufschule“). Dann nur Seiten mit WebFetch öffnen, die die Suche geliefert hat, am besten die Seite, die der gespeicherten Adresse entspricht. Liefert die Suche keine passende Seite, den Anbieter als „nicht prüfbar (Suche)“ im Bericht nennen. Gespeicherte Adressen nicht direkt abrufen und keine anderen Umwege nutzen. Unbeantwortete Freigabe-Abfragen sofort stehen lassen und weitermachen. Im Bericht zählen: geprüft, nicht prüfbar, Freigaben ausgelöst.

## Ablauf
1. Christian per SendUserMessage kurz sagen, dass die Prüfung startet: Wochentag und was heute dran ist.
2. Repository holen und aktualisieren (`git pull`). Vergangene Einträge entfernen, also Einträge in `DATA` mit `bis` vor heute.
3. JEDEN TAG: alle Camps, Turniere und freien Trainings mit Termin in den nächsten 6 Wochen direkt auf der Anbieterseite prüfen: ausgebucht, abgesagt, verschoben, freie Plätze, neue Termine. Gibt es eine Übersichtsseite für viele Termine, diese nutzen statt jede Einzelseite.
4. JEDEN TAG fest: nxtmove (https://www.nxtmove.de/campsmore.html) auf Wunsch von Christian, egal wie weit die Termine entfernt sind.
5. NUR MONTAG und DONNERSTAG zusätzlich: alle Camp- und Turnier-Anbieter mit Terminen später als 6 Wochen sowie die Anbieter ohne Termin (OhneTermin > 0).
6. JEDEN TAG die Laufschulen des heutigen Wochentags aus `laufschulen_woche.json`. Änderungen in `LAUFEND` per URL bearbeiten.
7. AM 1. JEDES MONATS zusätzlich: `nicht_lesbar.json` erneut versuchen.
8. Bei Änderungen Notizen mit „Stand TT.MM.JJJJ“ versehen. Freie Plätze wie bisher schreiben, zum Beispiel „5 frei (7/12) – Stand 28.11.2026“.
9. In `pruefung/anbieter.json` den Status geprüfter Anbieter auf „geprüft TT.MM.“ setzen. Wenn das Sheet-Werkzeug verfügbar ist, auch im Sheet https://claude.ai/artifact/Fa78fFbdSGTtuignm93wo1 Spalte C setzen. Container: `{"kind":"project","id":"75ff43c1-2dc6-40b0-973b-afebc134f414"}`, node `cd8db97c-e817`, engine `workbook`. Spalte C ist ein Dropdown: Fehlt die Option „geprüft TT.MM.“, zuerst `setDropdownOptions` (mit `sheet`, alle bisherigen Optionen behalten, neue mit `optionId: null`, Farbe grün 200) im selben `applyEdits` ausführen. Höchstens 64 Änderungen pro Aufruf.
10. Wenn sich `daten.js` geändert hat: `STAND` auf heute setzen, `sh pruefung/version.sh` ausführen, node-Check und Test laufen lassen. Dann commit mit diesen Zeilen am Ende der Nachricht:
    ```
    Co-Authored-By: Claude <noreply@anthropic.com>
    ```
    Danach `git pull --rebase`, `git push`, mit `git ls-remote origin main` prüfen. `pruefung/anbieter.json` immer mit committen.
11. Kurzer Bericht an Christian per SendUserMessage, auf Deutsch: was geändert wurde, was nicht prüfbar war. Wenn nichts geändert wurde, reicht ein Satz.
