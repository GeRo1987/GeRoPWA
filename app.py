from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, jsonify
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import datetime
from flask import session
from google.cloud import storage
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from openpyxl import load_workbook
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from firebase_admin import credentials, initialize_app, storage
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask import Flask, render_template, flash, request, redirect, url_for, session
import requests
import json
import io
import math
import locale
import requests
import os
import random
import string
import logging
import re
import ssl
import google.auth
import smtplib
from flask import Flask
from flask_talisman import Talisman
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from flask import Flask, request, jsonify
import subprocess



app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Resto de tu código aquí...


logging.basicConfig(level=logging.INFO)
SERVICE_ACCOUNT_FILE = "G:/Mi unidad/GeRo/German/GEROPWA/prod-imagen-firebase-adminsdk-m3n48-825aaa603b.json"
from google.oauth2 import service_account

# Define el alcance (scope) que necesitas
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# Usa las credenciales en tu aplicación
cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

cred = credentials.Certificate("G:/Mi unidad/GeRo/German/GEROPWA/prod-imagen-firebase-adminsdk-m3n48-825aaa603b.json")
initialize_app(cred, {'storageBucket': 'prod-imagen.appspot.com'})

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# ID de la hoja de cálculo (extraído del enlace proporcionado)
SPREADSHEET_ID = '10TtIug4WTOA0wHhfT_3io4q40yxuHHRj'

service = build('sheets', 'v4', credentials=credentials)


#BORRAR
def subir_imagen_drive(imagen):
    # Lógica para subir la imagen a Google Drive y obtener la URL
    # Esta función debe estar implementada correctamente
    return "https://drive.google.com/uc?id=tu_id_de_imagen"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Cambia esto por una clave secreta segura

@app.route('/user_servicios')
def user_servicios():
    nombre = request.args.get('nombre')
    if nombre:
        return render_template('servicios.html', nombre=nombre)
    else:
        return "Nombre de usuario no proporcionado", 400


# Función para sanitizar entradas de texto
def sanitize_input(text):
    return re.sub(r'[^\w\s]', '', text)  # Eliminar caracteres especiales, excepto letras, números y espacios

# verificacion horario de atencion
def is_open(horarios):
    current_time = datetime.now().time()
    try:
        horario_inicio, horario_fin = horarios.split('-')
        horario_inicio = datetime.strptime(horario_inicio, '%H:%M').time()
        horario_fin = datetime.strptime(horario_fin, '%H:%M').time()

        if horario_inicio <= current_time <= horario_fin:
            return True
    except ValueError:
        pass
    return False

# cobertir a mayusuculas
def to_uppercase(data):
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, dict):
        return {k: to_uppercase(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_uppercase(i) for i in data]
    else:
        return data

# Configurar el registro de errores
logging.basicConfig(filename='error.log', level=logging.DEBUG)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'  # Cambia esto por tu correo
app.config['MAIL_PASSWORD'] = 'tu_contraseña'        # Cambia esto por tu contraseña

mail = Mail(app)

# Establece la configuración regional a la de tu país, por ejemplo, 'es_CO' para Colombia
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}, route: {request.url}')
    return "Internal server error", 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error(f'Unhandled Exception: {e}, route: {request.url}')
    return "Something went wrong", 500

def generar_codigo_seguimiento(consecutivo):
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f'GERO-{consecutivo}-{random_part}'

# Definición de Formularios
class ProductForm(FlaskForm):
    name = StringField('Nombre del Producto', validators=[Optional()])
    price = DecimalField('Precio de Venta por Unidad (Ej: Precio de Venta del Producto)', validators=[Optional(), NumberRange(min=0)])
    variable_cost = DecimalField('Costo Variable por Unidad (Ej: Materias Primas del Producto)', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Calcular Punto de Equilibrio')

class FixedCostsForm(FlaskForm):
    fixed_costs = DecimalField('Gastos Fijos Totales Mensuales (Ej: Arriendos, Servicios, Sueldos)', validators=[DataRequired(), NumberRange(min=0)])

class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    subject = StringField('Asunto', validators=[DataRequired()])
    message = TextAreaField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/static/<path:filename>')
def serve_static(filename):
    try:
        return send_from_directory(os.path.join(app.root_path, 'static'), filename)
    except Exception as e:
        app.logger.error(f"Error al servir archivo estático: {str(e)}")
        return "Archivo no encontrado", 404

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'service-worker.js')

