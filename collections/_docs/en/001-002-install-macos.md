---
title: "Install Ink/Stitch on macOS"
permalink: /docs/install-macos/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2021-11-28
toc: true
---
{% comment %}
## Video Guide

We also provide beginner tutorial videos on our <i class="fab fa-youtube"></i> [YouTube channel](https://www.youtube.com/c/InkStitch).

Watch the installation process for <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3).
{% endcomment %}

## Requirements

Ink/Stitch is an Inkscape extension. Download and install [Inkscape](https://inkscape.org/release/) Version 1.0.2 or higher before you install Ink/Stitch.

## Download

Download the latest release for your macOS version.

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for macOS<br /><span style="color:lightblue;">Mojave / Catalina / Big Sur / Monterey</span></a></p>
<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-sierra-osx.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for macOS<br><span style="color:lightblue;">El Capitan / Sierra / High Sierra</span></a></p>

**Latest release:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }})](https://github.com/inkstitch/inkstitch/releases/latest)

## Installation

**Mojave - Monterey:** Click on the downloaded file to run the installer.

**El Capitan - High Sierra:** `Ctrl+Click` on the downloaded file and click on `Open`.

Click on `Continue`.

![Install Ink/Stitch](/assets/images/docs/en/macos-install/installer01.png)

Click on `Install`.

![Install Ink/Stitch](/assets/images/docs/en/macos-install/installer02.png)

A password prompt will open. Enter your user password and click on `Install Software`.

![Install Ink/Stitch](/assets/images/docs/en/macos-install/installer03.png)

In some cases your system will send a request, if you allow the installer to save files into your home directory. Ink/Stitch needs to be in the Inkscape extensions folder. Therefore answer this question with `Yes`.
{: .notice--info }

Your installation is now complete.

![Install Ink/Stitch](/assets/images/docs/en/macos-install/installer04.png)

Just one more question ...

Do you want to keep the downloaded installer file? This is up to you. Ink/Stitch doesn't need it anymore.

![Install Ink/Stitch](/assets/images/docs/en/macos-install/installer05.png)

## Run Ink/Stitch

Open Inkscape. You will find Ink/Stitch under `Extensions > Ink/Stitch`.

![Ink/Stitch menu](/assets/images/docs/en/macos-install/inkstitch-extensions-menu.png)

## Update Ink/Stitch

When a new Ink/Stitch version is released, download it and run the installer as described above. It will remove the old Ink/Stitch version by itself.

Installs older than 2.1.0 need to be removed manually. Go to the extensions folder and remove your inkstitch installation before running the installer script.

**Tip:** Subscribe to a news feed channel to keep track on Ink/Stitch Updates:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br />
{: .notice--info }

## Troubleshoot

### Ink/Stitch doesn't run / is greyed out

**Confirm installation path**

Check if you extracted Ink/Stitch into the correct folder. If the `User extensions folder` doesn't work out correctly, you can also try to install into the `Inkscape extensions folder`.
You can also look it up under `Inkscape > Preferences > System`.

**Confirm version**

Please verify if you have downloaded Ink/Stitch for your macOS version ([Download](#download)).

### 'xxxx' cannot be opened, because the developer cannot be verified

This can happen, if you run a development build release.

`Ctrl+Click` on the downloaded file and click on `Open`.

### Ink/Stitch is displayed in English

**Incomplete Translation**

It is possible, that not all text have been translated. This is indicated by **some parts of text beeing in English and others in your native language**.
If you like to complete the translation, have a look at our [description for translators](/developers/localize/).

**Language Settings**

If Ink/Stitch is uncertain, which language to support, it will fallback on English.
You can tell Inkscape explicitly to use your native language as follows:
  * Go to Inkscape > Preferences > Interface (Ctrl + Shift + P)
  * Set your language
  * Restart Inkscape

![Preferences > Interface](/assets/images/docs/en/preferences_language.png)

## Uninstall Ink/Stitch

Go to `Inkscape > Preferences > System` and open your extensions folder.

![Inkscape extensions folder](/assets/images/docs/en/extensions-folder-location-macos.jpg)

Remove each inkstitch* file and folder.