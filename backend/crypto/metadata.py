import json
import os
from datetime import datetime, timezone

from uploader.pinata import upload_to_pinata, METADATA_DIR


def generate_metadata(name, description, file_uri, symbol, attributes=None):
    """Generates NFT metadata and uploads to IPFS."""
    metadata = {
        "name": name,
        "symbol": symbol,
        "description": description,
        "image": file_uri,
        "attributes": attributes + [
            {"trait_type": "Engagement Score", "value": 100},
            {"trait_type": "Date", "value": datetime.now(
                timezone.utc).isoformat()}
        ],
    }

    metadata_filename = f"{name.replace(' ', '_').lower()}.json"
    metadata_path = os.path.join(METADATA_DIR, metadata_filename)

    with open(metadata_path, "w") as file:
        json.dump(metadata, file, indent=4)

    print(f"✅ Metadata saved: {metadata_path}")

    # Upload metadata to IPFS
    metadata_uri = upload_to_pinata(metadata_path)

    return metadata_uri or f"file://{metadata_path}"
