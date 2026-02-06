#!/usr/bin/env python3
"""
LUCID EMPIRE v5.0-TITAN Console (No-Fork Edition)
==================================================
Main GUI application for TITAN anti-detection system.

ARCHITECTURE: Naked Browser Protocol
- Standard Firefox ESR / Chromium (no forks)
- Hardware Shield (LD_PRELOAD) for GPU/CPU spoofing 
- Genesis Engine for profile warmup and handover
- eBPF for network fingerprint masquerading

AUTHORITY: Dva.12 | TITAN V5 FINAL
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Check for PyQt6
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTabWidget, QPushButton, QLabel, QListWidget, QListWidgetItem,
        QLineEdit, QSpinBox, QComboBox, QTextEdit, QGroupBox, QFormLayout,
        QMessageBox, QSplitter, QFrame, QProgressBar, QStatusBar,
        QDialog, QDialogButtonBox, QGridLayout, QScrollArea
    )
    from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
    from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    print("PyQt6 not available. Install with: pip install PyQt6")

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.zero_detect import ZeroDetectEngine, ZeroDetectProfile
from backend.genesis_engine import GenesisEngine
from backend.firefox_injector_v2 import FirefoxProfileInjectorV2
from backend.validation.preflight_validator import PreFlightValidator
from backend.handover_protocol import HandoverProtocol, ProfileSpec


class TitanStyles:
    """Cyberpunk-style CSS for TITAN Console."""
    
    MAIN_STYLE = """
    QMainWindow {
        background-color: #0a0a0f;
    }
    
    QWidget {
        background-color: #0a0a0f;
        color: #e0e0e0;
        font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    }
    
    QTabWidget::pane {
        border: 1px solid #00d4ff;
        background-color: #12121a;
        border-radius: 4px;
    }
    
    QTabBar::tab {
        background-color: #1a1a2e;
        color: #a0a0a0;
        padding: 10px 20px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    
    QTabBar::tab:selected {
        background-color: #00d4ff;
        color: #0a0a0f;
        font-weight: bold;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #2a2a4e;
    }
    
    QPushButton {
        background-color: #1a1a2e;
        color: #00d4ff;
        border: 1px solid #00d4ff;
        padding: 10px 20px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #00d4ff;
        color: #0a0a0f;
    }
    
    QPushButton:pressed {
        background-color: #00a0cc;
    }
    
    QPushButton#dangerBtn {
        border-color: #ff4757;
        color: #ff4757;
    }
    
    QPushButton#dangerBtn:hover {
        background-color: #ff4757;
        color: white;
    }
    
    QPushButton#successBtn {
        border-color: #00ff88;
        color: #00ff88;
    }
    
    QPushButton#successBtn:hover {
        background-color: #00ff88;
        color: #0a0a0f;
    }
    
    QLineEdit, QSpinBox, QComboBox {
        background-color: #1a1a2e;
        border: 1px solid #3a3a5e;
        padding: 8px;
        border-radius: 4px;
        color: #e0e0e0;
    }
    
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
        border-color: #00d4ff;
    }
    
    QListWidget {
        background-color: #12121a;
        border: 1px solid #2a2a4e;
        border-radius: 4px;
    }
    
    QListWidget::item {
        padding: 10px;
        border-bottom: 1px solid #1a1a2e;
    }
    
    QListWidget::item:selected {
        background-color: #00d4ff;
        color: #0a0a0f;
    }
    
    QListWidget::item:hover:!selected {
        background-color: #2a2a4e;
    }
    
    QGroupBox {
        border: 1px solid #2a2a4e;
        border-radius: 4px;
        margin-top: 10px;
        padding-top: 10px;
        font-weight: bold;
        color: #00d4ff;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }
    
    QTextEdit {
        background-color: #12121a;
        border: 1px solid #2a2a4e;
        border-radius: 4px;
        color: #00ff88;
        font-family: 'Consolas', 'Monaco', monospace;
    }
    
    QProgressBar {
        border: 1px solid #2a2a4e;
        border-radius: 4px;
        text-align: center;
        background-color: #1a1a2e;
    }
    
    QProgressBar::chunk {
        background-color: #00d4ff;
    }
    
    QStatusBar {
        background-color: #12121a;
        color: #a0a0a0;
    }
    
    QLabel#headerLabel {
        font-size: 18px;
        font-weight: bold;
        color: #00d4ff;
    }
    
    QLabel#statusActive {
        color: #00ff88;
        font-weight: bold;
    }
    
    QLabel#statusInactive {
        color: #ff4757;
    }
    """


class ProfileCreationDialog(QDialog):
    """Dialog for creating new profiles."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Profile")
        self.setMinimumWidth(400)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Form
        form = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., US_Shopper_01")
        form.addRow("Profile Name:", self.name_input)
        
        self.aging_spin = QSpinBox()
        self.aging_spin.setRange(0, 365)
        self.aging_spin.setValue(90)
        self.aging_spin.setSuffix(" days")
        form.addRow("Profile Age:", self.aging_spin)
        
        self.os_combo = QComboBox()
        self.os_combo.addItems(["windows", "macos", "linux", "android", "ios"])
        form.addRow("Target OS:", self.os_combo)
        
        self.browser_combo = QComboBox()
        self.browser_combo.addItems(["chrome", "firefox", "safari", "edge"])
        form.addRow("Browser Type:", self.browser_combo)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_values(self):
        return {
            "name": self.name_input.text(),
            "aging_days": self.aging_spin.value(),
            "os_type": self.os_combo.currentText(),
            "browser_type": self.browser_combo.currentText(),
        }


