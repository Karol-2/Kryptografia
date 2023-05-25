"""
Autor: Karol Krawczykiewicz
"""
import re

global ustalona_dlugosc
ustalona_dlugosc = 4
'''
Aktualnie działa opcja 1, 
tylko operuje onw wyłącznie na 0 i 1, i na długość tylko 4
trzeba dodać inną wiadomość: 3f49d0a278e1b56c
'''
# TODO: dodać konwersję na 0 i 1 wiadomości np. 3f49d0a278e1b56c


def zakodowanie_opcja1():
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
        if i < ustalona_dlugosc:
            if line.endswith(' '):
                decoded_message += '1'
            else:
                decoded_message += '0'

    with open("detect.txt", 'w') as file:
        file.write(decoded_message)


def zakodowanie_opcja2():
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
    # TODO: dodać usuwanie podwójnych spacji na początku

    number_of_spaces = len(re.findall(r' {1,2}', cover))

    if len(message) > number_of_spaces:
        print('Nośnik jest za mały, aby zmieścić wiadomość')
        return
    encoded_cover = cover.split('\n')
    for index_mes in range(len(message)):
        for index_cover in range(len(encoded_cover)):
            if " " not in encoded_cover[index_cover]:
                print("nie ma")
                continue
            else:
                print("jest")

            if index_mes < len(message) and message[index_mes] == '1':
               # print(index_cover)
                content = str(encoded_cover[index_cover])
                content = content.replace(' ', ' ' + ' ')
                encoded_cover[index_cover] = content

    with open("watermark.html", 'w', encoding='utf-8') as file:
        for i in encoded_cover:
            file.write(i + "\n")


def odkodowanie_opcja2():
    try:
        with open("watermark.html", 'r', encoding='utf-8') as file:
            encoded_cover = file.read()
    except FileNotFoundError:
        print("ERROR, Brak pliku watermark.html!")
        return

    spaces = re.findall(r' {1,2}', encoded_cover)
    decoded_message = ''
    for i, space in enumerate(spaces):
        if i < ustalona_dlugosc:
            if space.endswith(' '):
                decoded_message += '1'
            else:
                decoded_message += '0'

    with open("detect.txt", 'w') as file:
        file.write(decoded_message)
#
#
# def encode_option3(message, cover):
#     invalid_attributes = ['margin-botom', 'lineheight']
#     if len(message) > len(invalid_attributes):
#         raise ValueError('Nośnik jest za mały, aby zmieścić wiadomość')
#     encoded_cover = cover
#     for i, attr in enumerate(invalid_attributes):
#         if i < len(message):
#             encoded_cover = encoded_cover.replace(attr, message[i])
#     return encoded_cover
#
#
# def decode_option3(encoded_cover):
#     invalid_attributes = ['margin-botom', 'lineheight']
#     decoded_message = ''
#     for attr in invalid_attributes:
#         if attr in encoded_cover:
#             decoded_message += '1'
#         else:
#             decoded_message += '0'
#     return decoded_message
#
#
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
    zakodowanie_opcja2()
    odkodowanie_opcja2()
