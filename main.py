import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime

API_KEY = "ВАШ_КЛЮЧ_API"
HISTORY_FILE = "history.json"

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("500x500")

        # Элементы интерфейса
        tk.Label(root, text="Сумма:").pack(pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()

        self.from_currency = ttk.ComboBox(root, values=["USD", "EUR", "RUB", "GBP"])
        self.from_currency.set("USD")
        self.from_currency.pack(pady=5)

        tk.Label(root, text="в").pack()

        self.to_currency = ttk.ComboBox(root, values=["USD", "EUR", "RUB", "GBP"])
        self.to_currency.set("RUB")
        self.to_currency.pack(pady=5)

        tk.Button(root, text="Конвертировать", command=self.convert).pack(pady=10)

        self.result_label = tk.Label(root, text="Результат: ---", font=("Arial", 12, "bold"))
        self.result_label.pack()

        # Таблица истории
        self.tree = ttk.Treeview(root, columns=("Date", "From", "To", "Result"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("From", text="Из")
        self.tree.heading("To", text="В")
        self.tree.heading("Result", text="Итог")
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        self.load_history()

    def convert(self):
        amount = self.amount_entry.get()
        
        # Валидация
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительное число")
            return

        from_c = self.from_currency.get()
        to_c = self.to_currency.get()

        # Запрос к API
        url = f"https://exchangerate-api.com{API_KEY}/pair/{from_c}/{to_c}/{amount}"
        try:
            response = requests.get(url).json()
            if response["result"] == "success":
                result = response["conversion_result"]
                self.result_label.config(text=f"Результат: {result:.2f} {to_c}")
                self.save_history(amount, from_c, to_c, result)
            else:
                messagebox.showerror("Ошибка API", "Не удалось получить курс")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проблема с сетью: {e}")

    def save_history(self, amount, from_c, to_c, result):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "from": f"{amount} {from_c}",
            "to": to_c,
            "result": f"{result:.2f}"
        }
        
        history = []
        try:
            with open(HISTORY_FILE, "r") as f: history = json.load(f)
        except: pass

        history.append(entry)
        with open(HISTORY_FILE, "w") as f: json.dump(history, f)
        self.update_table(entry)

    def load_history(self):
        try:
            with open(HISTORY_FILE, "r") as f:
                for item in json.load(f):
                    self.update_table(item)
        except: pass

    def update_table(self, item):
        self.tree.insert("", 0, values=(item["date"], item["from"], item["to"], item["result"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
