import tkinter as tk
import customtkinter


class ProductFrame(tk.Frame):
    # remember to add remove image
    def __init__(self, parent, product_name, price, quantity, remove_image, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg='black', *args, **kwargs)

        self.product_name = product_name
        self.fixed = price
        self.price = price
        self.quantity = quantity
        # global ItemCnt
        ItemCnt += 1

        self.product_label = tk.Label(self, text=self.product_name, bg='black')
        self.price_label = tk.Label(self, text=f'${self.price}', bg='black')
        self.quantity_label = tk.Label(
            self, text=f'{self.quantity}', bg='black')
        self.quantity_button_up = customtkinter.CTkButton(
            self, width=15, height=10,  fg_color='#2D2A2A', text='+', anchor='w', font=('Poppins', 10), command=self.increase_quantity)
        self.quantity_button_down = customtkinter.CTkButton(
            self, width=15, height=10,  fg_color='#2D2A2A', text='-', anchor='w', font=('Poppins', 10), command=self.decrease_quantity)
        self.remove = tk.Button(
            self,  image=remove_image, relief='flat', borderwidth=0, font=('Poppins', 10), command=self.remove_item)

        self.product_label.pack(side='left', padx=50)
        self.quantity_button_down.pack(side='left', padx=5)
        self.quantity_label.pack(side='left', padx=5)
        self.quantity_button_up.pack(side='left', padx=5)
        self.price_label.pack(side='left', padx=50)
        self.remove.pack(side='left', padx=5)

    def increase_quantity(self):
        global TotalVal
        global ItemCnt
        TotalVal += self.fixed
        ItemCnt += 1
        self.quantity += 1
        self.quantity_label.config(text=f'{self.quantity}')
        self.price = int(self.fixed) * int(self.quantity)
        self.price_label.configure(text=f'${(self.price)}')

    def decrease_quantity(self):
        global TotalVal
        global ItemCnt
        if self.quantity > 1:
            ItemCnt -= 1
            TotalVal -= self.fixed
            self.quantity -= 1
            self.quantity_label.config(text=f'{self.quantity}')
            self.price = int(self.fixed) * int(self.quantity)
            self.price_label.configure(text=f'${(self.price)}')

    def get_product(self):
        return self.product_name

    def get_price(self):  # getters
        return int(self.price)

    def get_quantity(self):
        return int(self.quantity)

    def remove_item(self):
        global TotalVal
        global ItemCnt
        TotalVal -= self.fixed*self.quantity
        ItemCnt -= self.quantity
        self.quantity = 0
        self.price = 0
        self.pack_forget()
