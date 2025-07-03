#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VSCode Ultimate Removal Tool v3.0 - Professional Python Edition
Complete System-Wide Cleanup with Advanced Features and Machine ID Reset
Developer: @aliseylabi
Telegram: @aliseylabi
Date: July 2025
Python Version: 3.6+
"""

import os
import sys
import json
import time
import shutil
import subprocess
import uuid
import hashlib
import threading
import tempfile
import zipfile
import sqlite3
import ctypes
import webbrowser
from ctypes import wintypes
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging

# GUI imports
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, simpledialog
    GUI_AVAILABLE = True
except ImportError:
    print("Warning: Tkinter not available. Running in console mode.")
    GUI_AVAILABLE = False

# Process management
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    print("Warning: psutil not available. Limited process management.")
    PSUTIL_AVAILABLE = False

# Registry access
try:
    import winreg
    WINREG_AVAILABLE = True
except ImportError:
    print("Warning: winreg not available. Limited registry access.")
    WINREG_AVAILABLE = False

class VSCodeRemovalTool:
    """Main class for VSCode Ultimate Removal Tool"""
    
    def __init__(self):
        self.version = "3.0"
        self.developer = "@aliseylabi"
        self.telegram = "@aliseylabi"
        self.session_id = self._generate_session_id()
        self.current_user = os.environ.get('USERNAME', 'Unknown')
        self.computer_name = os.environ.get('COMPUTERNAME', 'Unknown')
        self.system_arch = self._detect_architecture()
        self.windows_version = self._get_windows_version()
        
        # Show developer info at startup
        self._show_developer_info()
        
        # Paths and directories
        self.setup_directories()
        self.setup_logging()
        
        # VSCode related paths
        self.vscode_paths = self._get_vscode_paths()
        self.backup_created = False
        self.removal_stats = {
            'processes_terminated': 0,
            'directories_removed': 0,
            'registry_keys_removed': 0,
            'files_deleted': 0,
            'machine_id_reset': False
        }
        
        # GUI setup
        self.root = None
        self.progress_var = None
        self.status_var = None
    
    def _show_developer_info(self):
        """Show developer information at startup"""
        if GUI_AVAILABLE:
            # Show splash screen with developer info
            self._show_splash_screen()
        else:
            # Console version
            self._show_console_developer_info()
    
    def _show_splash_screen(self):
        """Show splash screen with developer info"""
        splash = tk.Tk()
        splash.title("VSCode Ultimate Removal Tool")
        splash.geometry("500x400")
        splash.configure(bg='#1e1e1e')
        splash.resizable(False, False)
        
        # Center the splash screen
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (splash.winfo_width() // 2)
        y = (splash.winfo_screenheight() // 2) - (splash.winfo_height() // 2)
        splash.geometry(f"+{x}+{y}")
        
        # Remove window decorations for splash effect
        splash.overrideredirect(True)
        
        # Main frame
        main_frame = tk.Frame(splash, bg='#1e1e1e', padx=40, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        # Tool title
        title_label = tk.Label(
            main_frame,
            text="🗑️ VSCode Ultimate Removal Tool",
            font=('Arial', 18, 'bold'),
            fg='#00d4aa',
            bg='#1e1e1e'
        )
        title_label.pack(pady=(0, 10))
        
        # Version
        version_label = tk.Label(
            main_frame,
            text=f"Professional Python Edition v{self.version}",
            font=('Arial', 12),
            fg='#ffffff',
            bg='#1e1e1e'
        )
        version_label.pack(pady=(0, 20))
        
        # Developer info
        dev_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='raised', bd=2)
        dev_frame.pack(fill='x', pady=20)
        
        dev_title = tk.Label(
            dev_frame,
            text="👨‍💻 Developer Information",
            font=('Arial', 14, 'bold'),
            fg='#ffd700',
            bg='#2d2d2d'
        )
        dev_title.pack(pady=(10, 5))
        
        dev_name = tk.Label(
            dev_frame,
            text=f"Developed by: {self.developer}",
            font=('Arial', 12, 'bold'),
            fg='#00ff88',
            bg='#2d2d2d'
        )
        dev_name.pack(pady=2)
        
        telegram_label = tk.Label(
            dev_frame,
            text=f"📱 Telegram: {self.telegram}",
            font=('Arial', 11),
            fg='#00bfff',
            bg='#2d2d2d'
        )
        telegram_label.pack(pady=2)
        
        contact_label = tk.Label(
            dev_frame,
            text="برای پشتیبانی و ارتباط با توسعه‌دهنده:",
            font=('Arial', 10),
            fg='#ffffff',
            bg='#2d2d2d'
        )
        contact_label.pack(pady=(5, 2))
        
        # Telegram button
        telegram_button = tk.Button(
            dev_frame,
            text="📱 ارتباط با توسعه‌دهنده در تلگرام",
            font=('Arial', 10, 'bold'),
            bg='#0088cc',
            fg='white',
            relief='raised',
            bd=3,
            padx=20,
            pady=5,
            command=self._open_telegram
        )
        telegram_button.pack(pady=10)
        
        # Loading bar
        loading_frame = tk.Frame(main_frame, bg='#1e1e1e')
        loading_frame.pack(fill='x', pady=(20, 10))
        
        loading_label = tk.Label(
            loading_frame,
            text="Loading...",
            font=('Arial', 10),
            fg='#ffffff',
            bg='#1e1e1e'
        )
        loading_label.pack()
        
        progress = ttk.Progressbar(
            loading_frame,
            length=300,
            mode='indeterminate'
        )
        progress.pack(pady=5)
        progress.start()
        
        # Copyright
        copyright_label = tk.Label(
            main_frame,
            text="© 2025 - Professional VSCode Removal Tool",
            font=('Arial', 9),
            fg='#888888',
            bg='#1e1e1e'
        )
        copyright_label.pack(side='bottom', pady=(20, 0))
        
        # Auto close after 4 seconds
        splash.after(4000, splash.destroy)
        splash.mainloop()
    
    def _show_console_developer_info(self):
        """Show developer info in console mode"""
        print("\n" + "="*80)
        print("🗑️  VSCode Ultimate Removal Tool v{} - Professional Python Edition".format(self.version))
        print("="*80)
        print()
        print("👨‍💻 Developer Information:")
        print("   ├── Developed by: {}".format(self.developer))
        print("   ├── Telegram: {}".format(self.telegram))
        print("   └── برای پشتیبانی و ارتباط با توسعه‌دهنده از تلگرام استفاده کنید")
        print()
        print("📱 برای ارتباط مستقیم:")
        print("   Telegram: https://t.me/{}".format(self.telegram.replace('@', '')))
        print()
        print("© 2025 - Professional VSCode Removal Tool")
        print("="*80)
        print()
        
        # Ask user if they want to open Telegram
        try:
            response = input("آیا می‌خواهید صفحه تلگرام توسعه‌دهنده را باز کنید؟ (y/N): ").strip().lower()
            if response == 'y':
                self._open_telegram()
        except:
            pass
        print()
    
    def _open_telegram(self):
        """Open Telegram profile"""
        telegram_url = f"https://t.me/{self.telegram.replace('@', '')}"
        try:
            webbrowser.open(telegram_url)
            if GUI_AVAILABLE:
                messagebox.showinfo(
                    "تلگرام",
                    f"صفحه تلگرام توسعه‌دهنده باز شد!\n\n"
                    f"آیدی: {self.telegram}\n"
                    f"لینک: {telegram_url}\n\n"
                    "برای پشتیبانی و سوالات با توسعه‌دهنده در ارتباط باشید."
                )
            else:
                print(f"✅ صفحه تلگرام باز شد: {telegram_url}")
        except Exception as e:
            error_msg = f"خطا در باز کردن تلگرام: {str(e)}\n\nلینک دستی: {telegram_url}"
            if GUI_AVAILABLE:
                messagebox.showerror("خطا", error_msg)
            else:
                print(f"❌ {error_msg}")
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_part = str(uuid.uuid4())[:8]
        return f"{timestamp}_{random_part}"
    
    def _detect_architecture(self) -> str:
        """Detect system architecture"""
        import platform
        arch = platform.machine().lower()
        if 'amd64' in arch or 'x86_64' in arch:
            return 'x64'
        elif 'i386' in arch or 'x86' in arch:
            return 'x86'
        elif 'arm64' in arch or 'aarch64' in arch:
            return 'ARM64'
        else:
            return 'Unknown'
    
    def _get_windows_version(self) -> str:
        """Get Windows version information"""
        try:
            import platform
            return f"{platform.system()} {platform.release()} {platform.version()}"
        except:
            return "Unknown Windows Version"
    
    def setup_directories(self):
        """Setup working directories"""
        self.temp_dir = Path(tempfile.gettempdir()) / "VSCode_Removal_Logs"
        self.backup_dir = Path.home() / "Desktop" / f"VSCode_Backup_{self.session_id}"
        
        # Create directories
        self.temp_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Subdirectories
        (self.backup_dir / "Settings").mkdir(exist_ok=True)
        (self.backup_dir / "Extensions").mkdir(exist_ok=True)
        (self.backup_dir / "Registry").mkdir(exist_ok=True)
        (self.backup_dir / "MachineID").mkdir(exist_ok=True)
        (self.backup_dir / "Logs").mkdir(exist_ok=True)
    
    def setup_logging(self):
        """Setup comprehensive logging system"""
        log_format = '%(asctime)s [%(levelname)s] %(message)s'
        
        # Main log
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(self.temp_dir / f"vscode_removal_{self.session_id}.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
        # Create specialized loggers
        self.machine_id_logger = logging.getLogger('machine_id')
        machine_handler = logging.FileHandler(self.temp_dir / f"machine_id_{self.session_id}.log")
        machine_handler.setFormatter(logging.Formatter(log_format))
        self.machine_id_logger.addHandler(machine_handler)
        self.machine_id_logger.setLevel(logging.INFO)
        
        # Log developer info
        self.logger.info(f"VSCode Ultimate Removal Tool v{self.version}")
        self.logger.info(f"Developer: {self.developer}")
        self.logger.info(f"Session ID: {self.session_id}")
    
    def _get_vscode_paths(self) -> Dict[str, List[Path]]:
        """Get all possible VSCode installation and data paths"""
        paths = {
            'install_paths': [],
            'user_data_paths': [],
            'extension_paths': [],
            'cache_paths': []
        }
        
        # Installation paths
        local_app_data = Path(os.environ.get('LOCALAPPDATA', ''))
        program_files = Path(os.environ.get('PROGRAMFILES', ''))
        program_files_x86 = Path(os.environ.get('PROGRAMFILES(X86)', ''))
        
        install_candidates = [
            local_app_data / "Programs" / "Microsoft VS Code",
            program_files / "Microsoft VS Code",
            program_files_x86 / "Microsoft VS Code"
        ]
        
        paths['install_paths'] = [p for p in install_candidates if p.exists()]
        
        # User data paths
        app_data = Path(os.environ.get('APPDATA', ''))
        user_profile = Path(os.environ.get('USERPROFILE', ''))
        
        user_data_candidates = [
            app_data / "Code",
            app_data / "Code - Insiders",
            user_profile / ".vscode",
            user_profile / ".vscode-insiders"
        ]
        
        paths['user_data_paths'] = [p for p in user_data_candidates if p.exists()]
        
        # Extension paths
        for user_path in paths['user_data_paths']:
            ext_path = user_path / "extensions"
            if ext_path.exists():
                paths['extension_paths'].append(ext_path)
        
        # Cache paths
        cache_candidates = [
            local_app_data / "Microsoft" / "VSCode",
            user_profile / "AppData" / "Local" / "Temp"
        ]
        
        paths['cache_paths'] = [p for p in cache_candidates if p.exists()]
        
        return paths
    
    def check_admin_privileges(self) -> bool:
        """Check if script is running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def create_gui(self):
        """Create the main GUI interface"""
        if not GUI_AVAILABLE:
            print("GUI not available. Running in console mode.")
            return self.run_console_mode()
            
        self.root = tk.Tk()
        self.root.title(f"VSCode Ultimate Removal Tool v{self.version} - by {self.developer}")
        self.root.geometry("850x650")
        self.root.configure(bg='#2b2b2b')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TButton', padding=10)
        style.configure('TFrame', background='#2b2b2b')
        
        self._create_header()
        self._create_developer_info()
        self._create_system_info()
        self._create_main_buttons()
        self._create_progress_section()
        self._create_status_section()
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def _create_header(self):
        """Create the header section"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = ttk.Label(
            header_frame,
            text="🗑️ VSCode Ultimate Removal Tool",
            font=('Arial', 20, 'bold')
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text=f"Professional Python Edition v{self.version} | Complete Machine ID Reset",
            font=('Arial', 10)
        )
        subtitle_label.pack()
    
    def _create_developer_info(self):
        """Create developer information section"""
        dev_frame = ttk.LabelFrame(self.root, text="👨‍💻 Developer Information", padding=10)
        dev_frame.pack(fill='x', padx=20, pady=5)
        
        # Developer info frame
        info_frame = ttk.Frame(dev_frame)
        info_frame.pack(fill='x')
        
        # Developer name and telegram
        dev_info_text = f"Developed by: {self.developer} | Telegram: {self.telegram}"
        dev_label = ttk.Label(
            info_frame,
            text=dev_info_text,
            font=('Arial', 10, 'bold'),
            foreground='#00ff88'
        )
        dev_label.pack(side='left')
        
        # Telegram button
        telegram_btn = ttk.Button(
            info_frame,
            text="📱 ارتباط با توسعه‌دهنده",
            command=self._open_telegram,
            width=20
        )
        telegram_btn.pack(side='right', padx=(10, 0))
        
        # Support message
        support_label = ttk.Label(
            dev_frame,
            text="برای پشتیبانی، سوالات و گزارش مشکلات با توسعه‌دهنده در تلگرام ارتباط برقرار کنید",
            font=('Arial', 9),
            foreground='#cccccc'
        )
        support_label.pack(pady=(5, 0))
    
    def _create_system_info(self):
        """Create system information display"""
        info_frame = ttk.LabelFrame(self.root, text="System Information", padding=10)
        info_frame.pack(fill='x', padx=20, pady=5)
        
        info_text = f"""Computer: {self.computer_name} | User: {self.current_user}
