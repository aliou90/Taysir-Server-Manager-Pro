# 🚀 Taysir Server Manager Pro (TSMP)

**Taysir Server Manager Pro** est une application desktop robuste conçue par **Taysir Digital Group** pour simplifier le quotidien des développeurs PHP et administrateurs système sous Linux. 

Oubliez la gestion manuelle des processus PHP et les conflits de ports. TSMP centralise vos environnements de développement dans une interface élégante, performante et isolée.

---

## 📸 Aperçu de l'interface

![Vue d'ensemble de l'application](Screenshots/Taysir%20Server%20Manager%20Pro_001.png)

*Un aperçu de la gestion multi-serveurs avec incrémentation automatique des ports.*

---

## ✨ Points Forts

* **⚡ Gestion Multi-Instances :** Lancez plusieurs serveurs PHP simultanément sans effort.
* **🔢 Ports Intelligents :** Incrémentation automatique des ports (8081, 8082, 8083...) pour éviter les erreurs "Port already in use".
* **📟 Console Haute Visibilité :** Un terminal intégré fixé en mode sombre pour une lecture parfaite des logs (requêtes, erreurs 404, succès 200), même en thème clair.
* **🗄️ Panneau MySQL/MariaDB :** Gérez vos services de base de données (Démarrage/Arrêt) avec support `pkexec` pour une sécurité native Linux.
* **🌓 Interface Adaptative :** Basculez entre le **Mode Sombre** (confort visuel) et le **Mode Clair** (haute luminosité) instantanément.

---

## 📂 Captures d'écran

| Mode Sombre & Logs | Configuration Environnement |
| :---: | :---: |
| ![Mode Sombre](Screenshots/Taysir%20Server%20Manager%20Pro_002.png) | ![Home Status](Screenshots/Taysir%20Server%20Manager%20Pro_003.png) |
| *Visualisation des logs en temps réel* | *Vérification automatique de PHP et MySQL* |

---

## 🛠️ Installation (Debian / Ubuntu / Linux Mint)

L'application est fournie avec un installateur natif `.deb`.

1.  **Téléchargement :** Récupérez le fichier `taysirserver_1.0.deb`.
2.  **Installation :**
    ```bash
    sudo apt update
    sudo apt install ./taysirserver_1.0.deb
    ```
3.  **Lancement :** Recherchez "Taysir Server Manager" dans votre menu d'applications ou tapez `taysirserver` dans votre terminal.

---

## 🏗️ Guide pour les Développeurs

Si vous souhaitez contribuer ou compiler votre propre version :

### Prérequis
* Python 3.x
* PHP (CLI)
* MySQL ou MariaDB

### Installation locale (Venv)
```bash
# Cloner le projet
git clone git@github.com:aliou90/Taysir-Server-Manager-Pro.git
cd Taysir-Server-Manager-Pro

# Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install PyQt5 pyinstaller

# Lancer l'application
python app.py

# Compilation de l'exécutable
## Générer l'exécutable Linux
pyinstaller --noconsole --onefile --name "taysirserver" app.py

```
---

# 📜 À propos

Développé par Aliou Mbengue pour Taysir Digital Group.
Cet outil s'inscrit dans notre mission de fournir des solutions logicielles innovantes et optimisées pour l'écosystème Tech local et international.

© 2026 Taysir Digital Group. All rights reserved.

