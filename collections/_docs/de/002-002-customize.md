---
title: "Anpassung von Ink/Stitch"
permalink: /de/docs/customize/
excerpt: ""
last_modified_at: 2021-10-23
toc: true
---

## Tastenkürzel

Deine Arbeit mit Ink/Stitch kann sich erheblich beschleunigen, wenn du Tastenkürzel benutzt.

Die folgende Liste zeigt Tastenkürzel, die über die unten zur Verfügung gestellte Datei schnell eingerichtet werden könne.

Einige dieser Tastenkürzel werden andere Tastenkürzel, die bereits durch Inkscape verwendet werden, ersetzen. In der Tabelle kannst du sehen, welche das sind und wie diese Funktionen weiterhin erreichbar sind.
{: .notice--warning }

Tastenkürzel | Effekt | Ersetzt
-------- | --------
<key>Bild↑</key>                        | Anheben* | Objekt > Anheben (see also toolbar buttons)
<key>Bild↑</key>                        | Absenken* | Objekt > Absenken (see also toolbar buttons)
<key>Strg</key><key>R</key>             | Pfad > Richtung umkehren**
<key>Strg</key><key>⇧</key><key>P</key> | Parameter | Bearbeiten > Einstellungen
<key>Strg</key><key>⇧</key><key>L</key> | Simulator (Live Simulation)
<key>Strg</key><key>⇧</key><key>/</key> | Stichplan Vorschau (neben der Leinwand) | Pfad > Division (nutze stattdessen Strg+/)
<key>Strg</key><key>⇧</key><key>O</key> | Aufteilen von Füllobjekten... (O für Object) | Objekt > Objekteigenschaften
<key>Strg</key><key>⇧</key><key>I</key> | PDF-Export
<key>Strg</key><key>⇧</key><key>Q</key> | Text (Q für QWERTY) | Objekt > Selectoren und CSS
<key>Strg</key><key>⇧</key><key>Entf</key> | Fehlerbehebung an Objekten (Fehler entfernen)
<key>Strg</key><key>⇧</key><key>+</key> | Befehle mit gewählten Objekten verknüpfen
<key>Strg</key><key>⇧</key><key>U</key> | Konvertierung Linie zu Satinstich (U sieht wie zwei Schienen aus) | Objekt > Gruppieren (benutze stattdessen Strg+G)
<key>Strg</key><key>⇧</key><key>J</key> | Konturen der Satinkolumne umkehren (J sieht wie ein Pfeil aus)
<key>Strg</key><key>⇧</key><key>B</key> | Satinkolumne schneiden (B ist in der Hälfte geschnitten) | Pfad > Vereinigen (nutze stattdessen Strg++)
<key>Strg</key><key>⇧</key><key>*</key> | Automatisch geführte Satinkolumne (\* bringt Ordnung)

