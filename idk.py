import tkinter as tk


class ProductFrame(tk.Frame):
    def __init__(self, parent, product_name, price, quantity, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.product_name = product_name
        self.price = price
        self.quantity = quantity

        self.product_label = tk.Label(self, text=self.product_name)
        self.price_label = tk.Label(self, text=f'${self.price}')
        self.quantity_label = tk.Label(self, text=f'Quantity: {self.quantity}')
        self.quantity_button = tk.Button(
            self, text='+', command=self.increase_quantity)

        self.product_label.pack(side='left')
        self.price_label.pack(side='left')
        self.quantity_label.pack(side='left')
        self.quantity_button.pack(side='right')

    def increase_quantity(self):
        self.quantity += 1
        self.quantity_label.config(text=f'Quantity: {self.quantity}')


root = tk.Tk()
product_frame = ProductFrame(root, 'Product 1', 10, 1)
product_frame.pack()
root.mainloop()
