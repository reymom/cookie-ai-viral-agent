import { Metaplex, keypairIdentity } from "@metaplex-foundation/js";
import { Connection, Keypair, clusterApiUrl } from "@solana/web3.js";

import dotenv from "dotenv";
import fs from "fs";

// Load environment variables
dotenv.config();

// Load Solana wallet keypair
const walletPath = process.env.SOLANA_WALLET_PATH || "/home/reymon/.config/solana/id.json";
const walletData = fs.readFileSync(walletPath, "utf8");
const payer = Keypair.fromSecretKey(new Uint8Array(JSON.parse(walletData)));

// Connect to Solana Devnet
const connection = new Connection(clusterApiUrl("devnet"));
const metaplex = Metaplex.make(connection).use(keypairIdentity(payer));

// Function to Mint an NFT
async function mintNFT(recipientAddress, metadataUri, name, symbol, sellerFee) {
  try {
    console.log(`Minting NFT: ${name} (${symbol}) for recipient: ${recipientAddress}...`);
    console.log(`Metadata URI: ${metadataUri}`);

    // Mint NFT
    const { nft } = await metaplex.nfts().create({
      uri: metadataUri,
      name: name,
      symbol: symbol,
      sellerFeeBasisPoints: 500, // 5% royalties
      maxSupply: 1,
      creators: [{ address: payer.publicKey, share: 100 }],
    });

    console.log(`✅ NFT Minted Successfully! Address: ${nft.address.toBase58()}`);
    return nft.address.toBase58();
  } catch (error) {
    console.error("❌ Error minting NFT:", error);
  }
}

// Handle CLI arguments for minting
const args = process.argv.slice(2);
if (args.length < 5) {
  console.error("❌ Usage: node mint_nft.js <recipient_wallet> <metadata_uri> <name> <symbol> <seller_fee>");
  process.exit(1);
}

const [recipient, metadataUri, name, symbol, sellerFee] = args;
mintNFT(recipient, metadataUri, name, symbol, parseInt(sellerFee));