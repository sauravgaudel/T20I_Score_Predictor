from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import pickle


app = FastAPI()

from Backend.cors import setup_cors
from schemas.input import Input

with open('Model/model.pkl', "rb") as file:
    model = pickle.load(file)

setup_cors(app)

@app.get('/')
def Home():
    return {'Hello': 'This is the homepage of the score predcition API'}

@app.post('/predict')
def Predict(data: Input):

    input_df = pd.DataFrame([{
        'batting_team': data.batting_team,
        'bowling_team': data.bowling_team,
        'current_score': data.current_score,
        'balls_left': data.balls_left,
        'wicket_left': data.wicket_left,
        'CRR': data.CRR,
        'last_5': data.last_five
    }])

    prediction = int(model.predict(input_df)[0])

    return JSONResponse(status_code=200, content={'Probability': prediction})



