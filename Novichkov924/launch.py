"""
Это лаунчер для основной программы.
Его задача, получить код активации от пользователя и запустить программа.
"""
from Crypto.Cipher import AES

WELCOME_MESSAGE = 'Чтобы запустить программу, введите код активации: '
WRONG_CODE_MESSAGE = 'Вы ввели неправильный код, попробуйте еще раз!'

if __name__ == '__main__':
    while True:
        try:
            activation_code = input(WELCOME_MESSAGE)

            with open('encoded_program.bin', 'rb') as f:
                obj = AES.new(activation_code, AES.MODE_ECB)
                encoded_text = f.read()
                decoded_text = obj.decrypt(encoded_text).decode('utf-8')
                decoded_text = decoded_text[:int(len(decoded_text) / 16)]
                exec(decoded_text)
                break
        except:
            print(WRONG_CODE_MESSAGE)
            print()
