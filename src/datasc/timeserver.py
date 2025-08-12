from fastapi import FastAPI
from datetime import datetime
import json


app = FastAPI()


@app.get('/time')
async def get_current_time():
    """
    Returns the current server time and timezone in JSON format.
    """
    current_time = datetime.now()
    response = {
        'current_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'timezone': datetime.now().astimezone().tzname()
    }
    return json.dumps(response)
