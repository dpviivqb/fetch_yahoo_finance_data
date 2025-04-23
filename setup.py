from setuptools import setup

APP = ['app.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pandas', 'yfinance', 'openpyxl'],
}

setup(
    app=APP,
    name='YahooFinanceExporter',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
