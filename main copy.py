import tkinter as tk
from tkinter import messagebox
import math
from itertools import combinations
import MinMax
import random

stb = []
povezani_stubovi = []
zauzeta_komb = []
istorija_poteza = []
simX = 0
simO = 0
ukupno_trouglica = 0
trenutni_igrac = ["igrac", "simbol"]

def heuristika(igrac, protivnik):
    global simX, simO, ukupno_trouglica, povezani_stubovi, zauzeta_komb

    # Razlika u trenutnom broju trouglova
    trenutna_prednost = simX - simO if igrac == "X" else simO - simX

    # Potencijal za igrača i protivnika
    potencijal_igrac = broj_potencijalnih_trouglova(igrac)
    potencijal_protivnik = broj_potencijalnih_trouglova(protivnik)

    # Heuristika: trenutna prednost + potencijalna prednost
    return trenutna_prednost + potencijal_igrac - potencijal_protivnik


def broj_potencijalnih_trouglova(igrac):
    global stb

    potencijal = 0

    # Prolazimo kroz sve nepovezane kombinacije stubova
    for prvi in stb:
        for drugi in stb:
            if drugi == prvi:
                continue
            for treci in stb:
                if treci == prvi or treci == drugi:
                    continue

                # Proveravamo da li bi formirali trougao
                if (proveri_povezanost(prvi, drugi) and proveri_povezanost(prvi, treci) and proveri_povezanost(drugi, treci) 
                    and validna_kombinacija(prvi, drugi, treci)):
                    potencijal += 1
                    print(f"dobar potencijal: {potencijal}")

    return potencijal

def generisi_validne_poteze(stubovi, n):
    global povezani_stubovi, zauzeta_komb
    potezi = []
    smerovi = ['D', 'DD', 'DL']

    for stub in stubovi:
        red, kolona = stub[0], stub[1]
        for smer in smerovi:
            selektovani_stubovi = []
            validan = True

            # Simuliramo potez da proverimo validnost
            kolona_u_last_row = kolona
            for i in range(1, 4):
                if smer == 'DD':
                    novi_red = chr(ord(red) + i)
                    novi_kolona = kolona + i if ord(novi_red) <= ord('A') + n - 1 else kolona_u_last_row
                elif smer == 'DL':
                    novi_red = chr(ord(red) + i)
                    novi_kolona = kolona_u_last_row if ord(novi_red) <= ord('A') + n - 1 else kolona_u_last_row - 1
                elif smer == 'D':
                    novi_red = red
                    novi_kolona = kolona + i
                else:
                    validan = False
                    break

                # Proveravamo da li su koordinate validne i nisu zauzete
                novi_stub = next((s for s in stubovi if s[0] == novi_red and s[1] == novi_kolona), None)
                if not novi_stub or (novi_stub, stub) in povezani_stubovi or (stub, novi_stub) in povezani_stubovi:
                    validan = False
                    break
                selektovani_stubovi.append(novi_stub)

            if validan:
                potezi.append((red, kolona, smer))

    return potezi


def ukloni_gumicu(canvas, stubovi, red, kolona, smer, n):
    global povezani_stubovi

    selektovani_stubovi = []

    # Pronalaženje prvog stuba
    for stub in stubovi:
        if stub[0] == red and stub[1] == kolona:
            selektovani_stubovi.append(stub)
            break
    else:
        messagebox.showerror("Greška", "Nevalidna koordinata za uklanjanje gumice!")
        return False

    kolona_u_last_row = kolona

    # Pronalaženje ostalih stubova u smeru
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
            kolona_u_last_row = novi_kolona
        else:
            messagebox.showerror("Greška", "Izabrani smer izlazi iz granica table za uklanjanje gumice!")
            return False

    # Uklanjanje linija između stubova
    for i in range(len(selektovani_stubovi) - 1):
        stub1 = selektovani_stubovi[i]
        stub2 = selektovani_stubovi[i + 1]

        x1, y1 = stub1[2], stub1[3]
        x2, y2 = stub2[2], stub2[3]

        # Pronađi i ukloni liniju sa kanvasa
        for item in canvas.find_all():
            coords = canvas.coords(item)
            if len(coords) == 4 and coords == [x1, y1, x2, y2]:
                canvas.delete(item)
                break

        # Uklanjanje veze iz liste povezanih stubova
        if (stub1, stub2) in povezani_stubovi:
            povezani_stubovi.remove((stub1, stub2))
        elif (stub2, stub1) in povezani_stubovi:
            povezani_stubovi.remove((stub2, stub1))

    # Uklanjanje krugova sa stubova
    for stub in selektovani_stubovi:
        x_pos, y_pos = stub[2], stub[3]

        for item in canvas.find_all():
            coords = canvas.coords(item)
            if len(coords) == 4 and coords == [x_pos - 5, y_pos - 5, x_pos + 5, y_pos + 5]:
                canvas.delete(item)
                break

    return True


