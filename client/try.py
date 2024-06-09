from mbedtls import pk, hmac, hashlib, cipher
import time
import os
import base64

# Constants
RSA_SIZE = 256
EXPONENT = 65537

SECRET_KEY = b"Fj2-;wu3Ur=ARl2!Tqi6IuKM3nG]8z1+"
hmac_key = hashlib.sha256(SECRET_KEY).digest()
hmac_key = hmac.new(hmac_key, digestmod="SHA256")

def client_send(buf: bytes):
    hmac_key.update(buf)
    buf += hmac_key.digest()
    # Here you would implement sending the buffer over the network

def client_receive(size: int) -> bytes:
    buffer = recv(size + hmac_key.digest_size)
    hmac_key.update(buffer[0:size])
    if buffer[size:size + hmac_key.digest_size] != hmac_key.digest():
        print("Hash Error")
        exit(1)
    return buffer

def generate_rsa_key():
    client_rsa = pk.RSA()
    client_rsa.generate(RSA_SIZE * 8, EXPONENT)
    public_key = client_rsa.export_public_key()
    return client_rsa, public_key

def exchange_public_keys(server_public_key):
    client_rsa, client_public_key = generate_rsa_key()
    
    # Send client's public key to server
    client_send(client_public_key)
    
    # Receive server's public key
    buffer = client_receive(2 * RSA_SIZE)
    server_public_key = client_rsa.decrypt(buffer[0:RSA_SIZE])
    server_public_key += client_rsa.decrypt(buffer[RSA_SIZE: 2 * RSA_SIZE])
    server_rsa = pk.RSA().from_DER(server_public_key)
    
    # Encrypt and send client's public key and signature to server
    buffer = client_rsa.export_public_key() + client_rsa.sign(SECRET_KEY, "SHA256")
    buffer = server_rsa.encrypt(buffer[0:184]) + server_rsa.encrypt(buffer[184:368]) + server_rsa.encrypt(buffer[368:550])
    client_send(buffer)
    
    # Receive server's response
    buffer = client_receive(RSA_SIZE)
    if b"DONE" == client_rsa.decrypt(buffer):
        # Send signature to server
        buffer = client_rsa.sign(SECRET_KEY, "SHA256")
        buffer = server_rsa.encrypt(buffer[0:RSA_SIZE//2]) + server_rsa.encrypt(buffer[RSA_SIZE//2: RSA_SIZE])
        client_send(buffer)
        
        # Receive session ID from server
        buffer = client_receive(RSA_SIZE)
        session_id = client_rsa.decrypt(buffer)
        return session_id

    return None
