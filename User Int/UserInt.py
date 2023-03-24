import threading
import tkinter as tk
import customtkinter
# import barcode_scanner as brs
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
        self.root.option_add("*Font", "Nunito 20 ")
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
        self.label_1 = tk.Label(self.root, text="Basket", bg=self.BG_COL,
                                fg=self.TEXT_COL, font=("Nunito", 20), anchor='w')
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

        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.root, width=418, height=120, fg_color='black', label_anchor='w')
        self.scrollable_frame.place(x=29, y=70.51)

        self.cmds = tk.Canvas(self.root, bg=self.BG_COL, height=382,
                              width=189, highlightthickness=0)
        self.cmds.place(x=555, y=39)

        self.cmds.create_line(0, 262, 189,
                              262, fill=self.TEXT_COL, width=1)

        self.Park = customtkinter.CTkButton(
            self.cmds, width=189, height=78, text='Park', fg_color='#473C89')
        self.Park.place(x=0, y=0)

        self.Stop = customtkinter.CTkButton(
            self.cmds, width=189, height=78, text='Stop', fg_color='#473C89', command=lambda: self.toggle_button_text(self.Stop))
        self.Stop.place(x=0, y=128)

        self.CheckoutFrame = tk.Frame(
            self.cmds, bg=self.BG_COL, borderwidth=0, relief="groove")

        self.Checkout = customtkinter.CTkButton(
            self.cmds, width=189, height=78,  border_color='white',  border_width=1, fg_color='black', text=f'$ {self.TotalVal} Checkout', anchor='w', font=('Nunita', 20))
        self.Checkout.place(x=0, y=303)
        # self.Checkout.pack(anchor='ne')

       # self.TotalCost = tk.Label(self.CheckoutFrame, text="Total", bg=self.BG_COL,
       #                           fg=self.TEXT_COL, font=("Poppins", 9), anchor='w')

        # socket parameters:
        # depends on server used , probs makes more sense to use it as an instance variable
        self.SERVER_IP = '129.215.2.45'
        self.SERVER_PORT = 50001

        self.STOP = '1'
        self.FOLLOW = '2'
        self.PARK = '3'

        print('done')

        # self.cmdSocket = CommandSocket(self.SERVER_IP, self.SERVER_PORT)

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

    # probs have to initialise item cnt and total cnt as an array to pass by ref
    def update_cart(self, scroll_frame):
        # global TotalVal

        if os.stat("barcodes.txt").st_size != 0:

            product, price = self.get_products()
            price = int(price)

            print('a')

            check = ProductFr.ProductFrame(
                scroll_frame, product, price, 1, self.remove_image, self.ItemCnt)

            self.frames[check.get_product()] = check
            self.TotalVal = self.TotalVal + \
                (check.get_price())*(check.get_quantity())
            print(check.get_quantity())
            check.pack(anchor='w')
            self.root.update()

    # def barcode_run(self):
     #   brs.main()

    # def start_thread(self):  # run the scanner in the background
     #   update_thread = threading.Thread(target=self.barcode_run)
      #  update_thread.start()

    def update_gui(self):
        while True:

            # global ItemCnt
            self.update_cart(self.scrollable_frame)

            if self.ItemCnt == 1:
                self.Items.configure(
                    text=f'You have {self.ItemCnt} item in your cart')
            else:
                self.Items.configure(
                    text=f'You have {self.ItemCnt} Items in your cart')
            self.root.update()
            time.sleep(.25)

    def main(self):
        # self.start_thread()
        self.update_gui()
        self.root.mainloop()

        # close server socket
        self.cmdSocket.close()


test1 = interface()
test1.main()
