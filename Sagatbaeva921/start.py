from Crypto.Cipher import AES


while True:
    try:
        activation_code = input("Введите ключ активации программного обеспечения: ")

        with open('program.bin', 'rb') as f:
            decoder = AES.new(activation_code, AES.MODE_ECB)
            decoded = decoder.decrypt(f.read()).decode('utf-8')
            exec(decoded)
            break
    except Exception:
        print("Неправильный код, попробуйте еще раз!")
