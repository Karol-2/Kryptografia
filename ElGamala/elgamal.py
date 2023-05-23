"""
Autor: Karol Krawczykiewicz
"""
import random
import sys


def nwd(a, b):
    if a < b:
        return nwd(b, a)
    elif a % b == 0:
        return b
    else:
        return nwd(b, a % b)


def generowanie_klucza():
    try:
        with open("elgamal.txt", "r") as f:
            p = int(f.readline().replace("\n", '').replace(" ", ''))
            g = int(f.readline().replace("\n", '').replace(" ", ''))
    except FileNotFoundError:
        print("ERROR, Brak pliku elgamal.txt!")
        return

    klucz_prywatny = random.randint(10 ** 20, p)

    while nwd(p, klucz_prywatny) != 1:
        klucz_prywatny = random.randint(10 ** 20, p)
    klucz_publiczny = pow(g, klucz_prywatny, p)

    with open("public.txt", "w") as f:
        f.write(str(p) + "\n" + str(g) + "\n" + str(klucz_publiczny))
        print("Zapisano do pliku public.txt")

    with open("private.txt", "w") as f:
        f.write(str(p) + "\n" + str(g) + "\n" + str(klucz_prywatny))
        print("Zapisano do pliku private.txt")

    print(f"klucz prywatny: {klucz_prywatny}")
    print(f"klucz publiczny: {klucz_publiczny}")


def enkrypcja():
    try:
        with open("public.txt", 'r') as f:
            p = int(f.readline().replace("\n", ''))
            g = int(f.readline().replace("\n", ''))
            klucz_publiczny = int(f.readline().replace("\n", ''))
    except FileNotFoundError:
        print("ERROR, Brak pliku public.txt!")
        return

    k = random.randint(10 ** 20, p)
    while nwd(p, k) != 1:
        k = random.randint(10 ** 20, p)

    try:
        with open("plain.txt", 'r') as f:
            m = int(f.readline().replace("\n", " "))
    except FileNotFoundError:
        print("ERROR, Brak pliku plain.txt!")
        return

    if not m < p:
        print("ERROR, warunek m<p nie jest spełniony ")
        return

    with open("crypto.txt", "w") as f:
        f.write(str(pow(g, k, p)) + "\n"
                + str((pow(klucz_publiczny, k, p) * m)))
        print("Zapisano do pliku crypto.txt")


def dekrypcja():
    try:
        with open("crypto.txt", "r") as f:
            gk = int(f.readline().replace("\n", ''))
            m = int(f.readline().replace("\n", ''))
    except FileNotFoundError:
        print("ERROR, Brak pliku crypto.txt!")
        return

    try:
        with open("private.txt", "r") as f:
            p = int(f.readline().replace("\n", ''))
            g = int(f.readline().replace("\n", ''))
            b = int(f.readline().replace("\n", ''))
    except FileNotFoundError:
        print("ERROR, Brak pliku private.txt!")
        return

    klucz = pow(gk, b, p)
    with open("decrypt.txt", "w") as f:
        f.write(str(int(m // klucz)))
        print("Zapisano do pliku decrypt.txt")


def podpis():
    try:
        with open("private.txt", 'r') as f:
            p = int(f.readline().strip())
            g = int(f.readline().strip())
            b = int(f.readline().strip())
    except FileNotFoundError:
        print("ERROR, Brak pliku private.txt!")
        return

    try:
        with open("message.txt", 'r') as f:
            message = int(f.read().strip())
    except FileNotFoundError:
        print("ERROR, Brak pliku message.txt!")
        return

    while True:
        k = random.randint(2, p - 2)
        if nwd(k, p - 1) == 1:
            break

    r = pow(g, k, p)

    k_inverse = pow(k, -1, p - 1)
    x = ((message - b * r) * k_inverse) % (p - 1)

    with open("signature.txt", "w") as f:
        f.write(str(r) + "\n")
        f.write(str(x))
        print("Zapisano do pliku signature.txt")


def weryfikacja_podpisu():
    try:
        with open("public.txt", 'r') as f:
            p = int(f.readline().strip())
            g = int(f.readline().strip())
            public_key = int(f.readline().strip())
    except FileNotFoundError:
        print("ERROR, Brak pliku public.txt!")
        return

    try:
        with open("message.txt", 'r') as f:
            message = int(f.read().strip())
    except FileNotFoundError:
        print("ERROR, Brak pliku message.txt!")
        return

    try:
        with open("signature.txt", 'r') as f:
            r = int(f.readline().replace("\n", ''))
            x = int(f.readline().replace("\n", ''))
    except FileNotFoundError:
        print("ERROR, Brak pliku signature.txt!")
        return

    gm = pow(g, message, p)

    rx_beta_r = (pow(r, x, p) * pow(public_key, r, p)) % p

    if gm == rx_beta_r:
        status = True
    else:
        status = False

    print(status)
    with open("verify.txt", "w") as f:
        f.write(str(status) + "\n")
        print("Zapisano do pliku verify.txt")


if __name__ == "__main__":
    if '-k' in sys.argv:
        generowanie_klucza()
    elif '-e' in sys.argv:
        enkrypcja()
    elif '-d' in sys.argv:
        dekrypcja()
    elif '-s' in sys.argv:
        podpis()
    elif '-v' in sys.argv:
        weryfikacja_podpisu()
    else:
        print("ERROR, Nieprawidłowe argumenty!")
