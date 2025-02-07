def calculate_reputation_score(engagement):
    """
    Calculates a reputation score based on engagement metrics.

    Weights:
    - Likes: 1 point each
    - Retweets: 2 points each
    - Comments: 3 points each
    - Impressions: 0.001 points each
    - Smart Engagement: 5 points each
    """
    score = (
        engagement["likes"] * 1 +
        engagement["retweets"] * 2 +
        engagement["comments"] * 3 +
        engagement["impressions"] * 0.001 +
        engagement["smart_engagement"] * 5
    )

    return round(score, 2)  # Return rounded score
