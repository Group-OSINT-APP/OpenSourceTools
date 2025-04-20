import tkinter as tk
from tkinter import ttk
from data.fetch_weather import get_weather
from data.fetch_air_quality import get_air_quality
from data.fetch_traffic import get_traffic
from data.fetch_news import get_news

class SmartCityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartCity Insights Hub")
        self.geometry("800x600")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill='both')

        self.create_tab("Weather Info")
        self.create_tab("Air Quality")
        self.create_tab("Traffic Updates")
        self.create_tab("News & Alerts")

    def create_tab(self, title):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text=title.split()[0])

        label = tk.Label(tab, text=title, font=("Arial", 16))
        label.pack(pady=10)

        input_city = tk.Entry(tab)
        input_city.insert(0, "Enter city name")
        input_city.pack(pady=5)

        fetch_btn = tk.Button(tab, text="Fetch Data")
        fetch_btn.pack(pady=5)

        result_label = tk.Label(tab, text="", justify="left", anchor="w")
        result_label.pack(pady=10, fill='both', expand=True)

        loading_bar = ttk.Progressbar(tab, mode='indeterminate')
        loading_bar.pack(pady=5)

        def show_loading():
            result_label.config(text="")
            loading_bar.start()

        def hide_loading():
            loading_bar.stop()

        if title == "Weather Info":
            def fetch_weather():
                show_loading()
                self.after(100, run_weather)

            def run_weather():
                city = input_city.get()
                result = get_weather(city)
                hide_loading()
                if 'error' in result:
                    result_label.config(text=result['error'])
                else:
                    display = (f"City: {result['city']}\n"
                               f"Temperature: {result['temperature']}°C\n"
                               f"Weather: {result['description'].title()}\n"
                               f"Humidity: {result['humidity']}%\n"
                               f"Wind Speed: {result['wind_speed']} m/s")
                    result_label.config(text=display)
            fetch_btn.config(command=fetch_weather)

        elif title == "Air Quality":
            input_state = tk.Entry(tab)
            input_state.insert(0, "Enter state")
            input_state.pack(pady=5)

            input_country = tk.Entry(tab)
            input_country.insert(0, "Enter country")
            input_country.pack(pady=5)

            def fetch_air():
                show_loading()
                self.after(100, run_air)

            def run_air():
                city = input_city.get()
                state = input_state.get()
                country = input_country.get()
                result = get_air_quality(city, state, country)
                hide_loading()
                if 'error' in result:
                    result_label.config(text=result['error'])
                else:
                    display = (f"Location: {result['city']}, {result['state']}, {result['country']}\n"
                               f"AQI (US): {result['aqi_us']}\n"
                               f"Main Pollutant: {result['main_pollutant'].upper()}")
                    result_label.config(text=display)
            fetch_btn.config(command=fetch_air)

        elif title == "Traffic Updates":
            def fetch_traffic():
                show_loading()
                self.after(100, run_traffic)

            def run_traffic():
                city = input_city.get()
                result = get_traffic(city)
                hide_loading()
                if 'error' in result:
                    result_label.config(text=result['error'])
                else:
                    display = (f"Traffic Incidents in {result['city']} ({result['count']} total):\n" +
                               "\n".join(result['incidents']))
                    result_label.config(text=display)
            fetch_btn.config(command=fetch_traffic)

        elif title == "News & Alerts":
            def fetch_news():
                show_loading()
                self.after(100, run_news)

            def run_news():
                city = input_city.get()
                result = get_news(city)
                hide_loading()
                if 'error' in result:
                    result_label.config(text=result['error'])
                else:
                    news_lines = [f"- {article}" for article in result['headlines'][:5]]
                    display = f"Top News for {city}:\n" + "\n".join(news_lines)
                    result_label.config(text=display)
            fetch_btn.config(command=fetch_news)

if __name__ == '__main__':
    app = SmartCityApp()
    app.mainloop()
