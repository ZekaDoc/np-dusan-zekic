from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import Any, ClassVar, Protocol

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


# FACTORY
class ModelFactory:
    REGISTAR: ClassVar[dict[str, Callable[[], Any]]] = {
        "logisticki": lambda: make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000, random_state=42),
        ),
        "stablo": lambda: DecisionTreeClassifier(random_state=42),
        "knn": lambda: make_pipeline(
            StandardScaler(),
            KNeighborsClassifier(n_neighbors=5),
        ),
    }

    @classmethod
    def kreiraj(cls, naziv: str) -> Any:
        if naziv not in cls.REGISTAR:
            raise ValueError(f"Nepoznat model: {naziv}")

        return cls.REGISTAR[naziv]()


# STRATEGY
class Metrika(Protocol):
    naziv: str

    def izracunaj(self, stvarno: Any, predikcije: Any) -> float: ...


class Accuracy:
    naziv = "accuracy"

    def izracunaj(self, stvarno: Any, predikcije: Any) -> float:
        return float(accuracy_score(stvarno, predikcije))


class F1Macro:
    naziv = "f1_macro"

    def izracunaj(self, stvarno: Any, predikcije: Any) -> float:
        return float(
            f1_score(
                stvarno,
                predikcije,
                average="macro",
                zero_division=0,
            )
        )


# OBSERVER
class Posmatrac(Protocol):
    def obavijesti(
        self,
        dogadjaj: str,
        podaci: dict[str, Any],
    ) -> None: ...


class KonzolniPosmatrac:
    def obavijesti(
        self,
        dogadjaj: str,
        podaci: dict[str, Any],
    ) -> None:
        print(f"[{dogadjaj}] {podaci}")


# DECORATOR
def mjeri_vrijeme(funkcija):
    @wraps(funkcija)
    def omotac(*args, **kwargs):
        pocetak = perf_counter()
        rezultat = funkcija(*args, **kwargs)
        trajanje = perf_counter() - pocetak

        return {
            **rezultat,
            "vrijeme_sekunde": trajanje,
        }

    return omotac


# TEMPLATE METHOD
class Eksperiment(ABC):
    def __init__(
        self,
        naziv_modela: str,
        metrika: Metrika,
    ) -> None:
        self.naziv_modela = naziv_modela
        self.metrika = metrika
        self.posmatraci: list[Posmatrac] = []

    def pretplati(self, posmatrac: Posmatrac) -> None:
        self.posmatraci.append(posmatrac)

    def objavi(self, dogadjaj: str, **podaci: Any) -> None:
        for posmatrac in self.posmatraci:
            posmatrac.obavijesti(dogadjaj, dict(podaci))

    @mjeri_vrijeme
    def pokreni(self) -> dict[str, Any]:
        self.objavi(
            "pocetak_eksperimenta",
            model=self.naziv_modela,
        )

        x, y = self.ucitaj()
        x_train, x_test, y_train, y_test = self.pripremi(x, y)

        model = ModelFactory.kreiraj(self.naziv_modela)

        self.objavi("pocetak_treninga")
        model.fit(x_train, y_train)
        self.objavi("kraj_treninga")

        predikcije = model.predict(x_test)
        rezultat = self.metrika.izracunaj(y_test, predikcije)

        self.objavi(
            "kraj_eksperimenta",
            metrika=self.metrika.naziv,
            rezultat=rezultat,
        )

        return {
            "model": self.naziv_modela,
            "metrika": self.metrika.naziv,
            "rezultat": rezultat,
        }

    @abstractmethod
    def ucitaj(self) -> tuple[Any, Any]: ...

    def pripremi(
        self,
        x: Any,
        y: Any,
    ) -> tuple[Any, Any, Any, Any]:
        return train_test_split(
            x,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y,
        )


class IrisEksperiment(Eksperiment):
    def ucitaj(self) -> tuple[Any, Any]:
        return load_iris(return_X_y=True)
