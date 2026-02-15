
import pyzipper

# Create a zip with password '123'
with pyzipper.AESZipFile('test_files/test_123.zip', 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
    zf.setpassword(b'123')
    zf.writestr('secret.txt', 'You cracked it!')

# Create a wordlist
with open('test_files/wordlist.txt', 'w') as f:
    f.write('password\n')
    f.write('123456\n')
    f.write('123\n')
    f.write('qwerty\n')
