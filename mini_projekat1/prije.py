import csv
from pathlib import Path


def obradi_rezervacije(ulaz: Path, izlaz: Path) -> list[float]:
    iznosi = []

    with ulaz.open(newline="", encoding="utf-8") as fajl:
        for red in csv.DictReader(fajl):
            noci = int(red["noci"])
            cijena = float(red["cijena_noci"])
            iznosi.append(noci * cijena)

    izlaz.write_text(str(iznosi), encoding="utf-8")
    return iznosi


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    obradi_rezervacije(
        folder / "rezervacije.csv",
        folder / "izvjestaj.txt",
    )
