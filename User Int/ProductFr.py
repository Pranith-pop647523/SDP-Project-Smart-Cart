import tkinter as tk
import customtkinter


class ProductFrame(tk.Frame):
    def __init__(self, parent, product_name, product_price,  rem_img, remove_callback, update_callback, ** kwargs):
        super().__init__(parent, bg='black', ** kwargs)

        # Initialize the product name and price
        self.product_name = product_name
        print(product_name)
        self.product_price = product_price
        self.quantity = 1
        self.remove_callback = remove_callback
        self.update_callback = update_callback
        # Create the label for the product name and add it to the frame
        self.name_label = tk.Label(
            self, text=self.product_name, bg='black', font=("Poppins", 32), anchor="w", width=9)
        self.name_label.pack(side="left", padx=(0, 10))

        # Create the button to decrease the quantity and add it to the frame
        self.quantity_button_down = customtkinter.CTkButton(
            self, width=32, fg_color='#6A51FF',  text='-', font=("Poppins", 32), command=self.decrease_quantity)
        self.quantity_button_down.pack(side='left')

        self.quantity_label = tk.Label(
            self, text="1", bg='black', width=2, font=("Poppins", 32))
        self.quantity_label.pack(side="left")

        # Create the button to increase the quantity and add it to the frame
        self.quantity_button_up = customtkinter.CTkButton(
            self, width=32, fg_color='#6A51FF', text='+', font=("Poppins", 32), command=self.increase_quantity)
        self.quantity_button_up.pack(side='left')

        # Create the label for the product price and add it to the frame
        self.price_label = tk.Label(
            self, text=f"£{self.product_price:.2f}", width=6, font=("Poppins", 32), bg='black')
        self.price_label.pack(side="left")

        self.remove = tk.Button(
            self,  image=rem_img, bg='black', relief='flat', borderwidth=0, font=('Poppins', 32), command=self.remove_product)
        self.remove.pack(side='left')
        # Create the label for the change in price and add it to the frame

    def remove_product(self):

        # call the callback function with this ProductFrame object as an argument
        self.destroy()
        self.remove_callback(self)

    def decrease_quantity(self):
        # Decrease the quantity and update the quantity label
        if self.quantity == 1:
            return

        self.quantity -= 1
        self.quantity_label.config(text=f"{self.quantity}")

        # Update the change in price label
        change = self.product_price
        self.price_label.config(text=f"£{change*self.quantity:.2f}")
        self.update_callback(self)

    def increase_quantity(self):
        # Increase the quantity and update the quantity label
        self.quantity += 1
        self.quantity_label.config(text=f"{self.quantity}")

        # Update the change in price label
        change = self.product_price

        self.price_label.config(text=f"£{change*self.quantity:.2f}")
        self.update_callback(self)
