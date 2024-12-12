from flask import jsonify, request
from modelo.coneccion import db_connection

# Función que busca una movilidad por placa
def buscar_movilidad(placa):
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT placa, marca, modelo, n_chasis, tipo_mov, propietario
            FROM movilidad WHERE placa = %s
        """, (placa,))
        datos = cur.fetchone()
        conn.close()
        if datos:
            movilidad = {
                'placa': datos[0], 
                'marca': datos[1], 
                'modelo': datos[2],
                'n_chasis': datos[3], 
                'tipo_mov': datos[4], 
                'propietario': datos[5]
            }
            return movilidad
        else:
            return None
    except Exception as ex:
        raise ex

class MovilidadModel:
    @classmethod
    def listar_movilidad(cls):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT placa, marca, modelo, n_chasis, tipo_mov, propietario 
                FROM movilidad
            """)
            datos = cur.fetchall()
            movilidad = []
            for fila in datos:
                movilidad.append({
                    'placa': fila[0], 
                    'marca': fila[1], 
                    'modelo': fila[2], 
                    'n_chasis': fila[3],
                    'tipo_mov': fila[4], 
                    'propietario': fila[5]
                })
            conn.close()
            return jsonify({'movilidad': movilidad, 'mensaje': "Movilidades listadas.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error al listar movilidades", 'exito': False})

    @classmethod
    def listar_movilidad_especifica(cls, placa):
        try:
            movilidad = buscar_movilidad(placa)
            if movilidad:
                return jsonify({'movilidad': movilidad, 'mensaje': "Movilidad encontrada.", 'exito': True})
            else:
                return jsonify({'mensaje': "Movilidad no encontrada.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error al buscar movilidad", 'exito': False})

    @classmethod
    def registrar_movilidad(cls):
        try:
            placa = request.json['placa']
            movilidad = buscar_movilidad(placa)
            if movilidad:
                return jsonify({'mensaje': "Placa ya registrada, no se puede duplicar.", 'exito': False})
            else:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO movilidad (placa, marca, modelo, n_chasis, tipo_mov, propietario)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    request.json['placa'],
                    request.json['marca'],
                    request.json['modelo'],
                    request.json['n_chasis'],
                    request.json['tipo_mov'],
                    request.json['propietario']
                ))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Movilidad registrada.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error al registrar movilidad", 'exito': False})

    @classmethod
    def eliminar_movilidad(cls, placa):
        try:
            movilidad = buscar_movilidad(placa)
            if movilidad:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM movilidad WHERE placa = %s", (placa,))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Movilidad eliminada.", 'exito': True})
            else:
                return jsonify({'mensaje': "Movilidad no encontrada.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error al eliminar movilidad", 'exito': False})

    @classmethod
    def actualizar_movilidad(cls, placa):
        try:
            movilidad = buscar_movilidad(placa)
            if movilidad:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("""
                    UPDATE movilidad SET marca=%s, modelo=%s, n_chasis=%s, tipo_mov=%s, propietario=%s
                    WHERE placa=%s
                """, (
                    request.json['marca'],
                    request.json['modelo'],
                    request.json['n_chasis'],
                    request.json['tipo_mov'],
                    request.json['propietario'],
                    placa
                ))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Movilidad actualizada.", 'exito': True})
            else:
                return jsonify({'mensaje': "Movilidad no encontrada.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error al actualizar movilidad", 'exito': False})
