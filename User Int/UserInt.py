import threading
import tkinter as tk
import customtkinter
import barcode_scanner as brs
import time
import os
from PIL import Image


BG_COL = '#000000'
TEXT_COL = '#FFFFFF'

frames = {}  # reference to each product frame created

totals = {}  # calc total

TotalVal = 0
ItemCnt = 0


root = tk.Tk()
root.title("Shopping Cart")
root.option_add("*Font", "Poppins 12 ")


# Configure first column
root.geometry('800x480')
root.config(bg=BG_COL)


remove_image = tk.PhotoImage(file="bin_white.png")

# Top line

canvas = tk.Canvas(root, bg=BG_COL, height=480,
                   width=800, highlightthickness=0)
canvas.place(x=0, y=0)

canvas.create_line(29.38, 27.6, 400+29.38, 27.6, fill=TEXT_COL, width=1)


# Shopping cart title


label_1 = tk.Label(root, text="Shopping Cart", bg=BG_COL,
                   fg=TEXT_COL, font=("Poppins", 12), anchor='w')
label_1.place(x=39.75, y=35.42, width=129.84, height=18)

# Item count


Items = tk.Label(root, text=f"You have {ItemCnt} items in your cart ", bg=BG_COL,
                 fg=TEXT_COL, font=("Nonita", 9), anchor='w')
Items.place(x=39.75, y=52.51, width=146.92, height=13)

# First frame

ProductFrame = tk.Frame(root, bg=BG_COL, borderwidth=1, relief="groove")
ProductFrame.place(x=29, y=70.51, width=418, height=120)


# Checkout frame


canvas.create_line(489.97, 325.55, 489.97+239.18,
                   325.55, fill=TEXT_COL, width=1)

Subtotal = tk.Label(root, text="Subtotal", bg=BG_COL,
                    fg=TEXT_COL, font=("Poppins", 9), anchor='w')
Subtotal.place(x=489.98, y=335.49, width=94.3, height=14)

Tax = tk.Label(root, text="Tax", bg=BG_COL,
               fg=TEXT_COL, font=("Poppins", 9), anchor='w')
Tax.place(x=489.98, y=353.94, width=94.3, height=14)

Total = tk.Label(root, text="Total", bg=BG_COL,
                 fg=TEXT_COL, font=("Poppins", 9), anchor='w')
Total.place(x=489.98, y=372.39, width=94.3, height=14)


SubtotalAmt = tk.Label(root, text=f"${0}", bg=BG_COL,
                       fg=TEXT_COL, font=("Poppins", 9), anchor='e')
SubtotalAmt.place(x=634.85, y=336.49, width=94.3, height=14)

TaxAmt = tk.Label(root, text=f"${0}", bg=BG_COL,
                  fg=TEXT_COL, font=("Poppins", 9), anchor='e')
TaxAmt.place(x=634.85, y=354.93, width=94.3, height=14)


TotalAmt = tk.Label(root, text=f"${0}", bg=BG_COL,
                    fg=TEXT_COL, font=("Poppins", 9), anchor='e')
TotalAmt.place(x=634.85, y=372.39, width=94.3, height=14)


CheckoutFrame = tk.Frame(root, bg=BG_COL, borderwidth=0, relief="groove")
CheckoutFrame.place(x=489.98, y=404.51, width=239.18, height=41)

TotalCost = tk.Label(CheckoutFrame, text="Total", bg=BG_COL,
                     fg=TEXT_COL, font=("Poppins", 9), anchor='w')


Checkout = customtkinter.CTkButton(
    CheckoutFrame, width=250, fg_color='#2D2A2A', text='Checkout', anchor='w', font=('Poppins', 10))

Checkout.pack(anchor='ne')


def toggle_button_text(button):
    if button.cget("text") == 'Stop':
        button.configure(text="Follow")

    else:
        button.configure(text="Stop")


Park = customtkinter.CTkButton(
    root, width=239, height=78, text='Park', fg_color='#2D2A2A')
Park.place(x=490, y=69)

Stop = customtkinter.CTkButton(
    root, width=239, height=78, text='Stop', fg_color='#2D2A2A', command=lambda: toggle_button_text(Stop))
Stop.place(x=490, y=203)


scrollable_frame = customtkinter.CTkScrollableFrame(
    root, width=418, height=120, fg_color='black', label_anchor='w')
scrollable_frame.place(x=29, y=70.51)

# Adding 10 items to the frame


def get_products():  # gets product and price , use for display

    with open("barcodes.txt", "r") as file:
        prod = file.readline()

    product_and_price = prod.split(',')
    product = product_and_price[0]
    price = product_and_price[1]
    print(product, price)

    open("barcodes.txt", "w").close()

    return product, price


def update_cart(scroll_frame):
    global TotalVal

    if os.stat("barcodes.txt").st_size != 0:

        product, price = get_products()
        price = int(price)

        print('a')

        check = ProductFrame(scroll_frame, product, price, 1)

        frames[check.get_product()] = check
        TotalVal = TotalVal + (check.get_price())*(check.get_quantity())
        print(check.get_quantity())
        SubtotalAmt.configure(text=TotalVal)
        check.pack(anchor='w')
        root.update()


class ProductFrame(tk.Frame):
    def __init__(self, parent, product_name, price, quantity,  *args, **kwargs):
        tk.Frame.__init__(self, parent, bg='black', *args, **kwargs)

        self.product_name = product_name
        self.fixed = price
        self.price = price
        self.quantity = quantity
        global ItemCnt
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


def barcode_run():
    brs.main()


def start_thread():  # run the scanner in the background
    update_thread = threading.Thread(target=barcode_run)
    update_thread.start()


def update_gui():
    while True:
        global TotalVal
        global ItemCnt
        update_cart(scrollable_frame)
        SubtotalAmt.configure(text=f'${(TotalVal)}')
        TaxAmt.configure(text=f'${(TotalVal * 0.1)}')
        TotalAmt.configure(text=f'${(TotalVal + (TotalVal * 0.1))}')
        if ItemCnt == 1:
            Items.configure(
                text=f'You have {ItemCnt} item in your cart')
        else:
            Items.configure(
                text=f'You have {ItemCnt} items in your cart')
        root.update()
        time.sleep(.25)


start_thread()
# brs.main()
update_gui()
root.mainloop()
