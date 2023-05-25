import re


def podwoj_spacje(html_str, liczba):
    # Wyszukiwanie wszystkich wystąpień spacji
    spacje = re.findall(r' ', html_str)

    # Tworzenie podwójnych spacji na podstawie wzoru
    nowy_html_str = html_str
    for i, spacja in enumerate(spacje):
        if (liczba >> i) & 1 == 1:
            nowy_html_str = nowy_html_str.replace(spacja, '  ' + spacja)

    return nowy_html_str


# Wczytywanie kodu HTML z pliku
def wczytaj_html_z_pliku(nazwa_pliku):
    with open(nazwa_pliku, 'r',  encoding='utf-8') as plik:
        html_str = plik.read()
    return html_str


# Przykładowe użycie
nazwa_pliku = 'cover.html'
liczba = 0b101010

html_str = wczytaj_html_z_pliku(nazwa_pliku)
nowy_html_str = podwoj_spacje(html_str, liczba)

print(nowy_html_str)