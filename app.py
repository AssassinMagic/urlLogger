from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/tracker/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}