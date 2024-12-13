import tkinter as tk
from tkinter import messagebox
import math
from itertools import combinations

stb = []
povezani_stubovi = []
zauzeta_komb = []
istorija_poteza = []
simX = 0
simO = 0
ukupno_trouglica = 0

def crtaj_stubove(canvas, x, y, r, n):
    stubovi = []  # koordinate stubova
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

def proveri_trougao(canvas, stubovi, boja):
    # trazimo prvi stub
    for prvi in stubovi:
        vrsta1, kolona1 = prvi[0], prvi[1]

        # trazimo drugi stub
        for drugi in stubovi:
            if drugi == prvi:
                continue

            vrsta2, kolona2 = drugi[0], drugi[1]

            # dva stuba u istoj vrsti i razlikuju se za 1 kolonu
            if vrsta1 == vrsta2 and abs(kolona1 - kolona2) == 1:
                # trazimo treci stub
                for treci in stubovi:
                    vrsta3, kolona3 = treci[0], treci[1]

                    if treci != prvi and treci != drugi: # da li treci stub razlikuje za 1 vrstu i nalazi se u koloni sa jednim od dva stuba
                        if (abs(ord(vrsta1) - ord(vrsta3)) == 1 and (kolona3 == kolona1 or kolona3 == kolona2) and 
                            (proveri_povezanost(prvi, drugi) and proveri_povezanost(prvi, treci) and proveri_povezanost(drugi, treci)) and
                            validna_kombinacija(prvi, drugi, treci)):
                            print(f"Formiran trougao izmedju tacaka: ({vrsta1}, {kolona1}), ({vrsta2}, {kolona2}), ({vrsta3}, {kolona3})")
                            zauzeta_komb.append((prvi, drugi, treci))
                            stavi_simbol(canvas, prvi, drugi, treci, boja)
                            return True

            # dva stuba u istoj koloni i razlikuju se za 1 vrstu
            if kolona1 == kolona2 and abs(ord(vrsta1) - ord(vrsta2)) == 1:
                # trazimo treci stub
                for treci in stubovi:
                    vrsta3, kolona3 = treci[0], treci[1]

                    if treci != prvi and treci != drugi: # da li treci stub razlikuje za 1 kolonu i nalazi se u vrsti sa jednim od dva stuba
                        if (abs(kolona1 - kolona3) == 1 and (vrsta3 == vrsta1 or vrsta3 == vrsta2) and 
                            (proveri_povezanost(prvi, drugi) and proveri_povezanost(prvi, treci) and proveri_povezanost(drugi, treci)) and
                            validna_kombinacija(prvi, drugi, treci)):
                            print(f"Formiran trougao izmedju tacaka: ({vrsta1}, {kolona1}), ({vrsta2}, {kolona2}), ({vrsta3}, {kolona3})")
                            zauzeta_komb.append((prvi, drugi, treci))
                            stavi_simbol(canvas, prvi, drugi, treci, boja)
                            return True

    return False



def postavi_gumicu(canvas, stubovi, red, kolona, smer, n, boja):
    selektovani_stubovi = []

    for stub in stubovi:
        if stub[0] == red and stub[1] == kolona:
            selektovani_stubovi.append(stub)
            stb.append(stub)
            break
    else:
        messagebox.showerror("Greška", "Nevalidna koordinata!") # odvojeno jer ima bug sa kolonama, postoji kolona ali ne u toj vrsti
        return False

    kolona_u_last_row = kolona

    for i in range(1, 4):
        if smer == 'DD':
            novi_red = chr(ord(red) + i)
            if ord(novi_red) <= ord('A') + n - 1:
                if ord(novi_red) == ord('A') + n:
                    novi_kolona = kolona_u_last_row
                else:
                    novi_kolona = kolona + i
            else:
                novi_kolona = kolona_u_last_row

        elif smer == 'DL':
            novi_red = chr(ord(red) + i)
            if ord(novi_red) <= ord('A') + n - 1:
                novi_kolona = kolona_u_last_row
            else:
                novi_kolona = kolona_u_last_row - 1
        
        elif smer == 'D':
            novi_red = red
            novi_kolona = kolona + i

        novi_stub = next((s for s in stubovi if s[0] == novi_red and s[1] == novi_kolona), None)
        if novi_stub:
            selektovani_stubovi.append(novi_stub)
            stb.append(novi_stub)
            kolona_u_last_row = novi_kolona
        else:
            messagebox.showerror("Greška", "Izabrani smer izlazi iz granica table!")
            return False

    # povezivanje kosim linijama
    for i in range(len(selektovani_stubovi) - 1):
        stub1 = selektovani_stubovi[i]
        stub2 = selektovani_stubovi[i + 1]

        x1, y1 = stub1[2], stub1[3]
        x2, y2 = stub2[2], stub2[3]

        canvas.create_line(x1, y1, x2, y2, fill=boja, width=2)

        # Dodavanje povezanja u listu povezanih stubova
        if (stub1, stub2) not in povezani_stubovi and (stub2, stub1) not in povezani_stubovi:
            povezani_stubovi.append((stub1, stub2))

    for stub in selektovani_stubovi:
        x_pos, y_pos = stub[2], stub[3]
        canvas.create_oval(x_pos - 5, y_pos - 5, x_pos + 5, y_pos + 5, fill=boja, outline=boja)


    while proveri_trougao(canvas, stubovi, boja):
        proveri_trougao(canvas, stubovi, boja)

def proveri_povezanost(stub1, stub2):
    return (stub1, stub2) in povezani_stubovi or (stub2, stub1) in povezani_stubovi

