import pytest

from ml_okvir import (
    Accuracy,
    F1Macro,
    IrisEksperiment,
    ModelFactory,
    mjeri_vrijeme,
)


@pytest.mark.parametrize(
    "naziv",
    ["logisticki", "stablo", "knn"],
)
def test_factory_kreira_model(naziv):
    model = ModelFactory.kreiraj(naziv)

    assert callable(model.fit)
    assert callable(model.predict)


def test_factory_nepoznat_model():
    with pytest.raises(ValueError, match="Nepoznat model"):
        ModelFactory.kreiraj("nepostojeci")


def test_factory_vraca_nove_instance():
    prvi = ModelFactory.kreiraj("stablo")
    drugi = ModelFactory.kreiraj("stablo")

    assert prvi is not drugi


def test_accuracy():
    metrika = Accuracy()

    rezultat = metrika.izracunaj(
        [0, 1, 2, 2],
        [0, 1, 1, 2],
    )

    assert rezultat == pytest.approx(0.75)


def test_f1_macro():
    metrika = F1Macro()

    rezultat = metrika.izracunaj(
        [0, 0, 1, 1],
        [0, 1, 1, 1],
    )

    assert rezultat == pytest.approx(11 / 15)


def test_observer_prima_dogadjaje():
    class MemorijskiPosmatrac:
        def __init__(self):
            self.dogadjaji = []

        def obavijesti(self, dogadjaj, podaci):
            self.dogadjaji.append(dogadjaj)

    posmatrac = MemorijskiPosmatrac()
    eksperiment = IrisEksperiment("stablo", Accuracy())
    eksperiment.pretplati(posmatrac)

    eksperiment.pokreni()

    assert posmatrac.dogadjaji == [
        "pocetak_eksperimenta",
        "pocetak_treninga",
        "kraj_treninga",
        "kraj_eksperimenta",
    ]


def test_dekorator_cuva_rezultat_i_dodaje_vrijeme():
    @mjeri_vrijeme
    def primjer():
        return {"rezultat": 123}

    rezultat = primjer()

    assert rezultat["rezultat"] == 123
    assert rezultat["vrijeme_sekunde"] >= 0
    assert primjer.__name__ == "primjer"


@pytest.mark.parametrize(
    "naziv",
    ["logisticki", "stablo", "knn"],
)
def test_iris_eksperiment(naziv):
    eksperiment = IrisEksperiment(naziv, Accuracy())

    rezultat = eksperiment.pokreni()

    assert rezultat["model"] == naziv
    assert rezultat["metrika"] == "accuracy"
    assert 0 <= rezultat["rezultat"] <= 1
    assert rezultat["vrijeme_sekunde"] >= 0


def test_metrika_se_moze_zamijeniti():
    eksperiment = IrisEksperiment("stablo", Accuracy())
    prvi = eksperiment.pokreni()

    eksperiment.metrika = F1Macro()
    drugi = eksperiment.pokreni()

    assert prvi["metrika"] == "accuracy"
    assert drugi["metrika"] == "f1_macro"
