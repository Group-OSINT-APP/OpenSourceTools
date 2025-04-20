import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QTabWidget, QWidget,
    QVBoxLayout, QLineEdit, QPushButton
)
from PyQt5.QtGui import QFont


class SmartCityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartCity Insights Hub")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.weather_tab = self.create_weather_tab()
        self.air_tab = self.create_tab("Air Quality Info Coming Soon")
        self.traffic_tab = self.create_tab("Traffic Info Coming Soon")
        self.news_tab = self.create_tab("News Alerts Coming Soon")

        self.tabs.addTab(self.weather_tab, "Weather")
        self.tabs.addTab(self.air_tab, "Air Quality")
        self.tabs.addTab(self.traffic_tab, "Traffic")
        self.tabs.addTab(self.news_tab, "News")

    def create_tab(self, message):
        tab = QWidget()
        layout = QVBoxLayout()

        label = QLabel(message)
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label)

        tab.setLayout(layout)
        return tab

    def create_weather_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("Enter City for Weather Info")
        title_label.setFont(QFont("Arial", 16))
        layout.addWidget(title_label)

        input_city = QLineEdit()
        input_city.setPlaceholderText("Enter city name")
        layout.addWidget(input_city)

        result_label = QLabel("")
        result_label.setFont(QFont("Arial", 12))
        layout.addWidget(result_label)

        fetch_button = QPushButton("Get Weather")
        layout.addWidget(fetch_button)

        def fetch_weather():
            city = input_city.text()
            result = self.get_weather(city)
            if 'error' in result:
                result_label.setText(result['error'])
            else:
                display = (
                    f"City: {result['city']}\n"
                    f"Temperature: {result['temperature']}°C\n"
                    f"Weather: {result['description'].title()}\n"
                    f"Humidity: {result['humidity']}%\n"
                    f"Wind Speed: {result['wind_speed']} m/s"
                )
                result_label.setText(display)

        fetch_button.clicked.connect(fetch_weather)

        tab.setLayout(layout)
        return tab

    def get_weather(self, city):
        # This is a dummy method for now. Replace with actual API call logic.
        if not city:
            return {'error': 'Please enter a city name.'}
        # Simulated response
        return {
            'city': city,
            'temperature': 23,
            'description': 'clear sky',
            'humidity': 50,
            'wind_speed': 5.5
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SmartCityApp()
    window.show()
    sys.exit(app.exec_())
