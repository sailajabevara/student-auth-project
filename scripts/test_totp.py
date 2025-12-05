# from app.crypto_utils import decrypt_seed, load_private_key
# from app.totp_utils import generate_totp_code

# def main():
#     # Read encrypted seed from file
#     encrypted_seed_b64 = open("encrypted_seed.txt").read().strip()

#     # Decrypt the seed using your private key
#     private_key = load_private_key()
#     hex_seed = decrypt_seed(encrypted_seed_b64, private_key)

#     print("Decrypted Seed:", hex_seed)

#     # Generate TOTP code
#     code = generate_totp_code(hex_seed)
#     print("TOTP Code:", code)

# if __name__ == "__main__":
#     main()

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.crypto_utils import decrypt_seed, load_private_key
from app.totp_utils import generate_totp_code

def main():
    encrypted_seed_b64 = open("encrypted_seed.txt").read().strip()

    private_key = load_private_key()
    hex_seed = decrypt_seed(encrypted_seed_b64, private_key)
    print("Decrypted Seed:", hex_seed)

    code = generate_totp_code(hex_seed)
    print("TOTP Code:", code)

if __name__ == "__main__":
    main()
