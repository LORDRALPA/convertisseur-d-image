"""
Convertisseur d'Images Pro — Interface graphique
Copyright (c) 2026 Théophile TOKRE
Licence : MIT License — voir fichier LICENSE

Fourni « tel quel », sans garantie d'aucune sorte.
"""
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QListWidget, QListWidgetItem, QComboBox,
    QLabel, QProgressBar, QMessageBox, QDialog, QTextEdit, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from conversion_engine import (
    detect_format, get_available_conversions, convert_image,
    FORMAT_INFO, CONVERSION_MATRIX
)


class ConversionWorker(QThread):
    """Thread pour effectuer les conversions sans bloquer l'interface."""
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, files, target_format, output_dir):
        super().__init__()
        self.files = files
        self.target_format = target_format
        self.output_dir = output_dir
    
    def run(self):
        total = len(self.files)
        for idx, file_path in enumerate(self.files):
            try:
                filename = Path(file_path).stem
                output_path = os.path.join(
                    self.output_dir,
                    f"{filename}.{self.target_format}"
                )
                
                success, message = convert_image(file_path, output_path, self.target_format)
                
                if not success:
                    self.finished.emit(False, f"Erreur: {message}")
                    return
                
                progress = int((idx + 1) / total * 100)
                self.progress.emit(progress)
            
            except Exception as e:
                self.finished.emit(False, f"Erreur: {str(e)}")
                return
        
        self.finished.emit(True, "Conversion réussie!")


class RiskInfoDialog(QDialog):
    """Dialogue d'information sur les risques de conversion."""
    def __init__(self, parent, source_format, target_format):
        super().__init__(parent)
        self.setWindowTitle("Informations de conversion")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Titre
        title = QLabel(f"Conversion: {source_format.upper()} → {target_format.upper()}")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Informations détaillées
        info_text = self._get_conversion_info(source_format, target_format)
        text_edit = QTextEdit()
        text_edit.setText(info_text)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        # Bouton OK
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)
    
    def _get_conversion_info(self, source_format, target_format):
        """Retourne les informations détaillées sur la conversion."""
        conversion_key = (source_format, target_format)
        
        if conversion_key in CONVERSION_MATRIX:
            info = CONVERSION_MATRIX[conversion_key]
            source_type = FORMAT_INFO[source_format]["type"]
            target_type = FORMAT_INFO[target_format]["type"]
            
            text = f"Type de conversion: {source_type} → {target_type}\n\n"
            text += f"Remarque: {info['info']}\n\n"
            
            if info['risk'] == 'low':
                text += "⚠️ Risque: Faible\nCette conversion est généralement sans problème."
            elif info['risk'] == 'medium':
                text += "⚠️ Risque: Moyen\nQuelques pertes de qualité ou de compatibilité possibles."
            elif info['risk'] == 'high':
                text += "⚠️ Risque: Élevé\nCette conversion peut entraîner des pertes significatives."
            
            return text
        
        return "Information non disponible"


class AboutDialog(QDialog):
    """Dialogue À propos — informations légales et crédits."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("À propos")
        self.setFixedSize(560, 520)
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Titre
        title = QLabel("🖼️ Convertisseur d'Images Pro")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Version / auteur
        author_label = QLabel("Développé par <b>Théophile TOKRE</b> &mdash; Version 1.0 &mdash; 2026")
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setStyleSheet("color: #555; font-size: 12px;")
        layout.addWidget(author_label)

        # Séparateur visuel
        sep = QLabel()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #ddd;")
        layout.addWidget(sep)

        # Zone de texte légal
        legal = QTextEdit()
        legal.setReadOnly(True)
        legal.setStyleSheet("font-size: 12px; border: none; background: #fafafa;")
        legal.setHtml("""
<h3 style="color:#333;">Licence</h3>
<p>Ce logiciel est distribué sous la <b>licence MIT</b>.<br>
Copyright &copy; 2026 Théophile TOKRE. Tous droits réservés.</p>

