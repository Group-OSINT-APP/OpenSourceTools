import tkinter as tk
from tkinter import ttk
import json
from data.fetch_weather import get_weather
from data.fetch_air_quality import get_air_quality
from data.fetch_news import get_news
from data.fetch_mapquest_traffic import get_mapquest_traffic_incidents, get_city_coordinates

class SmartCityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌆 SmartCity Insights Hub")
        self.geometry("950x700")
        self.configure(bg="#f0f2f5")

        self.set_theme()
        self.create_tabs()

    def set_theme(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TNotebook.Tab", padding=[12, 8], font=("Segoe UI", 11, "bold"))
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TEntry", padding=4)

    def create_tabs(self):
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill='both', padx=10, pady=10)

        self.create_tab("Weather Info")
        self.create_tab("Air Quality")
        self.create_tab("Traffic Incidents")
        self.create_tab("News & Alerts")

    def create_tab(self, title):
        tab = ttk.Frame(self.tabs, padding=20)
        self.tabs.add(tab, text=title.split()[0])

        header = ttk.Label(tab, text=title, style="Header.TLabel")
        header.pack(pady=(0, 15))

        input_city = ttk.Entry(tab, width=30)
        input_city.insert(0, "Enter city name")
        input_city.pack(pady=5)

        fetch_btn = ttk.Button(tab, text="Fetch Data")
        fetch_btn.pack(pady=10)

        result_label = tk.Label(
            tab, text="", justify="left", anchor="nw",
            font=("Segoe UI", 10), bg="#ffffff",
            relief="solid", borderwidth=1, padx=10, pady=10, wraplength=800
        )
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
                    display = (
                        f"📍 City: {result['city']}\n"
                        f"🌡 Temperature: {result['temperature']}\u00b0C\n"
                        f"☁️ Weather: {result['description'].title()}\n"
                        f"💧 Humidity: {result['humidity']}%\n"
                        f"💨 Wind Speed: {result['wind_speed']} m/s"
                    )
                    result_label.config(text=display)

            fetch_btn.config(command=fetch_weather)

        elif title == "Air Quality":
            input_state = ttk.Entry(tab, width=30)
            input_state.insert(0, "Enter state")
            input_state.pack(pady=5)

            selected_country = tk.StringVar(value="USA")
            country_dropdown = ttk.Combobox(tab, textvariable=selected_country, state="readonly", values=["USA"])
            country_dropdown.pack(pady=5)

            def fetch_air():
                show_loading()
                self.after(100, run_air)

            def run_air():
                city = input_city.get()
                state = input_state.get()
                country = selected_country.get()
                result = get_air_quality(city, state, country)
                hide_loading()
                if 'error' in result:
                    result_label.config(text=result['error'])
                else:
                    display = (
                        f"📍 Location: {result['city']}, {result['state']}, {result['country']}\n"
                        f"🌫 AQI (US): {result['aqi_us']}\n"
                        f"🔬 Main Pollutant: {result['main_pollutant'].upper()}"
                    )
                    result_label.config(text=display)

            fetch_btn.config(command=fetch_air)

        elif title == "Traffic Incidents":
            def fetch_traffic():
                show_loading()
                self.after(100, run_traffic)

            def run_traffic():
                city = input_city.get()
                coordinates = get_city_coordinates(city)
                if coordinates:
                    lat, lng = coordinates
                    radius = 0.3
                    bbox = f"{lat - radius},{lng - radius},{lat + radius},{lng + radius}"
                    traffic_data = get_mapquest_traffic_incidents(bbox)
                    hide_loading()
                    if 'error' in traffic_data:
                        result_label.config(text=traffic_data['error'])
                    elif 'incidents' in traffic_data:
                        display_text = f"🚦 Traffic Incidents near {city}:\n"
                        if traffic_data['incidents']:
                            for incident in traffic_data['incidents'][:20]:
                                severity = incident.get('severity', 'N/A')
                                short_desc = incident.get('shortDesc', 'No Description')
                                incident_type = incident.get('type', 'N/A')
                                type_display = incident_type.title() if isinstance(incident_type, str) else str(incident_type)
                                lat_inc = incident.get('lat', 0.0)
                                lng_inc = incident.get('lng', 0.0)

                                display_text += (
                                    f"\n🛑 TYPE: {type_display}\n"
                                    f"⚠️ SEVERITY: {severity}\n"
                                    f"📝 DESCRIPTION: {short_desc}\n"
                                    f"📍 LOCATION: ({lat_inc:.4f}, {lng_inc:.4f})\n"
                                    f"{'-'*40}"
                                )
                        else:
                            display_text += "✅ No traffic incidents reported in this area."
                        result_label.config(text=display_text)
                    else:
                        result_label.config(text="Could not retrieve traffic incident data.")
                else:
                    hide_loading()
                    result_label.config(text=f"Could not find coordinates for '{city}'.")

            fetch_btn.config(command=fetch_traffic)

        elif title == "News & Alerts":
            def fetch_news_data():
                show_loading()
                self.after(100, run_news)

            def run_news():
                city = input_city.get()
                result = get_news(city)
                hide_loading()
                if 'error' in result:
                    result_label.config(text=result['error'])
                else:
                    seen = set()
                    unique_headlines = []
                    for headline in result['headlines']:
                        if headline not in seen:
                            unique_headlines.append(headline)
                            seen.add(headline)

                    news_lines = [f"- {article}" for article in unique_headlines[:15]]
                    display = f"📰 Top News for {city}:\n" + "\n".join(news_lines)
                    result_label.config(text=display)

            fetch_btn.config(command=fetch_news_data)

if __name__ == '__main__':
    app = SmartCityApp()
    app.mainloop()
