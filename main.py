from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="API Barbería - Módulo Catálogo")

# --- MODELOS DE DATOS (Validación de entrada) ---


class BarberoCreate(BaseModel):
    nombre: str = Field(..., min_length=2)
    telefono: str = Field(..., min_length=8)
    especialidad: Optional[str] = None

class ServicioCreate(BaseModel):
    nombre: str = Field(..., min_length=2)
    precio: float = Field(..., gt=0)  # Debe ser mayor a 0
    duracion_minutos: int = Field(..., gt=0)  # Debe ser mayor a 0

# --- BASE DE DATOS TEMPORAL EN MEMORIA ---
barberos_db = []
servicios_db = []

# ================= ENDPOINTS BARBEROS =================

@app.get("/barberos")
def listar_barberos(solo_activos: bool = True):
    if solo_activos:
        return [b for b in barberos_db if b["activo"]]
    return barberos_db

@app.post("/barberos", status_code=201)
def crear_barbero(barbero: BarberoCreate):
    nuevo = {
        "id": len(barberos_db) + 1,
        **barbero.model_dump(),
        "activo": True
    }
    barberos_db.append(nuevo)
    return nuevo

@app.put("/barberos/{barbero_id}")
def editar_barbero(barbero_id: int, datos: BarberoCreate):
    for b in barberos_db:
        if b["id"] == barbero_id:
            b.update(datos.model_dump())
            return b
    raise HTTPException(status_code=404, detail="Barbero no encontrado")

@app.patch("/barberos/{barbero_id}/desactivar")
def desactivar_barbero(barbero_id: int):
    for b in barberos_db:
        if b["id"] == barbero_id:
            b["activo"] = False
            return {"mensaje": f"Barbero {b['nombre']} desactivado", "data": b}
    raise HTTPException(status_code=404, detail="Barbero no encontrado")

# ================= ENDPOINTS SERVICIOS =================

@app.get("/servicios")
def listar_servicios(solo_activos: bool = True):
    if solo_activos:
        return [s for s in servicios_db if s["activo"]]
    return servicios_db

@app.post("/servicios", status_code=201)
def crear_servicio(servicio: ServicioCreate):
    nuevo = {
        "id": len(servicios_db) + 1,
        **servicio.model_dump(),
        "activo": True
    }
    servicios_db.append(nuevo)
    return nuevo

@app.put("/servicios/{servicio_id}")
def editar_servicio(servicio_id: int, datos: ServicioCreate):
    for s in servicios_db:
        if s["id"] == servicio_id:
            s.update(datos.model_dump())
            return s
    raise HTTPException(status_code=404, detail="Servicio no encontrado")

@app.patch("/servicios/{servicio_id}/desactivar")
def desactivar_servicio(servicio_id: int):
    for s in servicios_db:
        if s["id"] == servicio_id:
            s["activo"] = False
            return {"mensaje": f"Servicio {s['nombre']} desactivado", "data": s}
    raise HTTPException(status_code=404, detail="Servicio no encontrado")