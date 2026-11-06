import pytest

from rezervacije import Rezervacija, ServisRezervacija


class LazniIzvor:
    def __init__(self, podaci: list[Rezervacija]) -> None:
        self.podaci = podaci

    def ucitaj(self) -> list[Rezervacija]:
        return self.podaci


class LazniIzvjestaj:
    def __init__(self) -> None:
        self.sacuvani_iznosi: list[float] | None = None

    def sacuvaj(self, iznosi: list[float]) -> None:
        self.sacuvani_iznosi = list(iznosi)


def test_obrada_vise_rezervacija():
    izvor = LazniIzvor(
        [
            Rezervacija("Ana", 3, 80.0),
            Rezervacija("Marko", 5, 65.0),
            Rezervacija("Ivana", 2, 120.0),
        ]
    )
    izvjestaj = LazniIzvjestaj()
    servis = ServisRezervacija(izvor, izvjestaj)

    rezultat = servis.obradi()

    assert rezultat == pytest.approx([240.0, 325.0, 240.0])
    assert izvjestaj.sacuvani_iznosi == rezultat


def test_obrada_praznog_izvora():
    izvor = LazniIzvor([])
    izvjestaj = LazniIzvjestaj()
    servis = ServisRezervacija(izvor, izvjestaj)

    rezultat = servis.obradi()

    assert rezultat == []
    assert izvjestaj.sacuvani_iznosi == []


def test_obrada_decimalne_cijene():
    izvor = LazniIzvor(
        [
            Rezervacija("Ana", 3, 79.99),
        ]
    )
    izvjestaj = LazniIzvjestaj()
    servis = ServisRezervacija(izvor, izvjestaj)

    rezultat = servis.obradi()

    assert rezultat == pytest.approx([239.97])
    assert izvjestaj.sacuvani_iznosi == rezultat
