"""

Autor: Karol Krawczykiewicz

"""


def nwd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def afiniczny_szyfrowanie():
    try:
        with open("key.txt", "r") as file:
            klucze = file.read().split()
            a = int(klucze[0])
            b = int(klucze[1])
            print("Wczytano klucze")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku key.txt")
        return

    try:
        with open("plain.txt", "r") as file:
            tekst = file.read()
            print("Wczytano tekst jawny")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku plain.txt")
        return

    if nwd(a, 26) != 1:
        print('Klucz a musi być względnie pierwszy z 26.')
        return

    szyfr = ''
    for znak in tekst:
        if znak.isalpha():
            if znak.isupper():
                numer_litery = ord(znak) - 65
            else:
                numer_litery = ord(znak) - 97

            numer_w_szyfrze = (numer_litery * a + b) % 26

            if znak.isupper():
                szyfr += chr(numer_w_szyfrze + 65)
            else:
                szyfr += chr(numer_w_szyfrze + 97)
        else:
            szyfr += znak

    with open("crypto.txt", "w") as file:
        file.write(szyfr)
        print("Zapisano tekst zaszyfrowany")


def afiniczny_zlamanie_sila():
    try:
        with open("crypto.txt", "r") as crypto_file:
            szyfr = crypto_file.read()
            print("Wczytano szyfr")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku crypto.txt")
        return

    with open("decrypt.txt", "w") as decrypt_file:
        for a in range(1, 26):
            if nwd(a, 26) == 1:
                for b in range(26):
                    tekst = ''
                    for znak in szyfr:
                        if znak.isalpha():
                            if znak.isupper():
                                numer_litery = ord(znak) - 65
                            else:
                                numer_litery = ord(znak) - 97

                            a_odwrocone = pow(a, -1, 26)
                            odszyfrowany_numer = ((numer_litery - b) * a_odwrocone) % 26

                            if znak.isupper():
                                tekst += chr(odszyfrowany_numer + 65)
                            else:
                                tekst += chr(odszyfrowany_numer + 97)
                        else:
                            tekst += znak

                    decrypt_file.write(f"Klucz: ({a}, {b})\n{tekst}\n")

    print("Zapisano wszystkie kandydatury")


def afiniczny_kryptoanaliza_jawny():
    return


# TODO: afiniczny jawny

def afiniczny_odszyfrowanie():
    return
# TODO: afiniczny odszyfrowanie
