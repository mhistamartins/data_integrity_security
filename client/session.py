from mbedtls.cipher import AES
from mbedtls import pk, hmac, hashlib
import os

# Constants
RSA_SIZE = 256
EXPONENT = 65537
AES_KEY_SIZE = 32  # 256 bits
AES_IV_SIZE = 16   # 128 bits

SECRET_KEY = b"Fj2-;wu3Ur=ARl2!Tqi6IuKM3nG]8z1+"
hmac_key = hashlib.sha256(SECRET_KEY).digest()

class SecureSession:
    def __init__(self):
        # Initialize private key for RSA encryption/decryption
        self.private_key = pk.RSA()

        # Initialize public key (to be set when loaded or generated)
        self.public_key = None

        # Initialize AES key and initialization vector (IV)
        self.aes_key = None
        self.aes_iv = None

        # Initialize HMAC key for message authentication
        self.hmac_key = hmac.new(hmac_key, digestmod="sha256")
        
    # Generate RSA private/public key pair.
    def generate_rsa_keys(self):
        self.private_key.generate(key_size=2048, exponent=EXPONENT)
        self.public_key = self.private_key.export_public_key(format="pem")

    # Load peer's public key for RSA encryption.
    def load_peer_public_key(self, peer_public_key_pem):
        self.peer_public_key = pk.RSA()
        self.peer_public_key.import_key(peer_public_key_pem)

    # Encrypt data with peer's public key using RSA.
    def encrypt_with_peer_rsa(self, data):
        return self.peer_public_key.encrypt(data)

    # Decrypt data with own private key using RSA.
    def decrypt_with_private_rsa(self, data):
        return self.private_key.decrypt(data)

    # Generate AES key and initialization vector (IV).
    def generate_aes_key_iv(self):
        self.aes_key = os.urandom(AES_KEY_SIZE)
        self.aes_iv = os.urandom(AES_IV_SIZE)
        return self.aes_key, self.aes_iv

    # Encrypt data with AES using the generated key and IV.
    def encrypt_with_aes(self, data):
        aes_cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=self.aes_iv)
        padded_data = self.pad(data)
        return aes_cipher.encrypt(padded_data)

    # Decrypt data with AES using the generated key and IV.
    def decrypt_with_aes(self, data):
        aes_cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=self.aes_iv)
        decrypted_data = aes_cipher.decrypt(data)
        return self.unpad(decrypted_data)

    # Sign data with HMAC using the pre-generated key.
    def hmac_sign(self, data):
        return self.hmac_key.update(data).digest()

    # Verify HMAC signature of data.
    def hmac_verify(self, data, signature):
        self.hmac_key.update(data)
        return hmac.compare_digest(self.hmac_key.digest(), signature)

    # @staticmethod
    # def pad(data):
    #     """Pad data to be a multiple of the AES block size."""
    #     pad_len = AES_IV_SIZE - len(data) % AES_IV_SIZE
    #     return data + bytes([pad_len] * pad_len)

    # @staticmethod
    # def unpad(data):
    #     """Unpad data by removing the padding added during encryption."""
    #     pad_len = data[-1]
    #     return data[:-pad_len]
