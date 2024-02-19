import hashlib


class HashPassword:
    
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
