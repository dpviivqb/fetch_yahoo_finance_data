from setuptools import setup

APP = ['fetch_yahoo_finance_data.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pandas', 'yfinance', 'openpyxl', 'tkinter', 'certifi', 'chardet'],
    'includes': ['tkinter'],
}

setup(
    app=APP,
    name='YahooFinanceExporter',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
