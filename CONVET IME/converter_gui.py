"""
Interface graphique moderne et élégante pour le convertisseur d'images.
Design inspiré par les tendances UI/UX actuelles (rose, violet, géométrie).
"""
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QListWidget, QListWidgetItem, QComboBox,
    QLabel, QProgressBar, QMessageBox, QDialog, QTextEdit, QScrollArea,
    QFrame
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
        self.setWindowTitle("Détails de la conversion")
        self.setGeometry(100, 100, 600, 400)
        self.setup_modern_style()
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Titre
        title = QLabel(f"🔄 {source_format.upper()} → {target_format.upper()}")
        title_font = QFont("Segoe UI", 14, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #6B2C8C;")
        layout.addWidget(title)
        
        # Informations détaillées
        info_text = self._get_conversion_info(source_format, target_format)
        text_edit = QTextEdit()
        text_edit.setText(info_text)
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont("Segoe UI", 10))
        layout.addWidget(text_edit)
        
        # Bouton OK
        ok_button = QPushButton("Compris ✓")
        ok_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)
    
    def setup_modern_style(self):
        """Configure le style moderne."""
        self.setStyleSheet("""
            QDialog {
                background: linear-gradient(135deg, #FFFFFF 0%, #F5E6FF 100%);
            }
            QTextEdit {
                background-color: #FAFAFA;
                border: 2px solid #E6D5FF;
                border-radius: 8px;
                padding: 12px;
                color: #333;
            }
            QPushButton {
                background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #E6004D 0%, #FF1493 100%);
            }
        """)
    
    def _get_conversion_info(self, source_format, target_format):
        """Retourne les informations détaillées sur la conversion."""
        conversion_key = (source_format, target_format)
        
        if conversion_key in CONVERSION_MATRIX:
            info = CONVERSION_MATRIX[conversion_key]
            source_type = FORMAT_INFO[source_format]["type"]
            target_type = FORMAT_INFO[target_format]["type"]
            
            text = f"Type de conversion: {source_type} → {target_type}\n\n"
            text += f"📋 Remarque: {info['info']}\n\n"
            
            if info['risk'] == 'low':
                text += "🟢 Risque: Faible\nCette conversion est généralement sans problème."
            elif info['risk'] == 'medium':
                text += "🟡 Risque: Moyen\nQuelques pertes de qualité ou de compatibilité possibles."
            elif info['risk'] == 'high':
                text += "🔴 Risque: Élevé\nCette conversion peut entraîner des pertes significatives."
            
            return text
        
        return "Information non disponible"


