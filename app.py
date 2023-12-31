from flask import Flask , render_template, request,jsonify
import requests
import base64
import os
import pandas as pd
import cv2
from flask_mysqldb import MySQL
import yaml
import firebase_admin
from firebase_admin import credentials, storage



app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 16 MB
 
# print("test 1")
# # Initialize Firebase Admin SDK
# cred = credentials.Certificate('vprimagesearch-firebase-adminsdk-rmdc1-842c646ae3.json')
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'vprimagesearch.appspot.com'
# })
# print("test 2" )

image_folder = 'gallery'
os.makedirs(image_folder, exist_ok=True)

# def get_image_paths_from_storage():
#     print("test 3")
#     bucket = storage.bucket()
#     image_paths = []

#     # List all files in the Firebase Storage bucket
#     blobs = bucket.list_blobs()
#     for blob in blobs:
#         # Assuming your images are in a specific directory or have a naming pattern
        
#         image_paths.append(blob.name)

#     print(image_paths,"image paths")

#     return image_paths


# Function to insert image paths into MySQL
# def insert_image_paths_into_csv(image_paths):
#     print("test 4")
#     try:
#         with app.app_context():
#             cursor = mysql.connection.cursor()
#             for path in image_paths:
#                 # Assuming you have a 'images' table with a 'path' column
#                 query = "INSERT INTO prod_images (image_path) VALUES ;"
#                 cursor.execute(query, (path,))
#             mysql.connection.commit()
#             cursor.close()
#         return "Image paths inserted into MySQL successfully."

#     except Exception as e:
#         with app.app_context():
#             return jsonify({'error': "Failed to insert image paths into the database."})

# @app.route('/add_image_paths', methods=['GET'])
# def add_image_paths():
#     print("teqst 10")
#     image_paths = get_image_paths_from_storage()
#     result = insert_image_paths_into_mysql(image_paths)
#     return result


def read_image(image_file):
    print("test 5")
    img = cv2.imread(
        image_file, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION
    )
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if img is None:
        raise ValueError('Failed to read {}'.format(image_file))
    return img


def get_image_paths(prod_ids):
    csv_path = 'Imagepaths (1).csv'  # Replace with the actual path
    data = pd.read_csv(csv_path)
    image_paths = []
    print("test 6")
    data['ID'] = pd.to_numeric(data['ID'], errors='coerce')
    
    #print(data['ID'])

    for prod_id in (prod_ids):
        
        
       # print(prod_id,"test 7")

        row = data.loc[data['ID'] == int(prod_id)]
        #print(row,"test 7")
        
        if not row.empty:
            image_path = row.iloc[0]['Image URL']
            #print(image_path,"test 8")
            # print(image_path)
            image_paths.append(image_path)

    
    
    print(image_paths)
            
        

    return image_paths





print("test 9")

#configuration of the db

# db = yaml.load(open('db.yaml'),Loader=yaml.FullLoader)
# app.config['MYSQL_HOST'] = db['mysql_host']
# app.config['MYSQL_USER'] = db['mysql_user']
# app.config['MYSQL_PASSWORD'] = db['mysql_password']
# app.config['MYSQL_DB'] = db['mysql_db']

# def create_mysql_connection():
#     mysql = MySQL(app)
#     return mysql

# result = add_image_paths()
# print(result,"test 15")

API_ENDPOINT = 'https://indexvpr-4l2dxaoo7q-uc.a.run.app'




@app.route('/home',methods = ['GET','POST'])

def home():

    if request.method == 'POST':
        print("test 11")

        uploaded_image = request.files['imagefile']
        print(request.files,"test 12")
        print(uploaded_image,"test 13")

        if uploaded_image:

            files = {'file' : ('uploaded_image',uploaded_image)}

            response = requests.post(API_ENDPOINT,files=files)
            print("test 14")

            if response.status_code == 200:
                similar_images = response.json()
                image_ids = similar_images['prediction']['similar_image_ids'][0]
                #print(image_ids, "these are the image ids")


                image_paths = get_image_paths(image_ids)
                
                # similar_images_base64 = base64.b64decode(similar_images).decode('utf-8') # Assuming your model returns a JSON response

                # Render a template to display similar images
                # return render_template('results.html', similar_images_base64=similar_images)
            else:
                return "Error: Unable to retrieve similar images from the model API."

    return jsonify(data=image_paths)





@app.route('/dashboard')
def dashboard():
    # Define the Power BI dashboard URL
    power_bi_dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiMWIwMjZkNzAtMTY3NS00OTg3LWIxOWUtZmE2NDc3OGE5NjU2IiwidCI6ImFhYzBjNTY0LTZjNWUtNGIwNS04ZGMzLTQwODA8%3D"

    # Pass the URL to the dashboard.html template
    return render_template('dashboard.html', power_bi_dashboard_url=power_bi_dashboard_url)
@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
  
    app.run(port=3000,debug=True)