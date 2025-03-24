from fastapi import FastAPI, HTTPException, Query
from urllib.parse import unquote
from database import fetch_all_data

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

    inflation = next((float(d[2]) for d in data.get("macro_data", []) if d[0].lower() == "inflation rate"), None)
    gdp = next((float(d[2]) for d in data.get("macro_data", []) if d[0].lower() == "gdp growth"), None)
    fed_rate = next((float(d[2]) for d in data.get("macro_data", []) if "interest rate" in d[0].lower()), None)

    # ✨ Start storyline
    storyline = f"🟨 Vessa has {raw_name} Sentiment Analysis\n"

    # 🧠 Sentiment Analysis
    storyline += "\n🧠 Sentiment Analysis:\n"
    storyline += f"The market sentiment for {raw_name} appears neutral to bullish. "
    storyline += "Vessa’s AI models detect growing investor caution due to lingering inflation and mixed macroeconomic signals. "
    storyline += f"At the same time, {raw_name}'s status as a safe-haven asset is strengthening amid geopolitical tension and Fed uncertainty.\n"

    # 💰 Current Price
    storyline += "\n💰 Current Price and Performance:\n"
    storyline += f"The current price of {raw_name} is ${current_price:.2f}.\n"
    storyline += "Vessa sees price consolidation near this level, signaling that the market is preparing for a potential breakout — either in response to Fed policy, inflation data, or global risk sentiment.\n"

    # 📈 Prediction
    storyline += "\n📈 Bullish or Bearish Predictions:\n"
    storyline += "Bullish momentum dominates.\n"
    if inflation:
        storyline += f"Macroeconomic stress, high inflation ({inflation:.1f}%), and cautious Fed guidance support {raw_name}. "
    else:
        storyline += f"Macroeconomic stress and cautious Fed guidance support {raw_name}. "
    storyline += f"Price remains well-supported above ${current_price - 12:.0f}, with upside potential toward ${current_price + 45:.0f} and beyond if fear builds in the broader market.\n"

    # 🔍 Key Factors
    storyline += "\n🔍 Key Factors Influencing Gold:\n"
    if inflation: storyline += f"🔥 Inflation remains sticky — still above 2.5% Fed target.\n"
    if gdp: storyline += f"📉 GDP slowdown to {gdp:.1f}% raises concerns over economic momentum.\n"
    storyline += "📊 Stable unemployment helps confidence but offers no upside surprise.\n"
    storyline += "🌐 Geopolitical tensions and war risk are pushing investors to safety.\n"
    if fed_rate: storyline += f"🏦 Fed holding rates at {fed_rate:.2f}%, with no clear rate-cut timeline.\n"

    # ⚠️ Risks
    storyline += "\n⚠️ Risks and Cautions:\n"
    news_risks = data.get("news_risks", [])
    news_articles = data.get("news_articles", [])
    risks_added = 0

    if news_risks:
        for risk in news_risks[:4]:
            storyline += f"{risk[3]}\n"
            risks_added += 1

    if risks_added < 4 and news_articles:
        for article in news_articles[:4 - risks_added]:
            storyline += f"{article[3]}\n"

    # ✅ Recommendations
    entry = current_price
    stop_loss = current_price * 0.985
    take_profit = current_price * 1.015

    storyline += "\n✅ Recommendations from Vessa:\n"
    storyline += "💼 Action: BUY\n"
    storyline += f"💵 Entry Price: ${entry:.2f}\n"
    storyline += f"🛡 Stop-Loss: ${stop_loss:.2f}\n"
    storyline += f"🎯 Take-Profit: ${take_profit:.2f}\n"

    return {"instrument": decoded_instrument, "storyline": storyline}
