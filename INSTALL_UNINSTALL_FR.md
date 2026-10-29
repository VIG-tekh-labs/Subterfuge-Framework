# Installation et désinstallation — Subterfuge Framework

Ce guide couvre la version Python 3 (2.0.0a5), sur Linux Debian/Ubuntu/Kali. La version est encore **alpha**. Ne pas utiliser les anciens scripts Python 2 de l'archive.

## Installation locale depuis GitHub (sans modifier Python système)

Prérequis : Git, Python 3.11 ou plus récent, python3-venv et, pour l'interface native, une session graphique Linux et les bibliothèques Qt système.

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip \
    libegl1 libopengl0 libxkbcommon0 libxkbcommon-x11-0 libxcb-cursor0
git clone https://github.com/VIG-tekh-labs/Subterfuge-Framework.git
cd Subterfuge-Framework
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install ".[desktop,capture]"
.venv/bin/subterfuge --version
.venv/bin/subterfuge doctor
.venv/bin/subterfuge demo
.venv/bin/subterfuge desktop-shortcut
```

Démarrer la GUI depuis le menu « Subterfuge Framework » ou exécuter `.venv/bin/subterfuge gui` depuis le dépôt. Le raccourci utilise l'interpréteur de ce venv ; ne pas déplacer le dossier sans recréer le raccourci. En l'absence de session graphique, utiliser `.venv/bin/subterfuge serve --port 8080` puis ouvrir **http://127.0.0.1:8080/** sur la même machine. Le serveur reste sur loopback.

Pour la découverte réseau active, installer Nmap de façon facultative : `sudo apt install nmap`. Pour l'inspection TLS hors ligne, TShark est facultatif : `sudo apt install tshark`. Un laboratoire proxy explicite peut demander `mitmproxy`. Ces outils ne sont pas nécessaires au diagnostic ou aux analyses hors ligne.

## Désinstallation locale (installation venv)

Depuis le dossier cloné, **avant de retirer le venv** :

```bash
.venv/bin/subterfuge remove-desktop-shortcut
rm -rf -- .venv
```

La première commande ne supprime que le lanceur créé pour cet interpréteur et, si son contenu est inchangé, l'icône distribuée par l'application. Elle refuse un lanceur modifié par l'utilisateur. En cas d'erreur, inspecter manuellement `~/.local/share/applications/subterfuge-framework.desktop` avant de le retirer. Ne supprimer le dossier cloné (`cd .. && rm -rf -- Subterfuge-Framework`) **que si ses autres fichiers et modifications ne sont plus nécessaires**. Les fichiers de rapport/export créés ailleurs et les dépendances APT restent intacts.

## Installation DEB (amd64 uniquement)

Télécharger le `.deb` depuis la [release GitHub](https://github.com/VIG-tekh-labs/Subterfuge-Framework/releases), uniquement s'il est effectivement publié, puis :

```bash
sudo apt install ./Subterfuge-2.0.0a5-Linux-amd64.deb
subterfuge --version
subterfuge doctor
subterfuge gui
```

Pour désinstaller le paquet :

```bash
sudo apt remove subterfuge-framework
```

Éviter `apt autoremove` sans examiner sa liste de paquets. Si le lanceur du paquet est présent, ne pas utiliser la commande `remove-desktop-shortcut` : APT gère lui-même les fichiers du DEB.

## Windows 10/11

Les installateurs Windows sont décrits dans [DOWNLOADS.md](DOWNLOADS.md). Le désinstallateur se lance depuis **Paramètres > Applications > Applications installées > Subterfuge Framework > Désinstaller**. Les outils tiers installés via WinGet ne sont pas retirés automatiquement.

## Contrôles de santé

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/subterfuge doctor
.venv/bin/subterfuge demo
```

Les tests automatisés n'équivalent pas à une validation de tous les pilotes et adaptateurs réseau physiques. Ne réaliser des opérations réseau que sur des systèmes et réseaux dont l'audit est autorisé.
