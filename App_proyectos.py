import sqlite3

# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect("proyectos_db1.db")
cursor = conn.cursor()

try:
    # Crear tablas
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Proyectos (
         ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_proyecto TEXT NOT NULL,
    entidad TEXT NOT NULL,
    priorizacion TEXT,
    localidad TEXT,
    UPL TEXT,
    numero_predios INTEGER,
    ruta_plano TEXT -- Ruta del archivo del plano
    );

    CREATE TABLE IF NOT EXISTS Predios (
        chip TEXT PRIMARY KEY NOT NULL,
        direccion TEXT,
        area_terreno REAL,
        area_construccion REAL,
        destino_catastral TEXT,
        latitud REAL,
        longitud REAL,
        id_proyecto INTEGER,
        observaciones TEXT,
        FOREIGN KEY (id_proyecto) REFERENCES Proyectos(ID)
    );

    CREATE TABLE IF NOT EXISTS Info_juridica_predios (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        chip TEXT NOT NULL,
        fmi TEXT,
        propietario TEXT,
        observaciones TEXT,
        id_proyecto INTEGER,
        FOREIGN KEY (chip) REFERENCES Predios(chip),
        FOREIGN KEY (id_proyecto) REFERENCES Proyectos(ID)
    );

    CREATE TABLE IF NOT EXISTS Analisis_juridico (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        chip TEXT NOT NULL,
        fmi TEXT,
        fmai_matriz TEXT,
        propietario TEXT,
        titulo_adquisicion TEXT,
        gravamenes_o_limitaciones TEXT,
        observaciones TEXT,
        id_proyecto INTEGER,
        fecha_analisis TEXT DEFAULT (DATE('now')),
        FOREIGN KEY (chip) REFERENCES Predios(chip),
        FOREIGN KEY (id_proyecto) REFERENCES Proyectos(ID)
    );

    CREATE TABLE IF NOT EXISTS Geometria_Predios (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        chip TEXT NOT NULL,
        poligono_geojson TEXT,
        FOREIGN KEY (chip) REFERENCES Predios(chip)
    );
    """)

    # Commit the changes
    conn.commit()
    print("Tablas creadas exitosamente.")

except sqlite3.Error as e:
    print(f"Error al crear las tablas: {e}")

finally:
    # Cerrar la conexión
    conn.close()

import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("proyectos_db1.db")
cursor = conn.cursor()

try:
    # Insertar un proyecto
    cursor.execute("""
        INSERT INTO Proyectos (nombre_proyecto, entidad, priorizacion, localidad, UPL, numero_predios, ruta_plano)
        VALUES ('Proyecto A', 'Entidad X', 'Alta', 'Localidad 1', 'UPL-1', 10, 'ruta/plano_proyectoA.geojson')
    """)

    # Insertar un predio
    cursor.execute("""
        INSERT INTO Predios (chip, direccion, area_terreno, area_construccion, destino_catastral, latitud, longitud, id_proyecto, observaciones)
        VALUES ('CHIP001', 'Calle 10 #20-30', 200.5, 150.0, 'Residencial', 4.6097, -74.0817, 1, 'Predio en revisión')
    """)

    # Insertar información jurídica del predio
    cursor.execute("""
        INSERT INTO Info_juridica_predios (chip, fmi, propietario, observaciones, id_proyecto)
        VALUES ('CHIP001', 'FMI12345', 'Juan Pérez', 'Sin observaciones', 1)
    """)

    # Insertar análisis jurídico
    cursor.execute("""
        INSERT INTO Analisis_juridico (chip, fmi, fmai_matriz, propietario, titulo_adquisicion, gravamenes_o_limitaciones, observaciones, id_proyecto)
        VALUES ('CHIP001', 'FMI12345', 'FMAI6789', 'Juan Pérez', 'Compraventa', 'Hipoteca', 'Revisión en proceso', 1)
    """)

    # Insertar geometría del predio
    cursor.execute("""
        INSERT INTO Geometria_Predios (chip, poligono_geojson)
        VALUES ('CHIP001', '{"type": "Polygon", "coordinates": [[[4.6097, -74.0817], [4.6100, -74.0820], [4.6095, -74.0825], [4.6097, -74.0817]]]}')
    """)

    # Confirmar cambios
    conn.commit()
    print("✅ Datos insertados correctamente.")

except sqlite3.Error as e:
    print(f"❌ Error al insertar datos: {e}")

finally:
    conn.close()

