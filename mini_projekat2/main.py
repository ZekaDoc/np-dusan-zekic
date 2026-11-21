from ml_okvir import (
    Accuracy,
    F1Macro,
    IrisEksperiment,
    KonzolniPosmatrac,
)


def main() -> None:
    for naziv_modela in ("logisticki", "stablo", "knn"):
        for metrika in (Accuracy(), F1Macro()):
            print("\n" + "=" * 50)

            eksperiment = IrisEksperiment(
                naziv_modela=naziv_modela,
                metrika=metrika,
            )

            eksperiment.pretplati(KonzolniPosmatrac())
            rezultat = eksperiment.pokreni()

            print(f"Model: {rezultat['model']}")
            print(f"Metrika: {rezultat['metrika']}")
            print(f"Rezultat: {rezultat['rezultat']:.4f}")
            print(f"Vrijeme: {rezultat['vrijeme_sekunde']:.6f} sekundi")


if __name__ == "__main__":
    main()
