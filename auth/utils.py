import hashlib
import os
import secrets

def hash_password(password: str) -> str:
    """
    Hashea una contraseña de forma segura usando PBKDF2 con HMAC SHA-256.
    Retorna el hash con el formato salt$hash.
    """
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${pwd_hash}"

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifica una contraseña provista contra su hash guardado.
    """
    try:
        salt, pwd_hash = password_hash.split('$')
        computed_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(computed_hash, pwd_hash)
    except Exception:
        return False

def generate_session_token() -> str:
    """
    Genera un token de sesión seguro y único de alta entropía.
    """
    return secrets.token_urlsafe(32)
