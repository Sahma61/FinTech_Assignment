#!/usr/bin/python3

"""
Flask server Module.

Flask Server that initializes the LLM Model
and utilizes the backend utilities to
fetch data and info from LLM APIS
"""

import os
from flask import Flask, render_template, jsonify

import google.generativeai as genai
from dotenv import load_dotenv

from backend import download_sec10k_data, parse_sec_info, parse_sec_data

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    """
    Landing Page.

    args:
    returns:
        str - Marker to direct user to infer end-point
    """
    return render_template('landing_page.html')


@app.route("/infer/<ticker>/<start>/<end>")
def infer_from_sec10k(
        ticker: str,
        start: str,
        end: str) -> str:
    """
    Fetch sec 10-k data and info.
    
    fetches sec 10-k data and info from the LLM API
    args:
        ticker: str - company ticker
        start: str - start date
        end: str - end date
    returns:
        str - JSON string containing  data, info, column names
    """
    print(f"Received request for ticker {ticker} from {start} to {end}")
    status, msg = download_sec10k_data(ticker, start, end)
    if not status:
        return jsonify({'info': msg, 'data': [], 'cols': []})
    try:
        print("Parsing Info from 10-K filings")
        info = parse_sec_info(model, ticker)
        print("Parsed Info from 10-K filings")

        print("Parsing Data from 10-K filings")
        data = parse_sec_data(model, ticker)
        print("Parsed Data from 10-K filings")

        cols = [list(datum.columns) for datum in data]
        data = [datum.to_dict('records') for datum in data]
    except Exception as err:
        info = str(err)
        data = cols = []
    return jsonify({'info': info, 'data': data, 'cols': cols})


if __name__ == "__main__":
    load_dotenv()
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('gemini-pro')
    app.run('127.0.0.1', 8001)
