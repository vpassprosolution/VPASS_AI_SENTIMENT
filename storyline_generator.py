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
        
        # 📌 Storyline Generation in Story Mode
        storyline = f"📌 {decoded_instrument.upper()} SENTIMENT ANALYSIS (STORYLINE MODE)\n\n"
        
        # ✅ Market Sentiment Introduction
        storyline += f"\"Ladies and gentlemen, the {decoded_instrument} market is on fire! 🔥 Investors worldwide are closely watching {decoded_instrument} as major financial events unfold. Recent trends suggest significant movement that could shape the asset’s future.\"\n\n"
        
        # ✅ Why is this happening?
        storyline += "📌 WHY IS THIS HAPPENING?\n"
        
        # ✅ Key Factors Affecting Sentiment
        storyline += "🏦 Central Banks Are Buying: Institutional investors and central banks have shown increased interest, indicating strategic shifts.\n"
        storyline += "📉 Stock Market Uncertainty: Volatility in global markets has pushed traders toward safe-haven assets.\n"
        storyline += "🌎 Geopolitical Tensions: Ongoing global conflicts and regulatory changes are impacting {decoded_instrument}.\n\n"
        
        # ✅ Price Performance & Market Outlook
        if data.get("market_prices") and data["market_prices"]:
            price_info = data["market_prices"][0]
            price = price_info[2]
            storyline += f"📌 CURRENT PRICE: ${price:.2f}\n"
            storyline += "📊 Analysts are closely watching the price action to determine future movement.\n\n"
        
        # ✅ Technical Prediction & Future Outlook
        if data.get("price_predictions") and data["price_predictions"]:
            prediction_info = data["price_predictions"][0]
            trend = "🚀 Bullish" if prediction_info[2].lower() == "bullish" else "📉 Bearish"
            confidence = prediction_info[3]
            storyline += f"📌 THE BIG QUESTION: IS NOW THE TIME TO BUY?\n"
            storyline += f"If {decoded_instrument} continues this trend, expect movement toward key price levels in the coming months.\n"
            storyline += f"{trend} with {confidence}% confidence.\n\n"
        
        # ✅ Final Verdict
        storyline += "📌 FINAL VERDICT:\n"
        storyline += "🔥 Bullish on {decoded_instrument}! Investors should monitor market dips and strategic movements. Economic reports and institutional actions will determine the next major move!\n\n"
        
        return {"instrument": decoded_instrument, "storyline": storyline}
    
    except Exception as e:
        print(f"❌ Error generating storyline: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("storyline_generator:app", host="0.0.0.0", port=8000)
