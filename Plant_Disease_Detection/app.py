import os
import warnings
warnings.simplefilter("ignore")
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from flask import Flask, request, render_template
from tensorflow.keras import backend as K
from os import listdir
K.clear_session()

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
im = ''
result = '...'
percentage = '...'
i = 0
imageName = ''
solution = ''
@app.route("/")
def index():
    return render_template("main.html")

@app.route("/main", methods=["POST"])
def main():
    global im, result, percentage , i , imageName , solution
    target = os.path.join(APP_ROOT, 'static\\')
    print(f'Target : {target}')

    if not os.path.isdir(target):
        os.mkdir(target)
    for imgg in os.listdir(target):
        try:
            imgPath = target + imgg
            os.remove(imgPath)
            print(f'Removed : {imgPath}')
        except Exception as e:
            print(e)
        
    for file in request.files.getlist("file"):
        print(f'File : {file}')
        i += 1
        imageName = str(i) + '.JPG'
        filename = file.filename
        destination = "/".join([target, imageName])
        print(f'Destination : {destination}')
        file.save(destination)
        print('analysing Image')
        try:
            image = os.listdir('static')
            im = destination
            print(f'Analysing Image : {im}')
        except Exception as e:
            print(e)
        result = "Failed to Analyse"
        percentage = "0 %"
        try:
            detect()
            solution = solutions(result)
        except Exception as e:
            print(f'Error While Loading : {e}')  
    return render_template('complete.html', name=result, accuracy=percentage , img = imageName , soln = solution)


def detect():
    global im, result, percentage
    print(f'Image : {im}')
    classNames=["Apple___Apple_scab","Apple___Black_rot","Apple___Cedar_apple_rust","Apple___healthy","Blueberry___healthy","Cherry_including_sour___Powdery_mildew", "Cherry_including_sour___healthy","Corn_maize___Cercospora_leaf_spot Gray_leaf_spot","Corn_maize___Common_rust_","Corn_maize___Northern_Leaf_Blight","Corn_maize___healthy","Grape___Black_rot","Grape___Esca_Black_Measles","Grape___Leaf_blight_Isariopsis_Leaf_Spot","Grape___healthy","Orange___Haunglongbing_Citrus_greening","Peach___Bacterial_spot","Peach___healthy","Pepper,_bell___Bacterial_spot","Pepper,_bell___healthy","Potato___Early_blight","Potato___Late_blight","Potato___healthy","Raspberry___healthy","Soybean___healthy","Squash___Powdery_mildew","Strawberry___Leaf_scorch","Strawberry___healthy","Tomato___Bacterial_spot","Tomato___Early_blight","Tomato___Late_blight","Tomato___Leaf_Mold","Tomato___Septoria_leaf_spot","Tomato___Spider_mites Two-spotted_spider_mite","Tomato___Target_Spot","Tomato___Tomato_Yellow_Leaf_Curl_Virus","Tomato___Tomato_mosaic_virus","Tomato___healthy"]
    totClass = len(classNames)
    print(classNames)
    print(totClass)
    mdl = "vgg_model.h5"
    image = cv2.imread(im)
    orig = image.copy()
    try:
        image = cv2.resize(image,(224,224))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
    except Exception as e:
        print("Error Occured : ",e)
    # load the trained convolutional neural network
    print("[INFO] loading network...")
    model = load_model(mdl)
    (zero, one,two, three,four,five,six,seven, eight,nine, ten , eleven, twelve , thirteen , fourteen,Fifteen, sixteen, seventeen, eighteen, nineteen, twenty, twentyone, twentytwo, twentythree, twentyfour, twentyfive, twentysix, twentyseven, twentyeight, twentynine, thirty, thirtyone, thirtytwo, thirtythree, thirtyfour, thirtyfive, thirtysix, thirtyseven) = model.predict(image)[0]
    prob = [zero, one,two, three,four,five,six,seven, eight,nine, ten , eleven, twelve , thirteen , fourteen,Fifteen, sixteen, seventeen, eighteen, nineteen, twenty, twentyone, twentytwo, twentythree, twentyfour, twentyfive, twentysix, twentyseven, twentyeight, twentynine, thirty, thirtyone, thirtytwo, thirtythree, thirtyfour, thirtyfive, thirtysix, thirtyseven]

    maxProb = max(prob)
    maxIndex = prob.index(maxProb)
    label = classNames[maxIndex]
    proba = maxProb
    result = label
    percentage = float("{0:.2f}".format(proba * 100))
    for i in range(0,totClass):
        print(f'{classNames[i]} : {prob[i]}')


@app.route('/member_details')
def member_details():
    return render_template('member_details.html')

