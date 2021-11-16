---
title: "Install Ink/Stitch"
permalink: /fr/docs/install-macos/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2021-05-03
toc: true
---
## Guide vidéo

Nous fournissons aussi aux débutants des tutoriels vidéo sur notre <i class="fab fa-youtube"></i> [chaine YouTube](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Les vidéos sont en anglais. Mais il y a des sous-titres en français.

* <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3)

**Attention:** La vidéo pour les utilisteurs de Mac est obsolète. Lisez la mise à jour des infos ["Etapes additionnelles pour Catalina / Big Sur"](#addtitional-steps-for-catalina--big-sur)
{: .notice--warning }

## Prérequis

* [Inkscape](https://inkscape.org/releases) Version 1.0.2

C'est tout! Toutes les librairies python et dépendances externes sont incluses (en utilisant l'excellent [pyinstaller](http://www.pyinstaller.org)), de sorte que vous ne devriez pas avoir quoi que ce soit d'autre à installer.

## Installation rapide

### Télécharger
Télécharger, en tenant compte de votre plateforme.

Langue| Catalina & Big Sur | High Sierra & Mojave | Sierra & El Capitan
---|---|---|---
**Allemand** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-de_DE.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-de_DE.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-de_DE.zip)|
**Anglais** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-en_US.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-en_US.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-en_US.zip)|
**Finnois** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fi_FI.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-fi_FI.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-fi_FI.zip)|
**Français** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-fr_FR.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-fr_FR.zip)|
**Italien** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-it_IT.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-it_IT.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-it_IT.zip)|
**Japonais** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-ja_JP.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-ja_JP.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-ja_JP.zip)
**Néerlandais** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-nl_NL.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-nl_NL.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-nl_NL.zip)|
**Russe** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-ru_RU.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-ru_RU.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-ru_RU.zip)
{: .inline-table }
 
**Dernière version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

Le `LOCALE` sélectionné affecte les menus à l'intérieur d'Inkscape. Les dialogues d'Ink/Stitch sont dans la langue de votre OS (si cette langue est supportée).<br><br>Ink/Stitch n’existe pas dans votre langue? Aidez-nous à [traduire les dialogues dans votre langue maternelle](/fr/developers/localize/).
{: .notice--info }

### Installation
Dans Inkscape, allez à  `Edition > Préferences > Systeme` et cherchez dans ce tableau où se trouve votre dossier `Extensions utilisateur`.

![Extensions Utilisateur](/assets/images/docs/fr/extensions-folder-location-macos.jpg)

Décompressez l'archive Ink/Stitch dans ce dossier.

Ce dossier doit présenter une structure semblable à l'exemple ci-dessous (avec juste un tas de fichiers en plus):
![File Structure](/assets/images/docs/en/file_structure.png)

Redémarrez Inkscape.

Vous trouverez alors Ink/Stitch sous `Extensions > Ink/Stitch`.

### Etapes additionnelles pour Catalina / Big Sur

Les nouvelles versions de macOS n’accepteront pas Ink / Stitch s'il est téléchargé via votre navigateur. Vous recevrez un message d'erreur comme celui-ci: `impossible d'ouvrir'Inkstitch' car le développeur ne peut pas être vérifié`.

Pour éviter ce message d'erreur, ouvrez votre application Terminal. Cliquez sur la petite icône en forme de loupe dans votre barre de menu dans le coin supérieur droit (ou appuyez <key>Commande (⌘)</key>+<key>Espace</key>). Cherchez `Terminal` et ouvrez l'application.

Dans le terminal, entrez la commande suivante:

```
xattr -r -d com.apple.quarantine ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
```

Remplacer `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/` si le chemin de votre dossier d'extension Inkscape a un autre emplacement (vérifiez dans `Inkscape > Preferences > System>Extension Utilisateur`).

### Exécuter Ink/Stitch

Relancer Inkscape.

Vous trouverez alors Ink/Stitch dans `Extensions > Ink/Stitch`.