class ImageConverterUI(QMainWindow):
    """Interface utilisateur moderne et élégante."""
    
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.init_ui()
        self.apply_modern_style()
    
    def init_ui(self):
        """Initialise l'interface utilisateur."""
        self.setWindowTitle("🖼️ Convertisseur d'Images")
        self.setGeometry(100, 100, 1100, 750)
        self.setMinimumSize(900, 600)
        
        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Titre élégant
        title_frame = self._create_title_section()
        main_layout.addWidget(title_frame)
        
        # Section fichiers
        files_frame = self._create_files_section()
        main_layout.addWidget(files_frame, 1)
        
        # Section format
        format_frame = self._create_format_section()
        main_layout.addWidget(format_frame)
        
        # Section info conversion
        info_frame = self._create_info_section()
        main_layout.addWidget(info_frame)
        
        # Section actions
        action_frame = self._create_action_section()
        main_layout.addWidget(action_frame)
        
        central_widget.setLayout(main_layout)
    
    def _create_title_section(self):
        """Crée la section titre."""
        frame = QFrame()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("🖼️ Convertisseur d'Images")
        title_font = QFont("Segoe UI", 28, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #6B2C8C;")
        layout.addWidget(title)
        
        subtitle = QLabel("Convertissez vos images en toute facilité")
        subtitle_font = QFont("Segoe UI", 11)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #999; margin-top: -5px;")
        layout.addWidget(subtitle)
        
        frame.setLayout(layout)
        return frame
    
    def _create_files_section(self):
        """Crée la section de sélection de fichiers."""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 2px solid #FFE6F0;
            }
        """)
        frame.setMinimumHeight(250)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # En-tête
        header_layout = QHBoxLayout()
        label = QLabel("📋 Fichiers sélectionnés")
        label_font = QFont("Segoe UI", 12, QFont.Bold)
        label.setFont(label_font)
        label.setStyleSheet("color: #333;")
        header_layout.addWidget(label)
        header_layout.addStretch()
        
        add_btn = QPushButton("➕ Ajouter des images")
        add_btn.setMaximumWidth(200)
        add_btn.clicked.connect(self.select_files)
        add_btn.setStyleSheet(self._get_button_style("secondary"))
        header_layout.addWidget(add_btn)
        
        clear_btn = QPushButton("🗑️ Effacer")
        clear_btn.setMaximumWidth(120)
        clear_btn.clicked.connect(self.clear_files)
        clear_btn.setStyleSheet(self._get_button_style("danger"))
        header_layout.addWidget(clear_btn)
        
        layout.addLayout(header_layout)
        
        # Liste des fichiers
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: #FAFAFA;
                border-radius: 8px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 6px;
                margin: 4px;
            }
            QListWidget::item:selected {
                background: linear-gradient(135deg, #FFE6F0 0%, #FFD6E8 100%);
            }
        """)
        layout.addWidget(self.file_list)
        
        frame.setLayout(layout)
        return frame
    
    def _create_format_section(self):
        """Crée la section de sélection du format."""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 2px solid #E6D5FF;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 15, 20, 15)
        
        label = QLabel("📁 Format cible:")
        label_font = QFont("Segoe UI", 11, QFont.Bold)
        label.setFont(label_font)
        label.setStyleSheet("color: #333;")
        layout.addWidget(label)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["jpg", "png", "webp", "gif", "bmp", "tiff", "heic", "svg", "pdf"])
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        self.format_combo.setStyleSheet("""
            QComboBox {
                background-color: #FAFAFA;
                border: 2px solid #E6D5FF;
                border-radius: 8px;
                padding: 8px 12px;
                color: #333;
                font-family: Segoe UI;
                font-size: 10pt;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)
        self.format_combo.setMaximumWidth(200)
        layout.addWidget(self.format_combo)
        
        info_btn = QPushButton("ℹ️ Détails")
        info_btn.clicked.connect(self.show_conversion_info)
        info_btn.setStyleSheet(self._get_button_style("info"))
        info_btn.setMaximumWidth(120)
        layout.addWidget(info_btn)
        
        layout.addStretch()
        
        frame.setLayout(layout)
        return frame
    
    def _create_info_section(self):
        """Crée la section d'information sur la conversion."""
        self.info_label = QLabel("Sélectionnez des fichiers pour voir les recommandations")
        self.info_label.setWordWrap(True)
        self.info_label.setFont(QFont("Segoe UI", 10))
        self.info_label.setMinimumHeight(60)
        self.info_label.setStyleSheet("""
            QLabel {
                background: linear-gradient(135deg, #E6F3FF 0%, #E6F7FF 100%);
                border-left: 5px solid #007BFF;
                border-radius: 8px;
                padding: 15px;
                color: #0056B3;
            }
        """)
        return self.info_label
    
    def _create_action_section(self):
        """Crée la section d'actions."""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #DDD;
                border-radius: 6px;
                text-align: center;
                height: 8px;
            }
            QProgressBar::chunk {
                background: linear-gradient(90deg, #FF1493 0%, #FF69B4 100%);
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Bouton convertir
        convert_button = QPushButton("🚀 Convertir Maintenant")
        convert_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        convert_button.setMinimumHeight(50)
        convert_button.clicked.connect(self.start_conversion)
        convert_button.setStyleSheet(self._get_button_style("primary"))
        layout.addWidget(convert_button)
        
        return layout
    
    def _get_button_style(self, button_type="primary"):
        """Retourne le style CSS pour les boutons."""
        styles = {
            "primary": """
                QPushButton {
                    background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                    font-family: Segoe UI;
                }
                QPushButton:hover {
                    background: linear-gradient(135deg, #E6004D 0%, #FF1493 100%);
                }
                QPushButton:pressed {
                    background: linear-gradient(135deg, #CC004D 0%, #E60052 100%);
                }
            """,
            "secondary": """
                QPushButton {
                    background: linear-gradient(135deg, #6B2C8C 0%, #8B3A9E 100%);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 15px;
                    font-weight: bold;
                    font-family: Segoe UI;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background: linear-gradient(135deg, #5A1F7B 0%, #7B2C8E 100%);
                }
            """,
            "danger": """
                QPushButton {
                    background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 15px;
                    font-weight: bold;
                    font-family: Segoe UI;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background: linear-gradient(135deg, #E60000 0%, #FF3333 100%);
                }
            """,
            "info": """
                QPushButton {
                    background: linear-gradient(135deg, #007BFF 0%, #0056B3 100%);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 15px;
                    font-weight: bold;
                    font-family: Segoe UI;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background: linear-gradient(135deg, #0056B3 0%, #003D82 100%);
                }
            """
        }
        return styles.get(button_type, styles["primary"])
    
    def apply_modern_style(self):
        """Applique le style moderne à l'application."""
        self.setStyleSheet("""
            QMainWindow {
                background: linear-gradient(135deg, #FFFFFF 0%, #F5E6FF 100%);
            }
            QLabel {
                color: #333;
                font-family: Segoe UI;
            }
            QComboBox {
                font-family: Segoe UI;
            }
        """)
    
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
        self.info_label.setText("Sélectionnez des fichiers pour voir les recommandations")
    
    def update_file_list(self):
        """Met à jour l'affichage de la liste des fichiers."""
        self.file_list.clear()
        for file_path in self.selected_files:
            source_format = detect_format(file_path)
            if source_format:
                item_text = f"{Path(file_path).name} ({source_format.upper()})"
            else:
                item_text = Path(file_path).name
            
            item = QListWidgetItem(item_text)
            self.file_list.addItem(item)
        
        if self.selected_files:
            self.update_conversion_info()
    
    def on_format_changed(self):
        """Met à jour les informations quand le format change."""
        if self.selected_files:
            self.update_conversion_info()
    
    def update_conversion_info(self):
        """Affiche les informations sur la conversion possibles."""
        if not self.selected_files:
            self.info_label.setText("Sélectionnez des fichiers pour voir les recommandations")
            return
        
        source_format = detect_format(self.selected_files[0])
        target_format = self.format_combo.currentText()
        
        if not source_format:
            self.info_label.setText("⚠️ Format source non reconnu")
            return
        
        conversions = get_available_conversions(source_format)
        target_exists = any(c["target"] == target_format for c in conversions)
        
        if not target_exists:
            self.info_label.setStyleSheet("""
                QLabel {
                    background: linear-gradient(135deg, #FFE6E6 0%, #FFEBEB 100%);
                    border-left: 5px solid #FF6B6B;
                    border-radius: 8px;
                    padding: 15px;
                    color: #C92A2A;
                }
            """)
            self.info_label.setText(f"⚠️ La conversion {source_format.upper()} → {target_format.upper()} n'est pas supportée")
            return
        
        conversion_info = next((c for c in conversions if c["target"] == target_format), None)
        
        if conversion_info:
            risk_symbol = "🟢" if conversion_info["risk"] == "low" else "🟡" if conversion_info["risk"] == "medium" else "🔴"
            
            if conversion_info["risk"] == "low":
                bg_gradient = "linear-gradient(135deg, #E6F9E6 0%, #F0FFF0 100%)"
                border_color = "#28A745"
                text_color = "#155724"
            elif conversion_info["risk"] == "medium":
                bg_gradient = "linear-gradient(135deg, #FFF3E6 0%, #FFFBF0 100%)"
                border_color = "#FFC107"
                text_color = "#856404"
            else:
                bg_gradient = "linear-gradient(135deg, #FFE6E6 0%, #FFEBEB 100%)"
                border_color = "#FF6B6B"
                text_color = "#C92A2A"
            
            info_text = f"{risk_symbol} {conversion_info['info']}"
            
            self.info_label.setStyleSheet(f"""
                QLabel {{
                    background: {bg_gradient};
                    border-left: 5px solid {border_color};
                    border-radius: 8px;
                    padding: 15px;
                    color: {text_color};
                }}
            """)
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
            QMessageBox.information(
                self, 
                "✅ Succès", 
                "Vos images ont été converties avec succès!",
                QMessageBox.Ok
            )
            self.clear_files()
        else:
            QMessageBox.critical(self, "❌ Erreur", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverterUI()
    window.show()
    sys.exit(app.exec_())
