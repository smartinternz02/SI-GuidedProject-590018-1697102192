import re
import numpy as np
import os
from flask import Flask, app, request, render_template
from tensorflow.keras import models
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.python.ops.gen_array_ops import concat
from tensorflow.keras.applications.inception_v3 import preprocess_input
import requests
from flask import Flask, request, render_template, redirect,url_for
# from dbm import _Database
# loading the model
# from cloudant.client import Cloudant
# Specify your Cloudant credentials and database name
# Replace 'your_username' and 'your_password' with your Cloudant credentials
# Replace 'your_database_name' with the desired database name
# cloudant_credentials = {
#     'username': 'vamshi.em05@gmail.com',
#     'password': 'EmmadiVamshi@05',
# }

# database_name = 'my_database'

# # Initialize the Cloudant client with IAM authentication
# client = Cloudant(cloudant_credentials['username'], cloudant_credentials['password'], connect=True)

# # Connect to the server (you might not need this step if you're using IAM)
# # client.connect()

# # Create or retrieve the database
# my_database = client.create_database(my_database)

# if my_database.exists():
#     print(f"Database '{database_name}' successfully created or retrieved.")

# Perform your database operations here

# Disconnect from the Cloudant server when you're done
# client.disconnect()


# # Authentication using an I Am API key
# client = Cloudant.iam(connect=True)

# # create a database using an initialised client
# my_database = client.create_database('my_database')

model1 = load_model('level.h5')
model2 = load_model('body.h5')

app=Flask(__name__)

# default home page or route
@app.route('/')
def home():
    return render_template('home.html')
# registration page
@app.route('/register', methods=["GET","POST"])
def registration():
    return render_template('register.html')
# registration page
# @app.route('/register_new')
# def register_new():
#     return render_template('login.html')
    # Your view function logic here

# @app.route('/register')
# def register():
#     return render_template('register.html')
@app.route('/afterreg', methods=['POST'])
def afterreg():
    x = [x for x in request.form.value()]
    print(x)
    data = {
    '_id': x[1],    # setting_id is optional
    'name': x[0],
    'psw': x[2]
    }
    print(data)
     
    #  query = {'_id': {'$eq': data['_id']}}

    # docs = my_database.get_query_result(query)
    # print(docs)

    # print(len(docs.all()))

    # if(len(docs.all()))==0:
    #     url = my_database.create_document(data)
    #     # response = request.get(url)
    #     return render_template('register.html', pred="registration Successful, please login using your details")
    # else:
    #     return render_template('register.html', pred="you are already a member, please login using your details")


@app.route('/login', methods=["GET","POST"])
def login():
     return render_template('login.html')
@app.route('/afterlogin', methods=['POST'])
def afterlogin():
    user = request.form['_id']
    passw = request.form['psw']
    print(user,passw)

    # query = {'_id': {'$eq': user}}
     
    # docs = my_database.get_query_result(query)
    # print(docs)

    # print(len(docs.all()))

    # if(len(docs.all())==0):
    #     return render_template('login.html', pred="The username is not found")
    # else:
    #     if((user==docs[0][0]['_id'] and passw==docs[0][0]['psw'])):
    #         return redirect(url_for('prediction'))
    #     else:
    #         print('Invalid User')
@app.route('/prediction', methods=["GET","POST"] )
def prediction():
    return render_template('predict.html')

@app.route('/predict', methods=["GET","POST"])
def predict():
    if request.method=="POST":
        f=request.files['image']
        basepath=os.path.dirname(__file__)  #getting the current path i.e where app.py is present
        # print("current path",basepath)
        filepath=os.path.join(basepath,'uploads',f.filename) # from anywhere in the system we can give image
        # print("upload folder is ",filepath)
        f.save(filepath)

        img=image.load_img(filepath,target_size=(224,224))
        x=image.img_to_array(img) #img to array
        x=np.expand_dims(x,axis=0) #used for adding one more dimension
        print(x)
        img_data=preprocess_input(x)
        prediction1=np.argmax(model1.predict(img_data))
        prediction2=np.argmax(model2.predict(img_data))

        #prediction=model.predict(x) #instead of predict_classes(x) we can use predict(x)  ------>predict_classes
        #print("prediction is",prediction)
        index1=['front', 'rear', 'side']
        index2=['minor', 'moderate', 'severe']
        #result = str(index[output[0]])
        result1 = index1[prediction1]
        result2 = index2[prediction2]
        if(result1 == "front" and result2 == "minor"):
            value = "3000 - 5000 INR"
        elif(result1 == "front" and result2 == "moderate"):
            value = "6000 - 8000 INR"
        elif(result1 == "front" and result2 == "severe"):
            value = "9000 - 11000 INR"
        elif(result1 == "rear" and result2 == "minor"):
            value = "4000 - 6000 INR"
        elif(result1 == "rear" and result2 == "moderate"):
            value = "7000 - 9000 INR"
        elif(result1 == "rear" and result2 == "severe"):
            value = "11000 - 13000 INR"
        elif(result1 == "side" and result2 == "minor"):
            value = "11000 - 13000 INR"
        elif(result1 == "side" and result2 == "moderate"):
            value = "9000 - 11000 INR"
        elif(result1 == "side" and result2 == "severe"):
            value = "120000 - 11000 INR"
        else:
            value = "16000 - 50000 INR"  
        value = 'The predicted output is {}' .format(str(value)) 
        return render_template('predict.html', prediction=value)

@app.route('/logout', methods=["GET","POST"] )
def logout():
    return render_template('logout.html')
    
"""Running our application"""
if __name__ == "__main__":
    app.run(debug = True)
