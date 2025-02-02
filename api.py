from fastapi import FastAPI
import sqlite3

app = FastAPI()


# Conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect("proyectos_db1.db")
    conn.row_factory = sqlite3.Row  # Permite acceder a los datos como diccionarios
    return conn

# Endpoint para probar que la API funciona
@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente"}

# Endpoint para obtener todos los proyectos
@app.get("/proyectos")
def get_proyectos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Proyectos")
    proyectos = cursor.fetchall()
    conn.close()
    return {"proyectos": [dict(proyecto) for proyecto in proyectos]}

# Endpoint para obtener todos los predios
@app.get("/predios")
def get_predios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Predios")
    predios = cursor.fetchall()
    conn.close()
    return {"predios": [dict(predio) for predio in predios]}

# Endpoint para obtener predios de un proyecto específico
@app.get("/predios/{id_proyecto}")
def get_predios_por_proyecto(id_proyecto: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Predios WHERE id_proyecto = ?", (id_proyecto,))
    predios = cursor.fetchall()
    conn.close()
    return {"predios": [dict(predio) for predio in predios]}

from pydantic import BaseModel

# Modelo para recibir datos de proyectos
class Proyecto(BaseModel):
    nombre_proyecto: str
    entidad: str
    priorizacion: str
    localidad: str
    UPL: str
    numero_predios: int
    ruta_plano: str

# Endpoint para insertar un nuevo proyecto
@app.post("/proyectos")
def crear_proyecto(proyecto: Proyecto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Proyectos (nombre_proyecto, entidad, priorizacion, localidad, UPL, numero_predios, ruta_plano) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (proyecto.nombre_proyecto, proyecto.entidad, proyecto.priorizacion, proyecto.localidad,
          proyecto.UPL, proyecto.numero_predios, proyecto.ruta_plano))
    conn.commit()
    conn.close()
    return {"mensaje": "Proyecto creado exitosamente"}

# Modelo para recibir datos de predios
class Predio(BaseModel):
    chip: str
    direccion: str
    area_terreno: float
    area_construccion: float
    destino_catastral: str
    latitud: float
    longitud: float
    observaciones: str
    id_proyecto: int

# Endpoint para insertar un nuevo predio
@app.post("/predios")
def crear_predio(predio: Predio):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Predios (chip, direccion, area_terreno, area_construccion, destino_catastral, 
                             latitud, longitud, observaciones, id_proyecto) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (predio.chip, predio.direccion, predio.area_terreno, predio.area_construccion,
          predio.destino_catastral, predio.latitud, predio.longitud, predio.observaciones,
          predio.id_proyecto))
    conn.commit()
    conn.close()
    return {"mensaje": "Predio creado exitosamente"}

from pydantic import BaseModel
from typing import Optional
import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Modelo Pydantic para recibir datos
class ProyectoUpdate(BaseModel):
    nombre_proyecto: Optional[str] = None
    entidad: Optional[str] = None
    priorizacion: Optional[str] = None
    localidad: Optional[str] = None
    UPL: Optional[str] = None
    numero_predios: Optional[int] = None
    ruta_plano: Optional[str] = None

@app.put("/proyectos/{id}")

def actualizar_proyecto(id: int, proyecto: ProyectoUpdate):
    conn = sqlite3.connect("proyectos_db1.db")
    cursor = conn.cursor()

    # Verificar si el proyecto existe
    cursor.execute("SELECT * FROM Proyectos WHERE ID = ?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Actualizar solo los campos proporcionados
    campos = {key: value for key, value in proyecto.dict().items() if value is not None}
    if not campos:
        conn.close()
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")

    set_clause = ", ".join([f"{campo} = ?" for campo in campos.keys()])
    valores = list(campos.values()) + [id]

    cursor.execute(f"UPDATE Proyectos SET {set_clause} WHERE ID = ?", valores)
    conn.commit()
    conn.close()

    return {"message": "Proyecto actualizado correctamente"}

class PredioUpdate(BaseModel):
    direccion: Optional[str] = None
    area_terreno: Optional[float] = None
    area_construccion: Optional[float] = None
    destino_catastral: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    observaciones: Optional[str] = None

@app.put("/predios/{chip}")
def actualizar_predio(chip: str, predio: PredioUpdate):
    conn = sqlite3.connect("proyectos_db1.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Predios WHERE chip = ?", (chip,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Predio no encontrado")

    campos = {key: value for key, value in predio.dict().items() if value is not None}
    if not campos:
        conn.close()
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")

    set_clause = ", ".join([f"{campo} = ?" for campo in campos.keys()])
    valores = list(campos.values()) + [chip]

    cursor.execute(f"UPDATE Predios SET {set_clause} WHERE chip = ?", valores)
    conn.commit()
    conn.close()

    return {"message": "Predio actualizado correctamente"}

@app.delete("/proyectos/{id}")
def eliminar_proyecto(id: int):
    conn = sqlite3.connect("proyectos_db1.db")
    cursor = conn.cursor()

    # Verificar si hay predios asociados
    cursor.execute("SELECT * FROM Predios WHERE id_proyecto = ?", (id,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="No se puede eliminar el proyecto, tiene predios asociados")

    cursor.execute("DELETE FROM Proyectos WHERE ID = ?", (id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    conn.commit()
    conn.close()

    return {"message": "Proyecto eliminado correctamente"}

@app.delete("/predios/{chip}")
def eliminar_predio(chip: str):
    conn = sqlite3.connect("proyectos_db1.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Predios WHERE chip = ?", (chip,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Predio no encontrado")

    conn.commit()
    conn.close()

    return {"message": "Predio eliminado correctamente"}


# Ejecutar la API con Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)