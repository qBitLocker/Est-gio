from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes

from base64 import b64encode, b64decode

import bcrypt
import os
# Uma classe que contem o algoritmo AES
# Tambem e projetado para que se possa implementar outros
# algoritmos no futuro, como RSA, Blowfish, etc...
# - A Chave e gerada aleatóriamente no local especificado no construtor da classe

# - As informações sao armazenada em um arquivo binario criptografado!
class CipherTools():
    # Construtor da classe
    def __init__ (self, path: str=None, filename: str=None):
        default_path = os.path.join(os.getcwd(), 'security', 'secret')
        self.path = default_path if not path else path if os.path.exists(path) else default_path
        default_filename = 'cipher_file.bin'

        if self.__check_str__(filename):
            leaf = filename.split('\\')[-1].split('/')[-1]
            self.filename = default_filename if not filename else default_filename if not leaf else leaf
        else:

            self.filename = default_filename

        self.target = os.path.join(self.path, self.filename)
        self.gen_salt = 12

    # Verifica se o atributo e uma string e nao nula
    def __check_str__(self, attribute: str) -> bool:
        if not attribute:
            return False
        if not isinstance(attribute, str):
            return False
        return True
    
    def __check_bytes__(self, attribute: bytes) -> bool:    
        if not attribute:
            return False
        if not isinstance(attribute, bytes):
            return False
        return True

    def __str__ (self):
        return f"CipherTools(path={self.path}, filename={self.filename}, target={self.target})\n" + \
                "CipherTools.read_pieces\n" + \
                "CipherTools.AES_enc\n" + \
                "CipherTools.AES_dec\n" + \
                "CipherTools.Bcrypt_enc\n" + \
                "CipherTools.Bcrypt_match\n" + \
                "CipherTools.set_filename\n" + \
                "CipherTools.set_path\n" + \
                "CipherTools.get_filename\n" + \
                "CipherTools.get_path\n" + \
                "CipherTools.get_target\n"
                
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
        
    # Ciphertext deve ser uma binary string tambem
    def AES_dec(self, ciphertext=None) -> str:
        key, iv, ciphertext_ = self.read_pieces()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext if ciphertext else ciphertext_), AES.block_size)
        return plaintext.decode('utf-8')

    # Implementaçao do Bcrypt - Algoritmo de hash de senha baseado em Blowfish
    def Bcrypt_enc(self, plaintext: bytes) -> bytes:
        if not self.__check_bytes__(plaintext):
            raise ValueError("[ERROR] Tipo de dado invalido para plaintext")
        return bcrypt.hashpw(plaintext, bcrypt.gensalt(self.gen_salt))
    
    def Bcrypt_match(self, ciphertext: bytes, hash: bytes) -> bool:
        if self.__check_bytes__(ciphertext) and self.__check_bytes__(hash):
            return bcrypt.checkpw(ciphertext, hash)
        else:
            raise ValueError("[ERROR] Tipo de dado invalido para ciphertext ou hash")
        
    def Base64_enc(self, plaintext: bytes) -> bytes:
        if not self.__check_bytes__ (plaintext):
            raise ValueError("[ERROR] Tipo de dado invalido para plaintext")
        return b64encode(plaintext)
    
    def Base64_dec(self, ciphertext: bytes) -> bytes:
        if not self.__check_bytes__(ciphertext):
            raise ValueError("[ERROR] Tipo de dado invalido para ciphertext")
        return b64decode(ciphertext).decode('utf-8')




    # > Metodos Setters
    def set_filename(self, filename: str):
        if not self.__check_str__(filename):
            raise ValueError("[ERROR] Tipo de dado invalido para filename")

        default_filename = 'cipher_file.bin'
        leaf = filename.split('\\')[-1].split('/')[-1]

        self.filename = default_filename if not filename else default_filename if not leaf else leaf

        # Atualiza o target com o novo filename
        self.target = os.path.join(self.path, self.filename)

    def set_path(self, path: str):
        if not self.__check_str__(path):
            raise ValueError("[ERROR] Tipo de dado invalido para path")

        default_path = os.path.join(os.getcwd(), 'security', 'secret')
        self.path = default_path if not path else path if os.path.exists(path) else default_path

        # Atualiza o target com o novo path e filename
        self.target = os.path.join(self.path, self.filename)



    # > Metodos Getters
    def get_filename(self):
        return self.filename

    def get_path(self):
        return self.path

    def get_target(self):
        return self.target