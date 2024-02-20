from fastapi import FastAPI
import uvicorn
import models

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('main:app', port=9000, reload=True)
