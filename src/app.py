from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
from modelo.MovilidadModel import MovilidadModel

app = Flask(__name__)


CORS(app, resources={r"/movilidad/*": {"origins": "https://proyecto-modulo3.onrender.com"}})

# Configuración de la base de datos
app.config.from_object(config['development'])

# RUTA PARA PETICION GET listar movilidad
@app.route('/movilidad', methods=['GET'])
def listar_movilidad():
    return MovilidadModel.listar_movilidad()

# RUTA PARA PETICION GET movilidad específica por placa
@app.route('/movilidad/<placa>', methods=['GET'])
def lista_movilidad(placa):
    return MovilidadModel.listar_movilidad_especifica(placa)

# RUTA PARA PETICION POST insertar movilidad
@app.route('/movilidad', methods=['POST'])
def registrar_movilidad():
    return MovilidadModel.registrar_movilidad()

# RUTA PARA PETICION DELETE borrar movilidad
@app.route('/movilidad/<placa>', methods=['DELETE'])
def eliminar_movilidad(placa):
    return MovilidadModel.eliminar_movilidad(placa)

# RUTA PARA PETICION PUT actualizar movilidad
@app.route('/movilidad/<placa>', methods=['PUT'])
def actualizar_movilidad(placa):
    return MovilidadModel.actualizar_movilidad(placa)

# Capturar error de página
def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', debug=True)
