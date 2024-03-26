from flask import Flask,render_template,request,redirect,send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os as os
import pandas as pd
import plotly as plt
from ploting import plot
app = Flask(__name__)
app.config['UPLOAD_DIRECTORY']='uploads/'
app.config['MAX_CONTENT_LENGTH']=16*1024*1024 #16MB
app.config['ALLOWED_EXTENSIONS']=['.csv']
app.config['GRAPH_DIRECTORY']='/home/sorecaffeine/Desktop/Flasktuto/Graphs'





@app.route('/')
def  index():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload():
    try:
        file=request.files['file']
        extension=os.path.splitext(file.filename)[1].lower()
        if file:
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                return 'File is not of csv type!'
            file.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
            secure_filename(file.filename)
            ))

        return redirect('/table')

    except RequestEntityTooLarge:
        return "File is larger then 16MB limit"

@app.route('/table',methods=['POST','GET'])
def table():
    if request.method == 'GET':
        try:
            file_name = os.listdir(app.config['UPLOAD_DIRECTORY'])[0]
            file_path = os.path.join(app.config['UPLOAD_DIRECTORY'], file_name)
            data = pd.read_csv(file_path)
            return render_template('tables.html', tables=[data.to_html()], titles=[''])
        except Exception as e:
            return f"An error has occurred: {e}", 500
    elif request.method =='POST':
            x=request.form.get('x')
            y=request.form.get('y')
            file_name = os.listdir(app.config['UPLOAD_DIRECTORY'])[0]
            file_path = os.path.join(app.config['UPLOAD_DIRECTORY'], file_name)
            y=plot(x,y,file_path)
            if y is True:
                return redirect('/graph')
    else:
        print('')

@app.route('/Graphs/<filename>', methods=['GET'])
def serve_graph_image(filename):
    return send_from_directory(app.config['GRAPH_DIRECTORY'], filename)

@app.route('/graph')
def render_graph_page():
    return render_template('graph.html')
if __name__== "__main__":
    app.run(debug=True)
