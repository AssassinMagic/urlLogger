from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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

        # HTML response with a redirection message
        redirect_url = "https://docs.google.com/forms/d/e/1FAIpQLSe5EU_YX2JkaRejr_nqaSXZ9WWlNhb1uLYLe8XR3A69dekDnA/viewform?usp=header"
        html_content = f"""
        <html>
            <head>
                <meta http-equiv="refresh" content="5;url={redirect_url}" />
            </head>
            <body>
                <h1>You will be redirected shortly...</h1>
                <p>If you are not redirected, <a href="{redirect_url}">click here</a>.</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

    except Exception as e:
        # Handle errors (e.g., if Edge Config fails)
        raise HTTPException(status_code=500, detail=f"Error storing data: {str(e)}")
