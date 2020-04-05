import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template, url_for,session
from werkzeug.utils import secure_filename
import pandas as pd
from datos import listacodigos,codigosynbombres
from funciones import ordenarmenoramayor,buscar3,cambiarformato,imprimirtrimestres,obtenernummat,incluirpred,incluirreti,darprediccion
import json
import numpy as np
#os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'
import tika
tika.initVM()
from tika import parser
import keras
from keras.models import load_model
from keras_multi_head import MultiHeadAttention
from keras_layer_normalization import LayerNormalization
from keras.layers import *
#import numpy as np
metadata =pd.read_csv('static/metadata.csv',header=None)

UPLOAD_FOLDER = 'static'


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['pdf'])

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class NonMasking(Layer):   
    def __init__(self, **kwargs):   
        self.supports_masking = True  
        super(NonMasking, self).__init__(**kwargs)   
  
    def build(self, input_shape):   
        input_shape = input_shape   
  
    def compute_mask(self, input, input_mask=None):   
        # do not pass the mask to the next layers   
        return None   
  
    def call(self, x, mask=None):   
        return x   
  
    def get_output_shape_for(self, input_shape):   
        return input_shape

model = load_model('model07158acc.h5',custom_objects={'MultiHeadAttention': MultiHeadAttention,'LayerNormalization':LayerNormalization,'NonMasking':NonMasking})
model._make_predict_function()
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

			#x2=cambiarformato(x2)
			xx,x2=ordenarmenoramayor(xx,x2)
			#x3=obtenernummat(xx)
			lista=imprimirtrimestres(xx,metadata,x2)
			matynotas = lista
			#print(matynotas)
			#return redirect("/materias")
			x3=obtenernummat(xx)
			json_dump = json.dumps({'xx': xx, 'x2': x2, 'x3':x3}, cls=NumpyEncoder)
			session['json'] = json_dump
			#session['x2'] = x2
			session['matynotas'] = matynotas
			print(x3)
			return redirect(url_for('.prueba', matynotas=matynotas, json_dump=json_dump))
			#prueba(xx,x2,matynotas)
			#if request.method == 'POST':

			#return render_template('showdata1.html',matynotas=matynotas)
			#retiradas=request.form['arreglo']
			#print(retiradas)
			#flash('File successfully uploaded')
			#return redirect('/')
			#return xx,x2
		else:
			flash('Allowed file is  pdf')
			return redirect(request.url)


@app.route('/materia')
def prueba():
	matynotas=session['matynotas']
	return render_template('showdata1.html',matynotas=matynotas)


@app.route('/materia', methods=['POST'])
def prueba2():
	if request.method == 'POST':
		json_dump=session['json']
		json_load = json.loads(json_dump)
		xx = np.asarray(json_load["xx"])
		x2 = np.asarray(json_load["x2"])
		x3 = np.asarray(json_load["x3"])
		retiradas=request.form['arreglo']
		print(retiradas)
		x1,x2=incluirreti(xx,x2,retiradas)
		x1,x2=ordenarmenoramayor(xx,x2)
		lista=imprimirtrimestres(x1,metadata,x2)
		matynotas = lista
		x1=np.reshape(x1,(1,23*7))
		x2=np.reshape(x2,(1,23*7,1))
		x3=np.reshape(x3,((1,7)))
		pred=model.predict({'inputA':x1,'inputB':x2,'inputC':x3})
		x1=np.reshape(x1,(23,7))
		predi=darprediccion(x1,metadata,x3,pred)
		#print(x1)
		#print(x2)
		#print(x3)
	
		return render_template('/showpred.html',pred=predi)
	






if __name__ == '__main__':  
    app.run(debug = True)


