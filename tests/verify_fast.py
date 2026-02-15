
import os
import sys
import unittest
import pyzipper
from PyQt6.QtCore import QCoreApplication

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.worker import CrackerWorker

class TestCrackerWorkerFast(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a dummy app for QThread
        cls.app = QCoreApplication(sys.argv)
        
        # Use a simpler password for fast brute force testing
        cls.password = "abc"
        cls.zip_path = "test_fast.zip"
        cls.wordlist_path = "test_fast_wordlist.txt"
        
        # Create a zip file with AES encryption
        with pyzipper.AESZipFile(cls.zip_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(cls.password.encode('utf-8'))
            zf.writestr('secret.txt', 'Fast test message.')
            
        # Create a wordlist
        with open(cls.wordlist_path, 'w') as f:
            f.write("wrong\n")
            f.write("abc\n")

    @classmethod
    def tearDownClass(cls):
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
        worker.run() 
        
        self.assertEqual(found_pass[0], self.password)
        print("Dictionary Attack Success!")

    def test_brute_force_attack(self):
        print("\nTesting Brute Force Attack...")
        # Min length 1, max length 3, lower case only
        worker = CrackerWorker(self.zip_path, 'brute_force', 
                               min_length=1, max_length=3, 
                               use_lower=True, use_upper=False, 
                               use_digits=False, use_symbols=False)
        
        found_pass = []
        def on_found(p):
            found_pass.append(p)
            
        worker.password_found.connect(on_found)
        worker.run()
        
        self.assertTrue(len(found_pass) > 0)
        self.assertEqual(found_pass[0], self.password)
        print("Brute Force Attack Success!")

if __name__ == '__main__':
    unittest.main()
