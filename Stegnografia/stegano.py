"""
Autor: Karol Krawczykiewicz
"""
import re

global USTALONA_DLUGOSC
USTALONA_DLUGOSC = 8
'''
Aktualnie działa opcja 1, 
tylko operuje onw wyłącznie na 0 i 1, i na długość tylko 4
trzeba dodać inną wiadomość: 3f49d0a278e1b56c
'''
# TODO: dodać konwersję na 0 i 1 wiadomości np. 3f49d0a278e1b56c


def zakodowanie_opcja1():
    # spacja - 1
    # brak - 0
    try:
        with open("mess.txt", 'r') as file:
            message = file.read()
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


def odkodowanie_opcja1():
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
        file.write(decoded_message)


def zakodowanie_opcja2():
    # dwie spacje - 1
    # jedna spacja - 0
    try:
        with open("mess.txt", 'r') as file:
            message = file.read()
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


def odkodowanie_opcja2():
    try:
        with open("watermark.html", 'r', encoding='utf-8') as file:
            encoded_cover = file.read()
    except FileNotFoundError:
        print("ERROR, Brak pliku watermark.html!")
        return

    decoded_message = ""
    i = 0
    while i < len(encoded_cover):
        current = encoded_cover[i]
        next = encoded_cover[i+1]
        if len(decoded_message) == USTALONA_DLUGOSC:
            break

        if current == " " and next != " ":
            decoded_message += '0'
        elif current== " " and next == " ":
            decoded_message += "1"
            i+=2
            continue
        i+=1

    with open("detect.txt", 'w') as file:
        file.write(decoded_message)


def zakodowanie_opcja3():
    # zamiast p to na div
    # prawidłowy - 0
    # nieprawidłowy - 1

    try:
        with open("mess.txt", 'r') as file:
            message = file.read()
    except FileNotFoundError:
        print("ERROR, Brak pliku mess.txt!")
        return

    try:
        with open("cover.html", 'r', encoding='utf-8') as file:
            cover = file.read()
    except FileNotFoundError:
        print("ERROR, Brak pliku cover.html!")
        return

    number_of_divs = len(re.findall(r'<div', cover))
    if len(message)> number_of_divs:
        print('Nośnik jest za mały, aby zmieścić wiadomość')
        return


    invalid_atribute = " style=\"margin-botom: 0cm;\""
    vaild_atribute = " style=\"margin-bottom: 0cm;\""

    cover_tab = cover.split("\n")
    mes_index = 0
    while mes_index < len(message):
        for j in range(len(cover_tab)): # po linijkach
            line = cover_tab[j]
            if "<div" in line:
                words = line.split(" ")
                for i in range (len(words)): # po słowach w linijce
                    if mes_index >= len(message):
                        break
                    if "<div" in words[i]:
                        if message[mes_index] == '0':
                            words[i] += vaild_atribute
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


def odkodowanie_opcja3():
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
        file.write(decoded_message)


# def encode_option4(message, cover):
#     font_tag = '<font>'
#     open_tag = '<font>'
#     close_tag = '</font>'
#     occurrences = cover.count(font_tag)
#     if len(message) > occurrences:
#         raise ValueError('Nośnik jest za mały, aby zmieścić wiadomość')
#     encoded_cover = cover
#     for i, bit in enumerate(message):
#         if bit == '1':
#             encoded_cover = encoded_cover.replace(font_tag, open_tag + font_tag, 1)
#         else:
#             encoded_cover = encoded_cover.replace(font_tag, close_tag + font_tag, 1)
#     return encoded_cover
#
#
# def decode_option4(encoded_cover):
#     font_tag = '<font>'
#     open_tag = '<font>'
#     close_tag = '</font>'
#     decoded_message = ''
#     while font_tag in encoded_cover:
#         index = encoded_cover.index(font_tag)
#         if encoded_cover[index + len(font_tag):index + len(font_tag) + len(open_tag)] == open_tag:
#             decoded_message += '1'
#         else:
#             decoded_message += '0'
#         encoded_cover = encoded_cover[index + len(font_tag):]
#     return decoded_message
#
#
# def write_to_file(filename, content):
#     with open(filename, 'w') as file:
#         file.write(content)
#
#
# def read_from_file(filename):
#     with open(filename, 'r') as file:
#         content = file.read()
#     return content


if __name__ == '__main__':
    zakodowanie_opcja3()
    odkodowanie_opcja3()