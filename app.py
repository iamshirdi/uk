from fastai import *
from fastai.vision import *

from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)




path = Path("path")
export_file_name = 'export.pkl'
learn = load_learner(path, export_file_name)

def cls(pred_class,outputs):
    o1=outputs.tolist()[0]
    o2=outputs.tolist()[1]
    if str(pred_class)=='Baby Clothes':
        o=str(pred_class)+' with probability '+str(o1)
    else:
        o=str(pred_class)+' with probability '+str(o2)
    return o




@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        # Get the file from post request
        filename = request.files['file']
        img = open_image(filename)
        pred_class,pred_idx,outputs = learn.predict(img)

        return cls(pred_class,outputs)
    return None


if __name__ == '__main__':

    app.run()
