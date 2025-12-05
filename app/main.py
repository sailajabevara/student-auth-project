from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from app.crypto_utils import load_private_key, decrypt_seed
from app.totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()

PRIVATE_KEY_PATH = "student_private.pem"
SEED_PATH = "/data/seed.txt"


class DecryptRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/decrypt-seed")
def decrypt_seed_api(req: DecryptRequest):
    try:
        private_key = load_private_key(PRIVATE_KEY_PATH)
        hex_seed = decrypt_seed(req.encrypted_seed.strip(), private_key)

        os.makedirs("/data", exist_ok=True)
        with open(SEED_PATH, "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_PATH, "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    return {"code": code, "valid_for": 30}


@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_PATH, "r") as f:
        hex_seed = f.read().strip()

    valid = verify_totp_code(hex_seed, req.code)
    return {"valid": valid}
