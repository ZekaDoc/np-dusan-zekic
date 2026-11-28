# Rezervacije API

FastAPI servis za obračun cijene boravka (Mini projekat 3, Napredno programiranje).

## Endpointi
- `POST /cijena` - tijelo: `noci` (1-30), `cijena_noci` (>0), `popust` (0-1); vraća `iznos`.
- `GET /health` - provjera dostupnosti.

## Pokretanje
```bash
pip install -r requirements-dev.txt
uvicorn src.main:app --reload     # http://127.0.0.1:8000/docs
```

## Provjere (iste kao u CI-u)
```bash
ruff check .
mypy src/
pytest --cov=src
bandit -r src/
pip-audit -r requirements.txt
```

## Rizici i mjere smanjenja
| Rizik | Mjera |
|---|---|
| Nevalidan ili zlonamjeran unos (injekcija, ekstremne vrijednosti, DoS) | Pydantic modeli sa `ge/le/gt` ograničenjima; nevalidan unos vraća 422; testovi za granične i neispravne vrijednosti. Nema SQL-a, `eval`, `pickle` ni `shell=True`. |
| Ranjive zavisnosti | `pip-audit` u CI-u pri svakoj izmjeni; zavisnosti sa minimalnim verzijama. |
| Tajne u kodu ili repozitoriju | Nema tajni u kodu; konfiguracija kroz varijable okruženja; `.env` u `.gitignore`. |
| Endpointi bez autentikacije | `/cijena` je javan jer ne obrađuje lične podatke; za produkciju dodati API ključ/OAuth2 i rate limiting. |
| Curenje podataka kroz logove/greške | Ne logovati tijela zahtjeva; FastAPI ne vraća stack trace klijentu. |

