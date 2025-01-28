from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from vercel.edge_config import EdgeConfig
import time

app = FastAPI()

# Initialize Edge Config client
edge_config = EdgeConfig()

@app.get("/tracker/{item_id}")
async def read_item(item_id: int, q: str = None):
    try:
        # Create a unique key using item_id and a timestamp
        timestamp = int(time.time() * 1000)  # Current time in milliseconds
        key = f"{item_id},{timestamp}"
        value = {"item_id": item_id, "q": q}

        # Store data into Vercel Edge Config
        await edge_config.set(key, value)

        # Redirect to a new URL after storing the data
        redirect_url = "https://example.com/redirected"
        return RedirectResponse(url=redirect_url)

    except Exception as e:
        # Handle errors (e.g., if Edge Config fails)
        raise HTTPException(status_code=500, detail=f"Error storing data: {str(e)}")