<p style="color:#888; font-size:11px;">
Permission est accordée, gratuitement, à toute personne obtenant une copie
de ce logiciel, de l'utiliser, le copier, le modifier et le distribuer,
sous réserve de conserver la notice de copyright et de licence.<br><br>
CE LOGICIEL EST FOURNI <b>« TEL QUEL »</b>, SANS GARANTIE D'AUCUNE SORTE,
EXPRESSE OU IMPLICITE. L'AUTEUR NE SAURAIT ÊTRE TENU RESPONSABLE
D'AUCUN DOMMAGE DÉCOULANT DE SON UTILISATION.
</p>

<h3 style="color:#333;">Bibliothèques tierces</h3>
<table style="width:100%; font-size:11px; border-collapse:collapse;">
<tr><td><b>Pillow</b></td><td>HPND — python-pillow.org</td></tr>
<tr><td><b>pillow-heif</b></td><td>BSD 3-Clause — github.com/bigcat88/pillow_heif</td></tr>
<tr><td><b>PyQt5</b></td><td>GPL v3 — riverbankcomputing.com</td></tr>
<tr><td><b>CairoSVG</b></td><td>LGPL v3 — cairosvg.org</td></tr>
<tr><td><b>ReportLab</b></td><td>BSD 3-Clause — reportlab.com</td></tr>
<tr><td><b>ImageMagick</b></td><td>Apache-2.0 compatible — imagemagick.org</td></tr>
</table>

<p style="font-size:11px; color:#888; margin-top:10px;">
Voir le fichier <b>NOTICE.txt</b> pour le détail complet des licences tierces.
</p>

