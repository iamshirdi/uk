from fastai import *
from fastai.vision import *
import numpy as np
from mapper import dict
import keras
import tensorflow as tf
from flask import Flask, redirect, url_for, request, render_template
from PIL import Image
import io
import gdown
import os

app = Flask(__name__)

url='https://drive.google.com/uc?export=download&id=1ss1LmKyfNOzSIKosfuyPJyXGF_4E5Pjo'
output='export.pkl'
if 'export.pkl' not in os.listdir('path') :
    gdown.download(url,os.path.join('path',output),quiet=False)

from torchvision import transforms
t = transforms.Compose([
# transforms.ToPILImage(),                 #[1]
 transforms.Resize(256),                    #[2]
 transforms.CenterCrop(224),                #[3]
 transforms.ToTensor(),                     #[4]
 transforms.Normalize(                      #[5]
 mean=[0.5, 0.5, 0.5],                #[6]
 std=[0.5, 0.5, 0.5] )                 #[7]
 ])


path = Path("path")
export_file_name = 'export.pkl'
learn = load_learner(path, export_file_name)

model2=torch.load('path/checkpoint.pth').cpu()

# model3 = load_model('path/smart_price2.h5')
model3 = keras.models.load_model('path/smart_price2.h5')
global graph,model
graph = tf.get_default_graph()

def input_to_one_hot(data):
    # initialize the target vector with zero values
    dict2={}
    dict2=dict
    enc_input=[]
    enc_input.append( 'category_'+data['category'])
    enc_input.append( 'gender_'+data['gender'])
    enc_input.append('brand_'+data['brand'])
    enc_input.append('size_'+data['size'])
    for e in enc_input:
        dict2[e]=1
    return dict2


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

@app.route('/image', methods=['GET'])
def index2():
    return render_template('index2.html')

@app.route('/price', methods=['GET'])
def price():
    return render_template('price.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        filename = request.files['file']
        img = open_image(filename)
        pred_class,pred_idx,outputs = learn.predict(img)

        return cls(pred_class,outputs)
    return None


@app.route('/predict2', methods=['GET', 'POST'])
def upload_file():
        if request.method == 'POST':
            f = request.files['image']
            return render_template("success.html", name = f.filename)

        # filename2 = request.files['file2']
        # img2 = open_image(filename2)
        # # model2.eval()
        # outputs2=model2(t(img2).unsqueeze(0))
        # prob, predicted = torch.max(outputs2.data, 1)
        # print(predicted,prob)
        # return predicted
    # return Nones

@app.route("/api", methods=["POST"])
def api():

    result=request.form
    category_label = result['category']
    brand_label = result['brand']
    gender_label = result['gender']
    size_label = result['size']

    user_input = {'category':category_label, 'brand':brand_label, 'gender':gender_label, 'size':size_label}

    print(user_input)
    d = input_to_one_hot(user_input)
    testX=list(d.values())
    a=np.array(testX)
    with graph.as_default():
        price_pred = model3.predict(np.reshape(a, (-1,819)))
    price_pred = round(price_pred[0][0]*1999, 2)
    return json.dumps({'price':price_pred});
    # return render_template('result.html',prediction=price_pred)

if __name__ == '__main__':

    app.run()
