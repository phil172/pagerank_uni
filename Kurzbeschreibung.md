### PageRank by Philipp Michalik & Xander Hüther
## Karlsruher Institut für Technologie
## SS2021
## Einführung in Python

### Kurzbeschreibung

## Scraper.py

Der Scraper.py ist dafür da, die verlinkten internen Seiten auf der Seite www.math.kit.edu zu scrapen und herunterzuladen. Es werden die HTML Dateien im Ordner "/pages" gespeichert und ein Dictionary als JSON (links_to_pages.json)Datei abgelegt, welches die Verhältnisse der Seiten zueinander repräsentiert. Außerdem wird noch ein Dictioniary mit den IDs als Schlüssel und den URLs als Wert angelegt (id_dict) 

## ToGraph.py

ToGraph.py ist dazu da, einen Graphen als Dictionary mit den IDs anzulegen (id_graph.json).

## Rank.py 

Rank.py führt die mathematische Berechnung zur Bestimmung des PageRanks durch und speichert die Pageranks als Dictionary im JSON Format (pageranks.json).

## Search.py 

Die Suchfunktion umfasst das importieren des ID Dictionairy, des Pageranks und der HTML Dateien sowie die Zusammenführung bzw. in Verbindung bringen dieser Daten.

Nun kann man das Programm im Terminal starten und nach einem Suchbegriff suchen. Die Ergebnisse werden in der Reihenfolge des importierten Pageranks angezeigt. Anschließend kann man sich durch die Befehle durchdrücken und sich den Text mit dem gefundenen Suchbegriff anzeigen lassen.



