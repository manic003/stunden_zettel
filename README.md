
# Stundenzettel Generator für die easy Stundenerfassung
 Ein kleines Programm das die Termine aus dem GoogleCal importiert und daraus eine Abrechnung erstellt.
 Das Programm öffnet ein libreoffice calc sheet und füllt es je nach Wahl im Terminal aus.
 
 Speichern des Blattes und benennen muss selbst passieren, ggf Anpassungen an dem Sheet sind so möglich.

## Anpassungen:

- der genutzte Google Calendar ist in `./credentials/google_mail_accounts.meine_config` definiert
- im Code in `main.py` werden die Termine nach einem Suchbegriff gefiltert, in der Version hier ist das  **"Nachhilfe"** 

## How to Use..
- ausführen mit `python3 main.py` 
- bestätige öffnen von libre office mit Enter
- bestätige dass es geöffnet wurde (ist etwas unsauber programmiert.. python muss warten bis libreoffice wirklich offen ist bevor es weitergeht..)
- weiter mit Enter, Fragen ggf `n` oder `no` beantworten (yes) ist immer default
 

## TODO

- siehe Beispiel `cmdline_usageTODO.py`:
    - ´main.py´ entsprechend anpassen das man es über die cmdline ausführen kann
    - mit option `--fast` `--query="Nachhilfe"` etc.
    - ... siehe args.py..
    - danach kroenung mit autocomplete.. -> https://stackoverflow.com/questions/14597466/custom-tab-completion-in-python-argparse 


- besser als das oben argparse..
- siehe https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
## Falls je weiter entwickeln:
- Gute Dokumentation zur LibreOffice Uno-Api
- https://www.openoffice.org/de/doc/entwicklung/python_bruecke.html#intro
- noch viel mehr möglich..
    - u.a einbinden in die GUI von Libre Office
    - speichern als etc..
    - exportieren als..
    - uvm 

## benutzte Quellen 
- https://medium.com/analytics-vidhya/macro-programming-in-openoffice-libreoffice-with-using-python-en-a37465e9bfa5

- https://github.com/rebahozkoc/libreofficepythonmacros


## Arbeitsaufwand
- 6 h arbeitszeit inkl. recherche,schreiben, testen etc  
- 2 h für fein schliff und optische verschönerungen
