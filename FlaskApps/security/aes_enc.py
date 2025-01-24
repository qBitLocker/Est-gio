from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad

import sys

def in_bits (string: list) -> int:
    return len (string) * 8
    
def main(plaintext: list, key: list) -> int:
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open('./secret/cipher_file.bin', 'wb') as c_file:
        c_file.write(cipher.iv)
        c_file.write(ciphertext)
        c_file.close()

    return 0

if __name__ == "__main__":
    argc = len (sys.argv)
    if argc == 3:
        plaintext = sys.argv[1].encode()
        key = sys.argv[2].encode()

        if not in_bits(key) in [128, 192, 256]:
            print(f'The number of bytes of the key must be 16, 24 or 32')
        else:
            print(f'Main return flag: {main(plaintext, key)}')
    else:
        print (f'Usage: {sys.argv[0]} <plaintext> <enc_key>')