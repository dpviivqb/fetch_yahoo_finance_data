from setuptools import setup

APP = ['fetch_yahoo_finance_data.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pandas', 'yfinance', 'openpyxl', 'certifi', 'chardet'],
    'includes': ['tkinter'],
    'plist': {
        'CFBundleName': 'YahooFinanceExporter',
        'CFBundleShortVersionString': '1.0.9',
        'CFBundleIdentifier': 'com.example.yahoofetcher',
        'NSPrincipalClass': 'NSApplication',
        'LSUIElement': False, 
    },
}

setup(
    app=APP,
    name='YahooFinanceExporter',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
