from certificate import Certificate

class Account(Certificate):
    def __init__(self,issuerPublicKey):
        super().__init__(issuerPublicKey)
        self.pebbleAmount=20