def minimax(canvas, stubovi, dubina, maksimizuj, igrac, protivnik, alfa, beta, n):
    if dubina == 0 or kraj():
        return heuristika(igrac, protivnik), None

    najbolji_potez = None

    if maksimizuj:
        max_eval = float('-inf')
        for red, kolona, smer in generisi_validne_poteze(stubovi, n): # los potez generise
            # Simuliraj potez
            if postavi_gumicu(canvas, stubovi, red, kolona, smer, n, igrac): # ne ulazi jer vraca None
                vrednost, _ = minimax(canvas, stubovi, dubina - 1, False, igrac, protivnik, alfa, beta, n)
                # Vrati stanje table
                ukloni_gumicu(canvas, stubovi, red, kolona, smer, n)  # Potrebna funkcija za vraćanje

                if vrednost > max_eval:
                    max_eval = vrednost
                    najbolji_potez = (red, kolona, smer)
                alfa = max(alfa, vrednost)

                if beta <= alfa:
                    break
        return max_eval, najbolji_potez
    else:
        min_eval = float('inf')
        for red, kolona, smer in generisi_validne_poteze(stubovi, n): # los potez generise
            # Simuliraj potez
            if postavi_gumicu(canvas, stubovi, red, kolona, smer, n, protivnik): # ne ulazi jer vraca None
                vrednost, _ = minimax(canvas, stubovi, dubina - 1, True, igrac, protivnik, alfa, beta, n)
                # Vrati stanje table
                ukloni_gumicu(canvas, stubovi, red, kolona, smer, n)  # Potrebna funkcija za vraćanje

                if vrednost < min_eval:
                    min_eval = vrednost
                    najbolji_potez = (red, kolona, smer)
                beta = min(beta, vrednost)

                if beta <= alfa:
                    break
        return min_eval, najbolji_potez

def generisi_random_potez(n):
    # Ponovljena generacija dok ne dobijemo jedinstven potez
    global istorija_poteza

    while True:
        # Generisanje reda
        pocetni_red = 'A'
        maksimalni_red = chr(ord(pocetni_red) + 2 * n - 2)
        red = chr(random.randint(ord(pocetni_red), ord(maksimalni_red)))
        
        # Generisanje kolone
        kolona = random.randint(1, 2 * n - 1)
        
        # Generisanje smera
        smerovi = ['D', 'DD', 'DL']
        smer = random.choice(smerovi)
        
        # Kreiranje poteza
        potez = (red, kolona, smer)
        
        # Provera da li potez već postoji u istoriji

        if potez not in istorija_poteza:
            print("Generisani potez:", potez)
            istorija_poteza.append(potez)
            return potez



