# Imports
from flask import Flask, render_template,request,jsonify
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
import os
import tempfile

#Instancia de la app web
app = Flask(__name__)

# Configuracion del peso de las imagenes
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

data_global = None


# funciones para el modelo
def predecir():
    return

















""" FUNCIONES PARA GENERAR RECORTES DE LAS IMAGENES EN 3D  
    funciones auxiliares para los recortes y la generacion de las
    imagenes
"""
def generar_cortes(file):
    filename = file.filename
    if filename.endswith('.nii.gz'):
        suffix = '.nii.gz'
    elif filename.endswith('.nii'):
        suffix = '.nii'
    else:
        raise ValueError("Formatoinvalido")
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        file.save(tmp)
        tmp_path = tmp.name
    nifti_img = nib.load(tmp_path)
    data = nifti_img.get_fdata()
    os.remove(tmp_path)
    return data

def generar_corte_sagital(data, n):
    x, _, _ = data.shape
    indice = max(0, min(n, x - 1))
    return data[indice, :, :]

def generar_corte_coronal(data, n):
    _, y, _ = data.shape
    indice = max(0, min(n, y - 1))
    return data[:, indice, :]

def generar_corte_axial(data, n):
    _, _, z = data.shape
    indice = max(0, min(n, z - 1))
    return data[:, :, indice]

def corte_a_base64(corte, titulo):
    fig, eje = plt.subplots(1, 1, figsize=(6, 6))
    eje.imshow(corte.T, cmap='gray', origin='lower')
    eje.set_title(titulo)
    eje.axis('off')
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close(fig)
    return base64.b64encode(buffer.read()).decode('utf-8')



"""  PAGINA PRINCIPAL INDEX.HTML EN RAIZ  """
@app.route("/", methods=['GET','POST'])
def inicio():
    return render_template('index.html')



"""  PAGINA MOSTRADA CUANDO SE LE DA AL BOTON VER EN /ver  """
@app.route('/ver', methods=['GET', 'POST'])
def ver():
    file = request.files['imagen_subida']
    data = generar_cortes(file)
    global data_global
    data_global = data

    x,y,z = data.shape

    #CORTE SAGITAL
    frame_sagital = x//2
    corte_sagital = generar_corte_sagital(data, frame_sagital)
    #CORTE CORONAL
    frame_coronal = y//2
    corte_coronal = generar_corte_coronal(data, frame_coronal)
    #CORTE AXIAL
    frame_axial = z//2
    corte_axial = generar_corte_axial(data, frame_axial)

    imagen_base64_sagital = corte_a_base64(corte_sagital, "Sagital")
    imagen_base64_coronal = corte_a_base64(corte_coronal, "Coronal")
    imagen_base64_axial = corte_a_base64(corte_axial, "Axial")

    return render_template('ver.html', 
                           imagen_sagital = imagen_base64_sagital, 
                           imagen_coronal = imagen_base64_coronal, 
                           imagen_axial = imagen_base64_axial,
                           max_sagital = x,
                           max_coronal = y,
                           max_axial = z,
                           inicio_sagital = x//2,
                           inicio_coronal = y//2,
                           inicio_axial = z//2,
                           )

@app.route("/slider_sagital", methods=["POST"])
def recibir_slider_sagital():
    datos = request.get_json()
    if not datos or "intensidad" not in datos:
        return jsonify({ "error": "Dato faltante" }), 400
    intensidad = int(datos["intensidad"])
    print(f"Frame Sagital: {intensidad}")
    frame_sagital = intensidad
    corte_sagital = generar_corte_sagital(data_global, frame_sagital)
    imagen_base64 = corte_a_base64(corte_sagital, "Sagital")
    return jsonify({ "imagen": imagen_base64, "intensidad": intensidad })

@app.route("/slider_coronal", methods=["POST"])
def recibir_slider_coronal():
    datos = request.get_json()
    if not datos or "intensidad" not in datos:
        return jsonify({ "error": "Dato faltante" }), 400
    intensidad = int(datos["intensidad"])
    print(f"Frame Coronal: {intensidad}")
    frame_coronal = intensidad
    corte_coronal = generar_corte_coronal(data_global, frame_coronal)
    imagen_base64 = corte_a_base64(corte_coronal, "Coronal")
    return jsonify({ "imagen": imagen_base64, "intensidad": intensidad })

@app.route("/slider_axial", methods=["POST"])
def recibir_slider_axial():
    datos = request.get_json()
    if not datos or "intensidad" not in datos:
        return jsonify({ "error": "Dato faltante" }), 400
    intensidad = int(datos["intensidad"])
    print(f"Frame Axial: {intensidad}")
    frame_axial = intensidad
    corte_axial = generar_corte_axial(data_global, frame_axial)
    imagen_base64 = corte_a_base64(corte_axial, "Axial")
    return jsonify({ "imagen": imagen_base64, "intensidad": intensidad })




@app.route("/descargar", methods=["POST"])
def descargar():
    if data_global is None:
        return "No hay imagen cargada", 400
    ruta_base = os.path.abspath(__file__)
    base_dir = os.path.dirname(ruta_base)

    ruta_descarga = os.path.join(base_dir, "frames_recortados")
    os.makedirs(ruta_descarga, exist_ok=True)

    ruta_descarga_sagital = os.path.join(ruta_descarga, "cortes_sagitales")
    ruta_descarga_coronal = os.path.join(ruta_descarga, "cortes_coronales")
    ruta_descarga_axial = os.path.join(ruta_descarga, "cortes_axiales")

    os.makedirs(ruta_descarga_sagital, exist_ok=True)
    os.makedirs(ruta_descarga_coronal, exist_ok=True)
    os.makedirs(ruta_descarga_axial, exist_ok=True)

    for i in range(data_global.shape[0]):
        corte_sagital = generar_corte_sagital(data_global, i)
        ruta_corte_sagital = os.path.join(ruta_descarga_sagital, f"corte_sagital_{i}.png")
        plt.imsave(ruta_corte_sagital, corte_sagital.T, cmap='gray', origin='lower')
    for i in range(data_global.shape[1]):
        corte_coronal = generar_corte_coronal(data_global, i)
        ruta_corte_coronal = os.path.join(ruta_descarga_coronal, f"corte_coronal_{i}.png")
        plt.imsave(ruta_corte_coronal, corte_coronal.T, cmap='gray', origin='lower')
    for i in range(data_global.shape[2]):
        corte_axial = generar_corte_axial(data_global, i)
        ruta_corte_axial = os.path.join(ruta_descarga_axial, f"corte_axial_{i}.png")
        plt.imsave(ruta_corte_axial, corte_axial.T, cmap='gray', origin='lower')
    return render_template('ver.html')


#Ejecucion
if __name__ == '__main__':
    app.run(debug=True)