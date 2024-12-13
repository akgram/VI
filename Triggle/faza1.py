from itertools import product
import tkinter as tk
from tkinter import messagebox

def crtaj_stubove(canvas, x, y, r, n):
    stubovi = []  # koordinate i oznake
    red_visina = 30
    slovo = ord('A')

    # crtanje stubova i cuvanje koordinata
    for i in range(2 * n - 1):
        if i < n:
            broj_stubova = n + i
        else:
            broj_stubova = 2 * n - 2 - (i - n)
        
        y_pos = y + i * red_visina  # vertikalni razmak
        x_pos_start = x - (broj_stubova - 1) * r / 2

        # oznake levo
        canvas.create_text(x - (r * n), y_pos, text=chr(slovo + i), fill="red", anchor="e")

        for j in range(broj_stubova):
            x_pos = x_pos_start + j * r
            stubovi.append((chr(slovo + i), j + 1, x_pos, y_pos))  # koordinate stubova
            canvas.create_oval(x_pos - 3, y_pos - 3, x_pos + 3, y_pos + 3, fill="black", outline="black")

    # oznake iznad i ispod
    max_kolone = 2 * n - 1
    for j in range(max_kolone):
        x_pos = x - (max_kolone - 1) * r / 2 + j * r
        canvas.create_text(x_pos + (n-4) * 15 + 45, y - 10, text=str(j + 1), fill="red", anchor="s")  # iznad

        y_bottom = y + (2 * n - 2) * red_visina + 20
        canvas.create_text(x_pos + (n-4) * 15 + 45, y_bottom - 10, text=str(j + 1), fill="red", anchor="n")  # ispod

    return stubovi

def postavi_gumicu(canvas, stubovi, red, kolona, smer, n):
    selektovani_stubovi = []

    for stub in stubovi:
        if stub[0] == red and stub[1] == kolona:
            selektovani_stubovi.append(stub)
            break
    else:
        messagebox.showerror("Greška", "Nevalidna koordinata!")
        return

    kolona_u_last_row = kolona

    for i in range(1, 4):
        if smer == 'DD':
            novi_red = chr(ord(red) + i)
            if ord(novi_red) <= ord('A') + n - 1:
                if ord(novi_red) == ord('A') + n:
                    novi_kolona = kolona_u_last_row # kolona ista kao u poslednjem redu
                else:
                    novi_kolona = kolona + i  # kolona se povecava sa svakim redom
            else:
                novi_kolona = kolona_u_last_row  # kolona se ne povecava nakon reda n

        elif smer == 'DL':
            novi_red = chr(ord(red) + i)
            if ord(novi_red) <= ord('A') + n - 1:
                novi_kolona = kolona_u_last_row  # kolona ostaje ista kao u poketnom redu
            else:
                novi_kolona = kolona_u_last_row - 1  # kolona se smanjuje nakon reda n
        
        elif smer == 'D':
            novi_red = red # isti red
            novi_kolona = kolona + i  # kolona se povecava sa svakim sledećim stubom


        novi_stub = next((s for s in stubovi if s[0] == novi_red and s[1] == novi_kolona), None)
        if novi_stub:
            selektovani_stubovi.append(novi_stub)
            kolona_u_last_row = novi_kolona  # poslednja koriscena kolona
        else:
            messagebox.showerror("Greška", "Izabrani smer izlazi iz granica table!")
            return

    # povezivanje kosim linijama
    for i in range(len(selektovani_stubovi) - 1):
        stub1 = selektovani_stubovi[i]
        stub2 = selektovani_stubovi[i + 1]

        x1, y1 = stub1[2], stub1[3]
        x2, y2 = stub2[2], stub2[3]

        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    for stub in selektovani_stubovi:
        x_pos, y_pos = stub[2], stub[3]
        canvas.create_oval(x_pos - 5, y_pos - 5, x_pos + 5, y_pos + 5, fill="blue", outline="blue")



