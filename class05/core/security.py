from passlib.context import CryptContext

CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

def check_password(password: str, hash_password: str) -> bool:
    """
    Function to check if the password is correct. Comparing if the raw text informed by user and 
    the password hash that is saved in the database during the user creation
    """
    return CRYPTO.verify(password, hash_password)

def generate_password_hash(password: str) -> str:
    """
    Function that generates and returns the password hash
    """
    return CRYPTO.hash(password)

