from flask import Flask, request, redirect, url_for, render_template, flash
import os
import uuid

app = Flask(__name__)
# PASSANDO O CONFIG
app.config.from_object('config')
TIPOS_DISPONIVEIS = set(['png', 'jpg','jpeg', 'gif'])

def arquivos_permitidos(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in TIPOS_DISPONIVEIS
# primeira ROTA
@app.route('/')
# Chamando funcão
def home():
    return render_template('index.html')

@app.route('/', methods=["POST"])
#Duas condições
def upload_image():
    file = request.files['file']

    if file.filename == ' ':
        flash("Nenhum arquivo foi selecionado")
        return redirect(request.url)

    if not arquivos_permitidos(file.filename):
        flash("Utilize os tipos de arquivos referentes a imagem")
        return redirect(request.url)

    filename = str(uuid.uuid4())
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    flash("Imagem Enviada com Sucesso")
    return render_template('index.html', filename=filename)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
