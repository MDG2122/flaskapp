import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template, url_for,session
from werkzeug.utils import secure_filename
import pandas as pd
from datos import listacodigos,codigosynbombres
from funciones import ordenarmenoramayor,buscar3,cambiarformato,imprimirtrimestres,obtenernummat,incluirpred,incluirreti,darprediccion,validar1,validar2,validar3,validar4,validar5,darprediccion2,ulttrim
import json
import numpy as np
#os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'
import tika
tika.initVM()
from tika import parser
from tensorflow import keras
from keras.models import load_model
from keras_multi_head import MultiHeadAttention
from keras_layer_normalization import LayerNormalization
from keras.layers import *
import tensorflow as tf
'''from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model'''
from keras import backend as K
K.set_session

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
			todaspasadas=validar1(xx,pred,x2)
			matrepe=validar2(pred)
			if todaspasadas and matrepe==False :
				xx=incluirpred(xx,pred)

				#x2=cambiarformato(x2)
				xx,x2=ordenarmenoramayor(xx,x2)
				#x3=obtenernummat(xx)
				trimfinal=ulttrim(xx)
				lista=imprimirtrimestres(xx,metadata,x2)
				matynotas = lista
				#print(matynotas)
				#return redirect("/materias")
				x3=obtenernummat(xx)
				json_dump = json.dumps({'xx': xx, 'x2': x2, 'x3':x3}, cls=NumpyEncoder)
				session['json'] = json_dump
				#session['x2'] = x2
				session['matynotas'] = matynotas
				session['trimfinal'] = trimfinal
				#print(x3)
				return redirect(url_for('.prueba', matynotas=matynotas,trimfinal=trimfinal, json_dump=json_dump))
				#prueba(xx,x2,matynotas)
				#if request.method == 'POST':

				#return render_template('showdata1.html',matynotas=matynotas)
				#retiradas=request.form['arreglo']
				#print(retiradas)
				#flash('File successfully uploaded')
				#return redirect('/')
				#return xx,x2
			elif todaspasadas==False :
				return render_template('materiayaaprobada.html')
			elif matrepe==True :
				return render_template('materiasrepe.html')

		else:
			flash('Allowed file is  pdf')
			return redirect(request.url)


@app.route('/materia')
def prueba():
	matynotas=session['matynotas']
	trimfinal=session['trimfinal']
	return render_template('showdata1.html',matynotas=matynotas,trimfinal=trimfinal)


@app.route('/materia', methods=['POST'])
def prueba2():
	if request.method == 'POST':
		json_dump=session['json']
		json_load = json.loads(json_dump)
		xx = np.asarray(json_load["xx"])
		x2 = np.asarray(json_load["x2"])
		x3 = np.asarray(json_load["x3"])
		retiradas=request.form['arreglo']
		retimasde7=validar3(xx,retiradas)
		retirepe=validar4(retiradas)
		retiyaapro=validar5(xx,retiradas,x2)
		if retimasde7==False and retirepe==False and retiyaapro==False:
			x1,x2=incluirreti(xx,x2,retiradas)
			x1,x2=ordenarmenoramayor(xx,x2)
			lista=imprimirtrimestres(x1,metadata,x2)
			matynotas = lista
			x1=np.reshape(x1,(1,23*7))
			x2=np.reshape(x2,(1,23*7,1))
			x3=np.reshape(x3,((1,7)))\
			

			model = load_model('model07361acc.h5',custom_objects={'MultiHeadAttention': MultiHeadAttention,'LayerNormalization':LayerNormalization,'NonMasking':NonMasking})
			pred=model.predict({'inputA':x1,'inputB':x2})
			x1=np.reshape(x1,(23,7))
			predi=darprediccion(x1,metadata,x3,pred)
			
		
			return render_template('/showpred.html',pred=predi)
		elif retimasde7 :
			return render_template('retioverflow.html')
		elif retirepe:
			return render_template('retirepe.html')
		elif retiyaapro:
			return render_template('retiyaapro.html')


if __name__ == '__main__':  
    app.run(debug = True)