class ValidationWorker(QThread):
    """Background worker for pre-flight validation."""
    
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str)
    
    def __init__(self, profile_path: Path):
        super().__init__()
        self.profile_path = profile_path
    
    def run(self):
        self.progress.emit("Starting validation...")
        validator = PreFlightValidator(self.profile_path)
        passed, results = validator.validate_all()
        summary = validator.get_summary()
        self.finished.emit(summary)


class TitanConsole(QMainWindow):
    """Main TITAN Console window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LUCID EMPIRE v5.0-TITAN Console")
        self.setMinimumSize(1200, 800)
        
        # Initialize engine
        self.data_dir = Path.home() / ".lucid-empire"
        self.engine = ZeroDetectEngine(self.data_dir)
        
        self.setup_ui()
        self.load_profiles()
        
        # Status timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)
    
    def setup_ui(self):
        """Set up the main UI."""
        self.setStyleSheet(TitanStyles.MAIN_STYLE)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("🔮 LUCID EMPIRE :: TITAN CONSOLE v5.0")
        header.setObjectName("headerLabel")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Main tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_profiles_tab(), "📋 Profiles")
        tabs.addTab(self.create_browser_tab(), "🌐 Browser")
        tabs.addTab(self.create_validation_tab(), "✓ Pre-Flight")
        tabs.addTab(self.create_system_tab(), "🖥️ System")
        layout.addWidget(tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def create_profiles_tab(self) -> QWidget:
        """Create the profiles management tab."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Profile list
        list_group = QGroupBox("Available Profiles")
        list_layout = QVBoxLayout(list_group)
        
        self.profile_list = QListWidget()
        self.profile_list.itemClicked.connect(self.on_profile_selected)
        list_layout.addWidget(self.profile_list)
        
        # List buttons
        btn_layout = QHBoxLayout()
        
        create_btn = QPushButton("➕ Create")
        create_btn.clicked.connect(self.create_profile)
        btn_layout.addWidget(create_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_profiles)
        btn_layout.addWidget(refresh_btn)
        
        list_layout.addLayout(btn_layout)
        layout.addWidget(list_group)
        
        # Profile details
        details_group = QGroupBox("Profile Details")
        details_layout = QVBoxLayout(details_group)
        
        self.profile_details = QTextEdit()
        self.profile_details.setReadOnly(True)
        details_layout.addWidget(self.profile_details)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        load_btn = QPushButton("📂 Load Profile")
        load_btn.setObjectName("successBtn")
        load_btn.clicked.connect(self.load_selected_profile)
        action_layout.addWidget(load_btn)
        
        burn_btn = QPushButton("🔥 Burn Profile")
        burn_btn.setObjectName("dangerBtn")
        burn_btn.clicked.connect(self.burn_profile)
        action_layout.addWidget(burn_btn)
        
        details_layout.addLayout(action_layout)
        layout.addWidget(details_group)
        
        return widget
    
    def create_browser_tab(self) -> QWidget:
        """Create the browser launch tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Active profile display
        active_group = QGroupBox("Active Profile")
        active_layout = QVBoxLayout(active_group)
        
        self.active_label = QLabel("No profile loaded")
        self.active_label.setObjectName("statusInactive")
        self.active_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        active_layout.addWidget(self.active_label)
        
        layout.addWidget(active_group)
        
        # Browser selection
        browser_group = QGroupBox("Launch Browser")
        browser_layout = QGridLayout(browser_group)
        
        browsers = [
            ("🦊 Firefox (Shielded)", "firefox", "Standard Firefox ESR + Hardware Shield"),
            ("🌍 Chromium (Shielded)", "chromium", "Chromium + Hardware Shield"),
        ]
        
        for i, (name, browser_id, desc) in enumerate(browsers):
            btn = QPushButton(name)
            btn.setMinimumHeight(80)
            btn.clicked.connect(lambda checked, b=browser_id: self.launch_browser(b))
            browser_layout.addWidget(btn, 0, i)
            
            label = QLabel(desc)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            browser_layout.addWidget(label, 1, i)
        
        layout.addWidget(browser_group)
        
        # Launch log
        log_group = QGroupBox("Launch Log")
        log_layout = QVBoxLayout(log_group)
        
        self.launch_log = QTextEdit()
        self.launch_log.setReadOnly(True)
        self.launch_log.setMaximumHeight(200)
        log_layout.addWidget(self.launch_log)
        
        layout.addWidget(log_group)
        layout.addStretch()
        
        return widget
    
    def create_validation_tab(self) -> QWidget:
        """Create the pre-flight validation tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Validation controls
        control_layout = QHBoxLayout()
        
        validate_btn = QPushButton("🔍 Run Pre-Flight Check")
        validate_btn.clicked.connect(self.run_validation)
        control_layout.addWidget(validate_btn)
        
        self.validation_progress = QProgressBar()
        self.validation_progress.setTextVisible(False)
        control_layout.addWidget(self.validation_progress)
        
        layout.addLayout(control_layout)
        
        # Results
        results_group = QGroupBox("Validation Results")
        results_layout = QVBoxLayout(results_group)
        
        self.validation_results = QTextEdit()
        self.validation_results.setReadOnly(True)
        results_layout.addWidget(self.validation_results)
        
        layout.addWidget(results_group)
        
        return widget
    
    def create_system_tab(self) -> QWidget:
        """Create the system status tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # System info
        info_group = QGroupBox("System Information")
        info_layout = QFormLayout(info_group)
        
        self.kernel_label = QLabel("Checking...")
        info_layout.addRow("Kernel:", self.kernel_label)
        
        self.ebpf_label = QLabel("Checking...")
        info_layout.addRow("eBPF Status:", self.ebpf_label)
        
        self.interface_label = QLabel("Checking...")
        info_layout.addRow("Network Interface:", self.interface_label)
        
        self.profiles_label = QLabel("0")
        info_layout.addRow("Total Profiles:", self.profiles_label)
        
        layout.addWidget(info_group)
        
        # Actions
        actions_group = QGroupBox("System Actions")
        actions_layout = QHBoxLayout(actions_group)
        
        compile_btn = QPushButton("🔧 Compile Hardware Shield")
        compile_btn.clicked.connect(self.compile_hardware_shield)
        actions_layout.addWidget(compile_btn)
        
        reload_btn = QPushButton("🔄 Reload eBPF")
        reload_btn.clicked.connect(self.reload_ebpf)
        actions_layout.addWidget(reload_btn)
        
        layout.addWidget(actions_group)
        layout.addStretch()
        
        self.update_system_info()
        
        return widget
    
    def load_profiles(self):
        """Load profiles into the list."""
        self.profile_list.clear()
        profiles = self.engine.list_profiles()
        
        for name in profiles:
            item = QListWidgetItem(f"📁 {name}")
            item.setData(Qt.ItemDataRole.UserRole, name)
            self.profile_list.addItem(item)
        
        self.profiles_label.setText(str(len(profiles)))
        self.status_bar.showMessage(f"Loaded {len(profiles)} profiles")
    
    def on_profile_selected(self, item: QListWidgetItem):
        """Handle profile selection."""
        name = item.data(Qt.ItemDataRole.UserRole)
        try:
            profile = self.engine.load_profile(name)
            details = json.dumps(profile.to_dict(), indent=2)
            self.profile_details.setText(details)
        except Exception as e:
            self.profile_details.setText(f"Error loading profile: {e}")
    
    def create_profile(self):
        """Show profile creation dialog."""
        dialog = ProfileCreationDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()
            if not values["name"]:
                QMessageBox.warning(self, "Error", "Profile name is required")
                return
            
            try:
                profile = self.engine.create_profile(
                    name=values["name"],
                    aging_days=values["aging_days"],
                    os_type=values["os_type"],
                    browser_type=values["browser_type"],
                )
                self.load_profiles()
                self.status_bar.showMessage(f"Created profile: {values['name']}")
                QMessageBox.information(self, "Success", f"Profile '{values['name']}' created!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create profile: {e}")
    
    def load_selected_profile(self):
        """Load the selected profile as active."""
        item = self.profile_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "No profile selected")
            return
        
        name = item.data(Qt.ItemDataRole.UserRole)
        try:
            profile = self.engine.load_profile(name)
            self.engine.activate_profile(profile)
            
            self.active_label.setText(f"✓ {profile.profile_name}")
            self.active_label.setObjectName("statusActive")
            self.active_label.setStyleSheet("color: #00ff88; font-weight: bold; font-size: 16px;")
            
            self.status_bar.showMessage(f"Activated profile: {name}")
            self.log_launch(f"Profile '{name}' activated")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load profile: {e}")
    
    def burn_profile(self):
        """Burn (archive and delete) the active profile."""
        reply = QMessageBox.warning(
            self,
            "Confirm Burn",
            "⚠️ BURN PROFILE?\n\nThis will archive and wipe the current profile.\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.engine.burn_profile():
                self.active_label.setText("No profile loaded")
                self.active_label.setObjectName("statusInactive")
                self.active_label.setStyleSheet("color: #ff4757;")
                self.status_bar.showMessage("Profile burned")
                self.log_launch("Profile burned and archived")
            else:
                QMessageBox.warning(self, "Error", "No active profile to burn")
    
    def launch_browser(self, browser_type: str):
        """Launch a browser with the active profile."""
        profile = self.engine.get_active_profile()
        if not profile:
            QMessageBox.warning(self, "Error", "No active profile. Load a profile first.")
            return
        
        self.log_launch(f"Launching {browser_type}...")
        
        try:
            if browser_type == "firefox":
                cmd = ["/opt/lucid-empire/bin/lucid-firefox"]
            elif browser_type == "chromium":
                cmd = ["/opt/lucid-empire/bin/lucid-chromium"]
            else:
                cmd = ["firefox-esr"]
            
            subprocess.Popen(cmd, start_new_session=True)
            self.log_launch(f"{browser_type} launched successfully")
            self.status_bar.showMessage(f"{browser_type} launched")
        except FileNotFoundError:
            self.log_launch(f"Browser launcher not found: {cmd[0]}")
            # Fallback to system browser
            try:
                subprocess.Popen(["firefox"], start_new_session=True)
                self.log_launch("Launched system Firefox as fallback")
            except Exception as e:
                self.log_launch(f"Failed to launch browser: {e}")
    
    def log_launch(self, message: str):
        """Add message to launch log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.launch_log.append(f"[{timestamp}] {message}")
    
    def run_validation(self):
        """Run pre-flight validation."""
        profile = self.engine.get_active_profile()
        if not profile:
            self.validation_results.setText("No active profile to validate.\nLoad a profile first.")
            return
        
        profile_path = self.engine.active_dir
        
        self.validation_progress.setRange(0, 0)  # Indeterminate
        self.validation_results.setText("Running validation...")
        
        self.validation_worker = ValidationWorker(profile_path)
        self.validation_worker.finished.connect(self.on_validation_complete)
        self.validation_worker.start()
    
    def on_validation_complete(self, summary: dict):
        """Handle validation completion."""
        self.validation_progress.setRange(0, 100)
        self.validation_progress.setValue(100)
        
        output = []
        output.append("=" * 50)
        output.append("PRE-FLIGHT VALIDATION RESULTS")
        output.append("=" * 50)
        output.append("")
        output.append(f"Total Checks: {summary['total_checks']}")
        output.append(f"Passed: {summary['passed']} ✓")
        output.append(f"Failed: {summary['failed']} ✗")
        output.append(f"Warnings: {summary['warnings']} ⚠")
        output.append("")
        output.append("-" * 50)
        
        for result in summary['results']:
            icon = "✓" if result['passed'] else ("⚠" if result['severity'] == 'warning' else "✗")
            output.append(f"{icon} {result['name']}")
            output.append(f"   {result['message']}")
        
        output.append("-" * 50)
        output.append("")
        
        if summary['ready']:
            output.append("🚀 READY FOR LAUNCH")
        else:
            output.append("⛔ NOT READY - Fix errors before launching")
        
        self.validation_results.setText("\n".join(output))
    
    def update_system_info(self):
        """Update system information display."""
        # Kernel
        try:
            result = subprocess.run(["uname", "-r"], capture_output=True, text=True)
            self.kernel_label.setText(result.stdout.strip())
        except:
            self.kernel_label.setText("Unknown")
        
        # eBPF
        try:
            result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
            if "xdp" in result.stdout.lower():
                self.ebpf_label.setText("LOADED")
                self.ebpf_label.setStyleSheet("color: #00ff88;")
            else:
                self.ebpf_label.setText("Not loaded")
                self.ebpf_label.setStyleSheet("color: #ffc107;")
        except:
            self.ebpf_label.setText("Unknown")
        
        # Network interface
        try:
            result = subprocess.run(
                ["ip", "route", "show", "default"],
                capture_output=True, text=True
            )
            if result.stdout:
                parts = result.stdout.split()
                if "dev" in parts:
                    idx = parts.index("dev")
                    self.interface_label.setText(parts[idx + 1])
                else:
                    self.interface_label.setText("Unknown")
            else:
                self.interface_label.setText("No default route")
        except:
            self.interface_label.setText("Unknown")
    
    def update_status(self):
        """Periodic status update."""
        profile = self.engine.get_active_profile()
        if profile:
            self.active_label.setText(f"✓ {profile.profile_name}")
        
        self.profiles_label.setText(str(len(self.engine.list_profiles())))
    
    def compile_hardware_shield(self):
        """Compile the Hardware Shield LD_PRELOAD library."""
        try:
            result = subprocess.run(
                ["make", "-C", "/opt/lucid-empire/lib"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.status_bar.showMessage("Hardware Shield compiled successfully")
                QMessageBox.information(
                    self,
                    "Success",
                    "Hardware Shield (libhardwareshield.so) compiled!\n\n"
                    "The library will now intercept:\n"
                    "• WebGL GPU queries (glGetString)\n"
                    "• CPU core count (sysconf)\n"
                    "• /proc/cpuinfo reads (fopen)"
                )
            else:
                QMessageBox.warning(
                    self, 
                    "Compile Error", 
                    f"Hardware Shield compilation failed:\n{result.stderr}"
                )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to compile: {e}")
    
    def reload_ebpf(self):
        """Reload eBPF programs."""
        try:
            result = subprocess.run(
                ["sudo", "/opt/lucid-empire/bin/load-ebpf.sh"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.status_bar.showMessage("eBPF reloaded")
                self.update_system_info()
            else:
                QMessageBox.warning(self, "Error", f"eBPF reload failed:\n{result.stderr}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to reload eBPF: {e}")


def main():
    if not PYQT_AVAILABLE:
        print("ERROR: PyQt6 is required for the TITAN Console GUI")
        print("Install with: pip install PyQt6")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    app.setApplicationName("TITAN Console")
    app.setOrganizationName("LUCID EMPIRE")
    
    window = TitanConsole()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
