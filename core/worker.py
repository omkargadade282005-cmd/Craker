
import time
import pyzipper
from PyQt6.QtCore import QThread, pyqtSignal
from utils.helpers import get_charset, generate_brute_force_payloads

class CrackerWorker(QThread):
    """
    Worker thread that handles the password cracking process.
    """
    progress_updated = pyqtSignal(str)     # Emits current password being tried
    stats_updated = pyqtSignal(int)        # Emits total attempts
    password_found = pyqtSignal(str)       # Emits found password
    task_finished = pyqtSignal()           # Emits when task is done (success or fail)
    error_occurred = pyqtSignal(str)       # Emits error messages

    def __init__(self, zip_path, attack_mode, **kwargs):
        super().__init__()
        self.zip_path = zip_path
        self.attack_mode = attack_mode  # 'dictionary' or 'brute_force'
        self.kwargs = kwargs
        self.is_running = True
        self.attempts = 0

    def run(self):
        try:
            # Open the zip file once to verify it exists and is valid
            try:
                with pyzipper.AESZipFile(self.zip_path) as zf:
                    # We'll try to extract the first file to test the password
                    first_file = zf.namelist()[0]
            except Exception as e:
                self.error_occurred.emit(f"Invalid Zip File: {str(e)}")
                self.task_finished.emit()
                return

            if self.attack_mode == 'dictionary':
                self.run_dictionary_attack(first_file)
            elif self.attack_mode == 'brute_force':
                self.run_brute_force_attack(first_file)
            
        except Exception as e:
            self.error_occurred.emit(f"An unexpected error occurred: {str(e)}")
        finally:
            self.task_finished.emit()

    def run_dictionary_attack(self, target_file):
        wordlist_path = self.kwargs.get('wordlist_path')
        if not wordlist_path:
            self.error_occurred.emit("No wordlist provided.")
            return

        try:
            with open(wordlist_path, 'r', errors='ignore') as f:
                for line in f:
                    if not self.is_running:
                        break
                    
                    password = line.strip()
                    if self.try_password(password, target_file):
                        return
        except FileNotFoundError:
            self.error_occurred.emit("Wordlist file not found.")

    def run_brute_force_attack(self, target_file):
        charset = get_charset(
            self.kwargs.get('use_lower', True),
            self.kwargs.get('use_upper', True),
            self.kwargs.get('use_digits', True),
            self.kwargs.get('use_symbols', True),
            self.kwargs.get('custom_chars', "")
        )
        
        if not charset:
            self.error_occurred.emit("No character set selected.")
            return

        min_len = self.kwargs.get('min_length', 1)
        max_len = self.kwargs.get('max_length', 4)

        generator = generate_brute_force_payloads(charset, min_len, max_len)
        
        for password in generator:
            if not self.is_running:
                break
            if self.try_password(password, target_file):
                return

    def try_password(self, password, target_file):
        """
        Attempts to extract the target file with the given password.
        Returns True if successful, False otherwise.
        """
        self.attempts += 1
        
        # Emit stats periodically to avoid UI freeze
        if self.attempts % 100 == 0:
            self.stats_updated.emit(self.attempts)
            self.progress_updated.emit(password)

        try:
            with pyzipper.AESZipFile(self.zip_path) as zf:
                zf.setpassword(password.encode('utf-8'))
                zf.read(target_file)  # Try to read the file
                
            # If we get here, password is correct
            self.password_found.emit(password)
            return True
        except (RuntimeError, pyzipper.BadZipFile, pyzipper.LargeZipFile):
            # RuntimeError is raised for bad password by pyzipper/zipfile
            return False
        except Exception as e:
            # Ignore other errors but log them if needed
            return False

    def stop(self):
        self.is_running = False
