
import os
import re
import tempfile
import subprocess
from PyQt6.QtCore import QThread, pyqtSignal


class JTRWorker(QThread):
    """
    Worker thread that cracks ZIP passwords using John the Ripper.
    Flow: zip2john (extract hash) → john (crack) → john --show (retrieve password)
    """
    progress_updated = pyqtSignal(str)     # Emits current status text
    stats_updated = pyqtSignal(int)        # Emits attempt count (from JtR output)
    password_found = pyqtSignal(str)       # Emits found password
    task_finished = pyqtSignal()           # Emits when task is done
    error_occurred = pyqtSignal(str)       # Emits error messages

    def __init__(self, zip_path, john_dir, jtr_mode='wordlist', **kwargs):
        super().__init__()
        self.zip_path = zip_path
        self.john_dir = john_dir  # Directory containing john.exe and zip2john.exe
        self.jtr_mode = jtr_mode  # 'wordlist' or 'incremental'
        self.kwargs = kwargs
        self.is_running = True
        self.attempts = 0
        self._process = None
        self._hash_file = None

    def run(self):
        try:
            john_exe = os.path.join(self.john_dir, "john.exe")
            zip2john_exe = os.path.join(self.john_dir, "zip2john.exe")

            # Validate JtR executables exist
            if not os.path.isfile(john_exe):
                self.error_occurred.emit(
                    f"john.exe not found in: {self.john_dir}\n"
                    "Please provide the correct path to your John the Ripper installation."
                )
                self.task_finished.emit()
                return

            if not os.path.isfile(zip2john_exe):
                self.error_occurred.emit(
                    f"zip2john.exe not found in: {self.john_dir}\n"
                    "Please ensure your JtR installation includes zip2john."
                )
                self.task_finished.emit()
                return

            # Step 1: Extract hash with zip2john
            self.progress_updated.emit("[JtR] Extracting hash with zip2john...")
            hash_data = self._run_zip2john(zip2john_exe)
            if not hash_data or not self.is_running:
                return

            # Write hash to temp file
            self._hash_file = tempfile.NamedTemporaryFile(
                mode='w', suffix='.hash', delete=False, prefix='zipcrack_'
            )
            self._hash_file.write(hash_data)
            self._hash_file.close()

            # Step 2: Run john to crack
            self.progress_updated.emit(f"[JtR] Cracking with {self.jtr_mode} mode...")
            self._run_john(john_exe)

            if not self.is_running:
                return

            # Step 3: Retrieve cracked password with --show
            password = self._get_cracked_password(john_exe)
            if password:
                self.password_found.emit(password)
            else:
                self.progress_updated.emit("[JtR] Password not found with current settings.")

        except Exception as e:
            self.error_occurred.emit(f"JtR Error: {str(e)}")
        finally:
            # Clean up temp hash file
            if self._hash_file and os.path.exists(self._hash_file.name):
                try:
                    os.unlink(self._hash_file.name)
                except OSError:
                    pass
            self.task_finished.emit()

    def _run_zip2john(self, zip2john_exe):
        """Run zip2john to extract the password hash from the ZIP file."""
        try:
            result = subprocess.run(
                [zip2john_exe, self.zip_path],
                capture_output=True, text=True, timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            if result.returncode != 0 and not result.stdout:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                self.error_occurred.emit(f"zip2john failed: {error_msg}")
                self.task_finished.emit()
                return None

            # zip2john outputs the hash to stdout
            hash_output = result.stdout.strip()
            if not hash_output:
                self.error_occurred.emit("zip2john produced no output. Is this a valid encrypted ZIP?")
                self.task_finished.emit()
                return None

            self.progress_updated.emit(f"[JtR] Hash extracted successfully.")
            return hash_output

        except subprocess.TimeoutExpired:
            self.error_occurred.emit("zip2john timed out.")
            self.task_finished.emit()
            return None
        except Exception as e:
            self.error_occurred.emit(f"Failed to run zip2john: {str(e)}")
            self.task_finished.emit()
            return None

    def _run_john(self, john_exe):
        """Run john to crack the hash."""
        cmd = [john_exe]

        if self.jtr_mode == 'wordlist':
            wordlist_path = self.kwargs.get('wordlist_path')
            if not wordlist_path or not os.path.isfile(wordlist_path):
                self.error_occurred.emit("No valid wordlist file provided for JtR wordlist mode.")
                return
            cmd.append(f"--wordlist={wordlist_path}")
        elif self.jtr_mode == 'incremental':
            cmd.append("--incremental")

        cmd.append(self._hash_file.name)

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Read output line by line
            while self.is_running:
                line = self._process.stdout.readline()
                if not line and self._process.poll() is not None:
                    break

                line = line.strip()
                if line:
                    self.progress_updated.emit(f"[JtR] {line}")

                    # Try to parse guesses count from JtR output
                    guess_match = re.search(r'(\d+)g\s', line)
                    if guess_match:
                        self.attempts = int(guess_match.group(1))
                        self.stats_updated.emit(self.attempts)

            # If stopped by user, kill the process
            if not self.is_running and self._process.poll() is None:
                self._process.terminate()
                try:
                    self._process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self._process.kill()

        except Exception as e:
            self.error_occurred.emit(f"Failed to run john: {str(e)}")

    def _get_cracked_password(self, john_exe):
        """Run john --show to retrieve the cracked password."""
        try:
            result = subprocess.run(
                [john_exe, "--show", self._hash_file.name],
                capture_output=True, text=True, timeout=15,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            output = result.stdout.strip()
            if not output:
                return None

            # JtR --show output format: filename:password:...  or  archive.zip/file.txt:password:...
            for line in output.split('\n'):
                if ':' in line and 'password hash' not in line.lower():
                    parts = line.split(':')
                    if len(parts) >= 2:
                        password = parts[1]
                        if password:
                            return password

            return None

        except Exception as e:
            self.error_occurred.emit(f"Failed to read JtR results: {str(e)}")
            return None

    def stop(self):
        self.is_running = False
        if self._process and self._process.poll() is None:
            self._process.terminate()