# gore treca faza

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
    global trenutni_igrac
    selektovani_stubovi = []

    for stub in stubovi:
        if stub[0] == red and stub[1] == kolona:
            selektovani_stubovi.append(stub)
            stb.append(stub)
            break
    else:
        if trenutni_igrac[0] == "covek":
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
            if trenutni_igrac[0] == "covek": ###########################################################################################################################
                messagebox.showerror("Greška", "Izabrani smer izlazi iz granica table!")
            return False

    # povezivanje kosim linijama
    for i in range(len(selektovani_stubovi) - 1):
        stub1 = selektovani_stubovi[i]
        stub2 = selektovani_stubovi[i + 1]

        x1, y1 = stub1[2], stub1[3]
        x2, y2 = stub2[2], stub2[3]

        canvas.create_line(x1, y1, x2, y2, fill=boja, width=2)

        # dodavanje povezivanja u listu povezanih stubova
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

    if(trenutni_igrac[1] == "X"): #boja == "red" and 
        #simbol = trenutni_igrac[1]
        simX = simX + 1
        print(f"X: {simX}")
    else: 
        #simbol = "O"
        simO = simO + 1
        print(f"O: {simO}")
    canvas.create_text(cx, cy, text=trenutni_igrac[1], font=("Arial", 12, "bold"), fill=boja)

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
    global trenutni_igrac
    first = first_entry.get().lower()
    simbol = simbol_entry.get().upper()
    n = dimension_entry.get()
    trenutni_igrac[0] = first
    trenutni_igrac[1] = simbol

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
    
    turn_label = tk.Label(igra_prozor, text="", bg="lightgray", font=("Arial", 12, "bold"))
    turn_label.pack()


    def potez_racunara(canvas, stubovi, igrac, protivnik, dubina):
        if kraj():
            canvas.delete("all")  # brise sve elemente, moze i bez toga
            igra_prozor.destroy()

        global trenutni_igrac
        trenutni_igrac[0] = "racunar"
        potez_button.config(state="disabled") # racunar igra
        smer_menu.config(state="disabled")
        kolona_entry.config(state="disabled")
        red_entry.config(state="disabled")
        def odbrojavanje(sekunde):
            if sekunde > 0:
                canvas.delete("timer")
                turn_label.config(text=f"Računar igra: {sekunde}s", font=("Arial", 12, "bold"), fg="red")
                canvas.after(1000, odbrojavanje, sekunde - 1)
            else:
                canvas.delete("timer")
                turn_label.config(text="Računar je odigrao!", font=("Arial", 12, "bold"), fg="green")

                # potez
                '''red, kolona, smer = generisi_random_potez(dubina)
                while postavi_gumicu(canvas, stubovi, red, kolona, smer, dubina, igrac) == False:
                    red, kolona, smer = generisi_random_potez(dubina)'''

                
                vrednost, najbolji_potez = minimax(canvas, stubovi, dubina, True, igrac, protivnik, float('-inf'), float('inf'), n)
                if najbolji_potez:
                    red, kolona, smer = najbolji_potez
                    if not postavi_gumicu(canvas, stubovi, red, kolona, smer, len(stubovi), igrac):
                        print("Greška: potez nije validan!")  # Provera ako se pojavi neočekivana greška
                
                turn_label.config(text="Računar je odigrao!", font=("Arial", 12, "bold"), fg="green")
                potez_button.config(state="normal")
                smer_menu.config(state="normal")
                kolona_entry.config(state="normal")
                red_entry.config(state="normal")
                trenutni_igrac[1] = "X" if trenutni_igrac[1] == "O" else "O"
        
        odbrojavanje(2)
        

    def unesi_potez(igrac): # ovde je def jer nam trebaju podaci iz polja
        if kraj():
            canvas.delete("all")  # brise sve elemente, moze i bez toga
            igra_prozor.destroy()

        global trenutni_igrac
        red = red_entry.get().upper()
        kolona = kolona_entry.get()
        smer = smer_var.get()
        trenutni_igrac[0] = "covek"

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
            # reset unosa
            red_entry.delete(0, tk.END)
            kolona_entry.delete(0, tk.END)
            smer_var.set("D")
            return

        boja = "blue" if igrac == "blue" else "red"
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

        potez_button.config(state="disabled") # blokira sve dok racunar igra ali mora dupli kod jer ima delay 1.2s
        smer_menu.config(state="disabled")
        kolona_entry.config(state="disabled")
        red_entry.config(state="disabled")
        trenutni_igrac[1] = "X" if trenutni_igrac[1] == "O" else "O"
        if igrac == "blue":
            unos_frame.after(1200, lambda: potez_racunara(canvas, stubovi, "red", "blue", n))
        elif igrac == "red":
            unos_frame.after(1200, lambda: potez_racunara(canvas, stubovi, "blue", "red", n))
        trenutni_igrac[0] = "covek"

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

    potez_button = tk.Button(unos_frame, text="Odigraj potez", command=lambda: unesi_potez("blue"), bg="#2196F3", fg="white", font=("Arial", 12, "bold"), state="normal" if first == "covek" else "disabled")
    potez_button.grid(row=3, column=0, columnspan=2, pady=10)

    if first == "racunar":
        potez_racunara(canvas, stubovi, "red", "blue", n)

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
