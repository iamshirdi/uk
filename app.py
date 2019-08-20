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


@app.route('/image', methods=['GET'])
def index():
    return render_template('index.html')

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

@app.route("/api", methods=["POST"])
def api():

    result=request.form
    brand_label = result['brand']
    mileage = result['mileage']
    mark = result['mark']
    fiscal_power = result['fiscal_power']
    fuel_type = result['fuel_type']

    user_input = {'year_model':year_model, 'mileage':mileage, 'fiscal_power':fiscal_power, 'fuel_type':fuel_type, 'mark':mark}

    print(user_input)
    a = input_to_one_hot(user_input)
    price_pred = gbr.predict([a])[0]
    price_pred = round(price_pred, 2)
    return json.dumps({'price':price_pred});
    # return render_template('result.html',prediction=price_pred)

if __name__ == '__main__':

    app.run()
