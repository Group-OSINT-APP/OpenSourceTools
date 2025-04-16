
import tkinter as tk
from tkinter import ttk

class TravelSmartPlannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel Smart Planner")
        self.geometry("800x600")
        self.configure(bg="#f0f4f8")

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ttk.Label(self, text="Travel Smart Planner", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=20)

        # Frame for input fields
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10)

        # Destination input
        ttk.Label(input_frame, text="Destination:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.destination_entry = ttk.Entry(input_frame, width=30)
        self.destination_entry.grid(row=0, column=1, padx=5, pady=5)

        # Start Date input
        ttk.Label(input_frame, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.start_date_entry = ttk.Entry(input_frame, width=30)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        # End Date input
        ttk.Label(input_frame, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.end_date_entry = ttk.Entry(input_frame, width=30)
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Budget input
        ttk.Label(input_frame, text="Budget ($):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.budget_entry = ttk.Entry(input_frame, width=30)
        self.budget_entry.grid(row=3, column=1, padx=5, pady=5)

        # Submit button
        submit_button = ttk.Button(self, text="Generate Itinerary", command=self.generate_itinerary)
        submit_button.pack(pady=20)

        # Output text box
        self.output_text = tk.Text(self, height=10, width=80, wrap="word")
        self.output_text.pack(pady=10)

    def generate_itinerary(self):
        destination = self.destination_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        budget = self.budget_entry.get()

        itinerary = f"Planning trip to {destination} from {start_date} to {end_date} with a budget of ${budget}.\n"
        itinerary += "\nFetching data from APIs... (This will be implemented soon!)"

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, itinerary)

if __name__ == "__main__":
    app = TravelSmartPlannerApp()
    app.mainloop()

