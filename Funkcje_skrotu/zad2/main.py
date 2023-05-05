"""
Autor: Karol Krawczykiewicz
"""


def znajdz_roznice(hasze):

    roznice_tablica = []

    for i in range(0, len(hasze), 2):
        bity_h1 = f"{int(hasze[i], 16):08b}"
        bity_h2 = f"{int(hasze[i + 1], 16):08b}"
        roznice = 0

        if len(bity_h1) != len(bity_h2):
            roznice += 1

        for bit1, bit2 in zip(bity_h1, bity_h2):
            if bit1 != bit2:
                roznice += 1

        roznice_tablica.append(roznice)

    with open("diff.txt", "w") as f:
        funkcje = ["md5sum", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum", "b2sum"]
        bity = [128, 160, 224, 256, 384, 512, 512]

        for hasz in range(0, len(hasze), 2):
            f.write("cat hash.pdf personal.txt | " + funkcje[hasz // 2] + "\n")
            f.write("cat hash.pdf personal_.txt | " + funkcje[hasz // 2] + "\n")
            f.write(hasze[hasz] + "\n")
            f.write(hasze[hasz + 1] + "\n")
            f.write(f"Liczba różniących się bitów: {roznice_tablica[hasz // 2]} z {bity[hasz // 2]}, "
                    f"procentowo: {round(roznice_tablica[hasz // 2] / bity[hasz // 2], 3) * 100}%" + "\n" + "\n")

        print("Zapisano do pliku diff.txt")


if __name__ == "__main__":
    hasze = []
    with open("diff-pary.txt", "r") as f:
        for line in f:
            line = line.replace(" *-", "").replace("\n", "")
            hasze.append(line)

    znajdz_roznice(hasze)
