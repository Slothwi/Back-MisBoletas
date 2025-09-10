from fastapi import FastAPI
port = 3000

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API MisBoletas!"}