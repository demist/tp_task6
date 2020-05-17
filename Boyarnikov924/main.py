import sys
import traceback

ENCRYPTED_LIB_FILE = 'LIB.lib'
MIN_KEY_LENGTH = 8
MAX_PERMUTATION_LENGTH = 25
MIN_PERMUTATION_LENGTH = 15
ALPHABET = [chr(a) for a in range(33, 127)]
ALPHABET.append('\n')
ALPHABET.append(' ')
FROM_ALPHABET_DICT = dict(zip(ALPHABET, [a for a in range(len(ALPHABET))]))
TO_ALPHABET_DICT = dict(zip([a for a in range(len(ALPHABET))], ALPHABET))


def get_permutation(index, size):
    permutation = list()
    for i in range(size):
        permutation.insert(i - index % (i + 1), i)
        index //= i + 1
    return permutation


def reverse_permutation(permutation):
    new_permutation = permutation.copy()
    for i in range(len(permutation)):
        new_permutation[permutation[i]] = i
    return new_permutation


def shuffle_text(text, permutation):
    my_text = list(text)
    new_text = list(text)
    shuffle_period = len(permutation)
    text_length = len(text)
    processing_length = text_length - text_length % shuffle_period
    for position in range(processing_length):
        sub_position = position % shuffle_period
        shift = permutation[sub_position]
        from_position = position - sub_position + shift
        new_text[position] = my_text[from_position]
    return ''.join(new_text)


def v_encode(text, key):
    if len(key) == 0:
        return text
    return_text = list(text)
    for index in range(len(key)):
        ch = key[index]
        assert ch in FROM_ALPHABET_DICT.keys()
        num_key = FROM_ALPHABET_DICT[ch]
        func = dict()
        for j in range(len(ALPHABET)):
            func[TO_ALPHABET_DICT[j]] = TO_ALPHABET_DICT[(j + num_key) % len(ALPHABET)]
        for i in range(index, len(text), len(key)):
            if text[i] in func.keys():
                return_text[i] = func[text[i]]
    return ''.join(return_text)


def v_decode(text, key):
    if len(key) == 0:
        return text
    inverse_key = list()
    size_of_key_alphabet = len(ALPHABET)

    for ch in key:
        assert ch in FROM_ALPHABET_DICT.keys()
        new_char = TO_ALPHABET_DICT[-FROM_ALPHABET_DICT[ch] % size_of_key_alphabet]
        inverse_key.append(new_char)

    new_key = ''.join(inverse_key)
    return v_encode(text, new_key)


def string_into_int_through_alphabet_code(string):
    integer = 0
    for ch in string:
        integer *= len(ALPHABET)
        integer += FROM_ALPHABET_DICT[ch]
    return integer


def parse_key(key):
    if len(key) < MIN_KEY_LENGTH:
        return None
    string = key[MIN_KEY_LENGTH:]
    integer = string_into_int_through_alphabet_code(key[:MIN_KEY_LENGTH])
    permutation_size = integer % (MAX_PERMUTATION_LENGTH - MIN_PERMUTATION_LENGTH) + MIN_PERMUTATION_LENGTH
    permutation_index = integer // (MAX_PERMUTATION_LENGTH - MIN_PERMUTATION_LENGTH)
    return {'string': string, 'size': permutation_size, 'index': permutation_index}


def interface_loop():
    return


def include_encrypted_lib(key):
    try:
        key_data = parse_key(key)
        with open(ENCRYPTED_LIB_FILE, "r") as f:
            code = f.read()
        code = v_decode(code, key_data['string'])
        permutation = reverse_permutation(get_permutation(key_data['index'], key_data['size']))
        code = shuffle_text(code, permutation)
        exec(code, globals())
    except Exception as e:
        print("Invalid activation key! Please purchase the official version on the product website")
        input("Press any key to continue.")
        exit(0)


def main():
    key = input("Please enter an activation key: ")
    include_encrypted_lib(key)
    interface_loop()


if __name__ == '__main__':
    main()