@app.route('/project_details')
def project_details():
    drive_link ="https://docs.google.com/presentation/d/1cn9Rdbtk5DFC-iiSeS_KLe5cft88HCwV/edit?usp=sharing&ouid=113963127305371188444&rtpof=true&sd=true"
    github_link="https://github.com/jhashivam0022/Plant_Disease_Detection.git"
    return render_template('project_details.html',drive_link=drive_link,github_link=github_link)




Apple___Apple_scab="""Apply fungicides such as captan or myclobutanil according to label instructions.
Remove and destroy infected leaves, fruits, and twigs.
Prune trees to improve air circulation and sunlight penetration.
"""

Apple___Black_rot="""
Prune and destroy infected branches and cankers during dry weather.
Apply fungicides like myclobutanil or mancozeb during the growing season.
Clean up fallen leaves and fruit from the ground.
"""

Apple___Cedar_apple_rust="""
Remove galls or cankers from cedar trees.
Apply protective fungicides to apple trees during spring.
Choose resistant apple cultivars when planting.
"""

Apple___healthy="""
No action required. Your apple tree is healthy.
"""

Blueberry___healthy="""
No action required. Your blueberry plant is healthy.
"""

Cherry_including_sour___Powdery_mildew="""
Apply fungicides containing sulfur or potassium bicarbonate.
Prune infected branches during dormancy.
Improve air circulation around the tree.
"""

Cherry_including_sour___healthy="""
No action required. Your cherry tree is healthy.
"""

Corn_maize___Cercospora_leaf_spot_Gray_leaf_spot="""
Apply fungicides like chlorothalonil or azoxystrobin.
Rotate crops to reduce disease pressure.
Remove and destroy infected crop debris.
"""

Corn_maize___Common_rust_="""
Plant resistant corn varieties.
Apply fungicides during early infection stages.
Remove and destroy infected leaves.
"""

Corn_maize___Northern_Leaf_Blight="""
Apply fungicides containing triazoles or strobilurins.
Rotate crops to reduce disease pressure.
Remove and destroy infected crop debris.
"""

Corn_maize___healthy="""
No action required. Your corn plant is healthy.
"""

Grape___Black_rot="""
Apply fungicides like myclobutanil or copper-based sprays.
Remove and destroy infected fruits, leaves, and canes.
Improve air circulation and pruning practices.
"""

Grape___Esca_Black_Measles="""
Prune and remove infected wood during dormancy.
Apply preventive fungicides during spring and fall.
Minimize pruning wounds.
"""

Grape___Leaf_blight_Isariopsis_Leaf_Spot="""
Apply fungicides containing chlorothalonil or myclobutanil.
Remove and destroy infected leaves and debris.
Improve air circulation and sunlight penetration.
"""

Grape___healthy="""
No action required. Your grapevine is healthy.
"""

Orange___Haunglongbing_Citrus_greening="""
There is no cure for this disease.
Remove and destroy infected trees to prevent spread.
Control the Asian citrus psyllid vector using insecticides
"""

Peach___Bacterial_spot="""
Apply copper-based fungicides during dormant and pre-bloom stages.
Prune and remove infected branches.
Avoid overhead irrigation.
"""

Peach___healthy="""
No action required. Your peach tree is healthy.
"""

Pepper_bell___Bacterial_spot="""
Apply copper-based bactericides during early stages.
Remove and destroy infected plants and fruits.
Rotate crops and practice good sanitation.
"""

Pepper_bell___healthy="""
No action required. Your bell pepper plant is healthy
"""

Potato___Early_blight="""
Apply fungicides containing chlorothalonil or mancozeb.
Remove and destroy infected leaves and tubers.
Practice crop rotation and good sanitation.
"""

Potato___Late_blight="""
Apply fungicides containing chlorothalonil or metalaxyl.
Remove and destroy infected plants and tubers.
Practice crop rotation and good sanitation.
"""

Potato___healthy="""
No action required. Your potato plant is healthy.
"""

Raspberry___healthy="""
No action required. Your raspberry plant is healthy.
"""

Soybean___healthy="""
No action required. Your soybean plant is healthy.
"""

Squash___Powdery_mildew="""
Apply fungicides containing sulfur or potassium bicarbonate.
Remove and destroy infected leaves and vines.
Provide good airflow and avoid overhead irrigation.
"""

Strawberry___Leaf_scorch="""
Remove and destroy infected leaves and plants.
Apply fungicides containing myclobutanil or chlorothalonil.
Plant disease-resistant strawberry varieties.
"""

Strawberry___healthy="""
No action required. Your strawberry plant is healthy
"""

Tomato_Bacterial_spot = """
Apply copper-based bactericides during early stages.
Remove and destroy infected plants and fruits.
Practice crop rotation and good sanitation.
"""

