import asyncio
import sys
import json
import urllib.request
from PyQt6.QtWidgets import QLabel, QApplication, QWidget
import aiohttp

async def get_weather():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Bristol?unitGroup=metric&elements=temp&include=current%2Cfcst&key=R42LH4HH8PG59J5GLWNNNNLBA&contentType=json") as response:
                jsonData = await response.json()
                ctemp = jsonData['currentConditions']['temp']
                ctemp = f"{ctemp}°C"
                return ctemp
    except aiohttp.ClientError as e:
        print('HTTP error occurred:', e)
        sys.exit()

def main():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setGeometry(100, 100, 200, 50)
    w.setWindowTitle("PyQt6")

    loop = asyncio.get_event_loop()
    ctemp = loop.run_until_complete(get_weather())

    b = QLabel(w)
    b.setText(ctemp)
    b.show()

    w.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
