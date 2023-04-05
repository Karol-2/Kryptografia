"""
Autor: Karol Krawczykiewicz
"""
import re
import sys

def przygotowanie():
    try:
        with open('orig.txt','r') as f:
            print("Otwarto plik orig.txt")
            tekst = f.read().replace('\n',' ').lower()
            tekst = re.sub(r"[^a-z\s]","",tekst) # ususwanie cyfr i znaków specjalnych

    except FileNotFoundError:
        print("Brak pliku orig.txt !!!")
        return

    linijki = []
    for i in range(0,len(tekst),dlugosc_linijek):
        linijka = tekst[i:i + dlugosc_linijek]
        if len(linijka) < dlugosc_linijek:
            linijka += 'x' * (dlugosc_linijek - len(linijka))  # dopisujemy ciągi 'x' w przypadku linii krótszych niż 64
        linijki.append(linijka)

    with open('plain.txt','w') as f:
        print("Zapisano tekst to plain.txt")
        f.write('\n'.join(linijki))


def szyfrowanie():
    try:
        with open("plain.txt","r") as f:
            print("Otwarto plik plain.txt")
            tekst = f.read().splitlines()
    except FileNotFoundError:
        print("Brak pliku plain.txt !!!")
        return

    try:
        with open("key.txt","r") as f:
            print("Otwarto plik key.txt")
            klucz = f.read()
            klucz = ''.join(format(ord(i),'08b') for i in klucz)
    except FileNotFoundError:
        print("Brak pliku key.txt !!!")
        return

    zaszyfrowane = []

    for i in range(len(tekst)):
        nowa_linijka = ""
        linijka = ' '.join(format(ord(i),'08b') for i in tekst[i])
        linijka = linijka.split(" ")

        for j in range(len(linijka)):
            while len(linijka[j]) != 8:
                linijka[j] = "0" + linijka[j]

        linijka = ''.join(format(x) for x in linijka)

        if linijka != "00000000":
            for j in range(len(linijka)):
                xor = int(linijka[j]) ^ int(klucz[j])
                nowa_linijka = nowa_linijka + str(xor)
        zaszyfrowane.append(nowa_linijka)

    with open("crypto.txt","w") as f:
        print("Zapisano szyfr do crypto.txt")
        for rzad in zaszyfrowane:
            f.write(rzad + '\n')


def krypto_analiza():
    try:
        with open("crypto.txt","r") as f:
            print("Otwarto plik crypto.txt")
            tekst = f.read().strip().split("\n")
    except FileNotFoundError:
        print("Brak pliku key.txt !!!")
        return

    for i in range(len(tekst)):
        linijka = tekst[i]
        temp = [linijka[j:j + 8] for j in range(0,len(linijka),8)]
        tekst[i] = temp

    for i in range(len(tekst[0])):
        for j in range(len(tekst)):
            element = tekst[j][i]
            if len(element) > 1 and element[1] == "1":
                reset_key = element

                for k in range(len(tekst)):
                    zaszyfrowany_znak = tekst[k][i]
                    odszyfrowany_znak = ""

                    for m in range(8):
                        xor = int(zaszyfrowany_znak[m]) ^ int(reset_key[m])
                        odszyfrowany_znak += str(xor)

                    if odszyfrowany_znak == "00000000":
                        tekst[k][i] = " "
                    else:
                        znak = chr(int(odszyfrowany_znak,2))
                        tekst[k][i] = znak

    with open("decrypt.txt","w") as f:
        print("Zapisano rozszyfrowany tekst do decrypt.txt")
        for linijka in tekst:
            # print("zapisano rzad" + str(linijka))
            for znak in linijka:
                f.write(znak.lower())
            f.write("\n")


dlugosc_linijek = 64

# przygotowanie()
# szyfrowanie()
# krypto_analiza()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR, zła ilość argumentów!")
        exit()

    if '-p' in sys.argv:
        przygotowanie()
    elif '-e' in sys.argv:
        szyfrowanie()
    elif '-k' in sys.argv:
        krypto_analiza()
    else:
        print("ERROR, Nieprawidłowe argumenty!")