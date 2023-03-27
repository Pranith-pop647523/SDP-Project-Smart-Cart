import tkinter as tk
import test1a


class MyUI:
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(self.root, text="Scanned barcode: ")
        self.label.pack()
        self.barcode_scanner = test1a.BarcodeScanner(self.handle_barcode)

    def start(self):
        self.barcode_scanner.start()
        self.root.mainloop()
        self.barcode_scanner.stop()

    def handle_barcode(self, barcode):
        self.label.config(text="Scanned barcode: " + barcode)


ui = MyUI()
ui.start()
