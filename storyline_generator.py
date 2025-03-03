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
        
        # ✅ If data is missing, return a 404 instead of crashing
        if not data or not any(data.values()):
            print(f"⚠ No data found for: {decoded_instrument}")
            raise HTTPException(status_code=404, detail=f"No data found for {decoded_instrument}")

        print(f"✅ Database Query Found Data for: {decoded_instrument}")
        
        # 📌 Storyline Generation in Story Mode
        storyline = f"📌 {decoded_instrument.upper()} SENTIMENT ANALYSIS (STORYLINE MODE)\n\n"
        
        # ✅ Market Sentiment Introduction
        storyline += f"\"Ladies and gentlemen, the {decoded_instrument} market is on fire! 🔥 Investors worldwide are closely watching {decoded_instrument} as major financial events unfold. Recent trends suggest significant movement that could shape the asset’s future.\"\n\n"
        
        # ✅ Why is this happening?
        storyline += "📌 WHY IS THIS HAPPENING?\n"

        # ✅ Key Factors Affecting Sentiment
        storyline += "🏦 Institutional Investors: Increasing interest from hedge funds and central banks.\n"
        storyline += "📉 Stock Market Volatility: Uncertainty in global indices is pushing investors toward alternative assets.\n"
        storyline += "🌎 Geopolitical Tensions: Regulatory changes and global events impacting {decoded_instrument} prices.\n\n"
        
        # ✅ Price Performance & Market Outlook
        if data.get("market_prices") and data["market_prices"]:
            price_info = data["market_prices"][0]
            price = price_info[2]
            storyline += f"📌 CURRENT PRICE: ${price:.2f}\n"
            storyline += "📊 Analysts are monitoring price movements to determine future trends.\n\n"
        
        # ✅ Sentiment Analysis - Ensure 5 News Articles Are Shown
        if data.get("news_articles") and len(data["news_articles"]) >= 5:
            storyline += "📌 MARKET SENTIMENT ANALYSIS:\n"
            seen_articles = set()
            news_count = 0
            for news in data["news_articles"]:
                description = news[4] if news[4] else "No Description Available"
                sentiment = news[7] if news[7] else "Neutral"
                
                if description not in seen_articles:
                    storyline += f"- {description} ({sentiment} Sentiment)\n"
                    seen_articles.add(description)
                    news_count += 1
                
                if news_count >= 5:
                    break  # Stop after 5 unique news articles

            storyline += "📌 Recent events influencing market sentiment.\n\n"
        else:
            storyline += "📌 MARKET SENTIMENT ANALYSIS: No relevant news articles available at this moment.\n\n"
        
        # ✅ Bullish or Bearish Predictions
        if data.get("price_predictions") and data["price_predictions"]:
            prediction_info = data["price_predictions"][0]
            trend = "🚀 Bullish" if prediction_info[2].lower() == "bullish" else "📉 Bearish"
            confidence = prediction_info[3]
            storyline += f"📌 MARKET OUTLOOK: {trend} ({confidence}% Confidence)\n"
            storyline += "📌 Analysts recommend monitoring key support and resistance zones.\n\n"
        
        # ✅ Final Verdict
        storyline += "📌 FINAL VERDICT:\n"
        storyline += f"🔥 {decoded_instrument.capitalize()} remains a key asset to watch. Strategic decisions from institutions and macroeconomic shifts will determine the next major move.\n\n"

        return {"instrument": decoded_instrument, "storyline": storyline}
    
    except HTTPException as http_exc:
        raise http_exc  # Let FastAPI handle HTTP errors
    except Exception as e:
        print(f"❌ Error generating storyline: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Debugging: Print the fetched data before processing
print("🔍 Debug: Fetched Data from Database:", data)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("storyline_generator:app", host="0.0.0.0", port=8000)
