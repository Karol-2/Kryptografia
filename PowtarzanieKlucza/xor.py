def prepare_text():
    try:
        with open('orig.txt','r') as f:
            print("Otwarto plik orig.txt")
            text = f.read().replace('\n',' ').lower()
        lines = [text[i:i + dlugosc_linijek] for i in range(0,len(text),dlugosc_linijek)]
    except FileNotFoundError:
        print("Brak pliku orig.txt !!!")
        return

    # dopisujemy odpowiednią ilość x w przypadku linii krótszych niż 64
    for i in range(len(lines)):
        lines[i] += 'x' * (dlugosc_linijek - len(lines[i]))

    with open('plain.txt','w') as f:
        print("Zapisano tekst to plain.txt")
        f.write('\n'.join(lines))


def encrypt():
    try:
        with open("plain.txt","r") as f:
            print("Otwarto plik plain.txt")
            plain = f.read()
            plain = plain.split("\n")
    except FileNotFoundError:
        print("Brak pliku plain.txt !!!")
        return

    try:
        with open("key.txt","r") as f:
            print("Otwarto plik key.txt")
            key = f.read()
            key = ' '.join(format(ord(i),'b') for i in key)
            key = key.split(" ")
            for i in range(len(key)):
                while len(key[i]) != 8:
                    key[i] = "0" + key[i]
            key = ''.join(format(x) for x in key)
    except FileNotFoundError:
        print("Brak pliku key.txt !!!")
        return

    for l in range(len(plain)):
        new_line = ""
        coded_line = ""
        line = ' '.join(format(ord(i),'b') for i in plain[l])
        line = line.split(" ")
        for i in range(len(line)):
            while len(line[i]) != 8:
                line[i] = "0" + line[i]
        line = ''.join(format(x) for x in line)
        if line != "00000000":
            for i in range(len(line)):
                result = int(line[i]) ^ int(key[i])

                if result:
                    coded_line += "1"
                else:
                    coded_line += "0"
                new_line = new_line + str(result)
        with open("crypto.txt","a") as f:
            f.write(new_line + '\n')


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
prepare_text()
encrypt()
crypto_analysis()
