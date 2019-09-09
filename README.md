## Demo website
- https://bclothes.herokuapp.com/price

## Data Gathering- Model Creation link
- https://github.com/iamshirdi/ETL

## Project Description
Price Prediction API creation and front end development within App using Ionic, Angular. Nodejs

- Data gathering from 20 websites using selenium, python-requests library on GCP compute, Azure.
- Data cleaning and Image classifier in PyTorch, Price Prediction in Tensorflow
- API creation using Python Flask framework and deploying on Heroku Cloud
- Frontend demo website on Heroku Cloud
- Deploying the working model in the App for production

## Tech used

- Bootstrap
- Flask.Jinja
- Jquery
- Select2
- Fastai
- Pytorch
- Tensorflow
- gdown
- Selinium Scrapper
- Requests
- Sendgrid
- Node.js
- Ionic
- Angular
- MongoDB
- Google App Engine and Heroku Cloud
- nvidia-smi -l 100
- gcloud Tesla T4 and Colab

## API Docs

- Price Predictor Python API example

 ```
import requests
url = 'https://bclothes.herokuapp.com/api'
myobj = {'category': 'bodysuits','brand': 'no brand','gender': 'unisex','size': '79'}
x = requests.post(url, data = myobj)
print(x.text)
# {"price": 130.67}
```
- Image Predictor Python API example
```
url='https://bclothes.herokuapp.com/predict'
file_list = [
    ('file', ('img1.jpg', open('img1.jpg', 'rb')))
]
r = requests.post(url, files=file_list)
print(r.text)
# Baby Clothes with probability 0.9999775886535645
