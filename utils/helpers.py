
import os
import shutil
import string
import itertools

def get_charset(use_lower=True, use_upper=True, use_digits=True, use_symbols=True, custom_chars=""):
    """
    Generates a string of characters based on the selected options.
    """
    charset = ""
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += string.punctuation
    
    charset += custom_chars
    return charset

def generate_brute_force_payloads(charset, min_length, max_length):
    """
    Generator that yields passwords for brute force attack.
    """
    for length in range(min_length, max_length + 1):
        for payload in itertools.product(charset, repeat=length):
            yield ''.join(payload)


def find_john_path():
    """
    Auto-detect John the Ripper installation on Windows.
    Returns the directory containing john.exe, or None if not found.
    """
    # Check if john is in PATH
    john_in_path = shutil.which("john")
    if john_in_path:
        return os.path.dirname(os.path.abspath(john_in_path))

    # Common Windows install locations
    search_dirs = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "John"),
        os.path.join(os.environ.get("PROGRAMFILES", ""), "JohnTheRipper", "run"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "JohnTheRipper", "run"),
        r"C:\John\run",
        r"C:\JohnTheRipper\run",
        r"C:\john\run",
        # Project-local john directory
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "john", "run"),
    ]

    for directory in search_dirs:
        john_exe = os.path.join(directory, "john.exe")
        if os.path.isfile(john_exe):
            return directory

    return None

