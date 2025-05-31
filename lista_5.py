import tkinter as tk
from tkinter import ttk
from access_data import Data


def on_entry_click(event):
    if entry.get() == text:
        entry.delete(0, tk.END)
        entry.config(fg='black')
    else:
        entry.selection_range(0, tk.END)

def on_focusout(event):
    if entry.get() == "":
        entry.insert(0, text)
        entry.config(fg='grey')

def submit_action():
    try:
        amount = float(entry.get())
    except ValueError:
        amount = 0
    country_1 = first_option.get()
    country_2 = second_option.get()
    index_1 = countries.index(country_1)
    index_2 = countries.index(country_2)
    total = rate[index_1] / rate[index_2] * amount
    total = round(total, 2)
    response_text.set(f'You will receive: {total} {short[index_2]}')
    submit_button.focus_set()

def swap_action():
    country_1 = first_option.get()
    country_2 = second_option.get()
    first_option.set(country_2)
    second_option.set(country_1)

window = tk.Tk()
window.title('Currencies calculator')

# zmienne
dt = Data()
date = dt.date
rate = dt.conv_rate
countries = dt.countries
short = dt.short
first_option = tk.StringVar()
first_option.set(countries[0])
second_option = tk.StringVar()
second_option.set(countries[0])

text = "Enter amount..."
font = ('Helvetica', 20)
amount = 0
response_text = tk.StringVar()
response_text.set('You will receive: 0.00 PLN')

main_color = "#3399ff"
color_2 = "#ff9966"
color_3 = "#739900"
color_4 = "#006666"
color_5 = "#bbff99"

# tworzenie widgetow
frame = tk.Frame(master=window, width=600, height=750, bg=main_color)
frame.pack()

menu_1 = tk.OptionMenu(frame, first_option, *countries)
menu_1.config(width =20,bg=color_5, fg='black')

menu_2 = tk.OptionMenu(frame, second_option, *countries)
menu_2.config(width =20,bg=color_5, fg='black')

label2 = tk.Label(master = frame, text='Pick first currency',
                 bg=color_2, font = font)
label3 = tk.Label(master = frame, text='Pick second currency', 
                  bg=color_2, font = font)
results_label = tk.Label(master = frame, textvariable = response_text,
                        bg=color_4, fg = 'black', font = font, width = 30)
submit_button = tk.Button(master = frame, text='Submit', 
                          background=color_3, font = font, command = submit_action)
swap_button = tk.Button(master = frame, text='Reverse', background=color_3, 
                        font = font, command = swap_action)
entry = tk.Entry(master = frame, fg='grey', font=("Arial", 20), justify="left")

# pozycjonowanie widgetow

swap_button.place(x = 250, y = 250)
submit_button.place(x = 250, y = 400)
label2.place(x=100,y=100)
label3.place(x=100,y=150)
results_label.place(x = 80, y = 500)
entry.insert(0, text)
entry.place(x=150, y=340)
menu_1.place(x = 400, y = 100)
menu_2.place(x = 400, y = 150)

# eventy

entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_focusout)

window.mainloop()