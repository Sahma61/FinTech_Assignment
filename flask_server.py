import os

from flask import Flask, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

from backend import *

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/infer/<ticker>")
def infer_from_sec10k(ticker: str) -> None:
    info = parse_sec_info(model, ticker)
    data = parse_sec_data(model, ticker)
    cols = [list(datum.columns) for datum in data]
    data = [datum.to_dict('records') for datum in data]
    return jsonify({'info': info, 'data': data, 'cols': cols})


if __name__ == "__main__":
    os.environ['GOOGLE_API_KEY'] = "AIzaSyBNRZ25ezFXLH8TIhRPTOjuIdozGc4cWtY"
    genai.configure(api_key="AIzaSyBNRZ25ezFXLH8TIhRPTOjuIdozGc4cWtY")
    model = genai.GenerativeModel('gemini-pro')
    app.run('127.0.0.1', 8001)
