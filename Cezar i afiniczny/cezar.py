"""

Autor: Karol Krawczykiewicz

"""


def cezar_szyfrowanie():
    try:
        with open("key.txt", "r") as file:
            klucz = file.read().split()[0]
            print("Wczytano klucz")
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

    try:
        klucz = int(klucz)
        if 1 < int(klucz) > 25:
            print("ERROR, Klucz spoza przedziału 1 - 25!")
            return
    except ValueError:
        print("ERROR, klucz nie jest liczbą!")
        return

    wynik = ""
    for znak in tekst:
        if znak.isalpha():
            if znak.isupper():
                wynik += chr((ord(znak) + klucz - 65) % 26 + 65)
            else:
                wynik += chr((ord(znak) + klucz - 97) % 26 + 97)
        else:
            wynik += znak

    with open("crypto.txt", "w") as file:
        file.write(wynik)
        print("Zapisano tekst zaszyfrowany")


def cezar_odszyfrowanie():
    try:
        with open("key.txt", "r") as file:
            klucz = file.read().split()[0]
            print("Wczytano klucz")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku key.txt")
        return

    try:
        with open("crypto.txt", "r") as file:
            szyfr = file.read()
            print("Wczytano tekst zaszyfrowany")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku crypto.txt")
        return

    try:
        klucz = int(klucz)
        if 1 < int(klucz) > 25:
            print("ERROR, Klucz spoza przedziału 1 - 25!")
            return
    except ValueError:
        print("ERROR, klucz nie jest liczbą!")
        return

    tekst = ""
    for znak in szyfr:
        if znak.isalpha():
            if znak.isupper():
                tekst += chr((ord(znak) - klucz - 65) % 26 + 65)
            else:
                tekst += chr((ord(znak) - klucz - 97) % 26 + 97)
        else:
            tekst += znak

    with open("decrypt.txt", "w") as file:
        file.write(tekst)
        print("Zapisano tekst odszyfrowany")


def cezar_kryptoanaliza_tylko_kryptogram():
    try:
        with open("crypto.txt", "r") as crypto_file:
            szyfr = crypto_file.read()
            print("Wczytano szyfr")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku crypto.txt")
        return

    with open("decrypt.txt", "w") as decrypt_file:
        for klucz in range(1, 26):
            tekst = ""
            for znak in szyfr:
                if znak.isalpha():
                    if znak.isupper():
                        tekst += chr((ord(znak) - klucz - 65) % 26 + 65)
                    else:
                        tekst += chr((ord(znak) - klucz - 97) % 26 + 97)

                else:
                    tekst += znak
            decrypt_file.write(f"klucz {klucz}:\n{tekst}\n")
    print("Zapisano wszystkie kandydatury")


def cezar_kryptoanaliza_z_jawnym():
    try:
        with open("crypto.txt", "r") as f:
            kryptogram = f.read()
            print("Wczytano szyfr")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku crypto.txt")
        return

    try:
        with open("extra.txt", "r") as f:
            extra = f.read()
            print("Wczytano tekst dodatkowy")
    except FileNotFoundError:
        print("ERROR, Brakuje pliku extra.txt")
        return

    for i in range(len(kryptogram)):
        znak = kryptogram[i]
        if ord(znak) in range(ord('A'), ord('Z') + 1) or ord(znak) in range(ord('a'), ord('z') + 1):
            znak_w_jawnym = extra[i][
                i % len(extra[i])]  # znak w tekście jawnym, który odpowiada pozycji znaku w tekście zaszyfrowanym
            klucz = (ord(znak) - ord(znak_w_jawnym)) % 26

            with open("key-new.txt", "w") as f:
                f.write(str(klucz))
                print("Znaleziono klucz!", klucz)
            return

    print("Nie można znaleźć klucza!")

