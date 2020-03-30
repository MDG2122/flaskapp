import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import pandas as pd
from datos import listacodigos,codigosynbombres
from funciones import ordenarmenoramayor,buscar3,cambiarformato,imprimirtrimestres,obtenernummat,incluirpred
#os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'
import tika
tika.initVM()
from tika import parser
#import numpy as np
metadata =pd.read_csv('static/metadata.csv',header=None)

UPLOAD_FOLDER = 'static'


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')
	'''
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename("historico.pdf")
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#FileName = open('static/historico.pdf', 'rb')
			
			PDF_Parse = parser.from_file('static/historico.pdf')
			
			hist=PDF_Parse ['content']
			hist=hist.split()
			
			xx,x2=buscar3(hist,listacodigos,metadata,codigosynbombres)

			#x2=cambiarformato(x2)
			
			xx,x2=ordenarmenoramayor(xx,x2)
			bot=xx
			return redirect('showdata1.html',bot1=bot)

		else:
			flash('Allowed file is  pdf')
			return redirect(request.url)

'''

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename("historico.pdf")
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#FileName = open('static/historico.pdf', 'rb')
			pred=request.form['array']
			#apred=np.asarray(array)
			#print((apred))
			
			PDF_Parse = parser.from_file('static/historico.pdf')
			
			hist=PDF_Parse ['content']
			hist=hist.split()
			
			xx,x2=buscar3(hist,listacodigos,metadata,codigosynbombres)
			
			xx=incluirpred(xx,pred)
			print(xx)

			#x2=cambiarformato(x2)
			xx,x2=ordenarmenoramayor(xx,x2)
			print(xx)
			#x3=obtenernummat(xx)
			lista=imprimirtrimestres(xx,metadata,x2)
			matynotas = lista
			return render_template('showdata1.html',matynotas=matynotas)
			#flash('File successfully uploaded')
			#return redirect('/')
			#return xx,x2
		else:
			flash('Allowed file is  pdf')
			return redirect(request.url)
        


if __name__ == '__main__':  
    app.run(debug = True)


