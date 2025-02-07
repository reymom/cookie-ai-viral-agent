import { percentAmount, generateSigner, signerIdentity, createSignerFromKeypair } from "@metaplex-foundation/umi";
import { TokenStandard, createAndMint, mplTokenMetadata } from "@metaplex-foundation/mpl-token-metadata";
import { createUmi } from "@metaplex-foundation/umi-bundle-defaults";
import bs58 from "bs58";
import dotenv from "dotenv";

dotenv.config();

// Ensure proper usage
if (process.argv.length < 7) {
    console.error("Usage: node deploy_token.js <metadataUri> <name> <symbol> <decimals> <totalSupply>");
    process.exit(1);
}

// Read parameters from Python call
const [metadataUri, name, symbol, decimals, totalSupply] = process.argv.slice(2);

// Setup Solana Connection
const umi = createUmi(process.env.SOLANA_RPC_URL);

const treasuryKeypair = umi.eddsa.createKeypairFromSecretKey(
    new Uint8Array(bs58.decode(process.env.SOLANA_TREASURY_PRIVATE_KEY))
);
const treasurySigner = createSignerFromKeypair(umi, treasuryKeypair);


umi.use(signerIdentity(treasurySigner));
umi.use(mplTokenMetadata());

(async () => {
    console.log(`🚀 Deploying SPL Token: ${name} (${symbol})...`);

    // Generate a mint PDA
    const mint = generateSigner(umi);

    // Deploy & Mint Token
    await createAndMint(umi, {
        mint,
        authority: umi.identity,
        name,
        symbol,
        uri: metadataUri,
        sellerFeeBasisPoints: percentAmount(5),
        decimals: parseInt(decimals),
        amount: BigInt(totalSupply) * BigInt(10 ** parseInt(decimals)),
        tokenOwner: treasurySigner.publicKey,
        tokenStandard: TokenStandard.Fungible,
    }).sendAndConfirm(umi);

    console.log(`✅ Successfully minted ${totalSupply} ${symbol} to ${treasurySigner.publicKey}`);
    console.log(`🎉 Token Mint Address: ${mint.publicKey}`);
})();
