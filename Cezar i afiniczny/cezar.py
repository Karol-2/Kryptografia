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

    result = ""
    for char in szyfr:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - klucz - 65) % 26 + 65)
            else:
                result += chr((ord(char) - klucz - 97) % 26 + 97)
        else:
            result += char

    with open("plain.txt", "w") as file:
        file.write(result)
        print("Zapisano tekst odszyfrowany")

cezar_szyfrowanie()
cezar_szyfrowanie()
