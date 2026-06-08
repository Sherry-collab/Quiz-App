from fastapi import FastAPI

app = FastAPI()

@app.get('/blog')
def get():
    return {"details": "Hey hey hey"}

