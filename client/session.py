from mbedtls import pk, hmac, hashlib, cipher
import protocol

class Session:
    # Class-level constants
    RSA_SIZE = 256
    EXPONENT = 65537
    __SESSION_ID: bytes
    state = None
    
    SECRET_KEY = b"Fj2-;wu3Ur=ARl2!Tqi6IuKM3nG]8z1+"
    __SESSION_TEMPERATURE = 0x03
    __SESSION_TOGGLE_LED = 0x02
    __SESSION_OKAY = 0x00
    __SESSION_CLOSE = 0x04
    
    def __init__(self, port):
        self.__SESSION_ID = bytes(8 * [0])  # Session ID, initialized to 8 bytes
        
        # Initialize HMAC with the secret key
        self.HMAC_CS = hashlib.sha256()
        self.HMAC_CS.update(self.SECRET_KEY)
        self.HMAC_CS = self.HMAC_CS.digest()
        self.HMAC_CS = hmac.new(self.HMAC_CS, digestmod="SHA256")
        self.state = port

        # Initialize protocol with the specified port
        if protocol.protocol_init(port):
            self.__clientRSA = pk.RSA()
            self.__clientRSA.generate(Session.RSA_SIZE * 8, Session.EXPONENT)
            
            if self.send(self.__clientRSA.export_public_key()):
                buffer = self.receive(2 * Session.RSA_SIZE)
                if 0 < len(buffer):
                    server_pk = self.__clientRSA.decrypt(buffer[0:Session.RSA_SIZE])
                    server_pk += self.__clientRSA.decrypt(buffer[Session.RSA_SIZE:2*Session.RSA_SIZE])
                    self.__serverRSA = pk.RSA().from_DER(server_pk)
                    
                    del self.__clientRSA
                    
                    self.__clientRSA = pk.RSA()
                    self.__clientRSA.generate(Session.RSA_SIZE * 8, Session.EXPONENT)
                    
                    buffer = self.__clientRSA.export_public_key() + self.__clientRSA.sign(Session.SECRET_KEY, "SHA256")
                    buffer = self.__serverRSA.encrypt(buffer[0:184]) + self.__serverRSA.encrypt(buffer[184:368]) + self.__serverRSA.encrypt(buffer[368:550])
                    self.state = True 
                    if self.send(buffer):
                        buffer = self.receive(Session.RSA_SIZE)
                        if 0 < len(buffer):
                            if b"OKAY" == self.__clientRSA.decrypt(buffer):
                                self.establish()
                            else:
                                raise Exception("Temporary client public key response mismatch")
                        else:
                            raise Exception("Failed to receive the temporary client public key response")
                    else:
                        raise Exception("Failed to send the encrypted temporary client public key")
                else:
                    raise Exception("Failed to receive the server public key")
            else:
                raise Exception("Failed to send the initial client public key")
        else:
            raise Exception("Connection Error")
  
    def select():
        """
        Static method to check the current state of the session.
        Returns:
            bool: True if the session state is not None, otherwise False.
        """
        return Session.state

    def __bool__(self):
        """
        Method to check if the session ID is non-zero, indicating an active session.
        Returns:
            bool: True if the session ID is non-zero, otherwise False.
        """
        return (0 != int.from_bytes(self.__SESSION_ID, 'little'))

    def send(self, buf: bytes) -> bool:
        # Update HMAC with the buffer and append the HMAC digest
        self.HMAC_CS.update(buf)
        buf += self.HMAC_CS.digest()
        return protocol.protocol_send(buf)

    def receive(self, size: int) -> bytes:
        # Receive data with HMAC digest from the protocol
        buffer = protocol.protocol_receive(size + self.HMAC_CS.digest_size)
        self.HMAC_CS.update(buffer[0:size])

        # Verify HMAC and return the buffer if valid, otherwise return empty bytes
        if buffer[size:size + self.HMAC_CS.digest_size] == self.HMAC_CS.digest():
            return buffer[0:size]
        else:
            return b''
    
    def establish(self):
        try:
            buffer = self.__clientRSA.sign(self.SECRET_KEY, "SHA256")
            buffer = self.__serverRSA.encrypt(buffer[0:self.RSA_SIZE//2]) + self.__serverRSA.encrypt(buffer[self.RSA_SIZE//2:self.RSA_SIZE])
            self.send(buffer)
            
            buffer = self.receive(self.RSA_SIZE)  
            buffer = self.__clientRSA.decrypt(buffer)
            self.__SESSION_ID = buffer[0:8]
            self.aes = cipher.AES.new(buffer[24:56], cipher.MODE_CBC, buffer[8:24])
            self.state = True  # Session established successfully
        except Exception as e:
            self.state = False  # Session establishment failed
            print(e)
            
    def get_temperature(self):
        recieved = self.request(int(self.__SESSION_TEMPERATURE))
        return recieved
    
    def toggle_led(self):
        recieved = self.request(int(self.__SESSION_TOGGLE_LED))
        return recieved
            
    def request(self, message):
        request = bytes([message]) 
        buffer = request + self.__SESSION_ID
        plen = cipher.AES.block_size - (len(buffer) % cipher.AES.block_size)
        buffer = self.aes.encrypt(buffer + bytes([len(buffer)] * plen))
        if True == self.send(buffer):

            buffer = self.receive(cipher.AES.block_size)
            buffer = self.aes.decrypt(buffer)

            if buffer[0] == self.__SESSION_OKAY:
                return buffer[1:6]
            else:
                return None