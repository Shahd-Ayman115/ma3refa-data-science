from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Data Science API is running"}


@app.post("/recommendations")
def get_recommendations(data: dict):
    print("Received data:")
    print(data)

    return {
        "message": "Data received successfully",
        "recommendations": []
    }