import tkinter as tk
from tkinter import messagebox
import json
import yaml
import xmltodict
import threading

class DataHandler:
    def __init__(self):
        self.data = {}

    def load_file(self, filename):
        file_extension = filename.split('.')[-1]
        if file_extension == 'json':
            self.load_json(filename)
        elif file_extension == 'yml':
            self.load_yaml(filename)
        elif file_extension == 'xml':
            self.load_xml(filename)
        else:
            print("Error: Unsupported file format.")

    def save_file(self, filename):
        file_extension = filename.split('.')[-1]
        if file_extension == 'json':
            self.save_json(filename)
        elif file_extension == 'yml' or file_extension == 'yaml':
            self.save_yaml(filename)
        elif file_extension == 'xml':
            self.save_xml(filename)
        else:
            print("Error: Unsupported file format.")

    def load_json(self, filename):
        with open(filename, 'r') as file:
            try:
                self.data = json.load(file)
                print("Loaded JSON data successfully.")
            except json.JSONDecodeError:
                print("Error: Invalid JSON syntax.")

    def save_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.data, file, indent=4)
        print("Data saved to JSON file successfully.")

    def load_yaml(self, filename):
        with open(filename, 'r') as file:
            try:
                self.data = yaml.safe_load(file)
                print("Loaded YAML data successfully.")
            except yaml.YAMLError:
                print("Error: Invalid YAML syntax.")

    def save_yaml(self, filename):
        with open(filename, 'w') as file:
            yaml.dump(self.data, file, default_flow_style=False)
        print("Data saved to YAML file successfully.")

    def load_xml(self, filename):
        with open(filename, 'r') as file:
            try:
                self.data = xmltodict.parse(file.read())
                print("Loaded XML data successfully.")
            except xmltodict.expat.ExpatError:
                print("Error: Invalid XML syntax.")

    def save_xml(self, filename):
        with open(filename, 'w') as file:
            file.write(xmltodict.unparse(self.data, pretty=True))
        print("Data saved to XML file successfully.")

def transferuj():
    nazwa_pliku_we = entry_we.get()
    nazwa_pliku_wy = entry_wy.get()

    handler = DataHandler()
    load_event = threading.Event()

    def load_worker():
        try:
            handler.load_file(nazwa_pliku_we)
            load_event.set()  # Signal that loading is complete
        except FileNotFoundError:
            messagebox.showerror("Błąd", f"Plik {nazwa_pliku_we} nie został znaleziony.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

    def save_worker():
        load_event.wait()  # Wait for the loading to complete
        try:
            handler.save_file(nazwa_pliku_wy)
            messagebox.showinfo("Sukces", "Plik został przetworzony pomyślnie!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

    load_thread = threading.Thread(target=load_worker)
    save_thread = threading.Thread(target=save_worker)
    
    load_thread.start()
    save_thread.start()

# Tworzenie głównego okna
root = tk.Tk()
root.title("Transferuj Plik")
root.geometry("400x200")

# Etykieta i pole tekstowe dla pliku wejściowego
label_we = tk.Label(root, text="Nazwa pliku wejściowego:")
label_we.pack(pady=5)
entry_we = tk.Entry(root, width=50)
entry_we.pack(pady=5)

# Etykieta i pole tekstowe dla pliku wyjściowego
label_wy = tk.Label(root, text="Nazwa pliku wyjściowego:")
label_wy.pack(pady=5)
entry_wy = tk.Entry(root, width=50)
entry_wy.pack(pady=5)

# Tworzenie przycisku "Transferuj"
transfer_button = tk.Button(root, text="Transferuj", command=transferuj)
transfer_button.pack(pady=20)

# Uruchomienie głównej pętli
root.mainloop()
