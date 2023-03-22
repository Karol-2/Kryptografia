"""

Autor: Karol Krawczykiewicz

"""

from afiniczny import *
from cezar import *

import sys

if __name__ == "__main__":

    if len(sys.argv) > 3:
        print("ERROR, zła ilość argumentów!")
        exit()

    if '-c' in sys.argv:
        if '-e' in sys.argv:
            cezar_szyfrowanie()
        elif '-d' in sys.argv:
            cezar_odszyfrowanie()
        elif '-j' in sys.argv:
            cezar_kryptoanaliza_z_jawnym()
        elif '-k' in sys.argv:
            cezar_kryptoanaliza_tylko_kryptogram()
        else:
            print("ERROR, Nieprawidłowe argumenty!")

    elif '-a' in sys.argv:
        if '-e' in sys.argv:
            afiniczny_szyfrowanie()
        elif '-d' in sys.argv:
            afiniczny_odszyfrowanie()
        elif '-j' in sys.argv:
            afiniczny_kryptoanaliza_z_jawnym()
        elif '-k' in sys.argv:
            afiniczny_kryptoanaliza_tylko_kryptogram()
        else:
            print("ERROR, Nieprawidłowe argumenty!")
    else:
        print("ERROR, Nieprawidłowe argumenty!")
