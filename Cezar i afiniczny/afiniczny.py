"""

Autor: Karol Krawczykiewicz

"""


def nwd(a,b):
    while b != 0:
        a,b = b,a % b
    return a


def odwrotnosc(x):
    for b in range(26):
        if ((x * b) % 26) == 1:
            return b


def afiniczny_szyfrowanie():
    try:
        with open("key.txt","r") as file:
            klucze = file.read().split()
            a = int(klucze[0])
            b = int(klucze[1])
            print("Wczytano klucze z key.txt")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku key.txt")
        return

    try:
        with open("plain.txt", "r") as file:
            tekst = file.read()
            print("Wczytano tekst jawny z plain.txt")
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

    with open("crypto.txt","w") as file:
        file.write(szyfr)
        print("Zapisano tekst zaszyfrowany do crypto.txt")


def afiniczny_odszyfrowanie():
    try:
        with open("key.txt","r") as file:
            klucz = file.read().split()
            a = int(klucz[0])
            b = int(klucz[1])
            print("Wczytano klucze z key.txt")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku key.txt")
        return

    try:
        with open("crypto.txt","r") as crypto_file:
            szyfr = crypto_file.read()
            print("Wczytano szyfr z crypto.txt")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku crypto.txt")
        return

    tekst = ''
    for znak in szyfr:
        if znak.isalpha():
            if znak.isupper():
                numer_litery = ord(znak) - 65
            else:
                numer_litery = ord(znak) - 97

            a_odwrocone = pow(a,-1,26)
            odszyfrowany_numer = ((numer_litery - b) * a_odwrocone) % 26

            if znak.isupper():
                tekst += chr(odszyfrowany_numer + 65)
            else:
                tekst += chr(odszyfrowany_numer + 97)
        else:
            tekst += znak

    with open("decrypt.txt","w") as file:
        file.write(tekst)
        print("Zapisano tekst odszyfrowany do decrypt.txt")


def afiniczny_kryptoanaliza_tylko_kryptogram():
    try:
        with open("crypto.txt","r") as crypto_file:
            szyfr = crypto_file.read()
            print("Wczytano szyfr z crypto.txt")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku crypto.txt")
        return

    with open("decrypt.txt","w") as decrypt_file:
        for a in range(1,26):
            if nwd(a,26) == 1:
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

    print("Zapisano wszystkie kandydatury do decrypt.txt")


def afiniczny_kryptoanaliza_z_jawnym():
    kryptogram = []
    extra = []

    try:
        with open("crypto.txt","r") as f:
            for line in f:
                for char in line:
                    if char.isalpha():
                        kryptogram.append(char.lower())
    except FileNotFoundError:
        print("ERROR, Brakuje pliku crypto.txt")
        return

    try:
        with open("extra.txt","r") as f:
            for line in f:
                for char in line:
                    if char.isalpha():
                        extra.append(char.lower())
    except FileNotFoundError:
        print("ERROR, Brakuje pliku extra.txt")
        return

    alfabet = {}
    for i in range(26):
        alfabet[chr(ord('a') + i)] = i

    for i in range(len(extra) + 1):
        try:
            x0, x1 = alfabet[extra[i]], alfabet[extra[i + 1]]
            y0, y1 = alfabet[kryptogram[i]],  alfabet[kryptogram[i + 1]]

        except IndexError:
            print("Nie znaleziono klucza!")
            return

        y = (y0 - y1) % 26
        x = (x0 - x1) % 26
        x_odwrotny = odwrotnosc(x)
        if x_odwrotny is not None:
            a = (y * x_odwrotny) % 26
            y = (a * x0) % 26
            b = (y0 - y) % 26
            print("Znaleziono klucz, a:",a,"b:",b)

            with open("key-new.txt","w") as file:
                string = f"{a} {b}"
                file.write(string)
                print("Zapisano klucz do key-new.txt")

            with open("crypto.txt","r") as crypto_file:
                szyfr = crypto_file.read()

            tekst = ''
            for znak in szyfr:
                if znak.isalpha():
                    if znak.isupper():
                        numer_litery = ord(znak) - 65
                    else:
                        numer_litery = ord(znak) - 97

                    a_odwrocone = pow(a,-1,26)
                    odszyfrowany_numer = ((numer_litery - b) * a_odwrocone) % 26

                    if znak.isupper():
                        tekst += chr(odszyfrowany_numer + 65)
                    else:
                        tekst += chr(odszyfrowany_numer + 97)
                else:
                    tekst += znak

            with open("decrypt.txt","w") as file:
                file.write(tekst)
                print("Zapisano tekst odszyfrowany do decrypt.txt")
            return

    print("Nie znaleziono klucza!")


