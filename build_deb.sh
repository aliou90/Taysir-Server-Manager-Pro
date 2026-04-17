#!/bin/bash

# Configuration du projet
PACKAGE_NAME="taysirserver"
VERSION="1.0"
ARCH="amd64"
DESCRIPTION="Gestionnaire de serveurs PHP et MySQL par Taysir Digital Group"
MAINTAINER="Aliou Mbengue <mbengue.tech@gmail.com>"

# Dossier de construction
BUILD_DIR="${PACKAGE_NAME}_${VERSION}"

echo "🚀 Début de la création du paquet .deb..."

# 1. Création des répertoires
mkdir -p $BUILD_DIR/DEBIAN
mkdir -p $BUILD_DIR/usr/bin
mkdir -p $BUILD_DIR/usr/share/applications
mkdir -p $BUILD_DIR/usr/share/icons/hicolor/scalable/apps

# 2. Copie des fichiers
# Note : Assure-toi d'avoir un fichier icône .png ou .svg pour Linux
echo "📦 Copie de l'exécutable et de l'icône..."
if [ -f "dist/${PACKAGE_NAME}" ]; then
    cp dist/${PACKAGE_NAME} $BUILD_DIR/usr/bin/${PACKAGE_NAME}
else
    echo "❌ Erreur: Exécutable dist/${PACKAGE_NAME} introuvable. Compilez d'abord avec PyInstaller."
    exit 1
fi

# Copie de l'icône (On utilise un format PNG pour une meilleure compatibilité Linux)
if [ -f "assets/icon/logo.png" ]; then
    cp assets/icon/logo.png $BUILD_DIR/usr/share/icons/hicolor/scalable/apps/${PACKAGE_NAME}.png
fi

# Droits d'exécution
chmod +x $BUILD_DIR/usr/bin/${PACKAGE_NAME}

# 3. Création du fichier de contrôle (avec dépendances)
echo "📝 Génération du fichier control..."
cat <<EOF > $BUILD_DIR/DEBIAN/control
Package: ${PACKAGE_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Depends: python3, python3-pyqt5, policykit-1
Maintainer: ${MAINTAINER}
Description: ${DESCRIPTION}
 Un outil professionnel pour gérer plusieurs instances de serveurs PHP 
 et piloter les services MySQL/MariaDB avec support LAMP.
EOF

# 4. Création du fichier .desktop (Menu des applications)
echo "🖥️  Génération du raccourci bureau..."
cat <<EOF > $BUILD_DIR/usr/share/applications/${PACKAGE_NAME}.desktop
[Desktop Entry]
Name=Taysir Server Manager
Comment=Gérer vos serveurs PHP et MySQL
Exec=/usr/bin/${PACKAGE_NAME}
Icon=/usr/share/icons/hicolor/scalable/apps/${PACKAGE_NAME}.png
Terminal=false
Type=Application
Categories=Development;Network;
StartupNotify=true
EOF

# 5. Construction du paquet
echo "🛠️  Compilation du paquet .deb..."
dpkg-deb --build $BUILD_DIR

# Nettoyage
rm -rf $BUILD_DIR

echo "--------------------------------------------------"
echo "✅ Succès : ${PACKAGE_NAME}_${VERSION}.deb est prêt !"
echo "📌 Installation : sudo apt install ./${PACKAGE_NAME}_${VERSION}.deb"
echo "--------------------------------------------------"
