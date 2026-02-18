from uuid import UUID

from pydantic import BaseModel


class ProfileCreate(BaseModel):
    name: str


class ProfileUpdate(BaseModel):
    id: UUID
    name: str | None = None


class ProfileResponse(BaseModel):
    id: UUID
    name: str

    # Pydantic v2 Einstellung: erlaubt Modelle aus Objekt-Attributen zu erzeugen.
    # Wenn `from_attributes` auf True gesetzt ist, kann `ProfileResponse`
    # direkt aus einem Objekt (z. B. einer SQLAlchemy-Instanz) erstellt
    # werden, das Attribute wie `id` und `name` besitzt. Das ist nützlich,
    # wenn du ORM-Objekte als Antwort zurückgeben möchtest, ohne sie
    # vorher in ein Dict zu konvertieren. Entspricht grob `orm_mode = True`
    # in Pydantic v1.
    model_config = {"from_attributes": True}
