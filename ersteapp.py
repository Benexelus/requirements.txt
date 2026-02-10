import tkinter as tk
from tkinter import messagebox, filedialog
import json
import statistics
import matplotlib.pyplot as plt

# -----------------------------
# Analyse-Funktionen
# -----------------------------

def parse_numbers(text):
    try:
        numbers = list(map(int, text.replace(",", " ").split()))
        if not numbers:
            raise ValueError
        return numbers
    except:
        messagebox.showerror("Fehler", "Bitte nur ganze Zahlen eingeben.")
        return None


def analyze_numbers(numbers):
    analysis = {
        "sorted_asc": sorted(numbers),
        "sorted_desc": sorted(numbers, reverse=True),
        "max": max(numbers),
        "min": min(numbers),
        "positive": [n for n in numbers if n >= 0],
        "negative": [n for n in numbers if n < 0],
        "mean": statistics.mean(numbers),
        "repetitions": {n: numbers.count(n) for n in set(numbers)}
    }
    return analysis


# -----------------------------
# Diagramme
# -----------------------------

def show_diagram(numbers, analysis):
    plt.figure("Zahlenanalyse")

    plt.plot(numbers, marker="o", label="Zahlenfolge")
    plt.axhline(analysis["mean"], linestyle="--", label="Durchschnitt")

    plt.scatter(numbers.index(analysis["max"]), analysis["max"], color="green", s=100, label="Maximum")
    plt.scatter(numbers.index(analysis["min"]), analysis["min"], color="red", s=100, label="Minimum")

    plt.title("Interaktive Zahlenanalyse")
    plt.xlabel("Position")
    plt.ylabel("Wert")
    plt.legend()
    plt.grid(True)

    plt.show()


# -----------------------------
# GUI
# -----------------------------

class ZahlenApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Zahlenanalyse – Lernapp (Q1)")
        self.root.geometry("700x500")

        tk.Label(root, text="Ganze Zahlen eingeben:", font=("Arial", 12)).pack(pady=5)

        self.text_input = tk.Text(root, height=5)
        self.text_input.pack(fill="x", padx=10)

        tk.Label(
            root,
            text="Zahlen mit Leerzeichen oder Komma trennen",
            fg="gray"
        ).pack()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Analysieren", command=self.run_analysis).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Diagramm", command=self.show_plot).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Speichern", command=self.save_project).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Laden", command=self.load_project).grid(row=0, column=3, padx=5)

        self.output = tk.Text(root, height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

        self.numbers = []
        self.analysis = None


    def run_analysis(self):
        text = self.text_input.get("1.0", "end")
        numbers = parse_numbers(text)
        if not numbers:
            return

        self.numbers = numbers
        self.analysis = analyze_numbers(numbers)

        self.output.delete("1.0", "end")
        self.output.insert("end", f"Sortiert aufsteigend: {self.analysis['sorted_asc']}\n")
        self.output.insert("end", f"Sortiert absteigend: {self.analysis['sorted_desc']}\n\n")

        self.output.insert("end", f"Höchster Wert: {self.analysis['max']}\n")
        self.output.insert("end", f"Tiefster Wert: {self.analysis['min']}\n\n")

        self.output.insert("end", f"Positive Zahlen: {self.analysis['positive']}\n")
        self.output.insert("end", f"Negative Zahlen: {self.analysis['negative']}\n\n")

        self.output.insert("end", f"Durchschnitt: {self.analysis['mean']}\n")
        self.output.insert("end", f"Wiederholungen:\n")

        for k, v in self.analysis["repetitions"].items():
            self.output.insert("end", f"  {k}: {v}x\n")


    def show_plot(self):
        if not self.analysis:
            messagebox.showwarning("Hinweis", "Bitte zuerst analysieren.")
            return
        show_diagram(self.numbers, self.analysis)


    def save_project(self):
        if not self.numbers:
            return

        file = filedialog.asksaveasfilename(defaultextension=".json")
        if file:
            with open(file, "w") as f:
                json.dump(self.numbers, f)
            messagebox.showinfo("Gespeichert", "Projekt gespeichert.")


    def load_project(self):
        file = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if file:
            with open(file, "r") as f:
                self.numbers = json.load(f)

            self.text_input.delete("1.0", "end")
            self.text_input.insert("end", " ".join(map(str, self.numbers)))
            self.run_analysis()


# -----------------------------
# Start
# -----------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ZahlenApp(root)
    root.mainloop()
