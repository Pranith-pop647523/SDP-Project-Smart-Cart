import tkinter as tk


class ScannerApp:
    def __init__(self):
        # Create a root window
        self.root = tk.Tk()

        # Create a label to display scanned barcodes
        self.label = tk.Label(
            self.root, text="Scanned barcodes:", font=("Arial", 16))
        self.label.pack()

        # Create a variable to store the scanned barcode
        self.barcode = ""

        # Bind the '<Key>' event to the 'on_key' function
        self.root.bind('<Key>', self.on_key)

        # Start the main event loop
        self.root.mainloop()

    def on_key(self, event):
        # Get the character that was pressed
        char = event.char

        # Check if the character is a digit or a letter
        if char.isalnum():
            # Add the character to the scanned barcode
            self.barcode += char
        elif event.keysym == 'Return':
            # Add the scanned barcode to the label
            current_text = self.label.cget("text")
            self.label.config(text=current_text + "\n" + self.barcode)

            # Clear the scanned barcode variable
            self.barcode = ""


if __name__ == '__main__':
    # Create the scanner app
    app = ScannerApp()
