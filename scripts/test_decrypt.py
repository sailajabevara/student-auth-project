import os
import sys
from pathlib import Path

# Add project root (folder containing "app" and "scripts") to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.crypto_utils import load_private_key, decrypt_seed


def main():
    encrypted_seed_b64 = Path("encrypted_seed.txt").read_text(encoding="utf-8").strip()
    private_key = load_private_key()
    seed_hex = decrypt_seed(encrypted_seed_b64, private_key)
    print("Decrypted seed:", seed_hex)


if __name__ == "__main__":
    main()


# import sys
# import os

# # Add project root folder to path
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# from app.crypto_utils import decrypt_seed, load_private_key

# PRIVATE_KEY_PATH = "student_private.pem"
# ENCRYPTED_SEED_PATH = "encrypted_seed.txt"

# def main():
#     with open(ENCRYPTED_SEED_PATH, "r") as f:
#         encrypted_seed = f.read().strip()

#     private_key = load_private_key(PRIVATE_KEY_PATH)

#     hex_seed = decrypt_seed(encrypted_seed, private_key)

#     print("\n✅ Seed successfully decrypted")
#     print("✅ Stored at /data/seed.txt")
#     print("\nHex seed:", hex_seed)

# if __name__ == "__main__":
#     main()
