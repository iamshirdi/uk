from fastai import *
from fastai.vision import *
import numpy as np
import keras
import tensorflow as tf
from flask import Flask, redirect, url_for, request, render_template
from PIL import Image
import io
import gdown
import os
import json
import torch
from torchvision import datasets, utils, transforms, models
from torch import nn

app = Flask(__name__)

url='https://drive.google.com/uc?export=download&id=1ss1LmKyfNOzSIKosfuyPJyXGF_4E5Pjo'
url2='https://drive.google.com/uc?export=download&id=123sUYOgZcUYXnACFwUGliWO9i-ng8kF0'
output='export.pkl'
if 'export.pkl' not in os.listdir('path') :
    gdown.download(url,os.path.join('path',output),quiet=False)
if 'checkpoint.pth' not in os.listdir('path') :
    gdown.download(url2,os.path.join('path','checkpoint.pth'),quiet=False)

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

model2=models.resnet50()
model2.fc=nn.Linear(2048, 144)
model2.load_state_dict(torch.load(os.path.join('path','checkpoint.pth')), strict=False)
model2.eval()


#.cpu
global graph
graph = tf.get_default_graph()
model = keras.models.load_model('path/smart_price2.h5')



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
def predict2():
    if request.method == 'POST':
        filename2 = request.files['file2']
        img = Image.open(filename2).convert('RGB')
        outputs2=model2(t(img).unsqueeze(0))
        _, predicted = torch.max(outputs2.data, 1)
        print(predicted)
        values, indices = outputs2.max(0)

        return str(predicted.numpy()[0])
    return None

@app.route("/api", methods=["POST"])
def api():

    result=request.form
    user_input = {'category':result['category'], 'brand':result['brand'], 'gender':result['gender'], 'size':result['size']}

    print(user_input)

    with open('data_mapper.json', 'r') as f:
        dict2 = json.load(f)

    enc_input=[]
    enc_input.append( 'category_'+user_input['category'])
    enc_input.append( 'gender_'+user_input['gender'])
    enc_input.append('brand_'+user_input['brand'])
    enc_input.append('size_'+user_input['size'])
    for e in enc_input:
        dict2[e]=1

    testX=list(dict2.values())
    a=np.array(testX)

    image=np.reshape(a, (-1,819))

    with graph.as_default():
        price_pred =model.predict(image)
    price_pred2 = round(price_pred[0][0]*1999,2)

    return json.dumps({'price':price_pred2});
    # return render_template('result.html',prediction=price_pred)

if __name__ == '__main__':

    app.run()
