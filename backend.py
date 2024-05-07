"""
Module contains:
    utility to download sec 10-k filings
    utility to fetch data from LLM Model
    utility to fetch info from LLM Model
    utility to parse text from html page
    utility to get pandas Dataframe from list of string info
"""

import os
import re
import pandas as pd
from bs4 import BeautifulSoup

import google.generativeai as genai
from sec_edgar_downloader import Downloader


def get_dataframe(text: str) -> [pd.DataFrame]:
    """
    Converts string data to a list of pandas Dataframe
    args:
        text: str - output data from the LLM
    returns:
        [pd.DataFrame] - list of tables, each table as a pandas df
    """

    tables = []
    current_table = []
    text = re.sub(r'[\'$(),%]', '', text)
    text = text.split("\n")
    for i, t in enumerate(text):
        line = t.split("|")
        line = [x.strip() for x in line]
        line = list(filter(lambda x: x, line))
        print(line)
        if line:
            if line[0].startswith('-') or line[0].startswith(':'):
                continue
            line = [x.replace("-", "0").strip() for x in line]
            line = [x.replace("$", "").strip() for x in line]
            new_line = []
            if i >= 1:
                for x in line:
                    j = 0
                    y = ""
                    while j < len(x) and (x[j].isdigit() or x[j] == '.'):
                        y += x[j]
                        j += 1
                    new_line.append(y)
                line = new_line
            current_table.append(line)
        else:
            tables.append(
                    pd.DataFrame(
                        current_table[1:],
                        columns=current_table[0]
                        )
                    )
            current_table = []

    if current_table:
        print(current_table)
        tables.append(
                pd.DataFrame(
                    current_table[1:],
                    columns=current_table[0]
                    )
                )

    return tables


def extract_text_from_html(html_file_path: str) -> str:
    """
    Extracts text from html tags
    args:
        html_file_path: str - path to raw 10-K filings file
    returns:
        str - processed text with html tags removed
    """

    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)

    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text


def download_sec10k_data(
        ticker: str,
        start: str = "1995-01-01",
        end: str = "2023-12-31",
        path: str = "/home/sahma61/") -> None:
    """
    Downloads SEC 10-k Data by ticker
    and start and end dates
    args:
        ticker: str - the company ticker
        start: str - start date
        end: str - end date
        path: str - path to the download location
    returns:
        None
    """

    dl = Downloader("MyCompanyName", "my.email@domain.com", path)
    print(f"Downloading 10-K filings for {ticker}")
    try:
        dl.get("10-K", ticker, after=start, before=end)
        print(f"Downloaded 10-K filings for {ticker}")
        return True, ""
    except ValueError as err:
        print(f"Couldn't downloade 10-K filings for {ticker}")
        return False, str(err)


def parse_sec_data(
        model: genai.GenerativeModel,
        ticker: str,
        path: str = "/home/sahma61/sec-edgar-filings") -> [pd.DataFrame]:
    """
    Fetches sec 10-k data from
    LLM API and parses the Data into string
    args:
        model: genai.GenerativeModel - LLM Model to fetch data from
        ticker: str - company ticker
        path: str - path to the sec 10-K filings Path
    returns:
        [pd.DataFrame] - list of tables, each table as a pandas df
    """

    path += f'/{ticker}/10-K'
    for dr in os.listdir(path):
        text = extract_text_from_html(
                os.path.join(path, f'{dr}/full-submission.txt'))
        response = model.generate_content(
                "generate revenue and growth insights data \
                from the 10K filings in tabular format, \
                column should be years:\n" + text[:50000])
        print(response.text)
        return get_dataframe(response.text)


def parse_sec_info(
        model: genai.GenerativeModel,
        ticker: str,
        path: str = "/home/sahma61/sec-edgar-filings") -> str:
    """
    Fetches sec 10-k data from
    LLM API and parses the Data into string
    args:
        model: genai.GenerativeModel - LLM Model to fetch info from
        ticker: str - company ticker
        path: str - path to the sec 10-K filings Path
    returns:
        str - the info output from LLM Model
    """

    path += f'/{ticker}/10-K'
    for dr in os.listdir(path):
        text = extract_text_from_html(
                os.path.join(path, f'{dr}/full-submission.txt'))
        response = model.generate_content(
                "generate revenue and growth insights summary \
                from the 10K filings, in 1000 words\n" + text[:50000])
        return response.text
