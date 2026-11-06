import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class Rezervacija:
    gost: str
    noci: int
    cijena_noci: float

    @property
    def iznos(self) -> float:
        return self.noci * self.cijena_noci


class IzvorPodataka(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...


class Izvjestavanje(Protocol):
    def sacuvaj(self, iznosi: list[float]) -> None: ...


class CsvIzvor:
    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        rezervacije = []

        with self.putanja.open(newline="", encoding="utf-8") as fajl:
            for red in csv.DictReader(fajl):
                rezervacije.append(
                    Rezervacija(
                        gost=red["gost"],
                        noci=int(red["noci"]),
                        cijena_noci=float(red["cijena_noci"]),
                    )
                )

        return rezervacije


class TekstualniIzvjestaj:
    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def sacuvaj(self, iznosi: list[float]) -> None:
        self.putanja.write_text(str(iznosi), encoding="utf-8")


class ServisRezervacija:
    def __init__(
        self,
        izvor: IzvorPodataka,
        izvjestaj: Izvjestavanje,
    ) -> None:
        self.izvor = izvor
        self.izvjestaj = izvjestaj

    def obradi(self) -> list[float]:
        rezervacije = self.izvor.ucitaj()
        iznosi = [rezervacija.iznos for rezervacija in rezervacije]
        self.izvjestaj.sacuvaj(iznosi)
        return iznosi


def main() -> None:
    folder = Path(__file__).resolve().parent

    izvor = CsvIzvor(folder / "rezervacije.csv")
    izvjestaj = TekstualniIzvjestaj(folder / "izvjestaj.txt")

    servis = ServisRezervacija(izvor, izvjestaj)
    iznosi = servis.obradi()

    print("Iznosi rezervacija:", iznosi)
    print("Ukupan iznos:", sum(iznosi))


if __name__ == "__main__":
    main()
