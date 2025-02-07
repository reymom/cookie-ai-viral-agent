import subprocess

from backend.crypto.metadata import generate_metadata


def mint_nft_js(recipient_wallet, name, description, image_url, symbol, seller_fee, attributes=None):
    """Generates metadata and calls JavaScript NFT minting script with custom parameters."""

    metadata_uri = generate_metadata(
        name, description, image_url, symbol, attributes)

    subprocess.run([
        "node", "../solana/mint_nft.js",
        recipient_wallet, metadata_uri, name, symbol, str(seller_fee)
    ])
