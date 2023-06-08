"""
Autor: Karol Krawczykiewicz
"""
import re
import sys

global USTALONA_DLUGOSC
USTALONA_DLUGOSC = 32


def hex_to_binary(hex_string):
    try:
        decimal_num = int(hex_string, 16)  # dziesiętna
        binary_num = bin(decimal_num)[2:]  # binarna
        return binary_num.zfill(32)
    except ValueError:
        return "Nieprawidłowy format szesnastkowy"


def binary_to_hex(binary_string):
    try:
        decimal_num = int(binary_string, 2)  # dziesiętna
        hex_num = hex(decimal_num)[2:]  # szesnastkowa
        return hex_num
    except ValueError:
        return "Nieprawidłowy format binarny"


def zanurzanie_opcja1():
    # spacja - 1
    # brak - 0
    print("zanurzanie opcja 1")
    try:
        with open("mess.txt", 'r') as file:
            message = file.read()
            message = hex_to_binary(message)
    except FileNotFoundError:
        print("ERROR, Brak pliku mess.txt!")
        return
    try:
        with open("cover.html", 'r', encoding='utf-8') as file:
            page = file.read()
    except FileNotFoundError:
        print("ERROR, Brak pliku cover.html!")
        return

    lines = page.split('\n')
    if len(message) > len(lines):
        print('ERROR!, Nośnik jest za mały, aby zmieścić wiadomość')
        return
    encoded_lines = []

    for i, line in enumerate(lines):
        if line.endswith(" "):
            line = line.rstrip()

        if i < len(message) and message[i] == '1':
            encoded_lines.append(line + ' ')
        else:
            encoded_lines.append(line)

    with open("watermark.html", 'w', encoding='utf-8') as file:
        for i in encoded_lines:
            file.write(i + "\n")
        print("Saved to watermark.html")


def wyodrebnianie_opcja1():
    print("wyodrebnianie opcja 1")
    try:
        with open("watermark.html", 'r', encoding='utf-8') as file:
            encoded_cover = file.read()
    except FileNotFoundError:
        print("ERROR, Brak pliku watermark.html!")
        return

    lines = encoded_cover.split('\n')
    decoded_message = ''

    for i, line in enumerate(lines):
        if i < USTALONA_DLUGOSC:
            if line.endswith(' '):
                decoded_message += '1'
            else:
                decoded_message += '0'

    with open("detect.txt", 'w') as file:
        decoded_message = binary_to_hex(decoded_message)
        file.write(decoded_message)
        print("decoded message: ", decoded_message)
        print("Saved to detect.txt")


def zanurzanie_opcja2():
    # dwie spacje - 1
    # jedna spacja - 0
    print("zanurzanie opcja 2")
    try:
        with open("mess.txt", 'r') as file:
            message = file.read()
            message = hex_to_binary(message)
    except FileNotFoundError:
        print("ERROR, Brak pliku mess.txt!")
        return

    try:
        with open("cover.html", 'r', encoding='utf-8') as file:
            cover = file.read()
            cover = cover.replace("  ", " ")
    except FileNotFoundError:
        print("ERROR, Brak pliku cover.html!")
        return

    number_of_spaces = len(re.findall(r' {1,2}', cover))

    if len(message) > number_of_spaces:
        print('Nośnik jest za mały, aby zmieścić wiadomość')
        return

    modified_code = ""
    message_index = 0

    for char in cover:
        if char == " " and message_index < len(message):
            if message[message_index] == "1":
                modified_code += "  "
            else:
                modified_code += char
            message_index += 1
        else:
            modified_code += char

    with open("watermark.html", 'w', encoding='utf-8') as file:
        cover_tab = modified_code.split('\n')
        for i in cover_tab:
            file.write(i + "\n")
        print("Saved to watermark.html")


def wyodrebnianie_opcja2():
    print("wyodrebnianie opcja 2")
    try:
        with open("watermark.html", 'r', encoding='utf-8') as file:
            encoded_cover = file.read()
    except FileNotFoundError:
        print("ERROR, Brak pliku watermark.html!")
        return

    decoded_message = ""
    i = 0
    while i < len(encoded_cover):
        current_symbol = encoded_cover[i]
        next_symbol = encoded_cover[i + 1]
        if len(decoded_message) == USTALONA_DLUGOSC:
            break

        if current_symbol == " " and next_symbol != " ":
            decoded_message += '0'
        elif current_symbol == " " and next_symbol == " ":
            decoded_message += "1"
            i += 2
            continue
        i += 1

    with open("detect.txt", 'w') as file:
        decoded_message = binary_to_hex(decoded_message)
        file.write(decoded_message)
        print("decoded message: ", decoded_message)
        print("Saved to detect.txt")


def zanurzanie_opcja3():
    # zamiast p to na div
    # prawidłowy - 0
    # nieprawidłowy - 1

    print("zanurzanie opcja 3")

    try:
        with open("mess.txt", 'r') as file:
            message = file.read()
            message = hex_to_binary(message)
    except FileNotFoundError:
        print("ERROR, Brak pliku mess.txt!")
        return

    try:
        with open("cover.html", 'r', encoding='utf-8') as file:
            cover = file.read()
            cover = cover.replace("margin-botom: 0cm;", "")
            cover = cover.replace("margin-botom", "")
    except FileNotFoundError:
        print("ERROR, Brak pliku cover.html!")
        return

    number_of_divs = len(re.findall(r'<div', cover))
    if len(message) > number_of_divs:
        print('Nośnik jest za mały, aby zmieścić wiadomość')
        return

    invalid_atribute = " style=\"margin-botom: 0cm;\""
    valid_atribute = " style=\"margin-bottom: 0cm;\""

    cover_tab = cover.split("\n")
    mes_index = 0
    while mes_index < len(message):
        for j in range(len(cover_tab)):  # po linijkach
            line = cover_tab[j]
            if "<div" in line:
                words = line.split(" ")
                for i in range(len(words)):  # po słowach w linijce
                    if mes_index >= len(message):
                        break
                    if "<div" in words[i]:
                        if message[mes_index] == '0':
                            words[i] += valid_atribute
                        if message[mes_index] == '1':
                            words[i] += invalid_atribute
                        mes_index += 1
                        break
                sentence = ""
                for word in words:
                    sentence += word + " "
                cover_tab[j] = sentence

    with open("watermark.html", 'w', encoding='utf-8') as file:
        for i in cover_tab:
            file.write(i + "\n")
        print("Saved to watermark.html")


