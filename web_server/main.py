from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/question")
async def ask_question(longtext: str):
    print(f"longtext: {longtext}")
    return longtext