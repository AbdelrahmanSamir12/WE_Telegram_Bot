from Crypto.Cipher import AES
import base64


class WEPasswordEncryptor:
    def __init__(self):
        self.key = "0f0e0d0c0b0a09080706050403020100"
        self.iv = "000102030405060708090a0b0c0d0e0f"
        self.key = bytes.fromhex(self.key)
        self.iv = bytes.fromhex(self.iv)
        self.aes = AES.new(self.key, AES.MODE_CBC, self.iv)
    
    def encrypt(self, plaintext):
        padded_data = self.pkcs7pad(plaintext.encode('utf-8'))
        ciphertext = self.aes.encrypt(padded_data)
        return base64.b64encode(ciphertext).decode('utf-8')
    
    def utf8_to_bytes(self, utf8_str):
        return utf8_str.encode('utf-8')
    
    def hex_to_bytes(self, hex_str):
        return bytes.fromhex(hex_str)
    
    def pkcs7pad(self, data):
        block_size = AES.block_size
        padding_size = block_size - len(data) % block_size
        padding = bytes([padding_size] * padding_size)
        return data + padding

# Usage example

# plaintext = "h"

# encryptor = WEPasswordEncryptor()
# encrypted_text = encryptor.encrypt(plaintext)
# print("Encrypted:", encrypted_text)
