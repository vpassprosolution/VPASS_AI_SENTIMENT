import datetime
from fastapi import FastAPI, HTTPException, Query
from urllib.parse import unquote
from database import fetch_all_data

app = FastAPI()

@app.get("/storyline/")
async def get_storyline(instrument: str = Query(..., description="Financial instrument")):
    try:
        # Decode URL-encoded instrument names and ensure format consistency
        decoded_instrument = unquote(instrument).replace("/", "-")
        print(f"🔍 Debug: Attempting to fetch data for instrument: {decoded_instrument}")
        
        # Fetch storyline from the database
        data = fetch_all_data(decoded_instrument)
        print(f"🔍 Debug: Database query returned: {data}")
        
        if not data or not any(data.values()):
            print(f"⚠ Database Query Returned Empty for: {decoded_instrument}")
            raise HTTPException(status_code=404, detail="Not Found")
        
        print(f"✅ Database Query Found Data for: {decoded_instrument}")
        
        # 📌 Report Structure
        storyline = f"📌 {decoded_instrument.upper()} MARKET SENTIMENT & ANALYSIS\n\n"
        
        # ✅ Current Price and Performance
        if data.get("market_prices") and data["market_prices"]:
            price_info = data["market_prices"][0]
            price = price_info[2]
            storyline += f"💰 CURRENT MARKET PRICE: ${price:.2f}\n"
            storyline += "📊 Investors are watching price movements, assessing possible breakout or correction levels.\n\n"
        
        # ✅ Sentiment Analysis
        if data.get("news_articles") and len(data["news_articles"]) >= 5:
            storyline += "📌 MARKET SENTIMENT ANALYSIS:\n"
            for news in data["news_articles"][:5]:
                description = news[4] if news[4] else "No Description Available"
                sentiment = news[7] if news[7] else "Neutral"
                storyline += f"- {description} ({sentiment} Sentiment)\n"
            storyline += "📌 Recent events influencing market sentiment.\n\n"
        
        # ✅ Key Factors Affecting Sentiment
        storyline += "📌 KEY FACTORS INFLUENCING PRICE MOVEMENT:\n"
        storyline += "- 📉 Economic trends and central bank policies.\n"
        storyline += "- 🏦 Institutional and retail investor behavior.\n"
        storyline += "- ⚠️ Regulatory updates and compliance risks.\n"
        storyline += "- 📰 Social media influence and major investor commentary.\n\n"
        
        # ✅ Risk Analysis
        if data.get("news_risks") and data["news_risks"]:
            risk_info = data["news_risks"][0]
            risk_level = risk_info[3]
            risk_reason = risk_info[4] if risk_info[4] else "Not Available"
            storyline += "📌 RISK ANALYSIS:\n"
            storyline += f"- Risk Level: {risk_level}\n"
            storyline += f"- Potential Risk Factors: {risk_reason}\n"
            storyline += "📌 Traders should be aware of risks before entering positions.\n\n"
        
        # ✅ Bullish or Bearish Predictions
        if data.get("price_predictions") and data["price_predictions"]:
            prediction_info = data["price_predictions"][0]
            trend = "🚀 Bullish" if prediction_info[2].lower() == "bullish" else "📉 Bearish"
            confidence = prediction_info[3]
            storyline += f"📌 MARKET OUTLOOK: {trend} ({confidence}% Confidence)\n"
            storyline += "📌 Analysts recommend monitoring key support and resistance zones.\n\n"
        
        # ✅ Recommendations
        if data.get("trade_recommendations") and data["trade_recommendations"]:
            recommendation_info = data["trade_recommendations"][0]
            recommendation = recommendation_info[2].upper()
            confidence = recommendation_info[3]
            entry_price = recommendation_info[4]
            stop_loss = entry_price - 0.01  # Adjust based on strategy
            take_profit = entry_price + 0.01
            storyline += f"📌 TRADE RECOMMENDATION: {recommendation}! ({confidence}% Confidence)\n"
            storyline += f"- Entry Price: ${entry_price:.2f}\n"
            storyline += f"- Stop Loss: ${stop_loss:.2f}\n"
            storyline += f"- Take Profit: ${take_profit:.2f}\n\n"
        
        storyline += "📌 Stay informed, manage risks, and trade strategically! 🚀"
        
        return {"instrument": decoded_instrument, "storyline": storyline}
    
    except Exception as e:
        print(f"❌ Error generating storyline: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("storyline_generator:app", host="0.0.0.0", port=8000)
