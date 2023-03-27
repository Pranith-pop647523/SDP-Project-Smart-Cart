import threading
import tkinter as tk
import customtkinter
# import barcode_scanner as brs
import time
import os
from client import CommandSocket
from PIL import Image
import ProductFr
import productDB as pdb

# import bcScan


class interface():

    def __init__(self):
        self.pfmap = {}
        self.scanned = set()
        # Create a variable to store the scanned barcode
        self.barcode = ""
        self.BG_COL = '#000000'
        self.TEXT_COL = '#FFFFFF'

        self.TotalVal = 0
        self.ItemCnt = 0
        self.itemarr = []
        self.product_frames = {}  # list to hold all ProductFrame objects
        self.total_price = 0.0
        self.total_quantity = 0

        self.root = tk.Tk()
        self.root.title("Shopping Cart")
        self.root.option_add("*Font", "Nunito 20 ")

        # Configure first column
        self.root.geometry('800x480')
        self.root.config(bg=self.BG_COL)
        self.remove_image = tk.PhotoImage(file="bin.png")
        # Top line
        self.canvas = tk.Canvas(self.root, bg=self.BG_COL, height=480,
                                width=800, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # Shopping cart title
        self.label_1 = tk.Label(self.root, text="Basket", bg=self.BG_COL,
                                fg=self.TEXT_COL, font=("Montesserat", 24), anchor='w')
        self.label_1.place(x=40, y=24, width=245, height=24)

        self.canvas.create_line(40, 62, 40+243,
                                62, fill=self.TEXT_COL, width=1)

        self.Items = tk.Label(self.root, text=f"You have {self.ItemCnt} Items in your cart ", bg=self.BG_COL,
                              fg=self.TEXT_COL, font=("Montesserat", 16, 'bold'), anchor='w')
        self.Items.place(x=40, y=64, width=243, height=20)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.root, width=475, height=325, fg_color='black', label_anchor='w')
        self.scrollable_frame.place(x=40, y=101)

        self.cmds = tk.Canvas(self.root, bg=self.BG_COL, height=382,
                              width=200, highlightthickness=0)
        self.cmds.place(x=555, y=39)

        self.cmds.create_line(0, 262, 189,
                              262, fill=self.TEXT_COL, width=1)

        self.Park = customtkinter.CTkButton(
            self.cmds, width=189, height=78, text='Park', fg_color='#6A51FF')
        self.Park.place(x=0, y=0)

        self.Stop = customtkinter.CTkButton(
            self.cmds, width=189, height=78, text='Stop', fg_color='#6A51FF',  command=lambda: self.toggle_button_text(self.Stop))
        self.Stop.place(x=0, y=128)

        self.CheckoutFrame = tk.Frame(
            self.cmds, bg=self.BG_COL, borderwidth=0, relief="groove")

        self.Checkout = customtkinter.CTkButton(
            self.cmds, width=195, height=78,  border_color='white',  border_width=1, fg_color='black', text=f'£{self.TotalVal} Checkout', font=('Nunita', 24))
        self.Checkout.place(x=0, y=303)

        # socket parameters:
        # depends on server used , probs makes more sense to use it as an instance variable
        self.SERVER_IP = '129.215.2.45'
        self.SERVER_PORT = 50001

        self.STOP = '1'
        self.FOLLOW = '2'
        self.PARK = '3'

        print('done')
        self.root.bind('<Key>', self.on_key)
        # self.cmdSocket = CommandSocket(self.SERVER_IP, self.SERVER_PORT)

    def on_key(self, event):
        # Get the character that was pressed
        char = event.char

        # Check if the character is a digit or a letter
        if char.isalnum():
            # Add the character to the scanned barcode
            self.barcode += char
        elif event.keysym == 'Return':
            # Add the scanned barcode to the label
            self.update_carts(self.scrollable_frame, self.barcode)

            # Clear the scanned barcode variable
            self.barcode = ""
            self.update_gui()

    def add_product_frame(self, product_frame):
        self.product_frames[product_frame] = (
            product_frame.quantity, product_frame.product_price)
        self.update_totals()

    def remove_product_frame(self, product_frame):
        self.product_frames.pop(product_frame)
        self.update_totals()

    def update_totals(self):
        self.total_price = 0.0
        self.total_quantity = 0
        for product_frame in self.product_frames:

            self.total_price += self.product_frames[product_frame][1]
            self.total_quantity += self.product_frames[product_frame][0]
        # self.update_gui()

    def toggle_button_text(self, button):
        if button.cget("text") == 'Stop':
            button.configure(text="Follow")
            self.cmdSocket.sendCommand(self.STOP)

        else:
            button.configure(text="Stop")
            self.cmdSocket.sendCommand(self.FOLLOW)
        self.update_gui()

    # probs have to initialise item cnt and total cnt as an array to pass by ref

    def update_carts(self, scroll_frame, name):
        # global TotalVal
        if name not in pdb.product_name_list:
            return

        if pdb.product_name_list[name] in self.scanned:
            print('aaaaaaaaaascasbcsacusac')
            pf = self.pfmap[pdb.product_name_list[name]]
            pf.increase_quantity()
            self.update_callback(pf)
            # self.update_gui()

            print('help')
            return

        if len(name) >= 1:

            # name, price = self.get_products()
            check = ProductFr.ProductFrame(
                scroll_frame, pdb.product_name_list[name], pdb.product_price_list[name], self.remove_image, self.remove_callback, self.update_callback)
            self.add_product_frame(check)
            check.pack(anchor='nw', side='bottom', pady=(0, 76))
            self.pfmap[pdb.product_name_list[name]] = check
            self.scanned.add(pdb.product_name_list[name])
            print(self.scanned)
        self.root.update()

    def update_gui(self):
        while True:
            if self.total_quantity == 1:
                self.Items.configure(
                    text=f'You have {self.total_quantity} item in your cart')
                self.Checkout.configure(text=f'£{self.total_price} Checkout')
            else:
                self.Items.configure(
                    text=f'You have {self.total_quantity} Items in your cart')
                self.Checkout.configure(text=f'£{self.total_price} Checkout')

            self.root.update()
            # time.sleep(.05)

    def remove_product(self, product_frame):
        self.pfmap.pop(product_frame.product_name)
        self.scanned.remove(product_frame.product_name)
        self.product_frames.pop(product_frame)

        print(self.scanned)
        self.update_totals()

    def update_quantity(self, product_frame):
        self.product_frames.pop(product_frame)
        self.product_frames[product_frame] = (
            product_frame.quantity, product_frame.quantity * product_frame.product_price)
        self.update_totals()

    def remove_callback(self, product_frame):
        self.remove_product(product_frame)

    def update_callback(self, product_frame):
        print('aaaa')
        self.update_quantity(product_frame)

    def main(self):

        prod = input()
        print('hehe')
        print(pdb.product_name_list[prod])
        self.update_carts(
            self.scrollable_frame, pdb.product_name_list[prod])
        self.update_gui()
        self.root.mainloop()

        # close server socket
        # self.cmdSocket.close()


test1 = interface()
test1.main()
