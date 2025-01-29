from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes

import os
# Uma classe que contém o algoritmo AES
# Também é projetado para que se possa implementar outros
# algoritmos no futuro, como RSA, Blowfish, etc...
# - A Chave é gerada aleatóriamente no local especificado no construtor da classe
# - As informações são armazenada em um arquivo binário criptografado!
class CipherTools():
    # Construtor da classe
    def __init__ (self, path:str=None, filename:str=None):
        ''' Recebe um caminho onde serah armazenada as informaçoes '''
        if not path:
            self.path = os.path.join(os.getcwd(), 'security', 'secret')
        elif not os.path.exists(path):
            self.path = os.path.join(os.getcwd(), 'security', 'secret')
        else:
            self.path = path
        
        if not filename:
            self.filename = '/cipher_file.bin'
        elif filename[0] == '/':
            self.filename = filename
        else:
            self.filename = '/' + filename

        self.target = self.path + self.filename


    # Plaintext deve ser uma binary string! b'...'
    def AES_enc(self, plaintext):
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC)

        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        
        with open(self.target, 'wb') as c_file:
            c_file.write(key)
            c_file.write(cipher.iv)
            c_file.write(ciphertext)
            c_file.close()
    
    # Ciphertext deve ser uma binary string também
    def AES_dec(self):
        with open(self.target, 'rb') as c_file:
            key = c_file.read(16)
            iv  = c_file.read(16)
            ciphertext = c_file.read()
            c_file.close()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad (cipher.decrypt(ciphertext), AES.block_size)
        return plaintext