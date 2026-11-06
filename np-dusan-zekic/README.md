# Napredno programiranje — priprema radnog okruženja

Autor: Dušan Zekić

## Opis projekta

Projekat sadrži funkciju prosjecna_cijena koja iz CSV fajla
računa prosječnu cijenu noćenja.

Prosjek se računa kao ukupna vrijednost rezervacija podijeljena
ukupnim brojem noćenja.

CSV fajl sadrži kolone:
- gost
- noci
- cijena_noci

## Instalacija

Potrebni su Python 3.12 ili noviji i paketi iz requirements.txt.

```bash
python -m pip install -r requirements.txt
```

## Pokretanje testova

```bash
python -m pytest -v
```

## Provjera i formatiranje koda

```bash
ruff check .
ruff format .
```

## Korišćenje AI asistenta

Koristio sam Perplexity za pomoć pri pripremi projekta,
implementaciji funkcije i pisanju testova.

Upotrijebljeni upit:
„kako ovo da se uradi i što više objašnjenja zašto i kako radi?“ uz priloženu sliku zadatka.

## Uočeni nedostaci i ograničenja generisanog koda

- Funkcija pretpostavlja da CSV sadrži kolone noci i cijena_noci.
  Nedostajuća kolona izaziva KeyError bez posebno prilagođene poruke.
- Nenumeričke vrijednosti izazivaju ValueError, ali poruka ne navodi
  red CSV fajla u kojem je greška.
- Funkcija koristi float, što nije idealno za precizne finansijske
  obračune.
- Testovi ne pokrivaju sve slučajeve, na primjer nepostojeći fajl
  ili neispravne nazive kolona.

## Poboljšanja u odnosu na primjer sa vježbi

- Dodata je provjera negativnog broja noćenja i negativne cijene.
- Testovi koriste privremene fajlove umjesto fiksne Colab putanje.
- Dodat je test sa različitim brojem noćenja po rezervaciji.# np-dusan-zekic
