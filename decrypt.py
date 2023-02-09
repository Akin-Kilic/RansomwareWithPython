import os
from cryptography.fernet import Fernet
from pathlib import Path

# Dizin yolunu belirtin
directory = './deneme2'


def scanRecurse(baseDir):
    '''
    Scan a directory and return a list of all files
    return: list of files
    '''
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)


with open('key.txt', 'rb') as f:
    key = f.read()
    key = key.decode()

fernet = Fernet(key)


def decrypt_file(filename):
    with open(filename, 'rb') as f:
        ciphertext = f.read()

    # Dosyayı deşifreleyin
    plaintext = fernet.decrypt(ciphertext)

    # Deşifrelenmiş dosyayı kaydedin
    with open(filename, 'wb') as f:
        f.write(plaintext)


excludeExtension = ['.py', '.pem', '.exe']
for filename in scanRecurse(directory):
    filePath = Path(filename)
    fileType = filePath.suffix.lower()
    if fileType in excludeExtension:
        continue
    decrypt_file(filename)