<h3 style="color:#333;">Protection des données</h3>
<p style="font-size:11px; color:#888;">
Ce logiciel traite vos images <b>localement sur votre machine</b>.<br>
Aucune donnée n'est envoyée vers un serveur extérieur.
</p>
""")
        layout.addWidget(legal)

        # Bouton fermer
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("padding: 8px 24px; font-weight: bold;")
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)


class ImageConverterUI(QMainWindow):
    """Interface utilisateur principale du convertisseur."""
    
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.init_ui()
    
    def init_ui(self):
        """Initialise l'interface utilisateur."""
        self.setWindowTitle("Convertisseur d'Images Pro")
        self.setGeometry(100, 100, 900, 700)

        # Barre de menu
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Aide")
        about_action = help_menu.addAction("À propos / Mentions légales")
        about_action.triggered.connect(self.show_about)

        # Style personnalisé
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
                font-family: Arial;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
        """)
        
        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Titre
        title = QLabel("🖼️ Convertisseur d'Images Professionnel")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title)
        
        # Section 1: Sélection des fichiers
        file_section_layout = QHBoxLayout()
        
        select_button = QPushButton("📁 Ajouter des images")
        select_button.clicked.connect(self.select_files)
        file_section_layout.addWidget(select_button)
        
        clear_button = QPushButton("🗑️ Effacer la liste")
        clear_button.clicked.connect(self.clear_files)
        file_section_layout.addWidget(clear_button)
        
        main_layout.addLayout(file_section_layout)
        
        # Liste des fichiers sélectionnés
        file_label = QLabel("📋 Fichiers sélectionnés:")
        main_layout.addWidget(file_label)
        
        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(200)
        main_layout.addWidget(self.file_list)
        
        # Section 2: Sélection du format cible
        format_section_layout = QHBoxLayout()
        
        format_label = QLabel("Format cible:")
        format_section_layout.addWidget(format_label)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(sorted(FORMAT_INFO.keys()))
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        format_section_layout.addWidget(self.format_combo)
        
        info_button = QPushButton("ℹ️ Détails")
        info_button.clicked.connect(self.show_conversion_info)
        format_section_layout.addWidget(info_button)
        
        format_section_layout.addStretch()
        main_layout.addLayout(format_section_layout)
        
        # Section 3: Informations sur la conversion
        self.info_label = QLabel("Sélectionnez des fichiers pour voir les informations de conversion")
        self.info_label.setStyleSheet("""
            background-color: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 10px;
            border-radius: 3px;
        """)
        main_layout.addWidget(self.info_label)
        
        # Section 4: Conversion
        convert_button = QPushButton("🚀 Convertir")
        convert_button.setStyleSheet("""
            background-color: #28a745;
            font-size: 14px;
            padding: 12px;
        """)
        convert_button.clicked.connect(self.start_conversion)
        main_layout.addWidget(convert_button)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Crédits
        credits_label = QLabel("Développé par <b>Théophile TOKRE</b> · Convertisseur d'Images Pro")
        credits_label.setAlignment(Qt.AlignCenter)
        credits_label.setStyleSheet("""
            color: #888;
            font-size: 11px;
            padding: 6px 0 2px 0;
            border-top: 1px solid #ddd;
        """)
        main_layout.addWidget(credits_label)

        central_widget.setLayout(main_layout)
    
    def show_about(self):
        """Affiche le dialogue À propos / mentions légales."""
        dialog = AboutDialog(self)
        dialog.exec_()

    def select_files(self):
        """Ouvre le dialogue de sélection de fichiers."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Sélectionner les images à convertir",
            "",
            "Images (*.jpg *.jpeg *.png *.gif *.webp *.bmp *.tiff *.heic *.svg *.pdf *.eps *.ai *.psd);;Tous les fichiers (*)"
        )
        
        if files:
            self.selected_files.extend(files)
            self.update_file_list()
    
    def clear_files(self):
        """Efface la liste des fichiers."""
        self.selected_files.clear()
        self.file_list.clear()
        self.info_label.setText("Sélectionnez des fichiers pour voir les informations de conversion")
    
    def update_file_list(self):
        """Met à jour l'affichage de la liste des fichiers."""
        self.file_list.clear()
        for file_path in self.selected_files:
            item = QListWidgetItem(Path(file_path).name)
            source_format = detect_format(file_path)
            if source_format:
                item.setText(f"{Path(file_path).name} ({source_format.upper()})")
            self.file_list.addItem(item)
    
    def on_format_changed(self):
        """Met à jour les informations quand le format change."""
        if self.selected_files:
            self.update_conversion_info()
    
    def update_conversion_info(self):
        """Affiche les informations sur la conversion possibles."""
        if not self.selected_files:
            self.info_label.setText("Sélectionnez des fichiers pour voir les informations de conversion")
            return
        
        source_format = detect_format(self.selected_files[0])
        target_format = self.format_combo.currentText()
        
        if not source_format:
            self.info_label.setText("⚠️ Format source non reconnu")
            return
        
        conversions = get_available_conversions(source_format)
        target_exists = any(c["target"] == target_format for c in conversions)
        
        if not target_exists:
            self.info_label.setText(f"⚠️ La conversion {source_format.upper()} → {target_format.upper()} n'est pas supportée")
            return
        
        conversion_info = next((c for c in conversions if c["target"] == target_format), None)
        
        if conversion_info:
            risk_symbol = "🟢" if conversion_info["risk"] == "low" else "🟡" if conversion_info["risk"] == "medium" else "🔴"
            info_text = f"{risk_symbol} {conversion_info['info']}"
            self.info_label.setText(info_text)
    
    def show_conversion_info(self):
        """Affiche le dialogue d'information détaillée."""
        if not self.selected_files:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner au moins un fichier")
            return
        
        source_format = detect_format(self.selected_files[0])
        target_format = self.format_combo.currentText()
        
        if source_format:
            dialog = RiskInfoDialog(self, source_format, target_format)
            dialog.exec_()
    
    def start_conversion(self):
        """Démarre la conversion des images."""
        if not self.selected_files:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner au moins un fichier")
            return
        
        output_dir = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier de destination")
        
        if not output_dir:
            return
        
        target_format = self.format_combo.currentText()
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker = ConversionWorker(self.selected_files, target_format, output_dir)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.start()
    
    def update_progress(self, value):
        """Met à jour la barre de progression."""
        self.progress_bar.setValue(value)
    
    def on_conversion_finished(self, success, message):
        """Gère la fin de la conversion."""
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Succès", message)
            self.clear_files()
        else:
            QMessageBox.critical(self, "Erreur", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverterUI()
    window.show()
    sys.exit(app.exec_())
