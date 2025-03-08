from fastapi import FastAPI, HTTPException, Query
from urllib.parse import unquote
from database import fetch_all_data

app = FastAPI()

@app.get("/storyline/")
async def get_storyline(instrument: str = Query(..., description="Financial instrument")):
    decoded_instrument = unquote(instrument).replace("/", "-")
    data = fetch_all_data(decoded_instrument)

    if not data:
        raise HTTPException(status_code=404, detail="No data available.")

    # Market Prices (clearly used)
    current_price = data["market_prices"][0][2]

    # News sentiment (clearly used)
    bullish_count = sum(1 for n in data["news_articles"] if n[7] == 'Bullish')
    bearish_count = len(data["news_articles"]) - bullish_count
    news_sentiment = "Bullish" if bullish_count > bearish_count else "Bearish"

    # Predictions (clearly used)
    prediction = data["price_predictions"][0][2] if data["price_predictions"] else "Neutral"

    # Trade Recommendations (clearly used)
    recommendation = data["trade_recommendations"][0] if data["trade_recommendations"] else None
    recommended_action = recommendation[2] if recommendation else "Hold"
    entry = recommendation[3] if recommendation else current_price
    stop_loss = recommendation[4] if recommendation else current_price - 10
    take_profit = recommendation[5] if recommendation else current_price + 10

    # News Risk clearly mentioned if exists
    risks = data["news_risks"][0][2] if data["news_risks"] else "No major risks reported."

    storyline = f"{decoded_instrument.upper()} Sentiment Analysis\n\n"

    # Clearly formed sentiment
    storyline += "**Sentiment Analysis:**\n"
    storyline += f"Market sentiment appears {prediction.lower()}, driven by recent {news_articles} news and market predictions indicating a {prediction} bias.\n\n"

    storyline += "**Current Price and Performance:**\n"
    storyline += f"The current price of {decoded_instrument} is ${current_price:.2f}. Recent news sentiment suggests {news_sentiment.lower()} momentum.\n\n"

    storyline += "**Bullish or Bearish Predictions:**\n"
    storyline += f"Analysts predict a {prediction.lower()} market based on recent indicators and sentiment analysis.\n\n"

    storyline += "**Key Factors:**\n"
    storyline += f"1. Recent news sentiment indicates a {news_sentiment.lower()} market.\n"
    storyline += "2. Analysts' recent forecasts indicate potential market movements.\n"
    storyline += "3. Economic indicators and market trends influencing asset prices.\n\n"

    storyline += "**Risks and Cautions:**\n"
    storyline += f"{risks}\n\n"

    storyline += "**Recommendations:**\n"
    storyline += f"Based on current analysis, a '{recommendation[2]}' action is recommended. Suggested entry at ${entry:.2f}, stop loss at ${recommendation[3]:.2f}, take-profit at ${recommendation[4]:.2f}.\n"

    return {"instrument": decoded_instrument, "storyline": storyline}

