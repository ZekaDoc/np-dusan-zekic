# Mini projekat 1 — refaktoring obrade rezervacija

Autor: Dušan Zekić

## Cilj projekta

Refaktorisati početni monolitni program za obradu rezervacija
primjenom principa S i D.

Program učitava rezervacije, računa njihove iznose i čuva
tekstualni izvještaj.

## Početna verzija

Fajl prije.py sadrži sopstvenu skriptu.

Funkcija obradi_rezervacije istovremeno učitava CSV,
računa iznose i zapisuje izvještaj.

## Refaktorisana verzija

Fajl rezervacije.py sadrži:

- Rezervacija: podaci i iznos pojedinačne rezervacije.
- CsvIzvor: učitavanje rezervacija iz CSV fajla.
- TekstualniIzvjestaj: zapisivanje izvještaja.
- ServisRezervacija: koordinacija obrade.
- IzvorPodataka: Protocol za učitavanje podataka.
- Izvjestavanje: Protocol za čuvanje izvještaja.

## Primjena SOLID principa

### S — Single Responsibility

Učitavanje, obračun i zapisivanje izvještaja razdvojeni su
u posebne komponente.

### D — Dependency Inversion

Servis prima izvor podataka i izvještaj kroz konstruktor.
Zavisi od Protocol ugovora, a ne od konkretne CSV implementacije.

## Očuvanje ponašanja

Obje verzije računaju iznos kao noci * cijena_noci.

Izvještaj je u obje verzije tekstualni zapis liste iznosa.
Prazan CSV sa zaglavljem daje praznu listu.

## Instalacija

```bash
python -m pip install -r requirements.txt
```

## Pokretanje

Komande se izvršavaju iz foldera mini_projekat_1.

```bash
python rezervacije.py
```

## Testiranje

```bash
python -m pytest -v
```

Tri testa koriste zamjenski izvor i zamjensko izvještavanje.
Provjeravaju više rezervacija, prazan izvor i decimalnu cijenu.

## Provjera koda

```bash
python -m ruff check .
python -m ruff format .
```

## Korišćenje AI asistenta

Korišćen je Perplexity.

Upotrijebljeni upit:
„ovo je iz prezentacije 2 nedjelja, kako se ovo radi i objasni mi sve po stepu?“
uz priloženu sliku zadatka.

AI je predložio početni skript, refaktorisanu verziju i testove.

## Pregled i ispravke generisanog koda

Ovdje navesti stvarno izvršene provjere i izmjene nakon
pokretanja i pregleda koda.

## Ograničenja

- Nema dodatne validacije negativnih vrijednosti.
- Greške u CSV kolonama i vrijednostima nemaju prilagođene poruke.
- Za cijene se koristi float.
- Tri osnovna testa provjeravaju servis, ali ne provjeravaju
  stvarno čitanje CSV-a ni zapisivanje izvještaja na disk.