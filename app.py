import sys
import subprocess
import webbrowser
import platform
import shutil
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QLineEdit, QTextBrowser, QHBoxLayout, 
    QTabWidget, QInputDialog, QMessageBox, QFrame
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt

# --- CONFIGURATION DES THÈMES ---
# Note: console_bg et console_text sont maintenant fixes pour la lisibilité
THEMES = {
    "light": {
        "bg": "#f5f5f5", "card": "#ffffff", "text": "#333333", "border": "#dddddd",
        "input_bg": "#ffffff", "btn_bg": "#eeeeee", "console_bg": "#000000",
        "console_text": "#d1d1d1", "accent": "#00a86b", "tab_bg": "#e0e0e0", "header": "#2c3e50"
    },
    "dark": {
        "bg": "#121212", "card": "#1e1e1e", "text": "#e0e0e0", "border": "#333333",
        "input_bg": "#252525", "btn_bg": "#2c2c2c", "console_bg": "#000000",
        "console_text": "#d1d1d1", "accent": "#00ff9c", "tab_bg": "#1a1a1a", "header": "#00ff9c"
    }
}

class HomeWidget(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.init_ui()
        self.check_env()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("💻 Configuration de l'Environnement")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.php_box = self.create_status_box("Interpréteur PHP", "php_status")
        self.btn_install_php = QPushButton("🚀 Installer PHP")
        self.btn_install_php.clicked.connect(self.install_php)
        self.php_box.layout().addWidget(self.btn_install_php)
        layout.addWidget(self.php_box)

        self.mysql_box = self.create_status_box("Serveur MySQL / MariaDB", "mysql_status")
        self.btn_install_mysql = QPushButton("🚀 Installer MySQL")
        self.btn_install_mysql.clicked.connect(self.install_mysql)
        self.mysql_box.layout().addWidget(self.btn_install_mysql)
        layout.addWidget(self.mysql_box)

        layout.addStretch()
        btn_refresh = QPushButton("🔄 Actualiser l'état")
        btn_refresh.clicked.connect(self.check_env)
        layout.addWidget(btn_refresh)

    def create_status_box(self, name, object_name):
        frame = QFrame()
        frame.setObjectName("card_frame")
        t = THEMES[self.parent_app.current_theme]
        frame.setStyleSheet(f"QFrame#card_frame {{ background-color: {t['card']}; border: 1px solid {t['border']}; border-radius: 10px; padding: 20px; }}")
        l = QVBoxLayout(frame)
        title = QLabel(name)
        title.setStyleSheet("font-size: 11px; color: #888; text-transform: uppercase;")
        status = QLabel("Vérification...")
        status.setObjectName(object_name)
        status.setStyleSheet("font-size: 16px; font-weight: bold;")
        l.addWidget(title)
        l.addWidget(status)
        return frame

    def check_env(self):
        has_php = shutil.which("php") is not None
        status_php = self.findChild(QLabel, "php_status")
        status_php.setText("✅ Installé" if has_php else "❌ Non détecté")
        status_php.setStyleSheet(f"color: {'#00ff9c' if has_php else '#ff4c4c'}; font-weight: bold; font-size: 16px;")
        self.btn_install_php.setVisible(not has_php)

        has_mysql = shutil.which("mysql") is not None or os.path.exists("/opt/lampp/bin/mysql")
        status_mysql = self.findChild(QLabel, "mysql_status")
        status_mysql.setText("✅ Installé / Opérationnel" if has_mysql else "❌ Non détecté")
        status_mysql.setStyleSheet(f"color: {'#00ff9c' if has_mysql else '#ff4c4c'}; font-weight: bold; font-size: 16px;")
        self.btn_install_mysql.setVisible(not has_mysql)

    def install_php(self):
        if platform.system() == "Linux": subprocess.run(["pkexec", "apt", "install", "-y", "php-cli"])
        else: webbrowser.open("https://www.php.net/downloads.php")
        self.check_env()

    def install_mysql(self):
        if platform.system() == "Linux": subprocess.run(["pkexec", "apt", "install", "-y", "mariadb-server"])
        else: webbrowser.open("https://dev.mysql.com/downloads/installer/")
        self.check_env()

class MySQLWidget(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.os_type = platform.system()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        lbl = QLabel("Gestion du Service MySQL")
        lbl.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(lbl)
        
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("⚡ Démarrer Service")
        self.btn_stop = QPushButton("🛑 Arrêter Service")
        self.btn_pma = QPushButton("🐘 phpMyAdmin")
        
        self.btn_start.clicked.connect(self.start_mysql_service)
        self.btn_stop.clicked.connect(self.stop_mysql_service)
        self.btn_pma.clicked.connect(lambda: webbrowser.open("http://localhost/phpmyadmin"))
        
        for b in [self.btn_start, self.btn_stop, self.btn_pma]: btn_layout.addWidget(b)
        layout.addLayout(btn_layout)
        
        self.logs = QTextBrowser()
        self.logs.setObjectName("console")
        layout.addWidget(self.logs)

    def run_command(self, cmd_list, needs_sudo=True):
        try:
            if needs_sudo and self.os_type == "Linux": cmd_list = ["pkexec"] + cmd_list
            p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=(self.os_type == "Windows"))
            stdout, stderr = p.communicate()
            if stdout: self.add_log(stdout, "#e0e0e0")
            if stderr: self.add_log(f"⚠️ {stderr}", "#727067")
            return p.returncode == 0
        except Exception as e:
            self.add_log(f"❌ Erreur : {str(e)}", "#ff4c4c")
            return False

    def start_mysql_service(self):
        if not shutil.which("mysql") and not os.path.exists("/opt/lampp/bin/mysql"):
            self.prompt_install("MySQL"); return
        self.add_log("🔄 Tentative de démarrage du service...", "#4cafff")
        success = False
        if self.os_type == "Windows":
            success = self.run_command(["net", "start", "mysql"]) or self.run_command(["net", "start", "mariadb"])
        else:
            success = self.run_command(["systemctl", "start", "mysql"]) or self.run_command(["systemctl", "start", "mariadb"])
            if not success and os.path.exists("/opt/lampp/lampp"):
                success = self.run_command(["/opt/lampp/lampp", "startmysql"])
        if success: self.add_log("✅ MySQL est maintenant opérationnel.", "#00ff9c")

    def stop_mysql_service(self):
        self.add_log("🔄 Arrêt du service MySQL...", "#ffcc00")
        if self.os_type == "Windows":
            self.run_command(["net", "stop", "mysql"]); self.run_command(["net", "stop", "mariadb"])
        else:
            self.run_command(["systemctl", "stop", "mysql"]); self.run_command(["systemctl", "stop", "mariadb"])
            if os.path.exists("/opt/lampp/lampp"): self.run_command(["/opt/lampp/lampp", "stopmysql"])
        self.add_log("🛑 Service arrêté.", "#ff4c4c")

    def prompt_install(self, name):
        if QMessageBox.critical(self, "Composant manquant", f"Le serveur {name} n'est pas détecté.", QPushButton(f"Installer {name}"), QMessageBox.Cancel) == 0:
            self.parent_app.tabs.setCurrentIndex(0)

    def add_log(self, text, color):
        self.logs.append(f'<span style="color:{color};">{text.strip()}</span>')

class ServerThread(QThread):
    log_signal = pyqtSignal(str)
    def __init__(self, folder, port):
        super().__init__()
        self.folder, self.port = folder, port
        self.process, self._running = None, True

    def run(self):
        try:
            self.process = subprocess.Popen(["php", "-S", f"localhost:{self.port}"], cwd=self.folder, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while self._running:
                line = self.process.stdout.readline()
                if line: self.log_signal.emit(line.strip())
                if self.process.poll() is not None: break
        except Exception as e: self.log_signal.emit(f"❌ Erreur: {str(e)}")

    def stop(self):
        self._running = False
        if self.process: self.process.terminate()
        self.quit(); self.wait()

class ServerWidget(QWidget):
    def __init__(self, parent_app, default_port="8088"):
        super().__init__()
        self.parent_app, self.thread = parent_app, None
        self.default_port = default_port
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        layout.addWidget(QLabel("Dossier Racine du Projet"))
        h1 = QHBoxLayout()
        self.folder_in = QLineEdit()
        self.folder_in.setPlaceholderText("Sélectionnez le dossier contenant votre index.php")
        btn_b = QPushButton("Parcourir")
        btn_b.clicked.connect(self.browse)
        h1.addWidget(self.folder_in); h1.addWidget(btn_b)
        layout.addLayout(h1)

        layout.addWidget(QLabel("Port d'écoute"))
        self.port_in = QLineEdit(self.default_port)
        self.port_in.setFixedWidth(100)
        layout.addWidget(self.port_in)

        btns = QHBoxLayout()
        self.btn_start = QPushButton("🚀 Démarrer Serveur")
        self.btn_stop = QPushButton("🛑 Arrêter")
        self.btn_open = QPushButton("🌐 Ouvrir site")
        self.btn_clear = QPushButton("🧹 Effacer Logs")
        
        self.btn_start.clicked.connect(self.start_s)
        self.btn_stop.clicked.connect(self.stop_s)
        self.btn_open.clicked.connect(lambda: webbrowser.open(f"http://localhost:{self.port_in.text()}"))
        self.btn_clear.clicked.connect(lambda: self.logs.clear())
        
        for b in [self.btn_start, self.btn_stop, self.btn_open, self.btn_clear]: btns.addWidget(b)
        layout.addLayout(btns)

        self.logs = QTextBrowser()
        self.logs.setOpenExternalLinks(True)
        self.logs.setObjectName("console")
        layout.addWidget(self.logs)
        
        self.btn_stop.setEnabled(False)
        self.btn_open.setEnabled(False)

    def browse(self):
        path = QFileDialog.getExistingDirectory()
        if path: self.folder_in.setText(path)

    def start_s(self):
        folder, port = self.folder_in.text(), self.port_in.text()
        if not folder:
            QMessageBox.warning(self, "Attention", "Veuillez choisir un dossier racine.")
            return
        if not shutil.which("php"):
            if QMessageBox.critical(self, "Erreur", "PHP n'est pas installé.", QPushButton("Installer"), QMessageBox.Cancel) == 0:
                self.parent_app.tabs.setCurrentIndex(0)
            return
            
        self.thread = ServerThread(folder, port)
        self.thread.log_signal.connect(self.handle_log)
        self.thread.start()
        
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_open.setEnabled(True)
        
        # Le vert de succès reste vif car le fond est noir
        color = "#00ff9c" 
        self.add_log(f'🚀 Serveur lancé sur <a href="http://localhost:{port}" style="color:{color};">http://localhost:{port}</a>', color)

    def handle_log(self, text):
        # Toujours utiliser les couleurs vives (style dark) car le fond de console est forcé en noir
        color = "#d1d1d1"
        if "error" in text.lower() or "failed" in text.lower(): color = "#ff4c4c"
        elif "accepted" in text.lower(): color = "#4cafff"
        elif "started" in text.lower() or "200" in text.lower(): color = "#00ff9c"
        self.add_log(text, color)

    def add_log(self, text, color):
        self.logs.append(f'<span style="color:{color};">{text}</span>')
        self.logs.verticalScrollBar().setValue(self.logs.verticalScrollBar().maximum())

    def stop_s(self):
        if self.thread: self.thread.stop()
        self.add_log("🛑 Serveur arrêté.", "#ff4c4c")
        self.btn_start.setEnabled(True); self.btn_stop.setEnabled(False); self.btn_open.setEnabled(False)

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_theme = "dark"
        self.setWindowTitle("Taysir Server Manager Pro")
        self.resize(1000, 800)
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        layout = QVBoxLayout(self)
        top = QHBoxLayout()
        header = QLabel("TAYSIR SERVER MANAGER PRO"); header.setObjectName("header_title")
        
        self.btn_theme = QPushButton("☀️ Mode Clair")
        self.btn_theme.clicked.connect(self.toggle_theme)
        
        btn_add = QPushButton("+ Nouveau Serveur")
        btn_add.clicked.connect(self.add_new_tab)
        
        top.addWidget(header); top.addStretch(); top.addWidget(self.btn_theme); top.addWidget(btn_add)
        layout.addLayout(top)

        self.tabs = QTabWidget(); self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tabs)

        self.tabs.addTab(HomeWidget(self), "🏠 Accueil")
        self.tabs.addTab(ServerWidget(self, "8088"), "PHP 1")
        self.mysql_tab = MySQLWidget(self)
        self.tabs.addTab(self.mysql_tab, "🗄️ MySQL")

        self.tabs.tabBar().setTabButton(0, self.tabs.tabBar().RightSide, None)
        self.tabs.tabBar().setTabButton(2, self.tabs.tabBar().RightSide, None)

    def add_new_tab(self):
        count = 0
        for i in range(self.tabs.count()):
            if isinstance(self.tabs.widget(i), ServerWidget):
                count += 1
        
        next_port = str(8088 + count)
        idx = self.tabs.count() - 1 
        self.tabs.insertTab(idx, ServerWidget(self, next_port), f"PHP {count + 1}")
        self.tabs.setCurrentIndex(idx)

    def close_tab(self, i):
        if i == 0 or i == self.tabs.count()-1: return
        w = self.tabs.widget(i)
        if hasattr(w, 'stop_s'): w.stop_s()
        self.tabs.removeTab(i)

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.btn_theme.setText("🌙 Mode Sombre" if self.current_theme == "light" else "☀️ Mode Clair")
        self.apply_theme()

    def apply_theme(self):
        t = THEMES[self.current_theme]
        # Ici, console_bg et console_text sont fixés sur des valeurs sombres dans le dictionnaire THEMES['light']
        self.setStyleSheet(f"""
            QWidget {{ background-color: {t['bg']}; color: {t['text']}; font-family: 'Segoe UI', Arial; }}
            #header_title {{ font-size: 20px; font-weight: bold; color: {t['header']}; padding: 10px; }}
            QTabWidget::pane {{ border: 1px solid {t['border']}; background: {t['bg']}; border-radius: 8px; }}
            QTabBar::tab {{ background: {t['tab_bg']}; border: 1px solid {t['border']}; padding: 12px 25px; color: {t['text']}; min-width: 100px; }}
            QTabBar::tab:selected {{ background: {t['card']}; border-bottom: 3px solid {t['accent']}; font-weight: bold; }}
            QLineEdit {{ background-color: {t['input_bg']}; border: 1px solid {t['border']}; border-radius: 5px; padding: 8px; color: {t['text']}; }}
            QPushButton {{ background-color: {t['btn_bg']}; border: 1px solid {t['border']}; border-radius: 5px; padding: 10px; font-weight: bold; color: {t['text']}; }}
            QPushButton:hover {{ background-color: {t['accent']}; color: #000; }}
            #console {{ background-color: {t['console_bg']}; border: 1px solid {t['border']}; border-radius: 8px; font-family: 'Consolas', 'Monaco', monospace; font-size: 13px; color: {t['console_text']}; }}
            QLabel {{ font-weight: bold; font-size: 11px; text-transform: uppercase; color: {t['text']}; }}
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv); w = MainApp(); w.show(); sys.exit(app.exec_())