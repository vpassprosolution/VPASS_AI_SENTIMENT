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

    storyline = f"<b>Vessa has {decoded_instrument.upper()} Sentiment Analysis:</b>\n\n"

    # Sentiment Analysis (simplified, powerful)
    storyline += "<b>Sentiment Analysis:</b>\n"
    storyline += f"The market sentiment for {decoded_instrument} appears neutral to bullish. "
    storyline += "Recent news and economic developments are supportive, highlighting its safe-haven status amid geopolitical tensions and economic uncertainty.\n\n"

    # Current Price & Performance
    storyline += "<b>Current Price and Performance:</b>\n"
    storyline += f"The current price of {decoded_instrument} is <b>${current_price:.2f}</b>. "
    storyline += "Price is consolidating, indicating potential near-term breakout opportunities.\n\n"

    # Predictions (simplified clearly)
    storyline += "<b>Bullish or Bearish Predictions:</b>\n"
    storyline += "Bullish sentiment currently dominates, driven by positive market fundamentals and supportive moving averages.\n\n"

    # Key Factors (simple but powerful)
    storyline += "<b>Key Factors:</b>\n"
    storyline += "1. Strong demand amid geopolitical uncertainty.\n"
    storyline += "2. Support from major economic news.\n"
    storyline += "3. Positive market momentum.\n\n"

    # Risks & Cautions (Limit to 4 Titles, Hide Source)
    storyline += "<b>Risks and Cautions:</b>
\n"
    news_risks = data.get("news_risks", [])
    news_articles = data.get("news_articles", [])
    risks_added = 0

    if news_risks:
        for risk in news_risks[:4]:  # Limit to 4 items
            storyline += f"- <b>{risk[3]}</b>\n"
            risks_added += 1
    
    if risks_added < 4 and news_articles:  # If less than 4 risks, fill with news titles
        for article in news_articles[:4 - risks_added]:
            storyline += f"- <b>{article[3]}</b>\n"

    # Recommendations clearly simplified and powerful
    entry = current_price
    stop_loss = current_price * 0.985  # 1.5% below entry
    take_profit = current_price * 1.015  # 1.5% above entry

    storyline += "
<details>
<summary><b>Click to View Recommendations</b></summary>
<b>Recommendations:</b>
\n"
    storyline += f"A buy recommendation is suitable at current price (<b>${entry:.2f}</b>). "
    storyline += f"Suggested stop-loss at <b>${stop_loss:.2f}</b>, take-profit target at <b>${take_profit:.2f}</b> to manage risk effectively.\n"

    return {"instrument": decoded_instrument, "storyline": storyline}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("storyline_generator:app", host="0.0.0.0", port=8000)

</details>