def stavi_simbol(canvas, stub1, stub2, stub3, boja):
    x1, y1 = stub1[2], stub1[3]
    x2, y2 = stub2[2], stub2[3]
    x3, y3 = stub3[2], stub3[3]

    # centar trougla
    cx = (x1 + x2 + x3) / 3
    cy = (y1 + y2 + y3) / 3

    global simX
    global simO

    if(boja == "red"): 
        simbol = "X"
        simX = simX + 1
        print(f"X: {simX}")
    else: 
        simbol = "O"
        simO = simO + 1
        print(f"O: {simO}")
    canvas.create_text(cx, cy, text=simbol, font=("Arial", 12, "bold"), fill=boja)

def validna_kombinacija(stub1, stub2, stub3):
    if ((stub1, stub2, stub3) not in zauzeta_komb and (stub1, stub3, stub2) not in zauzeta_komb and 
       (stub2, stub1, stub3) not in zauzeta_komb and (stub2, stub3, stub1) not in zauzeta_komb and
       (stub3, stub1, stub2) not in zauzeta_komb and (stub3, stub2, stub1) not in zauzeta_komb):
        return True
    
def kraj():
    global simO, simX, ukupno_trouglica
    if simO > ukupno_trouglica / 2:
        messagebox.showinfo("Igra je gotova", "POBEDIO JE O!")
        return True
    elif simX > ukupno_trouglica / 2:
        messagebox.showinfo("Igra je gotova", "POBEDIO JE X!")
        return True
    elif simX == ukupno_trouglica / 2 and simO == ukupno_trouglica / 2:
        messagebox.showinfo("Igra je gotova", "NEMA POBEDNIKA, NEREŠENO!")
        return True
    else:
        print("Igra još traje!")
        return False

def start_game():
    first = first_entry.get().lower()
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

    n = int(n)
    global ukupno_trouglica
    start = n + n - 1
    for i in range(1, n - 1): # n-1 jer brojimo praznije pa ih ima -1 od dimenzije
        medjuZbir = start + i * 2
        ukupno_trouglica = ukupno_trouglica + medjuZbir

    ukupno_trouglica = (ukupno_trouglica + start) * 2
    print(ukupno_trouglica)

    root.destroy()

    igra_prozor = tk.Tk()
    igra_prozor.title("Triggle Game")
    igra_prozor.config(bg="lightgray")

    prozor_width = 300 + (n-4) * 50 + 250
    prozor_height = 300 + (n-4) * 50 + 250
    igra_prozor.geometry(f"{prozor_width}x{prozor_height}")
    igra_prozor.minsize(prozor_width, prozor_height)

    canvas_width = 350 + (n-4) * 50
    canvas_height = 250 + (n-4) * 50
    canvas = tk.Canvas(igra_prozor, width=canvas_width, height=canvas_height, bg="lightgray")
    canvas.pack(padx=10, pady=10, expand=True)

    stubovi = crtaj_stubove(canvas, canvas_width // 2, canvas_height * 0.1, 30, n)

    turn_label = tk.Label(igra_prozor, text="Na potezu: Plavi igrač", bg="lightgray", font=("Arial", 12, "bold"))
    turn_label.pack()

    def unesi_potez(igrac): # ovde je def jer nam trebaju podaci iz polja
        red = red_entry.get().upper()
        kolona = kolona_entry.get()
        smer = smer_var.get()

        if not ('A' <= red <= chr(ord('A') + 2 * n - 2)):
            messagebox.showerror("Greška!", "Nevalidan red!")
            return
        if not kolona.isdigit() or not (1 <= int(kolona) <= 2 * n - 1):
            messagebox.showerror("Greška!", "Nevalidna kolona!")
            return
        if smer not in ['D', 'DD', 'DL']:
            messagebox.showerror("Greška!", "Nevalidan smer!")
            return

        kolona = int(kolona)

        potez = (red, kolona, smer)
        if potez in istorija_poteza:
            messagebox.showerror("Greška!", "Ovaj potez je već odigran!")
            return

        boja = "blue" if igrac == "plavi" else "red"
        if postavi_gumicu(canvas, stubovi, red, kolona, smer, n, boja) == False:
            # reset unosa
            red_entry.delete(0, tk.END)
            kolona_entry.delete(0, tk.END)
            smer_var.set("D")
            return
        
        istorija_poteza.append(potez)

        # reset unosa
        red_entry.delete(0, tk.END)
        kolona_entry.delete(0, tk.END)
        smer_var.set("D")

        # promena poteza
        if igrac == "plavi":
            potez_button.config(state="disabled")
            potez_crveni_button.config(state="normal")
            turn_label.config(text="Na potezu: Crveni igrač")
        else:
            potez_button.config(state="normal")
            potez_crveni_button.config(state="disabled")
            turn_label.config(text="Na potezu: Plavi igrač")

        if kraj():
            canvas.delete("all")  # brise sve elemente, moze i bez toga
            igra_prozor.destroy()

    unos_frame = tk.Frame(igra_prozor, bg="lightgray")
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

    potez_button = tk.Button(unos_frame, text="Odigraj potez", command=lambda: unesi_potez("plavi"), bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
    potez_button.grid(row=3, column=0, pady=10)

    potez_crveni_button = tk.Button(unos_frame, text="Odigraj potez", command=lambda: unesi_potez("crveni"), bg="#FF0000", fg="white", font=("Arial", 12, "bold"), state="disabled")
    potez_crveni_button.grid(row=3, column=1, pady=10)

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