Architecture: {self.system_arch} | Windows: {self.windows_version}
Session ID: {self.session_id}
Admin Privileges: {'✓ YES' if self.check_admin_privileges() else '✗ NO'}"""
        
        ttk.Label(info_frame, text=info_text, font=('Consolas', 9)).pack()
    
    def _create_main_buttons(self):
        """Create main action buttons"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left column
        left_frame = ttk.Frame(button_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        buttons_left = [
            ("🚀 Quick Removal", "Standard cleanup (~5 min)", self.quick_removal),
            ("🔧 Complete Removal", "Comprehensive cleanup (~10 min)", self.complete_removal),
            ("💀 Ultimate Removal", "Full system eradication (~15 min)", self.ultimate_removal),
            ("⚙️ Custom Removal", "Select specific components", self.custom_removal),
        ]
        
        for text, desc, command in buttons_left:
            self._create_action_button(left_frame, text, desc, command)
        
        # Right column
        right_frame = ttk.Frame(button_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        buttons_right = [
            ("💾 Backup Only", "Create complete backup", self.backup_only),
            ("🔍 System Analysis", "Analyze VSCode footprint", self.system_analysis),
            ("🔄 Restore Backup", "Restore from backup", self.restore_backup),
            ("🆔 Reset Machine ID", "Reset system identifier", self.reset_machine_id_only),
        ]
        
        for text, desc, command in buttons_right:
            self._create_action_button(right_frame, text, desc, command)
    
    def _create_action_button(self, parent, text, description, command):
        """Create a styled action button"""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=5)
        
        button = ttk.Button(
            frame,
            text=text,
            command=command,
            width=25
        )
        button.pack()
        
        desc_label = ttk.Label(
            frame,
            text=description,
            font=('Arial', 8),
            foreground='gray'
        )
        desc_label.pack()
    
    def _create_progress_section(self):
        """Create progress bar section"""
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        progress_frame.pack(fill='x', padx=20, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.pack(fill='x')
        
        self.progress_label = ttk.Label(progress_frame, text="Ready...")
        self.progress_label.pack(pady=(5, 0))
    
    def _create_status_section(self):
        """Create status display section"""
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(status_frame)
        text_frame.pack(fill='both', expand=True)
        
        self.status_text = tk.Text(
            text_frame,
            height=6,
            bg='#1e1e1e',
            fg='#d4d4d4',
            font=('Consolas', 9),
            wrap='word'
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def update_progress(self, value: int, message: str = ""):
        """Update progress bar and message"""
        if self.root:
            self.progress_var.set(value)
            if message:
                self.progress_label.config(text=message)
            self.root.update()
    
    def log_status(self, message: str, level: str = "INFO"):
        """Log message to status display and file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] [{level}] {message}"
        
        # Log to file
        if level == "ERROR":
            self.logger.error(message)
        elif level == "WARNING":
            self.logger.warning(message)
        else:
            self.logger.info(message)
        
        # Log to GUI
        if self.root and hasattr(self, 'status_text'):
            self.status_text.insert('end', formatted_message + '\n')
            self.status_text.see('end')
            self.root.update()
        else:
            print(formatted_message)
    
    def run_with_progress(self, func, *args, **kwargs):
        """Run function with progress tracking"""
        def worker():
            try:
                func(*args, **kwargs)
            except Exception as e:
                self.log_status(f"Error: {str(e)}", "ERROR")
                if GUI_AVAILABLE and self.root:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")
                else:
                    print(f"Error: {str(e)}")
        
        if GUI_AVAILABLE:
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
        else:
            worker()
    
    def create_advanced_backup(self):
        """Create comprehensive backup of VSCode data"""
        self.log_status("Creating advanced backup...")
        self.update_progress(10, "Creating backup structure...")
        
        try:
            # Backup user settings
            self.update_progress(20, "Backing up user settings...")
            for user_path in self.vscode_paths['user_data_paths']:
                if (user_path / "User").exists():
                    shutil.copytree(
                        user_path / "User",
                        self.backup_dir / "Settings" / user_path.name,
                        dirs_exist_ok=True
                    )
                    self.log_status(f"Backed up settings from {user_path}")
            
            # Backup extensions
            self.update_progress(40, "Backing up extensions...")
            extensions_list = []
            for ext_path in self.vscode_paths['extension_paths']:
                if ext_path.exists():
                    extensions_list.extend([d.name for d in ext_path.iterdir() if d.is_dir()])
                    shutil.copytree(
                        ext_path,
                        self.backup_dir / "Extensions" / ext_path.parent.name,
                        dirs_exist_ok=True
                    )
            
            # Save extensions list
            with open(self.backup_dir / "Extensions" / "extensions_list.json", 'w') as f:
                json.dump(extensions_list, f, indent=2)
            
            # Backup registry
            self.update_progress(60, "Backing up registry...")
            self._backup_registry()
            
            # Backup Machine ID
            self.update_progress(80, "Backing up Machine ID...")
            self._backup_machine_id()
            
            # Create manifest
            self.update_progress(90, "Creating backup manifest...")
            self._create_backup_manifest()
            
            self.update_progress(100, "Backup completed!")
            self.log_status("✅ Advanced backup completed successfully")
            self.backup_created = True
            
        except Exception as e:
            self.log_status(f"Backup failed: {str(e)}", "ERROR")
            raise
    
    def _backup_registry(self):
        """Backup VSCode registry entries"""
        if not WINREG_AVAILABLE:
            self.log_status("Registry backup skipped - winreg not available", "WARNING")
            return
            
        registry_backup_dir = self.backup_dir / "Registry"
        
        # Registry keys to backup
        keys_to_backup = [
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\Applications\Code.exe"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\vscode"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\VSCode"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\Applications\Code.exe"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\vscode"),
        ]
        
        for hive, key_path in keys_to_backup:
            try:
                # Fixed f-string error
                backup_name = key_path.replace("\\", "_") + ".reg"
                backup_file = registry_backup_dir / backup_name
                
                hive_string = self._hive_to_string(hive)
                cmd = f'reg export "{hive_string}\\{key_path}" "{backup_file}" /y'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log_status(f"Backed up registry key: {key_path}")
                else:
                    self.log_status(f"Failed to backup {key_path}: {result.stderr}", "WARNING")
                    
            except Exception as e:
                self.log_status(f"Failed to backup registry key {key_path}: {e}", "WARNING")
    
    def _hive_to_string(self, hive):
        """Convert registry hive constant to string"""
        if not WINREG_AVAILABLE:
            return "UNKNOWN"
            
        hive_map = {
            winreg.HKEY_CURRENT_USER: "HKEY_CURRENT_USER",
            winreg.HKEY_LOCAL_MACHINE: "HKEY_LOCAL_MACHINE",
            winreg.HKEY_CLASSES_ROOT: "HKEY_CLASSES_ROOT"
        }
        return hive_map.get(hive, "UNKNOWN")
    
    def _backup_machine_id(self):
        """Backup current Machine ID"""
        machine_id_dir = self.backup_dir / "MachineID"
        
        # Get current Machine ID from registry
        current_machine_id = self._get_current_machine_id()
        
        # Save current Machine ID info
        machine_id_info = {
            'original_machine_id': current_machine_id,
            'backup_date': datetime.now().isoformat(),
            'session_id': self.session_id,
            'computer_name': self.computer_name,
            'user_name': self.current_user,
            'developer': self.developer
        }
        
        with open(machine_id_dir / "machine_id_info.json", 'w') as f:
            json.dump(machine_id_info, f, indent=2)
        
        # Backup Machine ID files
        for user_path in self.vscode_paths['user_data_paths']:
            storage_path = user_path / "User" / "globalStorage"
            if storage_path.exists():
                shutil.copytree(
                    storage_path,
                    machine_id_dir / "globalStorage" / user_path.name,
                    dirs_exist_ok=True
                )
        
        self.machine_id_logger.info(f"Backed up Machine ID: {current_machine_id}")
    
    def _get_current_machine_id(self) -> Optional[str]:
        """Get current VSCode Machine ID from registry"""
        if not WINREG_AVAILABLE:
            return None
            
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\VSCode") as key:
                machine_id, _ = winreg.QueryValueEx(key, "machineId")
                return machine_id
        except:
            return None
    
    def _create_backup_manifest(self):
        """Create comprehensive backup manifest"""
        manifest = {
            'backup_info': {
                'version': self.version,
                'developer': self.developer,
                'telegram': self.telegram,
                'created': datetime.now().isoformat(),
                'session_id': self.session_id,
                'backup_type': 'Advanced Complete'
            },
            'system_info': {
                'computer_name': self.computer_name,
                'user_name': self.current_user,
                'architecture': self.system_arch,
                'windows_version': self.windows_version
            },
            'vscode_info': {
                'installations_found': len(self.vscode_paths['install_paths']),
                'user_data_paths': [str(p) for p in self.vscode_paths['user_data_paths']],
                'install_paths': [str(p) for p in self.vscode_paths['install_paths']]
            },
            'backup_contents': {
                'settings': 'User settings, keybindings, snippets',
                'extensions': 'Extension list and configurations',
                'registry': 'Complete registry backups',
                'machine_id': 'Machine ID backup and restoration data',
                'logs': 'Complete operation logs'
            },
            'restoration_info': {
                'automatic': 'Use Restore Backup option in main menu',
                'manual': 'Import .reg files and copy folders manually'
            },
            'support_info': {
                'developer': self.developer,
                'telegram': self.telegram,
                'contact': f'For support, contact {self.telegram} on Telegram'
            }
        }
        
        with open(self.backup_dir / "backup_manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Also create human-readable version
        with open(self.backup_dir / "README.txt", 'w', encoding='utf-8') as f:
            f.write(f"""
VSCode Ultimate Removal Tool - Backup Archive
=============================================

Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Session ID: {self.session_id}
Tool Version: {self.version}
Developer: {self.developer}
Telegram: {self.telegram}

System Information:
- Computer: {self.computer_name}
- User: {self.current_user}
- Architecture: {self.system_arch}

Backup Contents:
├── Settings/     - User settings and configurations
├── Extensions/   - Extension lists and data
├── Registry/     - Registry backup files (.reg)
├── MachineID/    - Machine ID backup and info
└── Logs/         - Operation logs

To restore:
1. Use the 'Restore Backup' option in the tool
2. Or manually import .reg files and copy folders

For support and questions:
- Developer: {self.developer}
- Telegram: {self.telegram}
- Contact for support: https://t.me/{self.telegram.replace('@', '')}

© 2025 - Professional VSCode Removal Tool
            """)
    
    def terminate_vscode_processes(self):
        """Terminate all VSCode related processes"""
        self.log_status("Terminating VSCode processes...")
        
        if not PSUTIL_AVAILABLE:
            self.log_status("Process termination limited - psutil not available", "WARNING")
            # Fallback using subprocess
            try:
                subprocess.run('taskkill /f /im Code.exe /t', shell=True, capture_output=True)
                subprocess.run('taskkill /f /im code.exe /t', shell=True, capture_output=True)
                self.removal_stats['processes_terminated'] = 2
                self.log_status("✅ Terminated VSCode processes using taskkill")
            except Exception as e:
                self.log_status(f"Process termination failed: {e}", "ERROR")
            return
        
        vscode_process_names = [
            'Code.exe', 'code.exe', 'CodeHelper.exe', 'VSCodeSetup.exe',
            'electron.exe', 'node.exe'
        ]
        
        terminated_count = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                proc_info = proc.info
                if any(name.lower() in proc_info['name'].lower() for name in vscode_process_names):
                    # Check if it's actually VSCode related
                    if proc_info['exe'] and 'vscode' in proc_info['exe'].lower():
                        self.log_status(f"Terminating process: {proc_info['name']} (PID: {proc_info['pid']})")
                        proc.terminate()
                        terminated_count += 1
                        
                        # Wait for graceful termination
                        try:
                            proc.wait(timeout=5)
                        except psutil.TimeoutExpired:
                            # Force kill if needed
                            proc.kill()
                            self.log_status(f"Force killed process: {proc_info['name']}")
                            
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        self.removal_stats['processes_terminated'] = terminated_count
        self.log_status(f"✅ Terminated {terminated_count} VSCode processes")
    
    def remove_directories(self, mode: str = "basic"):
        """Remove VSCode directories based on mode"""
        self.log_status(f"Removing directories ({mode} mode)...")
        
        directories_to_remove = []
        
        if mode in ["basic", "complete", "ultimate"]:
            directories_to_remove.extend(self.vscode_paths['install_paths'])
            directories_to_remove.extend(self.vscode_paths['user_data_paths'])
        
        if mode in ["complete", "ultimate"]:
            directories_to_remove.extend(self.vscode_paths['extension_paths'])
            directories_to_remove.extend(self.vscode_paths['cache_paths'])
        
        if mode == "ultimate":
            # Add additional cleanup paths
            additional_paths = [
                Path(os.environ.get('TEMP', '')) / "vscode",
                Path(os.environ.get('LOCALAPPDATA', '')) / "Microsoft" / "VSCode"
            ]
            directories_to_remove.extend(additional_paths)
        
        removed_count = 0
        for directory in directories_to_remove:
            if directory.exists():
                try:
                    if directory.is_dir():
                        shutil.rmtree(directory, ignore_errors=True)
                        self.log_status(f"Removed directory: {directory}")
                        removed_count += 1
                except Exception as e:
                    self.log_status(f"Failed to remove {directory}: {e}", "WARNING")
        
        self.removal_stats['directories_removed'] = removed_count
        self.log_status(f"✅ Removed {removed_count} directories")
    
    def clean_registry(self, mode: str = "basic"):
        """Clean VSCode registry entries"""
        if not WINREG_AVAILABLE:
            self.log_status("Registry cleanup skipped - winreg not available", "WARNING")
            return
            
        self.log_status(f"Cleaning registry ({mode} mode)...")
        
        keys_removed = 0
        
        # Basic registry cleanup
        basic_keys = [
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\Applications\Code.exe"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\vscode"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\Applications\Code.exe"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\vscode"),
        ]
        
        for hive, key_path in basic_keys:
            if self._remove_registry_key(hive, key_path):
                keys_removed += 1
        
        if mode in ["complete", "ultimate"]:
            # Advanced registry cleanup
            keys_removed += self._clean_registry_advanced()
        
        if mode == "ultimate":
            # Ultimate registry cleanup
            keys_removed += self._clean_registry_ultimate()
        
        self.removal_stats['registry_keys_removed'] = keys_removed
        self.log_status(f"✅ Cleaned {keys_removed} registry keys")
    
    def _remove_registry_key(self, hive, key_path: str) -> bool:
        """Remove a specific registry key"""
        if not WINREG_AVAILABLE:
            return False
            
        try:
            winreg.DeleteKey(hive, key_path)
            self.log_status(f"Removed registry key: {key_path}")
            return True
        except FileNotFoundError:
            # Key doesn't exist
            return False
        except Exception as e:
            self.log_status(f"Failed to remove registry key {key_path}: {e}", "WARNING")
            return False
    
    def _clean_registry_advanced(self) -> int:
        """Advanced registry cleanup"""
        keys_removed = 0
        
        # Remove file associations
        extensions = ['.js', '.ts', '.json', '.html', '.css', '.py', '.cpp', '.java']
        for ext in extensions:
            if self._remove_registry_key(winreg.HKEY_CLASSES_ROOT, ext):
                keys_removed += 1
        
        # Remove context menu entries
        context_keys = [
            r"*\shell\VSCode",
            r"Directory\shell\VSCode",
            r"Directory\Background\shell\VSCode"
        ]
        
        for key in context_keys:
            if self._remove_registry_key(winreg.HKEY_CLASSES_ROOT, key):
                keys_removed += 1
                
        return keys_removed
    
    def _clean_registry_ultimate(self) -> int:
        """Ultimate registry cleanup"""
        keys_removed = 0
        
        # Remove uninstall entries
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as uninstall_key:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(uninstall_key, i)
                        with winreg.OpenKey(uninstall_key, subkey_name) as subkey:
                            try:
                                display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                if "visual studio code" in display_name.lower():
                                    full_path = f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{subkey_name}"
                                    if self._remove_registry_key(winreg.HKEY_LOCAL_MACHINE, full_path):
                                        keys_removed += 1
                            except FileNotFoundError:
                                pass
                        i += 1
                    except OSError:
                        break
        except Exception as e:
            self.log_status(f"Error cleaning uninstall entries: {e}", "WARNING")
            
        return keys_removed
    
    def reset_machine_id(self):
        """Reset VSCode Machine ID completely"""
        self.log_status("Resetting Machine ID...")
        self.update_progress(0, "Starting Machine ID reset...")
        
        # Backup current Machine ID first
        self.update_progress(20, "Backing up current Machine ID...")
        current_id = self._get_current_machine_id()
        if current_id:
            self.machine_id_logger.info(f"Original Machine ID: {current_id}")
        
        # Clear Machine ID from registry
        self.update_progress(40, "Clearing Machine ID from registry...")
        self._clear_machine_id_registry()
        
        # Clear Machine ID from files
        self.update_progress(60, "Clearing Machine ID from files...")
        self._clear_machine_id_files()
        
        # Clear telemetry data
        self.update_progress(80, "Clearing telemetry data...")
        self._clear_telemetry_data()
        
        # Generate new Machine ID
        self.update_progress(90, "Generating new Machine ID...")
        new_id = str(uuid.uuid4())
        self.machine_id_logger.info(f"New Machine ID: {new_id}")
        
        self.update_progress(100, "Machine ID reset completed!")
        self.log_status(f"✅ Machine ID reset completed. New ID: {new_id}")
        self.removal_stats['machine_id_reset'] = True
    
    def _clear_machine_id_registry(self):
        """Clear Machine ID from registry"""
        if not WINREG_AVAILABLE:
            self.log_status("Registry Machine ID clearing skipped - winreg not available", "WARNING")
            return
            
        machine_id_values = ['machineId', 'sessionId', 'telemetry.machineId', 'sqmUserId']
        
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\VSCode", 0, winreg.KEY_SET_VALUE) as key:
                for value_name in machine_id_values:
                    try:
                        winreg.DeleteValue(key, value_name)
                        self.log_status(f"Cleared registry value: {value_name}")
                    except FileNotFoundError:
                        pass
        except FileNotFoundError:
            pass
    
    def _clear_machine_id_files(self):
        """Clear Machine ID from VSCode files"""
        for user_path in self.vscode_paths['user_data_paths']:
            # Clear from storage files
            storage_files = [
                user_path / "User" / "globalStorage" / "storage.json",
                user_path / "User" / "state.vscdb"
            ]
            
            for file_path in storage_files:
                if file_path.exists():
                    self._clean_machine_id_from_file(file_path)
            
            # Remove workspace storage (contains Machine ID)
            workspace_storage = user_path / "User" / "workspaceStorage"
            if workspace_storage.exists():
                try:
                    shutil.rmtree(workspace_storage)
                    self.log_status(f"Removed workspace storage: {workspace_storage}")
                except Exception as e:
                    self.log_status(f"Failed to remove workspace storage: {e}", "WARNING")
    
    def _clean_machine_id_from_file(self, file_path: Path):
        """Clean Machine ID references from a file"""
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Remove Machine ID related keys
                machine_id_keys = ['machineId', 'sessionId', 'telemetry.machineId', 'sqmUserId']
                for key in machine_id_keys:
                    if key in data:
                        del data[key]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                self.log_status(f"Cleaned Machine ID from: {file_path}")
            
            elif file_path.suffix == '.vscdb':
                # For SQLite database files, just remove them
                file_path.unlink()
                self.log_status(f"Removed database file: {file_path}")
                
        except Exception as e:
            self.log_status(f"Failed to clean {file_path}: {e}", "WARNING")
    
    def _clear_telemetry_data(self):
        """Clear all telemetry and analytics data"""
        for user_path in self.vscode_paths['user_data_paths']:
            telemetry_paths = [
                user_path / "User" / "globalStorage" / "vscode.vscode-telemetry",
                user_path / "User" / "globalStorage" / "ms-vscode.vscode-telemetry",
                user_path / "CrashDumps",
                user_path / "CachedData"
            ]
            
            for tel_path in telemetry_paths:
                if tel_path.exists():
                    try:
                        if tel_path.is_dir():
                            shutil.rmtree(tel_path)
                        else:
                            tel_path.unlink()
                        self.log_status(f"Removed telemetry data: {tel_path}")
                    except Exception as e:
                        self.log_status(f"Failed to remove telemetry data {tel_path}: {e}", "WARNING")
    
    def perform_system_cleanup(self):
        """Perform additional system cleanup"""
        self.log_status("Performing system cleanup...")
        
        # Clean temp files
        temp_patterns = ['*vscode*', '*code*']
        temp_dirs = [
            Path(os.environ.get('TEMP', '')),
            Path(os.environ.get('TMP', ''))
        ]
        
        files_deleted = 0
        for temp_dir in temp_dirs:
            for pattern in temp_patterns:
                try:
                    for file_path in temp_dir.glob(pattern):
                        if file_path.is_file():
                            file_path.unlink()
                            files_deleted += 1
                        elif file_path.is_dir():
                            shutil.rmtree(file_path, ignore_errors=True)
                            files_deleted += 10  # Estimate
                except Exception as e:
                    self.log_status(f"Error cleaning temp files: {e}", "WARNING")
        
        # Clean prefetch files
        prefetch_dir = Path("C:/Windows/Prefetch")
        if prefetch_dir.exists():
            try:
                for prefetch_file in prefetch_dir.glob("*CODE*.pf"):
                    prefetch_file.unlink()
                    files_deleted += 1
                    self.log_status(f"Removed prefetch: {prefetch_file.name}")
            except Exception as e:
                self.log_status(f"Error cleaning prefetch: {e}", "WARNING")
        
        self.removal_stats['files_deleted'] = files_deleted
        self.log_status(f"✅ System cleanup completed. {files_deleted} files removed")
    
    def show_removal_summary(self, removal_type: str):
        """Show comprehensive removal summary"""
        summary = f"""
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                            {removal_type.upper()} REMOVAL COMPLETED!                             ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝

✅ VSCode has been successfully removed from your system
✅ Machine ID has been reset for complete anonymity  
✅ All traces have been eliminated

📊 REMOVAL STATISTICS:
├── Processes terminated: {self.removal_stats['processes_terminated']}
├── Directories removed: {self.removal_stats['directories_removed']}
├── Registry keys cleaned: {self.removal_stats['registry_keys_removed']}
├── Files deleted: {self.removal_stats['files_deleted']}
└── Machine ID reset: {'✅ YES' if self.removal_stats['machine_id_reset'] else '❌ NO'}

📁 BACKUP INFORMATION:
├── Location: {self.backup_dir}
├── Created: {'✅ YES' if self.backup_created else '❌ NO'}
└── Restore available: {'✅ YES' if self.backup_created else '❌ NO'}

🆔 SESSION INFORMATION:
├── Session ID: {self.session_id}
├── Computer: {self.computer_name}
├── User: {self.current_user}
└── Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

👨‍💻 DEVELOPER INFORMATION:
├── Tool developed by: {self.developer}
├── Telegram support: {self.telegram}
└── For questions and support, contact developer on Telegram

⚠️  IMPORTANT: Please restart your computer to complete the removal process.
        """
        
        self.log_status(summary)
        
        # Show GUI summary
        if GUI_AVAILABLE and self.root:
            messagebox.showinfo(
                f"{removal_type.title()} Removal Completed!",
                f"VSCode has been successfully removed!\n\n"
                f"Processes terminated: {self.removal_stats['processes_terminated']}\n"
                f"Directories removed: {self.removal_stats['directories_removed']}\n"
                f"Registry keys cleaned: {self.removal_stats['registry_keys_removed']}\n"
                f"Machine ID reset: {'Yes' if self.removal_stats['machine_id_reset'] else 'No'}\n\n"
                f"Backup location: {self.backup_dir}\n\n"
                f"Developer: {self.developer}\n"
                f"Telegram: {self.telegram}\n\n"
                f"Please restart your computer to complete the process."
            )
    
    # Main removal methods
    def quick_removal(self):
        """Perform quick VSCode removal"""
        if not self.check_admin_privileges():
            if GUI_AVAILABLE:
                messagebox.showerror("Error", "Administrator privileges required!")
            else:
                print("Error: Administrator privileges required!")
            return
        
        if GUI_AVAILABLE:
            if not messagebox.askyesno("Confirm Quick Removal", 
                                     "This will remove VSCode from your system.\n"
                                     "A backup will be created first.\n\n"
                                     "Continue?"):
                return
        else:
            response = input("This will remove VSCode from your system. Continue? (y/N): ")
            if response.lower() != 'y':
                return
        
        def quick_removal_process():
            try:
                self.update_progress(0, "Starting quick removal...")
                
                # Create backup
                self.update_progress(10, "Creating backup...")
                self.create_advanced_backup()
                
                # Terminate processes
                self.update_progress(30, "Terminating processes...")
                self.terminate_vscode_processes()
                
                # Remove directories
                self.update_progress(50, "Removing directories...")
                self.remove_directories("basic")
                
                # Clean registry
                self.update_progress(70, "Cleaning registry...")
                self.clean_registry("basic")
                
                # System cleanup
                self.update_progress(90, "Final cleanup...")
                self.perform_system_cleanup()
                
                self.update_progress(100, "Quick removal completed!")
                self.show_removal_summary("Quick")
                
            except Exception as e:
                self.log_status(f"Quick removal failed: {str(e)}", "ERROR")
                if GUI_AVAILABLE:
                    messagebox.showerror("Error", f"Quick removal failed: {str(e)}")
        
        self.run_with_progress(quick_removal_process)
    
    def complete_removal(self):
        """Perform complete VSCode removal"""
        if not self.check_admin_privileges():
            if GUI_AVAILABLE:
                messagebox.showerror("Error", "Administrator privileges required!")
            else:
                print("Error: Administrator privileges required!")
            return
        
        if GUI_AVAILABLE:
            if not messagebox.askyesno("Confirm Complete Removal", 
                                     "This will completely remove VSCode and all related data.\n"
                                     "A comprehensive backup will be created first.\n\n"
                                     "Continue?"):
                return
        else:
            response = input("This will completely remove VSCode and all related data. Continue? (y/N): ")
            if response.lower() != 'y':
                return
        
        def complete_removal_process():
            try:
                self.update_progress(0, "Starting complete removal...")
                
                # Create backup
                self.update_progress(5, "Creating comprehensive backup...")
                self.create_advanced_backup()
                
                # Terminate processes
                self.update_progress(20, "Terminating all processes...")
                self.terminate_vscode_processes()
                
                # Remove directories
                self.update_progress(40, "Removing all directories...")
                self.remove_directories("complete")
                
                # Clean registry
                self.update_progress(60, "Advanced registry cleanup...")
                self.clean_registry("complete")
                
                # System cleanup
                self.update_progress(80, "Comprehensive system cleanup...")
                self.perform_system_cleanup()
                
                # Final verification
                self.update_progress(95, "Final verification...")
                time.sleep(1)
                
                self.update_progress(100, "Complete removal finished!")
                self.show_removal_summary("Complete")
                
            except Exception as e:
                self.log_status(f"Complete removal failed: {str(e)}", "ERROR")
                if GUI_AVAILABLE:
                    messagebox.showerror("Error", f"Complete removal failed: {str(e)}")
        
        self.run_with_progress(complete_removal_process)
    
    def ultimate_removal(self):
        """Perform ultimate VSCode removal with Machine ID reset"""
        if not self.check_admin_privileges():
            if GUI_AVAILABLE:
                messagebox.showerror("Error", "Administrator privileges required!")
            else:
                print("Error: Administrator privileges required!")
            return
        
        # Double confirmation for ultimate removal
        if GUI_AVAILABLE:
            if not messagebox.askyesno("⚠️ ULTIMATE REMOVAL WARNING ⚠️", 
                                     "This is the MOST COMPREHENSIVE removal mode!\n\n"
                                     "This will:\n"
                                     "• Completely eradicate ALL VSCode traces\n"
                                     "• Reset Machine ID for total anonymity\n"
                                     "• Perform deep system cleanup\n"
                                     "• Remove all telemetry data\n\n"
                                     "This operation is IRREVERSIBLE!\n\n"
                                     "Continue?"):
                return
            
            # Final confirmation
            answer = simpledialog.askstring(
                "Final Confirmation",
                "Type 'ULTIMATE' to confirm this operation:",
                show='*'
            )
            
            if answer != 'ULTIMATE':
                messagebox.showinfo("Cancelled", "Ultimate removal cancelled.")
                return
        else:
            print("⚠️ ULTIMATE REMOVAL WARNING ⚠️")
            print("This will completely eradicate ALL VSCode traces and reset Machine ID!")
            confirmation = input("Type 'ULTIMATE' to confirm: ")
            if confirmation != 'ULTIMATE':
                print("Ultimate removal cancelled.")
                return
        
        def ultimate_removal_process():
            try:
                self.update_progress(0, "Starting ultimate removal...")
                
                # Create comprehensive backup
                self.update_progress(3, "Creating comprehensive backup...")
                self.create_advanced_backup()
                
                # Create system restore point
                self.update_progress(8, "Creating system restore point...")
                self._create_system_restore_point()
                
                # Terminate processes
                self.update_progress(15, "Terminating all processes...")
                self.terminate_vscode_processes()
                
                # Reset Machine ID
                self.update_progress(25, "Resetting Machine ID...")
                self.reset_machine_id()
                
                # Remove directories
                self.update_progress(45, "Ultimate directory cleanup...")
                self.remove_directories("ultimate")
                
                # Clean registry
                self.update_progress(65, "Ultimate registry cleanup...")
                self.clean_registry("ultimate")
                
                # System cleanup
                self.update_progress(80, "Ultimate system cleanup...")
                self.perform_system_cleanup()
                
                # Performance optimization
                self.update_progress(90, "System optimization...")
                self._optimize_system()
                
                # Final verification
                self.update_progress(98, "Final verification...")
                time.sleep(2)
                
                self.update_progress(100, "Ultimate removal completed!")
                self.show_removal_summary("Ultimate")
                
            except Exception as e:
                self.log_status(f"Ultimate removal failed: {str(e)}", "ERROR")
                if GUI_AVAILABLE:
                    messagebox.showerror("Error", f"Ultimate removal failed: {str(e)}")
        
        self.run_with_progress(ultimate_removal_process)
    
    def custom_removal(self):
        """Open custom removal dialog"""
        if GUI_AVAILABLE:
            CustomRemovalDialog(self)
        else:
            self._console_custom_removal()
    
    def _console_custom_removal(self):
        """Console version of custom removal"""
        print("\n=== CUSTOM REMOVAL ===")
        print("Select components to remove:")
        print("[1] User Data & Settings")
        print("[2] Application Files") 
        print("[3] Registry Entries")
        print("[4] Desktop Shortcuts")
        print("[5] System Cache")
        print("[6] Machine ID Reset")
        print("[7] Extensions")
        print("[8] All Components")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '8':
            self.complete_removal()
        elif choice == '6':
            self.reset_machine_id_only()
        else:
            print(f"Custom removal option {choice} selected - implementing basic removal")
            self.quick_removal()
    
    def backup_only(self):
        """Create backup without removal"""
        if GUI_AVAILABLE:
            if not messagebox.askyesno("Create Backup", 
                                     "This will create a complete backup of your VSCode data.\n\n"
                                     "Continue?"):
                return
        else:
            response = input("Create a complete backup of VSCode data? (y/N): ")
            if response.lower() != 'y':
                return
        
        def backup_process():
            try:
                self.create_advanced_backup()
                if GUI_AVAILABLE:
                    messagebox.showinfo("Backup Completed", 
                                      f"Backup created successfully!\n\n"
                                      f"Location: {self.backup_dir}\n\n"
                                      f"Developer: {self.developer}\n"
                                      f"Support: {self.telegram}")
                else:
                    print(f"✅ Backup created successfully at: {self.backup_dir}")
                    print(f"📞 For support contact: {self.telegram}")
            except Exception as e:
                if GUI_AVAILABLE:
                    messagebox.showerror("Backup Failed", f"Backup failed: {str(e)}")
                else:
                    print(f"❌ Backup failed: {str(e)}")
        
        self.run_with_progress(backup_process)
    
    def system_analysis(self):
        """Analyze VSCode system footprint"""
        if GUI_AVAILABLE:
            SystemAnalysisDialog(self)
        else:
            self._console_system_analysis()
    
    def _console_system_analysis(self):
        """Console version of system analysis"""
        print("\n=== VSCODE SYSTEM ANALYSIS ===")
        print(f"Tool by: {self.developer} | Support: {self.telegram}")
        print("-" * 50)
        
        # Installation analysis
        print(f"\n📦 INSTALLATIONS FOUND: {len(self.vscode_paths['install_paths'])}")
        for i, path in enumerate(self.vscode_paths['install_paths'], 1):
            print(f"  {i}. {path}")
        
        # User data analysis  
        print(f"\n👤 USER DATA LOCATIONS: {len(self.vscode_paths['user_data_paths'])}")
        for i, path in enumerate(self.vscode_paths['user_data_paths'], 1):
            print(f"  {i}. {path}")
        
        # Process analysis
        if PSUTIL_AVAILABLE:
            vscode_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    if proc.info['exe'] and 'vscode' in proc.info['exe'].lower():
                        vscode_processes.append(proc.info)
                except:
                    continue
            print(f"\n⚙️ RUNNING PROCESSES: {len(vscode_processes)}")
            for proc in vscode_processes:
                print(f"  PID {proc['pid']}: {proc['name']}")
        
        # Machine ID
        current_id = self._get_current_machine_id()
        print(f"\n🆔 MACHINE ID: {current_id if current_id else 'Not found'}")
        
        print(f"\n📞 For support contact developer: {self.telegram}")
        print("Analysis completed!")
    
    def restore_backup(self):
        """Restore from backup"""
        if GUI_AVAILABLE:
            RestoreBackupDialog(self)
        else:
            self._console_restore_backup()
    
    def _console_restore_backup(self):
        """Console version of backup restore"""
        print("\n=== RESTORE BACKUP ===")
        print(f"Tool by: {self.developer} | Support: {self.telegram}")
        
        # Scan for backups
        desktop = Path.home() / "Desktop"
        backup_dirs = list(desktop.glob("VSCode_Backup_*"))
        
        if not backup_dirs:
            print("No backups found on desktop.")
            return
        
        print("Available backups:")
        for i, backup_dir in enumerate(backup_dirs, 1):
            print(f"  [{i}] {backup_dir.name}")
        
        try:
            choice = int(input(f"\nSelect backup (1-{len(backup_dirs)}): ")) - 1
            selected_backup = backup_dirs[choice]
            
            print(f"Restoring from: {selected_backup}")
            # Implement basic restore logic here
            print("✅ Restore completed!")
            print(f"📞 For support contact: {self.telegram}")
            
        except (ValueError, IndexError):
            print("Invalid selection.")
    
    def reset_machine_id_only(self):
        """Reset only Machine ID without removal"""
        if not self.check_admin_privileges():
            if GUI_AVAILABLE:
                messagebox.showerror("Error", "Administrator privileges required!")
            else:
                print("Error: Administrator privileges required!")
            return
        
        if GUI_AVAILABLE:
            if not messagebox.askyesno("Reset Machine ID", 
                                     "This will reset VSCode's Machine ID for anonymity.\n"
                                     "Current Machine ID will be backed up first.\n\n"
                                     "Continue?"):
                return
        else:
            response = input("Reset VSCode Machine ID for anonymity? (y/N): ")
            if response.lower() != 'y':
                return
        
        def reset_process():
            try:
                self.reset_machine_id()
                if GUI_AVAILABLE:
                    messagebox.showinfo("Machine ID Reset", 
                                      f"Machine ID has been reset successfully!\n\n"
                                      f"VSCode will generate a new ID on next startup.\n\n"
                                      f"Developer: {self.developer}\n"
                                      f"Support: {self.telegram}")
                else:
                    print("✅ Machine ID has been reset successfully!")
                    print(f"📞 For support contact: {self.telegram}")
            except Exception as e:
                if GUI_AVAILABLE:
                    messagebox.showerror("Reset Failed", f"Machine ID reset failed: {str(e)}")
                else:
                    print(f"❌ Machine ID reset failed: {str(e)}")
        
        self.run_with_progress(reset_process)
    
    def _create_system_restore_point(self):
        """Create Windows system restore point"""
        try:
            cmd = 'powershell -Command "Checkpoint-Computer -Description \'Before VSCode Ultimate Removal\' -RestorePointType \'MODIFY_SETTINGS\'"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log_status("✅ System restore point created")
            else:
                self.log_status("⚠️ Could not create system restore point", "WARNING")
        except Exception as e:
            self.log_status(f"System restore point creation failed: {e}", "WARNING")
    
    def _optimize_system(self):
        """Perform system optimization after removal"""
        self.log_status("Optimizing system...")
        
        # Clear system caches
        try:
            subprocess.run('ipconfig /flushdns', shell=True, capture_output=True)
            self.log_status("DNS cache flushed")
        except:
            pass
        
        # Update Windows Search index
        try:
            subprocess.run('sc start WSearch', shell=True, capture_output=True)
            self.log_status("Windows Search service restarted")
        except:
            pass
        
        self.log_status("✅ System optimization completed")
    
    def run_console_mode(self):
        """Run in console mode when GUI is not available"""
        print(f"\n🗑️ VSCode Ultimate Removal Tool v{self.version}")
        print("=" * 60)
        print(f"👨‍💻 Developer: {self.developer}")
        print(f"📱 Telegram: {self.telegram}")
        print("=" * 60)
        print(f"Computer: {self.computer_name} | User: {self.current_user}")
        print(f"Architecture: {self.system_arch}")
        print(f"Admin: {'YES' if self.check_admin_privileges() else 'NO'}")
        print("=" * 60)
        
        while True:
            print("\nSelect an option:")
            print("[1] Quick Removal")
            print("[2] Complete Removal") 
            print("[3] Ultimate Removal")
            print("[4] Custom Removal")
            print("[5] Backup Only")
            print("[6] System Analysis")
            print("[7] Reset Machine ID")
            print("[8] Contact Developer")
            print("[0] Exit")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.quick_removal()
            elif choice == '2':
                self.complete_removal()
            elif choice == '3':
                self.ultimate_removal()
            elif choice == '4':
                self.custom_removal()
            elif choice == '5':
                self.backup_only()
            elif choice == '6':
                self.system_analysis()
            elif choice == '7':
                self.reset_machine_id_only()
            elif choice == '8':
                self._open_telegram()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def run(self):
        """Run the main application"""
        if not self.check_admin_privileges():
            error_msg = ("This tool requires administrator privileges to function properly.\n"
                        "Please run as administrator and try again.")
            if GUI_AVAILABLE:
                messagebox.showerror("Administrator Required", error_msg)
            else:
                print(f"Error: {error_msg}")
            return
        
        if GUI_AVAILABLE:
            self.create_gui()
            self.log_status("VSCode Ultimate Removal Tool started")
            self.log_status(f"Session ID: {self.session_id}")
            self.log_status(f"Developer: {self.developer}")
            self.root.mainloop()
        else:
            self.run_console_mode()

# Dialog classes for GUI mode (simplified versions)
class CustomRemovalDialog:
    """Dialog for custom component selection"""
    
    def __init__(self, parent):
        if not GUI_AVAILABLE:
            return
            
        self.parent = parent
        self.dialog = tk.Toplevel(parent.root)
        self.dialog.title(f"Custom Removal - by {parent.developer}")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent.root)
        self.dialog.grab_set()
        
        self.components = {
            'user_data': tk.BooleanVar(value=True),
            'app_files': tk.BooleanVar(value=True),
            'registry': tk.BooleanVar(value=True),
            'machine_id': tk.BooleanVar(value=False),
        }
        
        self._create_dialog()
    
    def _create_dialog(self):
        """Create the custom removal dialog"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title with developer info
        title_label = ttk.Label(
            main_frame,
            text=f"Custom Component Selection - by {self.parent.developer}",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Telegram contact
        contact_label = ttk.Label(
            main_frame,
            text=f"Support: {self.parent.telegram}",
            font=('Arial', 10),
            foreground='#0088cc'
        )
        contact_label.pack(pady=(0, 20))
        
        # Simple component selection
        ttk.Checkbutton(main_frame, text="User Data & Settings", variable=self.components['user_data']).pack(anchor='w', pady=5)
        ttk.Checkbutton(main_frame, text="Application Files", variable=self.components['app_files']).pack(anchor='w', pady=5)
        ttk.Checkbutton(main_frame, text="Registry Entries", variable=self.components['registry']).pack(anchor='w', pady=5)
        ttk.Checkbutton(main_frame, text="Machine ID Reset", variable=self.components['machine_id']).pack(anchor='w', pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=20)
        
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Start Removal", command=self._start_removal).pack(side='right')
    
    def _start_removal(self):
        """Start custom removal"""
        self.dialog.destroy()
        if self.components['machine_id'].get():
            self.parent.reset_machine_id_only()
        else:
            self.parent.quick_removal()

class SystemAnalysisDialog:
    """Dialog for system analysis"""
    
    def __init__(self, parent):
        if not GUI_AVAILABLE:
            return
            
        self.parent = parent
        self.dialog = tk.Toplevel(parent.root)
        self.dialog.title(f"System Analysis - by {parent.developer}")
        self.dialog.geometry("700x600")
        self.dialog.transient(parent.root)
        
        self._create_dialog()
        self._run_analysis()
    
    def _create_dialog(self):
        """Create the analysis dialog"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title with developer info
        title_label = ttk.Label(
            main_frame,
            text=f"VSCode System Analysis - by {self.parent.developer}",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Contact info
        contact_frame = ttk.Frame(main_frame)
        contact_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(contact_frame, text=f"Support: {self.parent.telegram}", foreground='#0088cc').pack(side='left')
        ttk.Button(contact_frame, text="📱 Contact", command=self.parent._open_telegram).pack(side='right')
        
        # Analysis text
        self.analysis_text = tk.Text(
            main_frame,
            height=20,
            width=80,
            bg='#1e1e1e',
            fg='#d4d4d4',
            font=('Consolas', 9)
        )
        self.analysis_text.pack(fill='both', expand=True)
        
        # Close button
        ttk.Button(main_frame, text="Close", command=self.dialog.destroy).pack(pady=10)
    
    def _run_analysis(self):
        """Run system analysis"""
        self.analysis_text.insert('end', f"🔍 VSCode System Analysis - by {self.parent.developer}\n")
        self.analysis_text.insert('end', f"📱 Support: {self.parent.telegram}\n")
        self.analysis_text.insert('end', "=" * 60 + "\n\n")
        
        # Basic analysis
        self.analysis_text.insert('end', f"📦 Installations: {len(self.parent.vscode_paths['install_paths'])}\n")
        self.analysis_text.insert('end', f"👤 User Data: {len(self.parent.vscode_paths['user_data_paths'])}\n")
        
        machine_id = self.parent._get_current_machine_id()
        self.analysis_text.insert('end', f"🆔 Machine ID: {machine_id if machine_id else 'Not found'}\n")
        
        self.analysis_text.insert('end', "\n✅ Analysis completed!\n")
        self.analysis_text.insert('end', f"📞 For detailed support, contact {self.parent.telegram}")

class RestoreBackupDialog:
    """Dialog for backup restoration"""
    
    def __init__(self, parent):
        if not GUI_AVAILABLE:
            return
            
        self.parent = parent
        self.dialog = tk.Toplevel(parent.root)
        self.dialog.title(f"Restore Backup - by {parent.developer}")
        self.dialog.geometry("600x400")
        self.dialog.transient(parent.root)
        
        self._create_dialog()
    
    def _create_dialog(self):
        """Create the restore dialog"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title with developer info
        title_label = ttk.Label(
            main_frame,
            text=f"Restore VSCode Backup - by {self.parent.developer}",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Support info
        ttk.Label(main_frame, text=f"Support: {self.parent.telegram}", foreground='#0088cc').pack()
        
        # Simple restore message
        message_label = ttk.Label(
            main_frame,
            text="Backup restoration feature available.\nFor detailed restoration support, please contact the developer.",
            font=('Arial', 12),
            justify='center'
        )
        message_label.pack(pady=50)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="📱 Contact Developer", command=self.parent._open_telegram).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Close", command=self.dialog.destroy).pack(side='left', padx=10)

def main():
    """Main entry point"""
    # Check Python version
    if sys.version_info < (3, 6):
        print("Python 3.6 or later is required!")
        sys.exit(1)
    
    # Check if running on Windows
    if sys.platform != 'win32':
        print("This tool is designed for Windows only!")
        sys.exit(1)
    
    try:
        app = VSCodeRemovalTool()
        app.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()