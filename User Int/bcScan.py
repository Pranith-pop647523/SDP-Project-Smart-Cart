import threading
import tkinter as tk
import keyboard


class BarcodeScanner:
    def __init__(self):
        self._barcode = []
        self._lock = threading.Lock()

    def _on_key(self, event):
        with self._lock:
            if event.event_type == 'down' and event.name != 'enter':
                self._barcode.append(event.name)

            elif event.event_type == 'down' and event.name == 'enter':
                print('csac')
                barcode = ''.join(self._barcode)
                print(barcode)
                self._barcode = []
                return barcode

    def start(self):
        keyboard.hook(self._on_key)


class BarcodeUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Barcode Scanner')
        self.geometry('400x100')

        self._barcode_scanner = BarcodeScanner()
        self._barcode_scanner.start()

        self._barcode_var = tk.StringVar()
        self._barcode_var.set('Scan a barcode...')

        barcode_label = tk.Label(self, textvariable=self._barcode_var)
        barcode_label.pack(pady=20)

        self.after(10, self._update_barcode)

    def _update_barcode(self):
        barcode = self._barcode_scanner._on_key(keyboard.read_event())
        print('help'+barcode)
        if barcode:
            self._barcode_var.set(f'Scanned: {barcode}')
        self.after(10, self._update_barcode)


if __name__ == '__main__':
    app = BarcodeUI()
    app.mainloop()
