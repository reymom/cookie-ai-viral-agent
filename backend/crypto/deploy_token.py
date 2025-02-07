import subprocess
import random
import os
import json
from uploader.pinata import upload_to_pinata, METADATA_DIR

from dotenv import load_dotenv
load_dotenv("../solana/.env")

script_path = os.path.abspath("../solana/deploy_token.js")
print(f"✅ Running JS Script at: {script_path}")
if not os.path.exists(script_path):
    raise RuntimeError(f"❌ JavaScript file not found: {script_path}")

os.makedirs(METADATA_DIR, exist_ok=True)


def deploy_spl_token_js(video_topic):
    """Deploys a Solana SPL token using the JavaScript script."""

    token_name = f"OBFUSCAT {video_topic[:8]} {random.randint(0, 1000000)}"
    token_symbol = f"OBF{random.randint(10, 99)}"
    decimals = 6
    total_supply = 1_000_000_000
    royalties = 500

    # ✅ Upload Metadata to IPFS
    metadata = {
        "name": token_name,
        "symbol": token_symbol,
        "description": f"Community engagement token for {video_topic}.",
        "decimals": decimals,
        "total_supply": total_supply,
        "royalties": royalties
    }
    metadata_filename = f"{token_name.replace(' ', '_')}.json"
    metadata_path = os.path.join(METADATA_DIR, metadata_filename)
    with open(metadata_path, "w") as file:
        json.dump(metadata, file, indent=4)

    print(f"✅ Metadata saved: {metadata_path}")

    metadata_uri = upload_to_pinata(metadata_path)

    if not metadata_uri:
        raise RuntimeError("❌ Failed to upload token metadata to IPFS!")

    print(f"✅ Metadata uploaded to IPFS: {metadata_uri}")

    # ✅ Call JavaScript script to deploy token
    result = subprocess.run([
        "node", "../solana/deploy_token.js",
        metadata_uri, token_name, token_symbol, str(
            decimals), str(total_supply)
    ], capture_output=True, text=True)

    print(f"✅ JavaScript Execution Output:\n{result.stdout.strip()}")
    print(f"❌ JavaScript Execution Errors:\n{result.stderr.strip()}")

    if result.returncode != 0:
        print(f"❌ JavaScript Error Output:\n{result.stdout.strip()}")
        raise RuntimeError("JavaScript execution failed.")

    return result.stdout.strip()
