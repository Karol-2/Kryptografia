import re


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


# prepare-test DZIAŁA


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
        for rzad in zaszyfrowane:
            f.write(rzad + '\n')


def crypto_analysis():
    with open("crypto.txt","r") as f:
        text = f.read()
        text = text.replace("\n","*")
        text = text.split("*")
        text.pop(len(text) - 1)

    for index,line in enumerate(text):
        output = [line[i:i + 8] for i in range(0,len(line),8)]
        text[index] = output

    for row_index,row in enumerate(text):
        for column_index,column in enumerate(row):
            reset_char = False
            if len(column) > 1:
                if column[1] == "1":
                    reset_char = column
                if reset_char:
                    for i in range(len(text)):
                        coded_char = text[i][column_index]
                        coded_line = ""
                        for j in range(8):
                            result = int(coded_char[j]) ^ int(reset_char[j])
                            if result:
                                coded_line += "1"
                            else:
                                coded_line += "0"
                        if coded_line == "00000000":
                            text[i][column_index] = " "
                        else:
                            text[i][column_index] = chr(int(coded_line,2))

    with open("decrypt.txt","w") as f:
        print("Zapisano rozszyfrowany tekst do decrypt.txt")
        for row in text:
            print("zapisano row" + str(row))
            for char in row:
                f.write(char.lower())
            f.write("\n")


dlugosc_linijek = 64
przygotowanie()
szyfrowanie()
crypto_analysis()