The Ink/Stitch [simulator](/docs/visualize/#simulation-shortcut-keys) also provides shortcut keys.

\* Anheben und Absenken gibt genaue Kontrolle darüber, in welcher Reihenfolge Objekte gestickt werden (von unten nach oben). Das ist sehr nützlich in Verbindung mit dem Objekt-Dialog (`Objekt > Objekte ...`).<br><br>** Für Satin- und Laufstiche ändert dies die Stickrichtung. Nutze dies mit der Einstellung `Zeige Pfadrichtung an Außenlinien` unter `Bearbeiten > Einstellungen > Werkzeuge > Knoten`. Wenn du nur einen Knoten mit dem Knotenwerkzeug auswählst und `Strg+R` drückst, kehrt sich nur der ausgewählte Unterpfad um. Auf diesem Wege kannst du sicherstellen, dass beide Schienen der Satinkolumne in die gleiche Richtung zeigen.
{: .notice--info }
{: style="font-size: 70%" }

#### Download and import custom shortcut keys

* [Download the Ink/Stitch shortcut key file](/assets/files/inkstitch.xml)
* Gehe zu `Bearbeiten > Einstellungen > Benutzeroberfläche > Tastenkürzel`
* Klicke auf `Importieren...`
* Wähle die Tastenkürzel-Datei (inkstitch.xml)
* Klicke auf öffnen

Jetzt kannst du die oben genannten Tastenkürzel verwenden.

Wenn du deine eigenen Tastenkürzel verwenden willst, füge sie in den Tastenkürzel-Dialog ein.
Benutze die Suchfunktion um die Erweiterungen schneller zu finden. [Mehr informationen](http://wiki.inkscape.org/wiki/index.php/Customizing_Inkscape)
{: .notice--info }

## Zoom correction factor

For embroidery it is essential to get a sense of the actual size of the design. Inkscape has a setting to adapt zoom levels to your display size.

* Go to `Edit > Preferences > Interface`
* Hold a ruler onto your display and adjust the slider until the length matches
 
![Zoom correction](/assets/images/docs/de/customize-zoom-correction.png)

## Gitter

Um Vektoren richtig auszurichten, kann die Rasterfunktion von Inkscape verwendet werden. Gehe zu `Ansicht` und aktiviere das `Seitengitter`. Stelle in der `Einrasten-Kontrollleiste` sicher, dass `Am Gitter einrasten` aktiviert ist. Es ist auch möglich, den Abstand und den Ursprung der Gitter unter `Datei > Dokumenteinstellungen > Gitter` anzupassen.

![Gitter](https://user-images.githubusercontent.com/11083514/40359052-414d3554-5db9-11e8-8b49-3be75c5e9732.png)

## Pfadkonturen & Pfadrichtungen

Bei der Arbeit mit Ink/Stitch ist es wichtig, erkennen zu können, in welche Richtung ein Pfad verläuft. Wir empfehlen daher, die Kontrollkästchen `Umriss zeigen` und `Zeige temporär Umrandung für ausgewählte Pfade` unter `Bearbeiten > Einstellungen > Werkzeuge > Knoten` zu aktivieren.

Damit die Pfadrichtungen auch wirklich angezeigt werden, aktiviere außerdem die Option `Zeige Entwurfspfad` in der Werkzeugleiste. In der Abbildung kannst du sehen, wo du die Option findest.

[![Path outlines & directions](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)

## Vorlagen

Wenn man Ink/Stitch häufiger verwendet, möchte man nicht die gleichen Arbeitsschritte immer und immer wieder wiederholen. In diesem Fall kann eine Vorlage für die grundlegende Stickkonfiguration erstellt werden. Nachdem alles nach Wunsch eingerichtet wurde, speichere die Datei einfach in dem Vorlagenverzeichnis. Nun kann mit `Datei > Neu aus Vorlage` darauf zugegriffen werden.

Betriebssystem | Vorlagenverzeichnis
---|---
Linux   | `~/.config/inkscape/templates`
Windows | `C:\Users\%USERNAME%\AppData\Roaming\inkscape\templates`

Das Benutzerverzeichnis für Erweiterungen kann in den Inkscape Einstellungen überprüft werden. [Mehr dazu](/de/docs/faq/#ich-habe-die-aktuelle-version-heruntergeladen-und-entpackt-was-soll-ich-jetzt-machen).

**Tip:** Hier gibt es [Vorlagen](/de/tutorials/resources/templates/) die du nutzen kannst.
{: .notice--info }

## Farbpaletten für Insckape installieren

Ink/Stitch enthält viele Farbpaletten der üblichen Garnhersteller. Diese können installiert werden, damit sie in Inkscape nutzbar sind.
Das erlaubt dir dein Design mit den richtigen Farben zu planen. Die Farben werden in die PDF-Ausgabe übernommen und auch in der Stickdatei abgespeichert, sofern dein Stickformat dies unterstützt.

[Mehr Informationen](/de/docs/thread-color/#farbpaletten-für-insckape-installieren)