@app.route('/terminos.html')
def terminos():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'terminos.html')

@app.route('/politica.html')
def politica():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'politica.html')

@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    celular = request.form['celular']
    correo = request.form['correo']
    
    data = {
        "nombre": nombre,
        "celular": celular,
        "correo": correo
    }
    
    tag = f"{celular}"
    response = requests.put(f'https://domi-usuarios.firebaseio.com/{tag}.json', json=data)
    
    if response.status_code == 200:
        flash('Registrado exitosamente')
    else:
        flash('Error al registrar usuario')
    
    return redirect(url_for('index'))

@app.route('/ingreso', methods=['POST'])
def ingreso():
    nombre = request.form['nombre']
    app.logger.info(f'Nombre ingresado: {nombre}')
    try:
        response = requests.get('https://domi-usuarios.firebaseio.com/.json')
        response.raise_for_status()
        usuarios = response.json()
        app.logger.debug(f'Usuarios obtenidos: {usuarios}')

        if usuarios is None:
            flash('No se pudo obtener los datos de los usuarios.')
            return redirect(url_for('index'))

        for key, usuario in usuarios.items():
            app.logger.debug(f"Verificando usuario: {usuario}")
            if usuario.get('nombre') == nombre:
                app.logger.info(f'Usuario encontrado: {usuario}')
                return redirect(url_for('user_servicios', nombre=nombre))
        flash('Usuario no encontrado')
    except requests.exceptions.RequestException as e:
        app.logger.error(f'Error al obtener usuarios: {e}')
        flash('Error al obtener usuarios. Por favor, intenta de nuevo.')
    return redirect(url_for('index'))

