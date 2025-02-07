from crypto.deploy_token import deploy_spl_token_js

if __name__ == "__main__":
    print("🔍 Testing SPL Token Deployment...")
    token_address = deploy_spl_token_js("Test Video")
    print(f"✅ Test Token Deployed at: {token_address}")
