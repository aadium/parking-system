import tkinter as tk

with open("occupiedParkings.txt", "r") as f:
    lines = f.readlines()

w2_occupied_parkings = 0
w4_occupied_parkings = 0
t_occupied_parkings = 0

for line in lines:
    if (int(line) < 10000):
        w2_occupied_parkings += 1
    elif ((int(line) >= 10000) and (int(line) < 13000)):
        w4_occupied_parkings += 1
    elif (int(line) >= 13000):
        t_occupied_parkings += 1

Billboard = tk.Tk()

frm_v = tk.Frame(padx=30, pady=30)
lbl_main1 = tk.Label(master=Billboard, font=("Consolas", 45), text='Available', padx=10, pady=5)
lbl_main2 = tk.Label(master=Billboard, font=("Consolas", 45), text='Parkings', padx=10, pady=5)
lbl_w2 = tk.Label(master=frm_v, font=("Consolas", 20), text=('2-Wheelers:', 10000 - w2_occupied_parkings))
lbl_w4 = tk.Label(master=frm_v, font=("Consolas", 20), text=('4-Wheelers:', 3000 - w4_occupied_parkings))
lbl_t = tk.Label(master=frm_v, font=("Consolas", 20), text=('Trucks:', 500 - t_occupied_parkings))
lbl_main1.pack()
lbl_main2.pack()
frm_v.pack()
lbl_w2.pack()
lbl_w4.pack()
lbl_t.pack()
Billboard.mainloop()