def start_game():
    first = first_entry.get().lower() # uzima vrednosti iz polja
    simbol = simbol_entry.get().upper()
    n = dimension_entry.get()
    
    if first not in ['covek', 'racunar']:
        messagebox.showerror("Greška", "Ko igra prvi? (covek/racunar)")
        return
    if simbol not in ['X', 'O']:
        messagebox.showerror("Greška", "Simbol prvog igrača mora biti X ili O")
        return
    if not n.isdigit() or int(n) not in range(4, 9):
        messagebox.showerror("Greška", "Dimenzija table mora biti broj između 4 i 8")
        return
    
    first, simbol, n = first, simbol, int(n)

    root.destroy() # zatvaramo prvi prozor

    igra_prozor = tk.Tk()
    igra_prozor.title("Triggle Game")
    igra_prozor.config(bg="lightgray")

    prozor_width = 300 + (n-4) * 50 + 250
    prozor_height = 300 + (n-4) * 50 + 250
    igra_prozor.geometry(f"{prozor_width}x{prozor_height}")
    igra_prozor.minsize(prozor_width, prozor_height)

    canvas_width = 350 + (n-4) * 50
    canvas_height = 250 + (n-4) * 50
    canvas = tk.Canvas(igra_prozor, width=canvas_width, height=canvas_height, bg="lightgray") # za crtanje table
    canvas.pack(padx=10, pady=10, expand=True)

    stubovi = crtaj_stubove(canvas, canvas_width // 2, canvas_height * 0.1, 30, n)

    def unesi_potez():
        try:
            red = red_entry.get().upper()
            kolona = int(kolona_entry.get())
            smer = smer_var.get()

            if not ('A' <= red <= chr(ord('A') + 2 * n - 2)):
                raise ValueError("Nevalidan red!")
            if not (1 <= kolona <= 2 * n - 1):
                raise ValueError("Nevalidna kolona!")
            if smer not in ['D', 'DD', 'DL']:
                raise ValueError("Nevalidan smer!")
            
            postavi_gumicu(canvas, stubovi, red, kolona, smer, n)

            # reset polja
            red_entry.delete(0, tk.END)
            kolona_entry.delete(0, tk.END)
            smer_var.set("D")

        except ValueError as e:
            messagebox.showerror("Greška!", str(e))

    unos_frame = tk.Frame(igra_prozor, bg = "lightgray")
    unos_frame.pack(side="bottom", pady=10)

    red_label = tk.Label(unos_frame, font=("Arial", 11, "bold"), text=f"Red (A-{chr(ord('A') + 2 * n - 2)}):", bg = "lightgray")
    red_label.grid(row=0, column=0, pady=5)
    red_entry = tk.Entry(unos_frame, font=("Arial", 12), bd=2, relief="solid", borderwidth=2, justify="center", width=10)
    red_entry.grid(row=0, column=1, pady=5)

    kolona_label = tk.Label(unos_frame, font=("Arial", 11, "bold"), text=f"Kolona (1-{n}/{2 * n - 1}):", bg = "lightgray")
    kolona_label.grid(row=1, column=0, pady=5)
    kolona_entry = tk.Entry(unos_frame, font=("Arial", 12), bd=2, relief="solid", borderwidth=2, justify="center", width=10)
    kolona_entry.grid(row=1, column=1, pady=5)

    smer_label = tk.Label(unos_frame, font=("Arial", 11, "bold"), text="Smer (D/DD/DL):", bg = "lightgray")
    smer_label.grid(row=2, column=0, pady=5)
    smer_var = tk.StringVar(value="D")
    smer_menu = tk.OptionMenu(unos_frame, smer_var, "D", "DD", "DL")
    smer_menu.grid(row=2, column=1, pady=5)

    unesi_potez_button = tk.Button(unos_frame, text="Odigraj potez", command=unesi_potez, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
    unesi_potez_button.grid(row=3, columnspan=2, pady=10)

    igra_prozor.mainloop()

root = tk.Tk()
root.title("Triggle Game")
root.geometry("300x300")
root.minsize(300, 300)

frame = tk.Frame(root, bg = "lightgray") # pravimo formu na frame
frame.pack(fill="both", expand=True)

welcome_label = tk.Label(frame, font=("Arial", 14, "bold", "underline"), text="Dobrodošli!", bg = "lightgray")
welcome_label.pack(pady=10)

first_label = tk.Label(frame, font=("Arial", 13, "bold"), text="Ko igra prvi? (covek/racunar):", bg = "lightgray")
first_label.pack(pady=2)
first_entry = tk.Entry(frame, font=("Arial", 13), bd=2, relief="solid", borderwidth=2, justify="center", width=15)
first_entry.pack(pady=2)

simbol_label = tk.Label(frame, font=("Arial", 13, "bold"), text="Simbol prvog igraca (X/O):", bg = "lightgray")
simbol_label.pack(pady=2)
simbol_entry = tk.Entry(frame, font=("Arial", 13), bd=2, relief="solid", borderwidth=2, justify="center", width=15)
simbol_entry.pack(pady=2)

dimension_label = tk.Label(frame, font=("Arial", 13, "bold"), text="Dimenzija table (4-8):", bg = "lightgray")
dimension_label.pack(pady=2)
dimension_entry = tk.Entry(frame, font=("Arial", 13), bd=2, relief="solid", borderwidth=2, justify="center", width=15)
dimension_entry.pack(pady=2)

start_button = tk.Button(frame, text="Start Game", command=start_game, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
start_button.pack(pady=10)

root.mainloop()