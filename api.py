from fastapi import FastAPI, HTTPException
from storyline_generator import get_storyline

app = FastAPI()

@app.get("/")
def home():
    """Root endpoint to check if the API is running."""
    return {"status": "API is running", "available_routes": ["/storyline/?instrument="]}

@app.get("/storyline/")
def fetch_storyline(instrument: str):
    """Fetch the financial storyline for a given instrument."""
    try:
        formatted_instrument = instrument.replace("/", "-")  # Convert '/' to '-'
        storyline = get_storyline(formatted_instrument)
        
        if not storyline or "No sufficient data" in storyline:
            raise HTTPException(status_code=404, detail="No sufficient data available")
        
        return {"instrument": formatted_instrument, "storyline": storyline}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8080)
