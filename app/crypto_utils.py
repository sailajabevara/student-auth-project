import base64
import re
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def load_private_key(path: str):
    with open(path, "rb") as f:
        data = f.read()
    private_key = serialization.load_pem_private_key(
        data,
        password=None,
    )
    return private_key


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP(SHA-256)
    and return 64-char hex string.
    """
    # 1. Base64 decode
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    # 2. RSA OAEP decrypt
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # 3. Decode UTF-8
    seed = decrypted_bytes.decode("utf-8").strip()

    # 4. Validate 64-char hex
    if len(seed) != 64:
        raise ValueError("Invalid seed length")
    if not re.fullmatch(r"[0-9a-f]{64}", seed):
        raise ValueError("Seed is not valid lowercase hex")

    return seed
