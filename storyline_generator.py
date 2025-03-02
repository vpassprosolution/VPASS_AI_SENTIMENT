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
    
    # 🔵 Storyline Generation Start
    storyline = f"📌 {decoded_instrument.upper()} 𝗠𝗔𝗥𝗞𝗘𝗧 𝗦𝗘𝗡𝗧𝗜𝗠𝗘𝗡𝗧 & 𝗔𝗡𝗔𝗟𝗬𝗦𝗜𝗦\n\n"
    
    # Market Prices and Performance
    if data.get("market_prices"):
        price_info = data["market_prices"][0]
        price = price_info[2]
        storyline += f"💰 𝗖𝗨𝗥𝗥𝗘𝗡𝗧 𝗠𝗔𝗥𝗞𝗘𝗧 𝗣𝗥𝗜𝗖𝗘: ${price:.2f}\n"
        storyline += "📊 Investors are closely watching price movement, anticipating potential breakouts or corrections.\n\n"
    
    # Sentiment Analysis (Best 5 News with 10-15 words, understandable by users)
    if data.get("news_articles"):
        seen_articles = set()
        storyline += "📌 𝗞𝗘𝗬 𝗙𝗜𝗡𝗔𝗡𝗖𝗜𝗔𝗟 𝗡𝗘𝗪𝗦:\n"
        news_count = 0
        for news in data["news_articles"]:
            title = news[3]  # Fetching news title
            sentiment = news[7] if news[7] else "Neutral"
            words = title.split()
            if 10 <= len(words) <= 15 and title not in seen_articles:
                storyline += f"- {title} ({sentiment} Sentiment)\n"
                seen_articles.add(title)
                news_count += 1
            if news_count >= 5:
                break  # Ensure at least 5 news items are displayed
        storyline += "📌 These key news events are shaping market expectations.\n\n"
    
    # Key Factors Affecting Sentiment
    storyline += "📌 𝗞𝗘𝗬 𝗙𝗔𝗖𝗧𝗢𝗥𝗦 𝗜𝗠𝗣𝗔𝗖𝗧𝗜𝗡𝗚 𝗣𝗥𝗜𝗖𝗘:\n"
    storyline += "- 📉 Global economic trends and central bank policies.\n"
    storyline += "- 🏦 Institutional interest in this asset class.\n"
    storyline += "- ⚠️ Major regulatory developments affecting market confidence.\n"
    storyline += "- 📰 Public sentiment from high-profile investors or social media influencers.\n\n"
    
    # Risk Analysis
    if data.get("news_risks"):
        risk_info = data["news_risks"][0]
        risk_level = risk_info[3]
        risk_reason = risk_info[4]
        storyline += f"📌 𝗥𝗜𝗦𝗞 𝗔𝗡𝗔𝗟𝗬𝗦𝗜𝗦 & 𝗖𝗔𝗨𝗧𝗜𝗢𝗡𝗦:\n"
        storyline += f"- **Risk Level:** {risk_level}\n"
        if isinstance(risk_reason, str):
            storyline += f"- **Potential Risk Factors:** {risk_reason}\n"
        storyline += "📌 Traders should be cautious and manage risk accordingly.\n\n"
    
    # AI Price Predictions
    if data.get("price_predictions"):
        prediction_info = data["price_predictions"][0]
        trend = "🚀 𝗕𝗨𝗟𝗟𝗜𝗦𝗛" if prediction_info[2].lower() == "bullish" else "📉 𝗕𝗘𝗔𝗥𝗜𝗦𝗛"
        confidence = prediction_info[3]
        storyline += f"📌 𝗔𝗜 𝗠𝗔𝗥𝗞𝗘𝗧 𝗢𝗨𝗧𝗟𝗢𝗢𝗞: {trend} ({confidence}% confidence)\n"
        storyline += "📌 Analysts suggest monitoring key support and resistance levels.\n\n"
    
    # Trade Recommendations
    if data.get("trade_recommendations"):
        recommendation_info = data["trade_recommendations"][0]
        recommendation = recommendation_info[2].upper()
        confidence = recommendation_info[3]
        storyline += f"📌 𝗙𝗜𝗡𝗔𝗟 𝗧𝗥𝗔𝗗𝗘 𝗥𝗘𝗖𝗢𝗠𝗠𝗘𝗡𝗗𝗔𝗧𝗜𝗢𝗡: {recommendation}! ({confidence}% confidence)\n\n"
    
    storyline += "📌 Stay informed, manage risks wisely, and trade with confidence! 🚀"
    
    return {"instrument": decoded_instrument, "storyline": storyline}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("storyline_generator:app", host="0.0.0.0", port=8000)
