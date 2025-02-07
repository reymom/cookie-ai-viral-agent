from config.celery import app, logger
from tokenomics.reputation import calculate_reputation_score

TOKEN_ALLOCATION = 1000000


@app.task(name="distribute_tokens")
def distribute_tokens(video_topic, engagement):
    """Distributes tokens based on engagement score."""
    logger.info(f"💰 Distributing tokens for {video_topic}")

    # Calculate reputation score
    score = calculate_reputation_score(engagement)
    logger.info(f"📊 Reputation Score: {score}")

    # Determine token rewards (normalize against max possible engagement)
    token_reward = (score / 1000) * TOKEN_ALLOCATION  # Adjust factor as needed

    # TODO: Implement smart contract call to send tokens
    logger.info(f"✅ Tokens to distribute: {token_reward} for {video_topic}")

    return token_reward
