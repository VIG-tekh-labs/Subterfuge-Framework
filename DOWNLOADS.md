# Télécharger et installer Subterfuge Framework 2.0.0a5

Téléchargements : https://github.com/VIG-tekh-labs/Subterfuge-Framework/releases

Deux installateurs natifs sont prévus : Windows 10/11 x64 (.exe) et Debian/Ubuntu/Kali Linux amd64 (.deb). Les fichiers de la version alpha ne doivent être considérés comme disponibles qu'après leur publication effective sur GitHub Releases. Un installateur macOS est reporté.

## Windows 10 / 11 — 64 bits

Télécharger : Subterfuge-Setup-2.0.0a5-Windows-x64.exe

Double-cliquer sur l'EXE, puis suivre l'assistant. Python, le GUI Qt/PySide6, Scapy et leurs bibliothèques principales sont inclus. Aucune installation manuelle de Python ou pip n'est nécessaire.

L'assistant propose par défaut une tâche facultative d'installation de Nmap, Wireshark/TShark et mitmproxy avec Windows Package Manager (WinGet). Cette tâche nécessite Internet, WinGet opérationnel et l'autorisation d'installer des logiciels tiers. Certaines confirmations Windows, licences, pilotes de capture Npcap, règles administrateur ou redémarrages peuvent rester nécessaires. Si un outil facultatif échoue, le GUI et l'analyse hors ligne restent utilisables.

Le journal d'installation facultatif est enregistré à :
%LOCALAPPDATA%\Subterfuge\optional-network-tools-install.log

L'installateur alpha n'est pas encore signé numériquement. Windows SmartScreen peut afficher un avertissement. Vérifier la provenance et les empreintes avant exécution.

Lancer ensuite « Subterfuge Framework » depuis le menu Démarrer.

## Debian / Ubuntu / Kali Linux — 64 bits Intel/AMD

Télécharger : Subterfuge-2.0.0a5-Linux-amd64.deb

Dans le répertoire du téléchargement :

    sudo apt install ./Subterfuge-2.0.0a5-Linux-amd64.deb

Le paquet comprend Python, Qt/PySide6, Scapy et le GUI. APT installe automatiquement les dépendances déclarées — Nmap, TShark, mitmproxy et bibliothèques système — depuis les dépôts configurés et approuvés. Il faut Internet si elles ne sont pas déjà installées ou disponibles en cache.

Utiliser apt install ./fichier.deb plutôt que dpkg -i, car dpkg -i seul ne télécharge pas les dépendances.

Un raccourci « Subterfuge Framework » est ajouté au menu des applications. En terminal, lancer :

    subterfuge gui

Sur un serveur sans interface graphique, lancer :

    subterfuge serve --port 8080

La page est alors disponible sur http://127.0.0.1:8080/ depuis le serveur. Pour un accès distant, utiliser un tunnel SSH sécurisé ou un reverse proxy HTTPS authentifié, suivant SERVER_ACCESS.md.

Désinstaller le paquet :

    sudo apt remove subterfuge-framework

## Vérification des téléchargements

La release contient SHA256SUMS.txt. Sous Windows, utiliser PowerShell :

    Get-FileHash .\Subterfuge-Setup-2.0.0a5-Windows-x64.exe -Algorithm SHA256

Sous Linux :

    sha256sum Subterfuge-2.0.0a5-Linux-amd64.deb

Comparer au fichier SHA256SUMS.txt officiel.

## Capacités et dépendances facultatives

Les analyses hors ligne et le GUI utilisent leurs dépendances embarquées. Nmap est nécessaire pour découvrir des hôtes et inventorier les ports en direct ; TShark pour déchiffrer des captures TLS munies de secrets de session obtenus légitimement ; mitmproxy pour le proxy de laboratoire explicite.

La capture directe peut encore demander un pilote réseau ou des autorisations système. Les restrictions imposées par l'entreprise, l'absence de paquets APT/WinGet ou de réseau empêchent certaines installations automatiques. Aucun certificat CA, élévation permanente ou changement de routage n'est installé en secret.

Version alpha : procéder à des essais avant un usage critique. Les architectures ARM et 32 bits, les vieux OS et les installateurs macOS ne sont pas couverts par cette release.

Code et licences : LICENSE et THIRD_PARTY_NOTICES.md. Aucune dépendance à un logiciel privé.
