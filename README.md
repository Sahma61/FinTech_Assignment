This Project is done for submission to **Financial Services Innovation Lab, Georgia Tech Programming Task for Summer Research**.
I have primarily used Python and its related tech-stack/libs for achieving the frontend and backend Developement work. I have taken certain degree of liberty in coding up the solution to the open-ended question.


## **Components**:
1. **backend.py** (Python3) - module that contains:
   - Utility to download SEC 10-K filings
   - Utility to fetch data from LLM Model
   - Utility to fetch info from LLM Model
   - Utility to parse text from HTML page
   - Utility to get Pandas DataFrame from list of string info

2. **flask_server.py** (Python3, Flask)  - Locally-hosted Flask Server that initializes the LLM Model and utilizes the backend utilities to fetch data and info from LLM APIs.

3. **app.py** (Python3, Dash) - Dashboard to show SEC 10-K info and data

## **Steps to run the Project**:
1. Run the **Flask Server** - `python flask_server.py`
2. Run the **Dash  App** - `python app.py`
3. Goto [Web Dashboard](http://127.0.0.1:8050/)

## **Note**:
The main reason for choosing **Python** is its extensive library support and the ease of coding up new things. Additionally, **Python** has been my go-to language since college days, and I have primarily worked in **Python** in a professional setting for 2 years. Therefore, it seems natural to me.

**Dashboard creation/frontend** development is usually not my primary experience, but I have tried to use **Dash** as it's Python-supported and I needed very little to get started.

**For Server Creation**, **Flask** is the best option available for Python environment. And, I have previously worked with it in a Production environment.