## Problème d'Installation Ink/Stitch

### J'ai téléchargé et décompressé la [dernière version](https://github.com/inkstitch/inkstitch/releases/latest). Où je la mets?

Dans Inkscape ouvrir: `Edition > Preferences > System` et vérifier les chemins pour les extensions.

![image](https://user-images.githubusercontent.com/11083514/37572872-899a7de0-2b09-11e8-93ed-e4be6228c414.png)

Vous devriez de préférence installer dans **USER EXTENSIONS**, car cela facilitera la mise à jour ultérieure.

Si vous avez des signes diacritiques dans votre nom d'utilisateur, essayez le chemin d'accès de **INKSCAPE EXTENSIONS** si vous rencontrez des difficultés pour exécuter Ink/Stitch.

### Ink/Stitch ne fonctionne pas!

**Confirmer le chemin d'installation**<br>

Check if you extracted Ink/Stitch into the correct folder. If the `User extensions folder` doesn't work out correctly, you can also try to install into the `Inkscape extensions folder`.
You can also look it up under `Edit > Preferences > System`.

**Confirm version**

Please verify if you have downloaded Ink/Stitch for macOS ([Download](#download)).

### 'xxxx' cannot be opened, because the developer cannot be verified

Read ["Additional Steps for Catalina and Big Sur"](#addtitional-steps-for-catalina--big-sur).

### ValueError: Null geometry supports no operations

Ink/Stitch on macOS could raise the following error message:  `[...] ValueError: Null geometry supports no operations`.

This error is caused by an incompatibality of the shapely speedups library, which is inlcuded in the Ink/Stitch files.
In order to bring Ink/Stitch back to work delete the library as follows:

* Open the folder of your Ink/Stitch installation (usually this is: `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/`)
* Open as well your Ink/Stitch subfolder if you have one
* Press `Ctrl` while you click on the inkstitch application file and select Show `Package Contents` 

  ![Show Package Contents](/assets/images/docs/en/macOS-nogeometry.png)

* Go into the Folder `Contents > MacOS` and delete the folder named `shapely`

### J'ai installé Ink/Stitch mais le menu est grisé (désactivé)

C'est souvent le cas si la mauvaise version Ink / Stitch a été installée.
Veuillez vérifier si vous avez téléchargé la bonne version Ink / Stitch pour votre système d'exploitation.

### J'ai installé Ink / Stitch dans ma langue maternelle, mais les fenêtres de dialogue sont affichées en anglais!

Premièrement, il est possible que toutes les chaînes n'aient pas été traduites. Ceci est indiqué par **certaines chaînes de texte en anglais et d'autres dans votre langue maternelle**.

Si vous souhaitez terminer la traduction, consultez notre [description pour les traducteurs](/developers/localize/).

Ensuite, nous devons faire la distinction entre le menu Extension dans Inkscape et les fenêtres de dialogue.
La sélection du fichier ZIP a pour seule conséquuence la traduction du menu Extension dans une certaine langue.
Les fenêtres de dialogue sont construites différemment. Elles utiliseront la langue de votre système d'exploitation.
Si Ink/Stitch n'est pas sûr de la langue à prendre en charge, il retombera sur l'anglais.
Vous pouvez indiquer explicitement à Inkscape d'utiliser votre langue maternelle comme suit:
  * Aller à Edition > Preferences > Interface (Ctrl + Shift + P)
  * choisissez votre langue
  * Redémarrer Inkscape

![Preferences > Interface](/assets/images/docs/fr/preferences_language.png)


## Mise à jour

 * Il faut d'abord effacer tous les fichiers de l'ancienne extension:<br />
   Ouvrez le répertoire des extensions et supprimez chaque dossier ou fichier inkstitch*.
 * Puis procédez comme ci-dessus.

**Astuce:** Inscrivez-vous aux news pour avoir connaissance des mises à jour d'Ink/Stitch:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br />
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Or watch the project on GitHub:<br /><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>