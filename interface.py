import tkinter
import customtkinter
import barcode_scanner

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("System")
# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x480")


def button_function():
    barcode_scanner.main()
    # barcode_scanner

    # Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(
    master=app, text="Scanner", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

app.mainloop()
