from fastapi import FastAPI



app = FastAPI()



if __name__ == "__main__":
    from uvicorn import run
    run(app)