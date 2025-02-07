# 🎬 Obfuscated Cat Agent - Viral Meme Video Generator 🚀

🔹 An AI-powered system that generates viral meme videos, mints Solana NFTs & meme coins, and distributes them based on engagement.

## 📌 Overview

Obfuscated Cat AI is an autonomous agent that:

- Generates viral meme videos based on trending topics (Cookie DataSwarm API)
- Uploads videos & images to IPFS for decentralized storage
- Mints NFTs & meme coins on Solana for each video
- Distributes tokens based on Twitter engagement (likes, retweets, reach, etc.)

🛠 Built for the Cookie DeFAI Hackathon, leveraging AI-driven content creation & crypto tokenomics.

## 📜 Monetization Strategy 💰

The project creates NFTs & meme coins for each video, allowing for multiple revenue streams:

### NFT Sales 🎨

- Each video has a dedicated NFT collection, with:
- One NFT per image in the video
- One NFT for the video itself
- Exclusive rewards for NFT holders (e.g., future airdrops, premium content)
- Sold via Solana marketplaces (Magic Eden, Tensor, etc.)

### Meme Coin Tokenomics 🪙

- Each video mints a unique meme coin, named OBFUSCAT#1, OBFUSCAT#2, etc.
- A global token $OBFUSCAT represents the entire AI bot economy.
- Engagement-based airdrops:
- Retweets, likes, and comments earn tokens (using Cookie Data API)
- Influencers get higher rewards based on their network effect
- Future integration with DEX liquidity pools to allow trading of video-specific meme coins.

### Brand & Community Growth 📢

- Sponsorships & partnerships (brands can pay for AI-generated videos)
- Viral meme campaigns boost adoption of the $OBFUSCAT ecosystem.

## ⚙️ Current Features & Status ✅

### 🎥 Video Generation & AI Content Creation

- ✅ Trending topics fetched via Cookie DataSwarm API
- ✅ AI-generated prompts for video content
- ✅ Stable Diffusion XL creates images
- ✅ AI-generated voiceovers for storytelling
- ✅ Jamendo API integration for background music

### 📀 IPFS & Metadata Storage

- ✅ Images & videos uploaded to Pinata IPFS
- ✅ Metadata stored & linked to NFTs

### 🎭 NFT Minting & Token Creation

- ✅ Mint NFTs on Solana for video content
- ✅ Deploy meme coins per video

### ⏳ Future Tasks & Improvements

- 🚧 Automate twitter and youtube engagement tracking
- 🚧 Automated token airdrop system
- 🚧 DEX liquidity pools for meme coins
- 🚧 Community leaderboard for engagement rewards

## 🔗 Related Repositories

This project consists of multiple components working together:

### 🎬 AI Video Generator

- **Repository:** [ai-video-generator](https://github.com/reymom/ai-video-generator)
- **Description:** This is the **video generation engine** that powers Obfuscated Cat Agent.
- **Functionality:**
  - Generates AI-powered images & videos
  - Uses **Stable Diffusion** for image generation
  - Integrates **AI voice synthesis** for narration
  - Compiles video with background music (Jamendo API)

⚡ **The AI Video Generator is responsible for generating all multimedia assets used in our viral meme automation pipeline.**

## **🚀 How to Run (Step-by-Step Testing)**

### 1️. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 2️. Start Redis & Celery Workers

```bash
redis-server
```

```bash
celery -A config.celery worker --loglevel=info
```

```bash
celery -A config.celery beat --loglevel=info
```

### 3. Running Individual Tasks for Testing

#### 🎯 Fetch Trending Topics (Cookie DataSwarm API)

```bash
celery -A config.celery call fetch_trending_topic --args='["ai agents", 7]'
```

- Description: Fetches trending Web3 topics from Cookie DataSwarm API.
- Purpose: Used to generate AI content automatically.

#### 🎙️ Generate AI Voice-Over

```bash
python -m scripts.test_create_voices
```

Generates AI voiceovers for video content.

#### Generate Video Specs

```bash
celery -A config.celery call generate_video_specs_task
```

- Description: Creates structured video specifications including: Image prompts, Subtitles, Audio settings.

#### Create Images (AI-Generated)

```bash
celery -A tasks.generate_video create_images
```

- Description: Generates images using AI (Stable Diffusion) based on trending topics.

### **4. Running a Manual Upload If Needed**

If the **upload task fails**, you can manually trigger the upload.

```bash
# Read the last generated video path
video_path=$(cat /path/to/video_execution_folder/video_path.log)

# Manually trigger upload
celery -A tasks.upload_task upload_video_task --args="('$video_path', 'youtube')"
```

Uploads the generated video to YouTube or Twitter.

### 5. Deploy SPL Token for a Video

```bash
python -m scripts.test_deploy_token
```

🔹 Purpose: Deploys a Solana SPL Token for each video, allowing for tokenized engagement.

🔹 Expected Output Example:

```bash
🔍 Testing SPL Token Deployment...
✅ Metadata saved: ../solana/metadata/OBFUSCAT_Test_Vid_805020.json
✅ File uploaded to IPFS: ../solana/metadata/OBFUSCAT_Test_Vid_805020.json -> ipfs://QmPPrvz6SYjuRobvuzSKUvZPj84qoL421shPGyiXcHNxtN
✅ Metadata uploaded to IPFS: ipfs://QmPPrvz6SYjuRobvuzSKUvZPj84qoL421shPGyiXcHNxtN
🚀 Deploying SPL Token: OBFUSCAT Test Vid 805020 (OBF95)...
✅ Successfully minted 1000000000 OBF95 to kWn3a7p5NrGhW9KUeTrAgw5W9jkAfDXFhZpVrW1T2id
🎉 Token Mint Address: HS6B26Ckd5nLch5vvCBsJCjfKVtyoJF7RT2kvMmyFQPF
```

## 🔥 Tokenized Engagement System (Solana SPL Token)

Each AI-generated video is tokenized on Solana as an SPL token.
This allows for on-chain engagement rewards and future monetization.

📌 Example Token

- Name: OBFUSCAT Test Vid
- Symbol: OBF95
- Decimals: 6
- Total Supply: 1,000,000,000
- Metadata: [ipfs://QmPPrvz6SYjuRobvuzSKUvZPj84qoL421shPGyiXcHNxtN](ipfs://QmPPrvz6SYjuRobvuzSKUvZPj84qoL421shPGyiXcHNxtN)

- 🔗 View on Solana Explorer
- 🔗 Solana Explorer: [HS6B26Ckd5nLch5vvCBsJCjfKVtyoJF7RT2kvMmyFQPF](https://explorer.solana.com/address/HS6B26Ckd5nLch5vvCBsJCjfKVtyoJF7RT2kvMmyFQPF?cluster=devnet)

## 🚀 Future Directions

This project aims to combine AI-generated viral content with decentralized tokenomics.
Upcoming features include:

- Fully automated Twitter engagement tracking & airdrops
- Integration with Solana DEXs for meme coin trading
- Gamification & community leaderboard for top engagers

📢 Join the revolution – viral AI videos + Web3 tokenomics! 🚀

## 📜 Hackathon Summary

This project was built for the Cookie DeFAI Hackathon, showcasing how AI & Web3 can work together to incentivize engagement using on-chain rewards.

> 🚀 Viral memes, AI-generated content, and crypto rewards – welcome to the Obfuscated Cat Agent! 😼🎬
