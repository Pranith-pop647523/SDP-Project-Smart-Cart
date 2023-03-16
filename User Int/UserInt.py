import threading
import tkinter as tk
import customtkinter
import barcode_scanner as brs
import time
import os
from client import CommandSocket
from PIL import Image
import ProductFr


class interface():
    def __init__(self):
        self.BG_COL = '#000000'
        self.TEXT_COL = '#FFFFFF'
        self.frames = {}  # reference to each product frame created
        self.totals = {}  # calc total
        self.TotalVal = 0
        self.ItemCnt = 0
        self.root = tk.Tk()
        self.root.title("Shopping Cart")
        self.root.option_add("*Font", "Poppins 12 ")
        # Configure first column
        self.root.geometry('800x480')
        self.root.config(bg=self.BG_COL)
        self.remove_image = tk.PhotoImage(file="bin_white.png")
        # Top line
        self.canvas = tk.Canvas(self.root, bg=self.BG_COL, height=480,
                                width=800, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        self.canvas.create_line(29.38, 27.6, 400+29.38,
                                27.6, fill=self.TEXT_COL, width=1)
        # Shopping cart title
        self.label_1 = tk.Label(self.root, text="Shopping Cart", bg=self.BG_COL,
                                fg=self.TEXT_COL, font=("Poppins", 12), anchor='w')
        self.label_1.place(x=39.75, y=35.42, width=129.84, height=18)
        # Item count
        self.Items = tk.Label(self.root, text=f"You have {self.ItemCnt} Items in your cart ", bg=self.BG_COL,
                              fg=self.TEXT_COL, font=("Nonita", 9), anchor='w')
        self.Items.place(x=39.75, y=52.51, width=146.92, height=13)
        # First frame
        self.ProductFrame = tk.Frame(
            self.root, bg=self.BG_COL, borderwidth=1, relief="groove")
        self.ProductFrame.place(x=29, y=70.51, width=418, height=120)
        # self.Checkout frame
        self.canvas.create_line(489.97, 325.55, 489.97+239.18,
                                325.55, fill=self.TEXT_COL, width=1)

        self.Subtotal = tk.Label(self.root, text="Subtotal", bg=self.BG_COL,
                                 fg=self.TEXT_COL, font=("Poppins", 9), anchor='w')
        self.Subtotal.place(x=489.98, y=335.49, width=94.3, height=14)

        self.Tax = tk.Label(self.root, text="Tax", bg=self.BG_COL,
                            fg=self.TEXT_COL, font=("Poppins", 9), anchor='w')
        self.Tax.place(x=489.98, y=353.94, width=94.3, height=14)

        self.Total = tk.Label(self.root, text="Total", bg=self.BG_COL,
                              fg=self.TEXT_COL, font=("Poppins", 9), anchor='w')
        self.Total.place(x=489.98, y=372.39, width=94.3, height=14)

        self.SubtotalAmt = tk.Label(self.root, text=f"${0}", bg=self.BG_COL,
                                    fg=self.TEXT_COL, font=("Poppins", 9), anchor='e')
        self.SubtotalAmt.place(x=634.85, y=336.49, width=94.3, height=14)

        self.TaxAmt = tk.Label(self.root, text=f"${0}", bg=self.BG_COL,
                               fg=self.TEXT_COL, font=("Poppins", 9), anchor='e')
        self.TaxAmt.place(x=634.85, y=354.93, width=94.3, height=14)

        self.TotalAmt = tk.Label(self.root, text=f"${0}", bg=self.BG_COL,
                                 fg=self.TEXT_COL, font=("Poppins", 9), anchor='e')
        self.TotalAmt.place(x=634.85, y=372.39, width=94.3, height=14)

        self.CheckoutFrame = tk.Frame(
            self.root, bg=self.BG_COL, borderwidth=0, relief="groove")
        self.CheckoutFrame.place(x=489.98, y=404.51, width=239.18, height=41)

        self.TotalCost = tk.Label(self.CheckoutFrame, text="Total", bg=self.BG_COL,
                                  fg=self.TEXT_COL, font=("Poppins", 9), anchor='w')

        self.Checkout = customtkinter.CTkButton(
            self.CheckoutFrame, width=250, fg_color='#2D2A2A', text='Checkout', anchor='w', font=('Poppins', 10))

        self.Checkout.pack(anchor='ne')

        self.Park = customtkinter.CTkButton(
            self.root, width=239, height=78, text='Park', fg_color='#2D2A2A')
        self.Park.place(x=490, y=69)

        self.Stop = customtkinter.CTkButton(
            self.root, width=239, height=78, text='Stop', fg_color='#2D2A2A', command=lambda: self.toggle_button_text(self.Stop))
        self.Stop.place(x=490, y=203)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.root, width=418, height=120, fg_color='black', label_anchor='w')
        self.scrollable_frame.place(x=29, y=70.51)

        # socket parameters:
        # depends on server used , probs makes more sense to use it as an instance variable
        self.SERVER_IP = '129.215.2.45'
        self.SERVER_PORT = 50001

        self.STOP = '1'
        self.FOLLOW = '2'
        self.PARK = '3'

        print('done')

        self.cmdSocket = CommandSocket(self.SERVER_IP, self.SERVER_PORT)

    # Adding 10 self.Items to the frame

    def toggle_button_text(self, button):
        if button.cget("text") == 'Stop':
            button.configure(text="Follow")
            self.cmdSocket.sendCommand(self.STOP)

        else:
            button.configure(text="Stop")
            self.cmdSocket.sendCommand(self.FOLLOW)
        self.update_gui()

    def get_products(self):  # gets product and price , use for display

        with open("barcodes.txt", "r") as file:
            prod = file.readline()

        product_and_price = prod.split(',')
        product = product_and_price[0]
        price = product_and_price[1]
        print(product, price)

        open("barcodes.txt", "w").close()

        return product, price

    def update_cart(self, scroll_frame):
        global TotalVal

        if os.stat("barcodes.txt").st_size != 0:

            product, price = self.get_products()
            price = int(price)

            print('a')

            check = ProductFr.ProductFrame(
                scroll_frame, product, price, 1, self.remove_image)

            self.frames[check.get_product()] = check
            TotalVal = TotalVal + (check.get_price())*(check.get_quantity())
            print(check.get_quantity())
            self.SubtotalAmt.configure(text=TotalVal)
            check.pack(anchor='w')
            self.root.update()

    def barcode_run(self):
        brs.main()

    def start_thread(self):  # run the scanner in the background
        update_thread = threading.Thread(target=self.barcode_run)
        update_thread.start()

    def update_gui(self):
        while True:

            global ItemCnt
            self.update_cart(self.scrollable_frame)
            self.SubtotalAmt.configure(text=f'${(self.TotalVal)}')
            self.TaxAmt.configure(text=f'${(self.TotalVal * 0.1)}')
            self.TotalAmt.configure(
                text=f'${(self.TotalVal + (self.TotalVal * 0.1))}')
            if self.ItemCnt == 1:
                self.Items.configure(
                    text=f'You have {self.ItemCnt} item in your cart')
            else:
                self.Items.configure(
                    text=f'You have {self.ItemCnt} self.Items in your cart')
            self.root.update()
            time.sleep(.25)

    def main(self):
        self.start_thread()
        self.update_gui()
        self.root.mainloop()

        # close server socket
        self.cmdSocket.close()


test1 = interface()
test1.main()
