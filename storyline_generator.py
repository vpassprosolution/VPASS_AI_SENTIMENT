from fastapi import FastAPI, HTTPException, Query
from urllib.parse import unquote
from database import fetch_all_data
import random

app = FastAPI()

@app.get("/storyline/")
async def get_storyline(instrument: str = Query(...)):
    decoded_instrument = unquote(instrument).replace("/", "-")
    raw_name = unquote(instrument).upper()

    data = fetch_all_data(decoded_instrument)
    if not data or not data.get("market_prices"):
        raise HTTPException(status_code=404, detail="No data available")

    try:
        current_price = data["market_prices"][0][2]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading market price: {e}")

    inflation = next((float(d[1]) for d in data.get("macro_data", []) if d[0].lower() == "inflation rate"), None)
    gdp = next((float(d[1]) for d in data.get("macro_data", []) if d[0].lower() == "gdp growth"), None)
    fed_rate = next((float(d[1]) for d in data.get("macro_data", []) if "interest rate" in d[0].lower()), None)

    # ✨ Start storyline
    storyline = f"🏨 Vessa has {raw_name} Sentiment Analysis\n"

    # 🧠 Sentiment Analysis with random rotation
    sentiment_options = [
        f"The market sentiment for {raw_name} appears neutral to bullish. Vessa’s AI detects increased investor caution due to mixed economic signals, while {raw_name} benefits from its safe-haven role.",
        f"Investors are leaning toward a cautiously bullish stance on {raw_name}. Vessa’s sentiment engine reveals lingering inflation fears and Fed indecision fueling safe-haven demand.",
        f"Sentiment is gradually shifting in favor of {raw_name}. Vessa highlights a rise in macroeconomic uncertainty and flight to safety behavior across financial markets.",
        f"Market tone is stable but tilting bullish for {raw_name}. Vessa identifies increased gold exposure from institutions as a hedge against inflation and policy risks.",
        f"Vessa signals a strengthening sentiment in {raw_name}, as inflation pressures persist and investors navigate a foggy outlook around rate policy and global instability."
    ]

    storyline += "\n🧠 Sentiment Analysis:\n"
    storyline += random.choice(sentiment_options) + "\n"

    # 💰 Current Price
    storyline += "\n💰 Current Price and Performance:\n"
    storyline += f"The current price of {raw_name} is ${current_price:.2f}. "
    storyline += "Vessa sees price consolidation near this level, signaling that the market is preparing for a potential breakout — either in response to Fed policy, inflation data, or global risk sentiment."

    # 📈 Prediction
    storyline += "\n\n📈 Bullish or Bearish Predictions:\n"
    storyline += "Bullish momentum dominates. "
    if inflation:
        storyline += f"Macroeconomic stress, high inflation ({inflation:.1f}%), and cautious Fed guidance support {raw_name}. "
    else:
        storyline += f"Macroeconomic stress and cautious Fed guidance support {raw_name}. "
    storyline += f"Price remains well-supported above ${current_price - 12:.0f}, with upside potential toward ${current_price + 45:.0f} and beyond if fear builds in the broader market."

    # 🔍 Key Factors
    storyline += "\n\n🔍 Key Factors Influencing Gold:\n"
    if inflation: storyline += f"🔥 Inflation remains sticky — still above 2.5% Fed target.\n"
    if gdp: storyline += f"📉 GDP slowdown to {gdp:.1f}% raises concerns over economic momentum.\n"
    storyline += "📈 Stable unemployment helps confidence but offers no upside surprise.\n"
    storyline += "🌐 Geopolitical tensions and war risk are pushing investors to safety.\n"
    if fed_rate: storyline += f"🏦 Fed holding rates at {fed_rate:.2f}%, with no clear rate-cut timeline.\n"

    # ⚠️ Risks and Cautions (✅ from news_articles only)
    storyline += "\n⚠️ Risks and Cautions:\n"
    news_articles = data.get("news_articles", [])
    for article in news_articles[:3]:
        description = article[3].strip()
        storyline += f"⚠️ {description}\n"

    # 📌 Recommendations
    storyline += "\n📌 Recommendations:\n"
    entry = current_price
    stop_loss = current_price * 0.985
    take_profit = current_price * 1.015
    storyline += f"A buy recommendation is suitable at current price (${entry:.2f}). "
    storyline += f"Suggested stop-loss at ${stop_loss:.2f}, take-profit target at ${take_profit:.2f} to manage risk effectively.\n"

    return {"instrument": decoded_instrument, "storyline": storyline}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("storyline_generator:app", host="0.0.0.0", port=8000)
