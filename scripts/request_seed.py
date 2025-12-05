import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id, github_repo_url):
    # 1. Read public key exactly as text
    with open("student_public.pem", "r") as f:
        public_key_text = f.read()

    # 2. Prepare JSON body
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_text
    }

    # 3. Send POST request
    response = requests.post(API_URL, json=payload)

    # 4. Convert response to Python dict
    data = response.json()

    if data.get("status") != "success":
        print("ERROR from API:\n", data)
        return

    encrypted_seed = data["encrypted_seed"]

    # 5. Save encrypted seed to file
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)

    print("✅ Encrypted seed saved to encrypted_seed.txt")


# ================================
# RUN IT HERE
# ================================
if __name__ == "__main__":
    request_seed(
        student_id="23P31A4207",
        github_repo_url="https://github.com/sailajabevara/student-auth-project"
    )
