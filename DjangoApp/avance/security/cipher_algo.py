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
    def __init__ (self, path: str=None, filename: str=None):
        default_path = os.path.join(os.getcwd(), 'security', 'secret')
        self.path = default_path if not path else path if os.path.exists(path) else default_path

        # Cuidado! Ao cortar o fio errado o projeto pode explodir
        default_filename = 'cipher_file.bin'
        self.filename = default_filename if not filename else default_filename if not filename.split('\\')[-1].split('/')[-1] else filename.split('\\')[-1].split('/')[-1]
        
        self.target = os.path.join(self.path, self.filename)
    
    # Leia as informações contidas no target da criptografia AES
    def read_pieces(self, key: bool=True, iv: bool=True, ciphertext: bool=True, seq: str="kic") -> tuple:
        key_, iv_, ciphertext_ = None, None, None
        read = [False, False, False]

        file_size = os.path.getsize(self.target)
        with open (self.target, 'rb') as c_file:
            for it, token in enumerate(seq):
                if token == "k" and key and not read[0]:
                    key_ = c_file.read(16)
                    read[0] = True

                elif token == "i" and iv and not read[1]:
                    iv_  = c_file.read(16)
                    read[1] = True

                elif token == "c" and ciphertext and not read[2]:
                    if it == 2:
                        ciphertext_ = c_file.read()
                    else:
                        ciphertext_ = c_file.read(file_size - ((2 - it) * 16))
                    read[2] = True

        return (key_, iv_, ciphertext_)
    
    def write_pieces(self, key=None, iv=None, ciphertext=None, seq:str="kic") -> bool:
        written = [False, False, False]
        with open (self.target, 'wb') as c_file:
            for it, token in enumerate(seq):
                if token == "k" and key and not written[0]:
                    c_file.write(key)
                    written[0] = True

                elif token == "i" and iv and not written[1]:
                    c_file.write(iv) 
                    written[1] = True

                elif token == "c" and ciphertext and not written[2]:
                    c_file.write(ciphertext)
                    written[2] = True

    # Plaintext deve ser uma binary string! b'...
    def AES_enc(self, plaintext: bytes) -> bytes:
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC)

        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
       
        self.write_pieces(key, cipher.iv, ciphertext, seq='kic')
        
        return ciphertext
        
    # Ciphertext deve ser uma binary string também
    def AES_dec(self, ciphertext=None) -> str:
        key, iv, ciphertext_ = self.read_pieces()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext if ciphertext else ciphertext_), AES.block_size)

        return plaintext.decode('utf-8')