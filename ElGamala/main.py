"""
Autor: Karol Krawczykiewicz
"""
import random


def nwd(a, b):
    if a < b:
        return nwd(b, a)
    elif a % b == 0:
        return b
    else:
        return nwd(b, a % b)


def generowanie_klucza():
    with open("elgamal.txt", "r") as f:
        p = int(f.readline().replace("\n", '').replace(" ", ''))
        g = int(f.readline().replace("\n", '').replace(" ", ''))
    klucz_prywatny = random.randint(10 ** 20, p)

    while nwd(p, klucz_prywatny) != 1:
        klucz_prywatny = random.randint(10 ** 20, p)
    klucz_publiczny = pow(g, klucz_prywatny, p)

    with open("public.txt", "w") as f:
        f.write(str(p) + "\n" + str(g) + "\n" + str(klucz_publiczny))

    with open("private.txt", "w") as f:
        f.write(str(p) + "\n" + str(g) + "\n" + str(klucz_prywatny))

    print(f"klucz prywatny: {klucz_prywatny}")
    print(f"klucz publiczny : {klucz_publiczny}")


generowanie_klucza()
