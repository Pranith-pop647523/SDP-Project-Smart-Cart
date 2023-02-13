import tkinter as tk


class ProductFrame:
    def __init__(self, master, product_name, price, quantity):
        self.master = master
        self.frame = tk.Frame(master)
        self.product_name = tk.Label(self.frame, text=product_name)
        self.price = tk.Label(self.frame, text="Price: $" + str(price))
        self.price_value = price
        self.quantity = tk.Label(self.frame, text="Quantity: " + str(quantity))
        self.quantity_value = quantity
        self.increase_button = tk.Button(
            self.frame, text="+", command=self.increase_quantity)
        self.decrease_button = tk.Button(
            self.frame, text="-", command=self.decrease_quantity)

        self.product_name.pack()
        self.price.pack()
        self.quantity.pack()
        self.increase_button.pack(side="left")
        self.decrease_button.pack(side="left")

    def increase_quantity(self):
        self.quantity_value += 1
        self.quantity.configure(text="Quantity: " + str(self.quantity_value))
        self.price_value = self.price_value * self.quantity_value
        self.price.configure(text="Price: $" + str(self.price_value))

    def decrease_quantity(self):
        if self.quantity_value > 0:
            self.quantity_value -= 1
            self.quantity.configure(
                text="Quantity: " + str(self.quantity_value))
            self.price_value = self.price_value / self.quantity_value
            self.price.configure(text="Price: $" + str(self.price_value))


class ShoppingCartApp:
    def __init__(self, master):
        self.master = master
        self.frames = []
        self.total_price = 0
        self.total_price_label = tk.Label(
            master, text="Total Price: $" + str(self.total_price))
        self.total_price_label.pack()

    def add_product_frame(self, product_name, price, quantity):
        new_frame = ProductFrame(self.master, product_name, price, quantity)
        self.frames.append(new_frame)
        new_frame.frame.pack
