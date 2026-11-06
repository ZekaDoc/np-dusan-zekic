import pytest

from prosjek import prosjecna_cijena


def test_prosjecna_cijena(tmp_path):
    putanja = tmp_path / "rezervacije.csv"
    putanja.write_text(
        "gost,noci,cijena_noci\nAna,2,100\nMarko,3,50\n",
        encoding="utf-8",
    )

    rezultat = prosjecna_cijena(putanja)

    assert rezultat == pytest.approx(70.0)


def test_nema_nocenja(tmp_path):
    putanja = tmp_path / "prazno.csv"
    putanja.write_text(
        "gost,noci,cijena_noci\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Nema ostvarenih nocenja"):
        prosjecna_cijena(putanja)


def test_negativne_vrijednosti(tmp_path):
    putanja = tmp_path / "neispravno.csv"
    putanja.write_text(
        "gost,noci,cijena_noci\nAna,-2,100\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="ne smiju biti negativni"):
        prosjecna_cijena(putanja)
