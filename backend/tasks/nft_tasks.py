import os
import random

from config.celery import app, logger
from backend.crypto.mint_nft import mint_nft_js
from uploader.pinata import upload_to_pinata
from crypto.deploy_token import deploy_spl_token


@app.task(name="generate_nft_metadata_and_mint")
def generate_nft_metadata_and_mint(topic, video_path, image_paths):
    """Uploads video & images to IPFS, generates metadata, and mints NFTs on Solana."""

    logger.info(f"🖼 Uploading video & images to IPFS for NFT minting...")

    token_address = deploy_spl_token(topic)

    logger.info(f"✅ Meme Coin Deployed: {token_address}")

    # 🔹 Upload Video to IPFS
    video_ipfs_cid = upload_to_pinata(video_path)
    if not video_ipfs_cid:
        logger.error(f"❌ Failed to upload video to IPFS!")
        return

    logger.info(f"✅ Video uploaded to IPFS: {video_ipfs_cid}")

    # 🔹 Mint Video NFT (metadata generated inside mint_nft_js)
    mint_nft_js(
        recipient_wallet=os.getenv("SOLANA_TREASURY"),
        name=f"OBFUSCAT#V{random.randint(0, 1000000)}",
        description=f"AI-generated video on {topic}.",
        image_url=video_ipfs_cid,
        symbol=f"OBFUSCAT#V{random.randint(0, 1000000)}",
        seller_fee=500,  # 5% royalties
        attributes=[{"trait_type": "Type", "value": "Video"}]
    )

    logger.info(f"✅ Video NFT minted successfully!")

    # 🔹 Process Each Image for NFT Minting
    for i, image_path in enumerate(image_paths):
        image_ipfs_cid = upload_to_pinata(image_path)
        if not image_ipfs_cid:
            logger.error(f"❌ Failed to upload image {i} to IPFS!")
            continue

        logger.info(f"✅ Image {i} uploaded to IPFS: {image_ipfs_cid}")

        # 🔹 Mint Image NFT (metadata generated inside mint_nft_js)
        mint_nft_js(
            recipient_wallet=os.getenv("SOLANA_TREASURY"),
            name=f"OBFUSCAT#I{random.randint(0, 1000000)}",
            description=f"AI-generated image for {topic}.",
            image_url=image_ipfs_cid,
            symbol=f"OBFUSCAT#I{random.randint(0, 1000000)}",
            seller_fee=500,  # 5% royalties
            attributes=[{"trait_type": "Type", "value": "Image"}]
        )

        logger.info(f"✅ Image {i+1} NFT minted successfully!")

    logger.info("✅ All NFTs successfully minted!")
