from flask import Flask , render_template, request,jsonify
import requests
import base64

app = Flask(__name__)

API_ENDPOINT = 'https://thenujan-vpr-deploy.hf.space/'

@app.route('/',methods = ['GET','POST'])

def index():

    if request.method == 'POST':

        uploaded_image = request.files['imagefile']

        if uploaded_image:

            files = {'imagefile' : ('uploaded_image',uploaded_image)}
            response = requests.post(API_ENDPOINT,files=files)

            if response.status_code == 200:
                similar_images = response.content
                similar_images_base64 = base64.b64decode(similar_images).decode('utf-8') # Assuming your model returns a JSON response

                # Render a template to display similar images
                return render_template('results.html', similar_images_base64=similar_images_base64)
            else:
                return "Error: Unable to retrieve similar images from the model API."

    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=3000,debug=True)