def wyodrebnianie_opcja3():
    print("wyodrebnianie opcja 3")
    try:
        with open("watermark.html", 'r', encoding='utf-8') as file:
            encoded_cover = file.read()
    except FileNotFoundError:
        print("ERROR, Brak pliku watermark.html!")
        return

    html_lines = encoded_cover.split("\n")
    decoded_message = ""
    div_lines = []

    for line in html_lines:
        if "<div" in line:
            div_lines.append(line)

    for word in div_lines:
        if len(decoded_message) > USTALONA_DLUGOSC:
            break

        if "margin-bottom" in word:
            decoded_message += '0'
        if "margin-botom" in word:
            decoded_message += '1'

    with open("detect.txt", 'w') as file:
        decoded_message = binary_to_hex(decoded_message)
        file.write(decoded_message)
        print("decoded message: ", decoded_message)
        print("Saved to detect.txt")


def zanurzanie_opcja4():
    # # przykład
    # <font style = "color: red;"> </font>
    #
    # # 1
    # <font></font><font style = "color: red;"> </font>
    #
    # # 0
    # <font style = "color: red;" > </font> <font></font>
    print("zanurzanie opcja 4")
    try:
        with open("mess.txt", 'r') as file:
            message = file.read()
            message = hex_to_binary(message)
    except FileNotFoundError:
        print("ERROR, Brak pliku mess.txt!")
        return

    try:
        with open("cover.html", 'r', encoding='utf-8') as file:
            cover = file.read()
            cover = cover.replace("<font> </font>", "")
            cover = cover.replace("<font></font>", "")
    except FileNotFoundError:
        print("ERROR, Brak pliku cover.html!")
        return

    number_of_font = len(re.findall(r'<font', cover))
    if len(message) > number_of_font:
        print('Nośnik jest za mały, aby zmieścić wiadomość')
        return

    cover_tab = cover.split("\n")
    mes_index = 0
    while mes_index < len(message):
        for j in range(len(cover_tab)):  # po linijkach
            if j == len(cover_tab):
                break

            line = cover_tab[j]
            if "<font" in line or "</font>" in line:
                line = line.replace("\t", "")
                words = line.split(" ")
                for i in range(len(words)):  # po słowach w linijce
                    if mes_index >= len(message):
                        break
                    if "<font" in words[i]:
                        if message[mes_index] == '1':
                            text = str(words[i])
                            words[i] = "\t" + "<font></font>" + text
                            mes_index += 1
                            continue
                    if "</font>" in words[i]:
                        if message[mes_index] == '0':
                            words[i] += " <font></font>"
                            mes_index += 1

                sentence = ""
                for word in words:
                    sentence += word + " "
                cover_tab[j] = sentence

    with open("watermark.html", 'w', encoding='utf-8') as file:
        for i in cover_tab:
            file.write(i + "\n")
        print("Saved to watermark.html")


def wyodrebnianie_opcja4():
    print("wyodrebnianie opcja 4")
    try:
        with open("watermark.html", 'r', encoding='utf-8') as file:
            encoded_cover = file.read()
    except FileNotFoundError:
        print("ERROR, Brak pliku watermark.html!")
        return

    html_lines = encoded_cover.split("\n")
    decoded_message = ""
    font_lines = []

    for line in html_lines:
        if "font" in line:
            font_lines.append(line)

    for line in font_lines:
        if len(decoded_message) == USTALONA_DLUGOSC:
            break
        if "<font></font><font" in line:
            decoded_message += "1"
        if "</font> <font></font>" in line:
            decoded_message += "0"

    with open("detect.txt", 'w') as file:
        decoded_message = binary_to_hex(decoded_message)
        file.write(decoded_message)
        print("decoded message: ", decoded_message)
        print("Saved to detect.txt")


if __name__ == '__main__':
    if '-e' in sys.argv:
        if '-1' in sys.argv:
            zanurzanie_opcja1()
        elif '-2' in sys.argv:
            zanurzanie_opcja2()
        elif '-3' in sys.argv:
            zanurzanie_opcja3()
        elif '-4' in sys.argv:
            zanurzanie_opcja4()
        else:
            print("ERROR, zła opcja numerowa, podaj -1, -2, -3 lub -4")

    elif '-d' in sys.argv:
        if '-1' in sys.argv:
            wyodrebnianie_opcja1()
        elif '-2' in sys.argv:
            wyodrebnianie_opcja2()
        elif '-3' in sys.argv:
            wyodrebnianie_opcja3()
        elif '-4' in sys.argv:
            wyodrebnianie_opcja4()
        else:
            print("ERROR, zła opcja numerowa, podaj -1, -2, -3 lub -4")
    else:
        print("ERROR, Brak opcji -d lub -e!")