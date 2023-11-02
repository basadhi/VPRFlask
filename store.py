
import MySQLdb
from flask_mysqldb import MySQL
import firebase_admin
from firebase_admin import credentials, storage
 

# Initialize Firebase Admin SDK
cred = credentials.Certificate('vprimagesearch-firebase-adminsdk-rmdc1-842c646ae3.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'vprimagesearch.appspot.com'
})

#configuration of the db

db = yaml.load(open('db.yaml'),Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


# Function to insert image paths into MySQL
def insert_image_paths_into_mysql(image_paths):
    print("test 4")
    try:
        cursor = mysql.connection.cursor()
        for path in image_paths:
            # Assuming you have a 'images' table with a 'path' column
            query = "INSERT INTO prod_images (image_path) VALUES ;"
            cursor.execute(query, (path,))
        MySQLdb.connection.commit()
        cursor.close()
        return "Image paths inserted into MySQL successfully."

    except Exception as e:
        return jsonify({'error': "Failed to insert image paths into the database."})


def get_image_paths_from_storage():
    print("test 3")
    bucket = storage.bucket()
    image_paths = []

    # List all files in the Firebase Storage bucket
    blobs = bucket.list_blobs()
    for blob in blobs:
        # Assuming your images are in a specific directory or have a naming pattern
        
        image_paths.append(blob.name)

    return image_paths


def add_image_paths():
    print("teqst 10")
    image_paths = get_image_paths_from_storage()
    result = insert_image_paths_into_mysql(image_paths)
    return result