# Configurar el registro de errores
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Definir los precios de los servicios sin paréntesis
precios_servicios = {
    "GeRo ultima milla proximamente envios desde 3 kg hasta 30 kg y hasta 50cm por lado dentro de la misma localidad o municipio": 6000,
    "GeRo Carga proximamente transporte de mercancias de mayores dimensiones en vehiculos de carga mudanzas y demas": "COTIZAR FLETE",
    "GeRo Express restaurantes comidas a domicilio productos de hasta 3 kg": 4000,
    "GeRo paqueteria proximamente servicio ideal para tiendas en linea": 9000
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def formulario():
    return '''
        <form method="post" action="/publicar_producto" enctype="multipart/form-data">
            Ciudad: <input type="text" name="ciudad"><br>
            Barrio: <input type="text" name="barrio"><br>
            Tipo de Negocio: <input type="text" name="tipo_negocio"><br>
            Codigo de Validación: <input type="text" name="codigo_validacion"><br>
            Nombre Negocio: <input type="text" name="nombre_negocio"><br>
            Dirección: <input type="text" name="direccion"><br>
            Teléfono: <input type="text" name="telefono"><br>
            Contacto: <input type="text" name="contacto"><br>
            Correo: <input type="text" name="correo"><br>
            Horarios: <input type="text" name="horarios"><br>
            Imagen Negocio: <input type="file" name="imagen_negocio"><br>
            Nombre Producto: <input type="text" name="nombre_producto"><br>
            Precio: <input type="text" name="precio"><br>
            Imagen Producto: <input type="file" name="imagen_producto"><br>
            <input type="submit">
        </form>
    '''


@app.route('/servicio_rastrea', methods=['GET', 'POST'])
def servicio_rastrea():
    if request.method == 'POST':
        codigo_seguimiento = request.form['codigo_seguimiento']
        # Obtener los datos del pedido desde Firebase
        url = f'https://pedidos-a1b94.firebaseio.com/solicitudes/{codigo_seguimiento}.json'
        response = requests.get(url)
        pedido = response.json()
        if pedido:
            print(f"Estado del pedido: {pedido.get('estado', 'No se encontró el estado')}")  # Depuración
            pedido['codigo_seguimiento'] = codigo_seguimiento  # Asegurarse de incluir el código de seguimiento en el pedido
            return render_template('rastrea.html', pedido=pedido)
        else:
            flash('No se encontró ningún pedido con ese código de seguimiento.')
            return redirect(url_for('servicio_rastrea'))

    return render_template('rastrea.html')

@app.route('/servicio_equilibrio', methods=['GET', 'POST'])
def servicio_equilibrio():
    product_forms = [ProductForm(prefix=f'form{i}') for i in range(5)]
    fixed_costs_form = FixedCostsForm(prefix='fixed')
    break_even_points = []
    total_break_even_point = 0
    total_daily_sales = 0
    total_monthly_sales_value = 0
    total_daily_sales_value = 0

    if request.method == 'POST':
        valid_data = True
        fixed_costs = None

        if fixed_costs_form.validate_on_submit():
            fixed_costs = fixed_costs_form.fixed_costs.data
        else:
            flash("Por favor, ingrese los gastos fijos totales mensuales.")
            valid_data = False

        total_contribution_margin = 0
        product_data = []

        if fixed_costs is not None:
            for form in product_forms:
                if form.name.data and form.price.data is not None and form.variable_cost.data is not None:
                    if form.price.data > form.variable_cost.data:
                        contribution_margin = form.price.data - form.variable_cost.data
                        total_contribution_margin += contribution_margin
                        product_data.append((form.name.data, form.price.data, form.variable_cost.data, contribution_margin))
                    else:
                        flash(f"El precio de venta debe ser mayor al costo variable para el producto {form.name.data}.")
                        valid_data = False
                elif form.name.data or form.price.data is not None or form.variable_cost.data is not None:
                    flash(f"Faltan datos en el formulario de {form.name.data}. Por favor, completa todos los campos.")
                    valid_data = False

            if total_contribution_margin > 0:
                for name, price, variable_cost, contribution_margin in product_data:
                    participation_percentage = contribution_margin / total_contribution_margin
                    prorated_fixed_costs = fixed_costs * participation_percentage
                    break_even_point = prorated_fixed_costs / contribution_margin
                    daily_sales = break_even_point / 30  # Asumiendo un mes de 30 días
                    monthly_sales_value = break_even_point * price
                    daily_sales_value = daily_sales * price
                    break_even_points.append((name, math.ceil(break_even_point), math.ceil(daily_sales),
                                              f"$ {math.ceil(monthly_sales_value):,}".replace(',', '.'),
                                              f"$ {math.ceil(daily_sales_value):,}".replace(',', '.')))

                total_break_even_point += break_even_point
                total_daily_sales += daily_sales
                total_monthly_sales_value += monthly_sales_value
                total_daily_sales_value += daily_sales_value

            total_break_even_point = math.ceil(total_break_even_point)
            total_daily_sales = math.ceil(total_daily_sales)
            total_monthly_sales_value = f"$ {math.ceil(total_monthly_sales_value):,}".replace(',', '.')
            total_daily_sales_value = f"$ {math.ceil(total_daily_sales_value):,}".replace(',', '.')

        if valid_data and not break_even_points:
            flash("Ingrese al menos un producto con todos los campos completos.")

    return render_template('equilibrio.html', product_forms=product_forms, fixed_costs_form=fixed_costs_form, break_even_points=break_even_points,
                           total_break_even_point=total_break_even_point, total_daily_sales=total_daily_sales,
                           total_monthly_sales_value=total_monthly_sales_value, total_daily_sales_value=total_daily_sales_value)

@app.route('/servicio_contacto', methods=['GET', 'POST'])
def servicio_contacto():
    form = ContactForm()
    if form.validate_on_submit():
        nombre = form.name.data
        asunto = form.subject.data
        mensaje = form.message.data

        msg = Message(asunto, sender='tu_correo@gmail.com', recipients=['app.domi.2020@gmail.com'])
        msg.body = f"Nombre: {nombre}\n\nMensaje: {mensaje}"
        msg.body = msg.body.encode('utf-8')  # Asegúrate de codificar el cuerpo del mensaje en UTF-8

        try:
            mail.send(msg)
            flash('Mensaje enviado exitosamente')
        except Exception as e:
            flash(f'Error al enviar el mensaje: {str(e)}')
            app.logger.error(f'Error al enviar el mensaje: {str(e)}')
        
        return redirect(url_for('index'))
    return render_template('contacto.html', form=form)

@app.route('/enviar_contacto', methods=['GET', 'POST'])
def enviar_contacto():
    form = ContactForm()
    if form.validate_on_submit():
        nombre = form.name.data
        correo = form.subject.data
        mensaje = form.message.data

        msg = Message(
            subject=correo,
            sender='tu_correo@gmail.com',
            recipients=['app.domi.2020@gmail.com']
        )
        msg.body = f"Nombre: {nombre}\n\nCorreo: {correo}\nMensaje: {mensaje}"
        msg.body = msg.body.encode('utf-8')  # Asegúrate de codificar el cuerpo del mensaje en UTF-8

        try:
            mail.send(msg)
            flash('Mensaje enviado exitosamente')
        except Exception as e:
            flash(f'Error al enviar el mensaje: {str(e)}')
            app.logger.error(f'Error al enviar el mensaje: {str(e)}')
        
        return redirect(url_for('index'))
    return render_template('contacto.html', form=form)

@app.route('/servicio_vende')
def servicio_vende():
    if not session.get('codigo_validado'):
        flash('Primero debe validar un código.')
        return redirect(url_for('home'))
    return render_template('ventas.html', ciudades_y_barrios=ciudades_y_barrios)

print("Ruta de trabajo actual:", os.getcwd())

# Lista de ciudades y barrios disponibles
ciudades_y_barrios = {
    "Bogotá": ["Bosa", "Kennedy", "Fontibon", "Suba", "Engativá"],
    "Medellín": ["El Poblado", "Laureles", "Belén", "Envigado", "Sabaneta"],
    "Cali": ["San Antonio", "Granada", "Versalles", "Ciudad Jardín", "El Ingenio"],
    "Barranquilla": ["El Prado", "Alto Prado", "Villa Country", "Riomar", "Boston"],
    "Cartagena": ["Getsemaní", "San Diego", "Crespo", "Castillogrande", "Bocagrande"],
    "Soacha": ["Despensa Leon XII Terreros Prado Rosales El Trebol San Mateo Ciudad Verde Conjuntos terragrande y tibanica Hogar del Sol"],
    "Pereira": ["Centro", "Cuba", "Kennedy", "San Joaquín", "Laureles"],
    "Bucaramanga": ["Cabecera", "Sotomayor", "Alarcón", "Real de Minas", "Cañaveral"],
    "Cúcuta": ["La Libertad", "Caobos", "San Luis", "Quinta Oriental", "El Centro"],
    "Ibagué": ["El Jordán", "La Pola", "La Macarena", "Ambalá", "Cadiz"]
}

# Ruta para validar código
@app.route('/validar_codigo', methods=['POST'])
def validar_codigo():
    codigo_validacion = request.json.get('codigo_validacion')
    response = requests.get(f'https://codigos-791ec.firebaseio.com/{codigo_validacion}.json')
    
    if response.status_code == 200:
        valor = response.json()
        print(f'Debug - Valor obtenido de Firebase: {valor}')  # Mensaje de depuración
        
        if valor:
            session['codigo_validado'] = True
            session['codigo_validacion'] = codigo_validacion
            if valor == 'si':
                session['correo_promotor'] = None
                return jsonify({'success': True, 'correo_promotor': None})
            else:
                session['correo_promotor'] = valor
                return jsonify({'success': True, 'correo_promotor': valor})
    
    return jsonify({'success': False, 'error': 'Código de validación no válido. Por favor, contáctenos.'})



# Función para filtrar valores nulos
def filtrar_valores_nulos(d):
    """ Filtrar los valores nulos en un diccionario """
    if isinstance(d, dict):
        return {k: filtrar_valores_nulos(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        return [filtrar_valores_nulos(v) for v in d if v is not None]
    else:
        return d


@app.route('/publicar_producto', methods=['POST'])
def publicar_producto():
    try:
        ciudad = request.form.get('ciudad')
        barrio = request.form.get('barrio')
        tipo_negocio = request.form.get('tipo_negocio')
        codigo_negocio = request.form.get('codigo_validacion')
        nombre_negocio = request.form.get('nombre_negocio')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        contacto = request.form.get('contacto')
        correo = request.form.get('correo')
        horarios = request.form.get('horarios')
        forma_pago = request.form.get('forma_pago')
        nombre_producto = request.form.get('nombre_producto')
        precio = request.form.get('precio')

        # Obtener el correo del promotor si está en la sesión
        correo_promotor = session.get('correo_promotor', None)

        # Generar un nuevo código de producto
        codigo_producto = generar_codigo_producto(nombre_negocio)
        activado_desactivado = "Activado"

        imagen_negocio = request.files.get('imagen_negocio')
        logo_url = subir_imagen_firebase(imagen_negocio) if imagen_negocio else ''

        imagen_producto = request.files.get('imagen_producto')
        producto_url = subir_imagen_firebase(imagen_producto) if imagen_producto else ''

        datos_producto = {
            codigo_producto: {
                "nombre_producto": nombre_producto,
                "precio": precio,
                "producto_url": producto_url,
                "activado_desactivado": activado_desactivado
            }
        }

        datos_negocio = {
            "ciudad": ciudad,
            "barrio": barrio,
            "tipo_negocio": tipo_negocio,
            "codigo_negocio": codigo_negocio,
            "nombre_negocio": nombre_negocio,
            "direccion": direccion,
            "telefono": telefono,
            "contacto": contacto,
            "correo": correo,
            "horarios": horarios,
            "logo_url": logo_url,
            "forma_pago": forma_pago,
            "correo_promotor": correo_promotor  # Añadir el correo del promotor si aplica
        }

        # Guardar los datos del negocio
        endpoint_negocio = f"{ciudad}/{barrio}/{tipo_negocio}/{codigo_negocio}.json"
        response_negocio = requests.patch(f"https://domi-negocios.firebaseio.com/{endpoint_negocio}", json=datos_negocio)
        if response_negocio.status_code != 200:
            raise Exception(f"Error al guardar los datos del negocio: {response_negocio.status_code} - {response_negocio.text}")

        # Guardar los datos del producto sin duplicación
        endpoint_producto = f"{ciudad}/{barrio}/{tipo_negocio}/{codigo_negocio}/productos/{codigo_producto}.json"
        response_producto = requests.put(f"https://domi-negocios.firebaseio.com/{endpoint_producto}", json=datos_producto[codigo_producto])
        if response_producto.status_code != 200:
            raise Exception(f"Error al guardar los datos del producto: {response_producto.status_code} - {response_producto.text}")

        # Devolver respuesta JSON
        return jsonify(success=True, codigo_producto=codigo_producto)

    except Exception as e:
        return jsonify(success=False, error=str(e))

def generar_codigo_producto(nombre_negocio):
    primera_palabra = nombre_negocio.split()[0].upper()
    numero_aleatorio = random.randint(0, 9999)
    codigo_producto = f"{primera_palabra}{numero_aleatorio:04d}"
    return codigo_producto

# Ruta para subir imágenes
@app.route('/subir_imagen', methods=['POST'])
def subir_imagen_route():
    try:
        imagen = request.files.get('imagen')
        if not imagen:
            return jsonify({"error": "No se proporcionó ninguna imagen"}), 400

        url = subir_imagen_firebase(imagen)
        if url:
            return jsonify({"url": url})
        else:
            return jsonify({"error": "Error al subir la imagen"}), 500
    except Exception as e:
        app.logger.error(f"Error al subir la imagen: {str(e)}")
        return jsonify({"error": str(e)}), 500


def subir_imagen_firebase(imagen):
    bucket = storage.bucket()
    blob = bucket.blob(imagen.filename)
    blob.upload_from_file(imagen.stream)
    blob.make_public()
    return blob.public_url


def guardar_datos_firebase(data, endpoint, merge=False):
    url = f"https://domi-negocios.firebaseio.com/{endpoint}.json"
    if merge:
        response = requests.get(url)
        if response.status_code == 200:
            existing_data = response.json() or {}
            existing_data.update(data)
            response = requests.put(url, json=existing_data)
        else:
            raise Exception(f"Error al obtener datos existentes de Firebase: {response.status_code} - {response.text}")
    else:
        response = requests.put(url, json=data)

    if response.status_code != 200:
        raise Exception(f"Error al guardar los datos en Firebase: {response.status_code} - {response.text}")
    else:
        print("Datos guardados exitosamente en Firebase")

@app.route('/home', methods=['GET'])
def home():
    return render_template('ventas.html', ciudades_y_barrios=ciudades_y_barrios)


@app.route('/cambiar_estado_producto', methods=['POST'])
def cambiar_estado_producto():
    try:
        codigo_producto = request.json.get('codigo_producto')
        ciudad = request.json.get('ciudad')
        barrio = request.json.get('barrio')
        tipo_negocio = request.json.get('tipo_negocio')
        codigo_negocio = request.json.get('codigo_negocio')
        nuevo_estado = request.json.get('activado_desactivado')

        # Construir la ruta del producto en Firebase
        endpoint = f"{ciudad}/{barrio}/{tipo_negocio}/{codigo_negocio}/productos/{codigo_producto}.json"
        url = f"https://domi-negocios.firebaseio.com/{endpoint}"

        # Realizar la solicitud GET para buscar el producto
        response = requests.get(url)
        if response.status_code == 200 and response.json():
            # Producto encontrado, actualizar el estado
            response_actualizar = requests.patch(url, json={"activado_desactivado": nuevo_estado})
            if response_actualizar.status_code == 200:
                return jsonify(success=True, message="Estado del producto actualizado exitosamente")
            else:
                return jsonify(success=False, error=f"Error al actualizar el estado del producto: {response_actualizar.status_code} - {response_actualizar.text}")
        else:
            return jsonify(success=False, error="Producto no encontrado")

    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/compra')
def compra():
    return render_template('compra.html') 

@app.route('/servicio_compra')
def servicio_compra():
    try:
        response = requests.get('https://domi-negocios.firebaseio.com/.json')
        if response.status_code == 200:
            datos = response.json()
            return jsonify(success=True, datos=datos)
        else:
            return jsonify(success=False, error=f"Error al obtener datos de Firebase: {response.status_code}")

    except Exception as e:
        return jsonify(success=False, error=str(e))

def enviar_correo(destinatarios, asunto, cuerpo):
    remitente = 'tu_correo@gmail.com'
    contrasena = 'tu_contrasena'
    
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = ', '.join(destinatarios)
    msg['Subject'] = asunto
    
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, contrasena)
        texto = msg.as_string()
        server.sendmail(remitente, destinatarios, texto)
        server.quit()
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")

@app.route('/enviar-correo', methods=['POST'])
def enviar_correo_endpoint():
    data = request.get_json()
    destinatarios = [data['to'], 'app.domi.2020@gmail.com']  # Agregar copia a app.domi.2020@gmail.com
    if data.get('cc'):
        destinatarios.append(data['cc'])  # Añadir el correo del promotor en CC si está presente
    asunto = data['subject']
    cuerpo = data['text']
    enviar_correo(destinatarios, asunto, cuerpo)
    return jsonify({'mensaje': 'Correo enviado exitosamente'})


@app.route('/servicio_nomina')
def servicio_nomina():
    return render_template('nomina.html')

@app.route('/servicio_administrador')
def servicio_administrador():
    return render_template('administrador.html')

            
@app.route('/servicio_importaciones')
def servicio_importaciones():
    return render_template('importaciones.html')    

@app.route('/servicio_contabilidad')
def servicio_contabilidad():
    return render_template('contabilidad.html')    


@app.route('/servicio_mensagero/<nombre>', methods=['GET', 'POST'])
def servicio_mensagero(nombre):
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            tipo_servicio = request.form['tipo_servicio']
            nombre_solicitante = request.form['nombre_solicitante']
            direccion_recogida = request.form['direccion_recogida']
            celular_recogida = request.form['celular_recogida']
            ciudad = request.form['ciudad']
            cantidad_entregas = int(request.form['cantidad_entregas'])
            
            # Obtener el último consecutivo general
            response = requests.get('https://pedidos-a1b94.firebaseio.com/solicitudes.json')
            pedidos = response.json() or {}
            ultimo_consecutivo = max([int(key.split('-')[1]) for key in pedidos.keys() if 'GERO-' in key], default=0)
            
            codigos_seguimiento = []
            entregas = []
            
            # Procesar cada entrega por separado
            for i in range(1, cantidad_entregas + 1):
                entrega = {
                    'tipo_servicio': tipo_servicio,

                }
                
                # Generar un código de seguimiento único para cada entrega
                ultimo_consecutivo += 1
                codigo_seguimiento = generar_codigo_seguimiento(ultimo_consecutivo)
                entrega['codigo_seguimiento'] = codigo_seguimiento
                codigos_seguimiento.append(codigo_seguimiento)
                entregas.append(entrega)
                logging.debug(f'Código de seguimiento generado: {codigo_seguimiento}')
                
                # Guardar los datos de la entrega en Firebase
                try:
                    response_pedido = requests.put(f'https://pedidos-a1b94.firebaseio.com/solicitudes/{codigo_seguimiento}.json', json=entrega)
                    logging.debug(f'Respuesta de guardar pedido: {response_pedido.status_code}')
                    logging.debug(f'Respuesta de Firebase: {response_pedido.text}')
                    if response_pedido.status_code != 200:
                        flash('Error al guardar el pedido. Por favor, intenta de nuevo.')
                        return redirect(url_for('servicio_mensagero', nombre=nombre))
                except Exception as e:
                    logging.error(f'Error al guardar el pedido en Firebase: {str(e)}')
                    flash('Error al guardar el pedido en Firebase. Por favor, intenta de nuevo.')
                    return redirect(url_for('servicio_mensagero', nombre=nombre))

            flash(f'Servicio solicitado con éxito. Revisa tus códigos de seguimiento en la sección correspondiente.')
            return redirect(url_for('confirmacion_multiple', codigos=codigos_seguimiento))
        
        except KeyError as e:
            logging.error(f'Error de clave al procesar el formulario: {str(e)}')
            flash('Faltan datos en el formulario. Por favor, completa todos los campos.')
            return redirect(url_for('servicio_mensagero', nombre=nombre))
        
        except Exception as e:
            logging.error(f'Error al procesar el formulario: {str(e)}')
            flash('Error al procesar el formulario. Por favor, intenta de nuevo.')
            return redirect(url_for('servicio_mensagero', nombre=nombre))

    return render_template('envios.html', nombre=nombre)


if __name__ == '__main__':
    app.run(debug=True)
