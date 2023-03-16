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
                    plaintext = ''
                    for letter in szyfr:
                        if letter.isalpha():
                            letter_num = ord(letter) - 65 if letter.isupper() else ord(letter) - 97
                            inverse_a = pow(a, -1, 26)
                            plain_num = ((letter_num - b) * inverse_a) % 26
                            plaintext += chr(plain_num + 65 if letter.isupper() else plain_num + 97)
                        else:
                            plaintext += letter
                    decrypt_file.write(f"Klucz: ({a}, {b})\n{plaintext}\n")

    print("Zapisano wszystkie kandydatury")



afiniczny_szyfrowanie()
afiniczny_zlamanie_sila()
