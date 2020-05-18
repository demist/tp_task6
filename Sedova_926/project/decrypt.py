from cryptography.fernet import Fernet

print("введите код")
cipher_key = input().encode('utf-8')


with open('encrypted_main.py', 'rb') as e_file:
    with open ('main.py', 'w') as file:
        try:
            cipher = Fernet(cipher_key)
            decrypted_file = cipher.decrypt(e_file.read())
        except:
            print("Код введен неправильно!!!")
        else:
            file.write(decrypted_file.decode('utf-8'))

import main