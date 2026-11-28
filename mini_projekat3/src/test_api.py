import pytest
from fastapi.testclient import TestClient

from src.main import app

klijent = TestClient(app)


def test_health() -> None:
    assert klijent.get("/health").json() == {"status": "ok"}


def test_cijena_ok() -> None:
    r = klijent.post("/cijena", json={"noci": 3, "cijena_noci": 80})
    assert r.status_code == 200
    assert r.json()["iznos"] == 240.0


def test_cijena_sa_popustom() -> None:
    r = klijent.post("/cijena", json={"noci": 2, "cijena_noci": 50, "popust": 0.5})
    assert r.json()["iznos"] == 50.0


@pytest.mark.parametrize("noci", [1, 30])
def test_granicne_noci_prihvacene(noci: int) -> None:
    r = klijent.post("/cijena", json={"noci": noci, "cijena_noci": 10})
    assert r.status_code == 200
    assert r.json()["iznos"] == noci * 10.0


@pytest.mark.parametrize("noci", [0, 31, -5])
def test_noci_van_opsega(noci: int) -> None:
    r = klijent.post("/cijena", json={"noci": noci, "cijena_noci": 80})
    assert r.status_code == 422


@pytest.mark.parametrize("cijena", [0, -10])
def test_neispravna_cijena(cijena: float) -> None:
    r = klijent.post("/cijena", json={"noci": 2, "cijena_noci": cijena})
    assert r.status_code == 422


@pytest.mark.parametrize("popust", [-0.1, 1.5])
def test_popust_van_opsega(popust: float) -> None:
    r = klijent.post("/cijena", json={"noci": 2, "cijena_noci": 50, "popust": popust})
    assert r.status_code == 422


def test_popust_100_posto_daje_nulu() -> None:
    r = klijent.post("/cijena", json={"noci": 3, "cijena_noci": 80, "popust": 1.0})
    assert r.json()["iznos"] == 0.0


def test_pogresan_tip_unosa() -> None:
    r = klijent.post("/cijena", json={"noci": "abc", "cijena_noci": 80})
    assert r.status_code == 422


def test_nedostaje_polje() -> None:
    r = klijent.post("/cijena", json={"noci": 3})
    assert r.status_code == 422
