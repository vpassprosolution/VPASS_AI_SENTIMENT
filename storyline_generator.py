import datetime
from database import fetch_all_data

def generate_storyline(instrument):
    """Generate a structured financial storyline based on database data with human-like insights."""
    data = fetch_all_data(instrument)
    
    if not any(data.values()):
        return f"No sufficient data available for {instrument}."
    
    storyline = f"📌 {instrument.upper()} Market Sentiment (Storyline Mode)\n\n"
    storyline += "🔥 The market is making moves! Here's the full breakdown:\n\n"
    
    # Market Prices and Performance
    if data["market_prices"]:
        price_info = data["market_prices"][0]
        price = price_info[2]
        storyline += f"💰 **Current Market Price:** ${price:.2f}\n"
        storyline += "📊 Traders are closely watching price movements, evaluating whether this is a turning point or just another phase in market volatility.\n\n"
    
    # Sentiment Analysis (Remove Duplicates)
    if data["news_articles"]:
        seen_articles = set()
        storyline += "📰 **Market Sentiment & Key News:**\n"
        for news in data["news_articles"]:
            description = news[4]  # Fetching sentiment from description
            sentiment = news[7] if news[7] else "Neutral"
            if description not in seen_articles:
                storyline += f"- {description} ({sentiment} Sentiment)\n"
                seen_articles.add(description)
        storyline += "📌 These news events are shaping market expectations and creating momentum.\n\n"
    
    # Key Factors Affecting Sentiment
    storyline += "🔍 **Key Factors Influencing Price Movements:**\n"
    storyline += "- 📉 Global economic trends and central bank policies\n"
    storyline += "- 🏦 Institutional interest in the asset class\n"
    storyline += "- ⚠️ Major regulatory developments\n"
    storyline += "- 📰 Public sentiment from high-profile investors or influencers\n\n"
    
    # Risk Analysis (Fix Timestamp Issue)
    if data["news_risks"]:
        risk_info = data["news_risks"][0]
        risk_level = risk_info[3]
        risk_reason = risk_info[4]
        storyline += f"⚠️ **Potential Risks & Cautions:**\n"
        storyline += f"- Risk Level: {risk_level}\n"
        if isinstance(risk_reason, str):  # Ensure risk reason is a string
            storyline += f"- {risk_reason}\n"
        storyline += "📌 Understanding these risks is crucial for making informed trading decisions.\n\n"
    
    # Price Predictions
    if data["price_predictions"]:
        prediction_info = data["price_predictions"][0]
        trend = "🚀 Bullish" if prediction_info[2].lower() == "bullish" else "📉 Bearish"
        confidence = prediction_info[3]
        storyline += f"🔮 **Market Outlook:** {trend} ({confidence}% confidence)\n"
        storyline += "📌 Analysts suggest watching key support and resistance levels closely.\n\n"
    
    # Trade Recommendations
    if data["trade_recommendations"]:
        recommendation_info = data["trade_recommendations"][0]
        recommendation = recommendation_info[2].upper()
        confidence = recommendation_info[3]
        storyline += f"📢 **Final Verdict: {recommendation}!** ({confidence}% confidence)\n"
        storyline += "📌 Suggested levels for traders:\n"
        storyline += "- 🎯 Entry Price: To be determined based on real-time conditions\n"
        storyline += "- 🚨 Stop Loss: Manage risk effectively\n"
        storyline += "- 📈 Take Profit: Identify strong resistance levels\n\n"
    
    storyline += "📌 Stay informed, manage risks wisely, and trade with confidence! 🚀"
    
    return storyline

if __name__ == "__main__":
    instrument = "nasdaq"
    story = generate_storyline(instrument)
    print(story)
