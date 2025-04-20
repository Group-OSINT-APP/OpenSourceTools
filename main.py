import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QPushButton, QProgressBar
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from data.fetch_weather import get_weather
from data.fetch_air_quality import get_air_quality
from data.fetch_traffic import get_traffic
from data.fetch_news import get_news

class SmartCityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartCity Insights Hub")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.weather_tab = self.create_tab("Weather Info")
        self.air_tab = self.create_tab("Air Quality")
        self.traffic_tab = self.create_tab("Traffic Updates")
        self.news_tab = self.create_tab("News & Alerts")

        self.tabs.addTab(self.weather_tab, "Weather")
        self.tabs.addTab(self.air_tab, "Air Quality")
        self.tabs.addTab(self.traffic_tab, "Traffic")
        self.tabs.addTab(self.news_tab, "News")

    def create_tab(self, title):
        tab = QWidget()
        layout = QVBoxLayout()

        label = QLabel(title)
        label.setFont(QFont("Arial", 16))
        layout.addWidget(label)

        input_city = QLineEdit()
        input_city.setPlaceholderText("Enter city name")
        layout.addWidget(input_city)

        fetch_btn = QPushButton("Fetch Data")
        layout.addWidget(fetch_btn)

        result_label = QLabel("")
        result_label.setAlignment(Qt.AlignTop)
        layout.addWidget(result_label)

        loading_bar = QProgressBar()
        loading_bar.setMaximum(0)
        loading_bar.setMinimum(0)
        loading_bar.setVisible(False)
        layout.addWidget(loading_bar)

        def show_loading():
            result_label.clear()
            loading_bar.setVisible(True)

        def hide_loading():
            loading_bar.setVisible(False)

        if title == "Weather Info":
            def fetch_weather():
                show_loading()
                QTimer.singleShot(100, lambda: run_weather())

            def run_weather():
                city = input_city.text()
                result = get_weather(city)
                hide_loading()
                if 'error' in result:
                    result_label.setText(result['error'])
                else:
                    display = (f"City: {result['city']}\n"
                               f"Temperature: {result['temperature']}°C\n"
                               f"Weather: {result['description'].title()}\n"
                               f"Humidity: {result['humidity']}%\n"
                               f"Wind Speed: {result['wind_speed']} m/s")
                    result_label.setText(display)
            fetch_btn.clicked.connect(fetch_weather)

        elif title == "Air Quality":
            input_state = QLineEdit()
            input_state.setPlaceholderText("Enter state")
            layout.insertWidget(2, input_state)

            input_country = QLineEdit()
            input_country.setPlaceholderText("Enter country")
            layout.insertWidget(3, input_country)

            def fetch_air():
                show_loading()
                QTimer.singleShot(100, lambda: run_air())

            def run_air():
                city = input_city.text()
                state = input_state.text()
                country = input_country.text()
                result = get_air_quality(city, state, country)
                hide_loading()
                if 'error' in result:
                    result_label.setText(result['error'])
                else:
                    display = (f"Location: {result['city']}, {result['state']}, {result['country']}\n"
                               f"AQI (US): {result['aqi_us']}\n"
                               f"Main Pollutant: {result['main_pollutant'].upper()}")
                    result_label.setText(display)
            fetch_btn.clicked.connect(fetch_air)

        elif title == "Traffic Updates":
            def fetch_traffic():
                show_loading()
                QTimer.singleShot(100, lambda: run_traffic())

            def run_traffic():
                city = input_city.text()
                result = get_traffic(city)
                hide_loading()
                if 'error' in result:
                    result_label.setText(result['error'])
                else:
                    display = (f"Traffic Incidents in {result['city']} ({result['count']} total):\n" +
                               "\n".join(result['incidents']))
                    result_label.setText(display)
            fetch_btn.clicked.connect(fetch_traffic)

        elif title == "News & Alerts":
            def fetch_news_data():
                show_loading()
                QTimer.singleShot(100, lambda: run_news())

            def run_news():
                city = input_city.text()
                result = get_news(city)
                hide_loading()
                if 'error' in result:
                    result_label.setText(result['error'])
                else:
                    news_lines = [f"- {article}" for article in result['headlines'][:5]]
                    display = f"Top News for {city}:\n" + "\n".join(news_lines)
                    result_label.setText(display)
            fetch_btn.clicked.connect(fetch_news_data)

        tab.setLayout(layout)
        return tab

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SmartCityApp()
    window.show()
    sys.exit(app.exec_())
