from Crypto.Cipher import AES 
from Crypto.Util.Padding import unpad

import sys

def in_bits (string: list) -> int:
    return len (string) * 8
    
def main(cipher_file: str, key: list) -> int:
    with open(cipher_file, 'rb') as c_file:
        iv = c_file.read(16)            # The pointer of the file follows the operations
        ciphertext = c_file.read()
        c_file.close()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad (cipher.decrypt(ciphertext), AES.block_size)
    print (plaintext.decode('utf-8'))

    return 0

if __name__ == "__main__":
    argc = len (sys.argv)
    if argc == 3:
        cipher_file = sys.argv[1].encode()
        key = sys.argv[2].encode()

        if not in_bits(key) in [128, 192, 256]:
            print(f'The number of bytes of the key must be 16, 24 or 32')
        else:
            print(f'Main return flag: {main(cipher_file, key)}')
    else:
        print (f'Usage: {sys.argv[0]} <cipher_file.bin> <enc_key>')