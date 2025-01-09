
def heuristika(igrac, protivnik):
    global simX, simO, ukupno_trouglica, povezani_stubovi, zauzeta_komb

    # Razlika u trenutnom broju trouglova
    trenutna_prednost = simX - simO if igrac == "X" else simO - simX

    # Potencijal za igrača i protivnika
    potencijal_igrac = broj_potencijalnih_trouglova(igrac)
    potencijal_protivnik = broj_potencijalnih_trouglova(protivnik)

    # Heuristika: trenutna prednost + potencijalna prednost
    return trenutna_prednost + (potencijal_igrac - potencijal_protivnik)


def broj_potencijalnih_trouglova(igrac):
    global stb

    potencijal = 0

    # Prolazimo kroz sve nepovezane kombinacije stubova
    for prvi in stb:
        for drugi in stb:
            if drugi == prvi or main.proveri_povezanost(prvi, drugi):
                continue
            for treci in stb:
                if treci == prvi or treci == drugi or main.proveri_povezanost(prvi, treci) or main.proveri_povezanost(drugi, treci):
                    continue

                # Proveravamo da li bi formirali trougao
                if main.validna_kombinacija(prvi, drugi, treci):
                    potencijal += 1

    return potencijal


def minimax(stubovi, dubina, maksimizuj, igrac, protivnik, alfa, beta):
    # Baza rekurzije: dostignuta dubina ili kraj igre
    if dubina == 0 or main.kraj():
        return heuristika(igrac, protivnik)

    if maksimizuj:
        max_eval = float('-inf')
        for prvi in stubovi:
            for drugi in stubovi:
                if drugi == prvi or main.proveri_povezanost(prvi, drugi):
                    continue
                for treci in stubovi:
                    if treci == prvi or treci == drugi or main.proveri_povezanost(prvi, treci) or main.proveri_povezanost(drugi, treci):
                        continue

                    if main.validna_kombinacija(prvi, drugi, treci):
                        # Simuliraj potez
                        zauzeta_komb.append((prvi, drugi, treci))
                        vrednost = minimax(stubovi, dubina - 1, False, igrac, protivnik, alfa, beta)
                        zauzeta_komb.pop()

                        max_eval = max(max_eval, vrednost)
                        alfa = max(alfa, vrednost)

                        if beta <= alfa:
                            break
        return max_eval
    else:
        min_eval = float('inf')
        for prvi in stubovi:
            for drugi in stubovi:
                if drugi == prvi or main.proveri_povezanost(prvi, drugi):
                    continue
                for treci in stubovi:
                    if treci == prvi or treci == drugi or main.proveri_povezanost(prvi, treci) or main.proveri_povezanost(drugi, treci):
                        continue

                    if main.validna_kombinacija(prvi, drugi, treci):
                        # Simuliraj potez
                        zauzeta_komb.append((prvi, drugi, treci))
                        vrednost = minimax(stubovi, dubina - 1, True, igrac, protivnik, alfa, beta)
                        zauzeta_komb.pop()

                        min_eval = min(min_eval, vrednost)
                        beta = min(beta, vrednost)

                        if beta <= alfa:
                            break
        return min_eval



def slobodni_stubovi(stubovi):
    return [stub for stub in stubovi if stub not in stb]




def simuliraj_potez(canvas, stub, igrac, stubovi):
    boja = "red" if igrac == "X" else "blue"
    main.postavi_gumicu(canvas, stubovi, stub[0], stub[1], "D", len(stubovi), boja)


def poništi_potez(canvas, stub, igrac, stubovi):
    global povezani_stubovi, zauzeta_komb, simX, simO
    # Očisti sve promene od poteza
    povezani_stubovi = povezani_stubovi[:-1]
    zauzeta_komb = zauzeta_komb[:-1]
    if igrac == "X":
        simX -= 1
    else:
        simO -= 1
    # Obnovi grafiku ako je potrebno


def odigraj_AI(canvas, stubovi, igrac, protivnik):
    najbolji_potez = None
    najbolja_vrednost = float('-inf') if igrac == "X" else float('inf')

    for stub in slobodni_stubovi(stubovi):
        simuliraj_potez(canvas, stub, igrac, stubovi)
        vrednost = minimax(stubovi, 3, float('-inf'), float('inf'), False, igrac, protivnik, canvas)
        poništi_potez(canvas, stub, igrac, stubovi)

        if (igrac == "X" and vrednost > najbolja_vrednost) or (igrac == "O" and vrednost < najbolja_vrednost):
            najbolja_vrednost = vrednost
            najbolji_potez = stub

    if najbolji_potez:
        simuliraj_potez(canvas, najbolji_potez, igrac, stubovi)


def potez_racunara(canvas, stubovi, igrac, protivnik, dubina):
    najbolji_potez = None
    najbolja_vrednost = float('-inf')  # Računar maksimizuje

    for prvi in stubovi:
        for drugi in stubovi:
            if drugi == prvi or main.proveri_povezanost(prvi, drugi):
                continue
            for treci in stubovi:
                if treci == prvi or treci == drugi or main.proveri_povezanost(prvi, treci) or main.proveri_povezanost(drugi, treci):
                    continue

                if main.validna_kombinacija(prvi, drugi, treci):
                    # Simuliramo potez
                    zauzeta_komb.append((prvi, drugi, treci))
                    vrednost = minimax(stubovi, dubina - 1, False, igrac, protivnik, float('-inf'), float('inf'))
                    zauzeta_komb.pop()  # Vraćamo stanje

                    if vrednost > najbolja_vrednost:
                        najbolja_vrednost = vrednost
                        najbolji_potez = (prvi, drugi, treci)

    # Odigraj najbolji potez
    if najbolji_potez:
        prvi, drugi, treci = najbolji_potez
        main.povezanost(prvi, drugi, treci)  # Dodajte povezanost
        main.stavi_simbol(canvas, prvi, drugi, treci, "red" if igrac == "X" else "blue")
