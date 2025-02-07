import os
import requests
from dotenv import load_dotenv

load_dotenv()
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY")
PINATA_API_URL = "https://api.pinata.cloud/pinning"

# Define metadata storage path
METADATA_DIR = "../solana/metadata/"
os.makedirs(METADATA_DIR, exist_ok=True)


def upload_to_pinata(file_path):
    """Uploads a file (image or video) to IPFS via Pinata.."""
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_KEY
    }

    with open(file_path, "rb") as file:
        response = requests.post(
            f"{PINATA_API_URL}/pinFileToIPFS",
            headers=headers,
            files={"file": file}
        )

    if response.status_code == 200:
        cid = response.json()["IpfsHash"]
        print(f"✅ File uploaded to IPFS: {file_path} -> ipfs://{cid}")
        return f"ipfs://{cid}"
    else:
        print("❌ File Upload Failed:", response.json())
        return None
