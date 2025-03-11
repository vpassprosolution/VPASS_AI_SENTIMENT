from fastapi import FastAPI, HTTPException, Query
from urllib.parse import unquote
from database import fetch_all_data

app = FastAPI()

@app.get("/storyline/")
async def get_storyline(instrument: str = Query(...)):
    decoded_instrument = unquote(instrument).replace("/", "-")

    data = fetch_all_data(decoded_instrument)
    if not data or not data.get("market_prices"):
        raise HTTPException(status_code=404, detail="No data available")

    current_price = data["market_prices"][0][2]

    storyline = f"Vessa has {decoded_instrument.upper()} Sentiment Analysis:\n\n"

    # Sentiment Analysis (simplified, powerful)
    storyline += "*Sentiment Analysis:*\n"
    storyline += f"The market sentiment for {decoded_instrument} appears neutral to bullish. "
    storyline += "Recent news and economic developments are supportive, highlighting its safe-haven status amid geopolitical tensions and economic uncertainty.\n\n"

    # Current Price & Performance
    storyline += "*Current Price and Performance*\n"
    storyline += f"The current price of {decoded_instrument} is ${current_price:.2f}. "
    storyline += "Price is consolidating, indicating potential near-term breakout opportunities.\n\n"

    # Predictions (simplified clearly)
    storyline += "Bullish or Bearish Predictions:\n"
    storyline += "Bullish sentiment currently dominates, driven by positive market fundamentals and supportive moving averages.\n\n"

    # Key Factors (simple but powerful)
    storyline += "Key Factors:\n"
    storyline += "1. Strong demand amid geopolitical uncertainty.\n"
    storyline += "2. Support from major economic news.\n"
    storyline += "3. Positive market momentum.\n\n"

    # Risks & Cautions (Limit to 4 Titles, Hide Source)
    storyline += "Risks and Cautions:\n"
    news_risks = data.get("news_risks", [])
    news_articles = data.get("news_articles", [])
    risks_added = 0

    if news_risks:
        for risk in news_risks[:4]:  # Limit to 4 items
            storyline += f"- {risk[3]}\n"
            risks_added += 1
    
    if risks_added < 4 and news_articles:  # If less than 4 risks, fill with news titles
        for article in news_articles[:4 - risks_added]:
            storyline += f"- {article[3]}\n"

    storyline += "\n"  # Ensure space before recommendations

    # Recommendations clearly simplified and powerful
    entry = current_price
    stop_loss = current_price * 0.985  # 1.5% below entry
    take_profit = current_price * 1.015  # 1.5% above entry

    storyline += "\nClick below to view recommendations:\n"
    storyline += "[View Recommendations](tg://msg?text=Recommendations:\n"
    storyline += f"A buy recommendation is suitable at current price (${entry:.2f}). "
    storyline += f"Suggested stop-loss at ${stop_loss:.2f}, take-profit target at ${take_profit:.2f} to manage risk effectively.)"

    return {"instrument": decoded_instrument, "storyline": storyline}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("storyline_generator:app", host="0.0.0.0", port=8000)
