import datetime
from fastapi import FastAPI, HTTPException, Query
from urllib.parse import unquote
from database import fetch_all_data

app = FastAPI()

@app.get("/storyline/")
async def get_storyline(instrument: str = Query(..., description="Financial instrument")):
    # Decode URL-encoded instrument names and ensure format consistency
    decoded_instrument = unquote(instrument).replace("/", "-")  # Ensure instrument format matches database
    
    print(f"🔍 Debug: Attempting to fetch data for instrument: {decoded_instrument}")
    
    # Fetch storyline from the database
    data = fetch_all_data(decoded_instrument)
    
    # Debugging: Print database query results
    print(f"🔍 Debug: Database query returned: {data}")
    
    if not data or not any(data.values()):
        print(f"⚠ Database Query Returned Empty for: {decoded_instrument}")
        raise HTTPException(status_code=404, detail="Not Found")
    
    print(f"✅ Database Query Found Data for: {decoded_instrument}")
    
    # 🔥 Storyline Generation Start
    storyline = f"📌 **{decoded_instrument.upper()} Market Sentiment & Analysis**\n\n"
    
    # Market Prices and Performance
    if data.get("market_prices"):
        price_info = data["market_prices"][0]
        price = price_info[2]
        storyline += f"💰 **Current Market Price:** **${price:.2f}**\n"
        storyline += "📊 Investors are closely watching the price movement, anticipating potential breakouts or corrections.\n\n"
    
    # Sentiment Analysis (Avoid Duplicates)
    if data.get("news_articles"):
        seen_articles = set()
        storyline += "📰 **Recent Market Sentiment & Key News:**\n"
        for news in data["news_articles"]:
            title = news[3]  # Fetching news title
            sentiment = news[7] if news[7] else "Neutral"
            if title not in seen_articles:
                storyline += f"- {title} ({sentiment} Sentiment)\n"
                seen_articles.add(title)
        storyline += "📌 These factors are shaping market expectations and momentum.\n\n"
    
    # Key Factors Affecting Sentiment
    storyline += "🔍 **Key Factors Influencing Price Movements:**\n"
    storyline += "- 📉 Global economic trends and central bank policies.\n"
    storyline += "- 🏦 Institutional interest in this asset class.\n"
    storyline += "- ⚠️ Major regulatory developments affecting market confidence.\n"
    storyline += "- 📰 Public sentiment from high-profile investors or social media influencers.\n\n"
    
    # Risk Analysis
    if data.get("news_risks"):
        risk_info = data["news_risks"][0]
        risk_level = risk_info[3]
        risk_reason = risk_info[4]
        storyline += f"⚠️ **Risk Analysis & Cautions:**\n"
        storyline += f"- **Risk Level:** {risk_level}\n"
        if isinstance(risk_reason, str):  # Ensure risk reason is a string
            storyline += f"- **Potential Risk Factors:** {risk_reason}\n"
        storyline += "📌 Traders should be cautious and manage risk accordingly.\n\n"
    
    # AI Price Predictions
    if data.get("price_predictions"):
        prediction_info = data["price_predictions"][0]
        trend = "🚀 **Bullish**" if prediction_info[2].lower() == "bullish" else "📉 **Bearish**"
        confidence = prediction_info[3]
        storyline += f"🔮 **AI Market Prediction:** {trend} ({confidence}% confidence)\n"
        storyline += "📌 Analysts suggest keeping an eye on key support and resistance levels.\n\n"
    
    # Trade Recommendations
    if data.get("trade_recommendations"):
        recommendation_info = data["trade_recommendations"][0]
        recommendation = recommendation_info[2].upper()
        confidence = recommendation_info[3]
        storyline += f"📢 **Final Verdict: {recommendation}!** ({confidence}% confidence)\n"
        storyline += "📌 Suggested trade setup:\n"
        storyline += "- 🎯 **Entry Price:** Adjust based on market conditions.\n"
        storyline += "- 🚨 **Stop Loss:** Set to minimize risk.\n"
        storyline += "- 📈 **Take Profit:** Identify strong resistance levels.\n\n"
    
    storyline += "📌 Stay informed, manage risks wisely, and trade with confidence! 🚀"

    return {"instrument": decoded_instrument, "storyline": storyline}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("storyline_generator:app", host="0.0.0.0", port=8000)
