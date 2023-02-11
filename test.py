import threading
import tkinter as tk
import customtkinter
import barcode_scanner as brs
import time
import os


BG_COL = '#000000'
TEXT_COL = '#FFFFFF'

barcodeProduct = {
    '5012345678900': 'item1',
    '0076950450479': 'item2'

}
productPrice = {
    '5012345678900': 10,
    '0076950450479': 20

}

item_cnt = 10
TotalVal = 0
SubtotalVal = 0
TaxVal = 0


root = tk.Tk()
root.title("Shopping Cart")
root.option_add("*Font", "Poppins 12 ")

# Configure first column
root.geometry('800x480')
root.config(bg=BG_COL)

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


label_2 = tk.Label(root, text=f"You have {item_cnt} items in your cart ", bg=BG_COL,
                   fg=TEXT_COL, font=("Nonita", 9), anchor='w')
label_2.place(x=39.75, y=52.51, width=146.92, height=13)

# First frame

ProductFrame = tk.Frame(root, bg=BG_COL, borderwidth=1, relief="groove")
ProductFrame.place(x=29, y=70.51, width=418, height=120)

products = tk.Listbox(ProductFrame, selectmode="multiple")
products.pack(fill="both", expand=True)

for item in ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", '4', "Item 1", "Item 2", "Item 3", "Item 4", "Item 5", '4']:
    products.insert("end", item)

scroll = tk.Scrollbar(ProductFrame, command=products.yview)
scroll.pack(side="right", fill="y")


# Products list


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


TotalAmt = tk.Label(root, text=f"${TotalVal}", bg=BG_COL,
                    fg=TEXT_COL, font=("Poppins", 9), anchor='e')
TotalAmt.place(x=634.85, y=354.93, width=94.3, height=14)

SubtotalAmt = tk.Label(root, text=f"${SubtotalVal}", bg=BG_COL,
                       fg=TEXT_COL, font=("Poppins", 9), anchor='e')
SubtotalAmt.place(x=634.85, y=336.49, width=94.3, height=14)

TaxAmt = tk.Label(root, text=f"${TaxVal}", bg=BG_COL,
                  fg=TEXT_COL, font=("Poppins", 9), anchor='e')
TaxAmt.place(x=634.85, y=372.39, width=94.3, height=14)


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


def increment_value(label_name):
    value = int(label_name.cget("text"))
    value += 1
    label_name.config(text=str(value))


def decrement_value(label_name):
    value = int(label_name.cget("text"))
    value -= 1
    label_name.config(text=str(value))


scrollable_frame = customtkinter.CTkScrollableFrame(
    root, width=418, height=120, fg_color='black', label_anchor='w')
scrollable_frame.place(x=29, y=70.51)

# Adding 10 items to the frame


def get_barcode_scan(barcodeno):
    # Code to get the barcode product name
    return (barcodeProduct[barcodeno], productPrice[barcodeno])


def update_file():  # already done in barcode scanner
    while True:
        product, price = get_barcode_scan()
        with open("barcodes.txt", "w") as file:
            file.write(f'{product},{price}' + "\n")


def get_products():  # gets product and price , use for display

    with open("barcodes.txt", "r") as file:
        prod = file.readline()

    product_and_price = prod.split(',')

    product = product_and_price[0]
    price = product_and_price[0]
    print(product, price)

    open("barcodes.txt", "w").close()

    return product, price


def update_cart(scroll_frame):

    if os.stat("barcodes.txt").st_size != 0:

        product, price = get_products()

        print('a')
        tk.Label(scroll_frame, text=product, bg='black').pack(anchor='w')
        root.update()


def barcode_run():
    brs.main()


def start_thread():
    update_thread = threading.Thread(target=barcode_run)
    update_thread.start()


def update_gui():
    while True:

        update_cart(scrollable_frame)
        root.update()
        time.sleep(1)


start_thread()
# brs.main()
update_gui()
root.mainloop()