Tomato_Early_blight = """
Apply fungicides containing chlorothalonil or mancozeb.
Remove and destroy infected leaves and fruits.
Practice crop rotation and good sanitation.
"""

Tomato_healthy = """
No action required. Your Tomato plant is healthy
"""

Tomato_Late_blight = """
Apply fungicides containing chlorothalonil or metalaxyl.
Remove and destroy infected plants and fruits.
Practice crop rotation and good sanitation.
"""

Tomato_Leaf_Mold = """
Apply fungicides containing chlorothalonil or mancozeb.
Provide good air circulation and reduce humidity.
Remove and destroy infected leaves.
"""

Tomato_Septoria_leaf_spot = """
Apply fungicides containing chlorothalonil or mancozeb.
Remove and destroy infected leaves and fruits.
Practice crop rotation and good sanitation.
"""

Tomato_Spider_mites_Two_spotted_spider_mite = """
Apply miticides like abamectin or spiromesifen.
Spray plants with high-pressure water to dislodge mites.
Introduce beneficial insects like ladybugs.
"""

Tomato__Target_Spot = """
Apply miticides like abamectin or spiromesifen.
Spray plants with high-pressure water to dislodge mites.
Introduce beneficial insects like ladybugs.
"""

Tomato__Tomato_mosaic_virus = """
There is no cure for this virus.
Remove and destroy infected plants to prevent spread.
Control aphids and practice good sanitation.
"""

Tomato__Tomato_YellowLeaf__Curl_Virus = """
There is no cure for this virus.
Control the whitefly vector using insecticides.
Remove and destroy infected plants to prevent spread.
"""

def solutions(disease):
    switcher = {
        "Apple___Apple_scab":Apple___Apple_scab,
        "Apple___Black_rot":Apple___Black_rot,
        "Apple___Cedar_apple_rust":Apple___Cedar_apple_rust,
        "Apple___healthy":Apple___healthy,
        "Blueberry___healthy":Blueberry___healthy,
        "Cherry_including_sour___Powdery_mildew":Cherry_including_sour___Powdery_mildew, 
        "Cherry_including_sour___healthy":Cherry_including_sour___healthy,
        "Corn_maize___Cercospora_leaf_spot Gray_leaf_spot":Corn_maize___Cercospora_leaf_spot_Gray_leaf_spot,
        "Corn_maize___Common_rust_":Corn_maize___Common_rust_,
        "Corn_maize___Northern_Leaf_Blight":Corn_maize___Northern_Leaf_Blight,
        "Corn_maize___healthy":Corn_maize___healthy,
        "Grape___Black_rot":Grape___Black_rot,
        "Grape___Esca_Black_Measles":Grape___Esca_Black_Measles,
        "Grape___Leaf_blight_Isariopsis_Leaf_Spot":Grape___Leaf_blight_Isariopsis_Leaf_Spot,
        "Grape___healthy":Grape___healthy,
        "Orange___Haunglongbing_Citrus_greening":Orange___Haunglongbing_Citrus_greening,
        "Peach___Bacterial_spot":Peach___Bacterial_spot,
        "Peach___healthy":Peach___healthy,
        "Pepper_bell___Bacterial_spot":Pepper_bell___Bacterial_spot,
        "Pepper_bell___healthy":Pepper_bell___healthy,
        "Potato___Early_blight":Potato___Early_blight,
        "Potato___Late_blight":Potato___Late_blight,
        "Potato___healthy":Potato___healthy,
        "Raspberry___healthy":Raspberry___healthy,
        "Soybean___healthy":Soybean___healthy,
        "Squash___Powdery_mildew":Squash___Powdery_mildew,
        "Strawberry___Leaf_scorch":Strawberry___Leaf_scorch,
        "Strawberry___healthy":Strawberry___healthy,
        "Tomato___Bacterial_spot":Tomato_Bacterial_spot,
        "Tomato___Early_blight":Tomato_Early_blight,
        "Tomato___Late_blight":Tomato_Late_blight,
        "Tomato___Leaf_Mold":Tomato_Leaf_Mold,
        "Tomato___Septoria_leaf_spot":Tomato_Septoria_leaf_spot,
        "Tomato___Spider_mites_Two-spotted_spider_mite":Tomato_Spider_mites_Two_spotted_spider_mite,
        "Tomato___Target_Spot":Tomato__Target_Spot,
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus":Tomato__Tomato_YellowLeaf__Curl_Virus,
        "Tomato___Tomato_mosaic_virus":Tomato__Tomato_mosaic_virus,
        "Tomato___healthy":Tomato_healthy,
        }
    return switcher.get(disease,"Not Found In The List")
        
if __name__ == "__main__":
    app.run(port=4555, debug=True)
