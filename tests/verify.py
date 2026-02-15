
import os
import sys
import unittest
import pyzipper
from PyQt6.QtCore import QCoreApplication

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.worker import CrackerWorker

class TestCrackerWorker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a dummy app for QThread
        cls.app = QCoreApplication(sys.argv)
        
        # Setup test files
        cls.password = "pass"
        cls.zip_path = "test_archive.zip"
        cls.wordlist_path = "test_wordlist.txt"
        
        # Create a zip file with AES encryption
        with pyzipper.AESZipFile(cls.zip_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(cls.password.encode('utf-8'))
            zf.writestr('secret.txt', 'This is a secret message.')
            
        # Create a wordlist
        with open(cls.wordlist_path, 'w') as f:
            f.write("wrong\n")
            f.write("incorrect\n")
            f.write("pass\n")
            f.write("fail\n")

    @classmethod
    def tearDownClass(cls):
        # Clean up
        if os.path.exists(cls.zip_path):
            os.remove(cls.zip_path)
        if os.path.exists(cls.wordlist_path):
            os.remove(cls.wordlist_path)

    def test_dictionary_attack(self):
        print("\nTesting Dictionary Attack...")
        worker = CrackerWorker(self.zip_path, 'dictionary', wordlist_path=self.wordlist_path)
        
        found_pass = []
        def on_found(p):
            found_pass.append(p)
            
        worker.password_found.connect(on_found)
        worker.run() # Run synchronously for testing
        
        self.assertEqual(found_pass[0], self.password)
        print("Dictionary Attack Success!")

    def test_brute_force_attack(self):
        print("\nTesting Brute Force Attack...")
        # Min length 3, max length 4, lower case only to be fast
        worker = CrackerWorker(self.zip_path, 'brute_force', 
                               min_length=3, max_length=4, 
                               use_lower=True, use_upper=False, 
                               use_digits=False, use_symbols=False)
        
        found_pass = []
        def on_found(p):
            found_pass.append(p)
            
        worker.password_found.connect(on_found)
        worker.run() # Run synchronously
        
        self.assertEqual(found_pass[0], self.password)
        print("Brute Force Attack Success!")

if __name__ == '__main__':
    unittest.main()
