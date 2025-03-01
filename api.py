from fastapi import FastAPI
from storyline_generator import generate_storyline

app = FastAPI()

@app.get("/")
def home():
    """Root endpoint to check if the API is running."""
    return {"status": "API is running", "available_routes": ["/storyline/{instrument}"]}

@app.get("/storyline/{instrument}")
def get_storyline(instrument: str):
    """Fetch the financial storyline for a given instrument."""
    try:
        storyline = generate_storyline(instrument.lower())
        if not storyline or "No sufficient data" in storyline:
            return {"error": "No sufficient data available", "instrument": instrument}
        return {"instrument": instrument, "storyline": storyline}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
