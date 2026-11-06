import csv
from pathlib import Path


def prosjecna_cijena(putanja: Path) -> float:
    """Vraca prosjecnu cijenu nocenja iz CSV fajla."""
    ukupno = 0.0
    broj_noci = 0

    with putanja.open(newline="", encoding="utf-8") as fajl:
        for red in csv.DictReader(fajl):
            noci = int(red["noci"])
            cijena = float(red["cijena_noci"])

            if noci < 0 or cijena < 0:
                raise ValueError("Broj noci i cijena ne smiju biti negativni.")

            ukupno += noci * cijena
            broj_noci += noci

    if broj_noci == 0:
        raise ValueError("Nema ostvarenih nocenja.")

    return ukupno / broj_noci
