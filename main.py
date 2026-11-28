from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Rezervacije API")


class ZahtjevCijene(BaseModel):
    noci: int = Field(ge=1, le=30)
    cijena_noci: float = Field(gt=0, le=10000)
    popust: float = Field(default=0.0, ge=0.0, le=1.0)


class OdgovorCijene(BaseModel):
    iznos: float


@app.post("/cijena", response_model=OdgovorCijene)
def izracunaj(z: ZahtjevCijene) -> OdgovorCijene:
    iznos = z.noci * z.cijena_noci * (1 - z.popust)
    return OdgovorCijene(iznos=round(iznos, 2))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
