# Run by typing python3 main.py

## **IMPORTANT:** only collaborators on the project where you run
## this can access this web server!

"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user? 
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model? 
"""

# import basics
import os

# import stuff for our web server
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory
from flask import jsonify
from utils import get_base_url, allowed_file, and_syntax
from utils import clean_text, remove_stop_words, remove_hashtags_atSigns_links, cleanup, lemmatizeText, predict_text
# from sklearn.metrics import confusion_matrix,f1_score
# import seaborn as sns, matplotlib.pyplot as plt
# import stuff for our models
import pickle

# from aitextgen import aitextgen

'''
Coding center code - comment out the following 4 lines of code when ready for production
'''
# load up the model into memory
# you will need to have all your trained model in the app/ directory.



# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 36280
base_url = get_base_url(port)
app = Flask(__name__, static_url_path=base_url+'static')

'''
Deployment code - uncomment the following line of code when ready for production
'''
#app = Flask(__name__)

#@app.route('/')
@app.route(base_url)
def home():
    return render_template('Main.html', generated=None)

#@app.route('/', methods=['POST'])
@app.route(base_url, methods=['POST'])
def home_post():
    return redirect(url_for('results'))

#@app.route('/results')
@app.route(base_url + '/results')
def results():
    return render_template('Main.html', generated=None)


#@app.route('/generate_text', methods=["POST"])
@app.route(base_url + '/generate_text', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """

    prompt = request.form['prompt']
    if prompt is not None:
        # Predict data through model
        negative_prob,class_prediction = predict_text(prompt)
        
        # make a dictionary mapping the results to relevant names
        results = {"prompt":prompt, 'Probability':str(negative_prob[0][0]), 'Label':class_prediction}
        print(results)
        

    return jsonify(results)

if __name__ == "__main__":
    '''
    coding center code
    '''
    # IMPORTANT: change the cocalcx.ai-camp.org to the site where you are editing this file.
    website_url = 'cocalc3.ai-camp.org'
    print(f"Try to open\n\n    https://{website_url}" + base_url + '\n\n')

    app.run(host = '0.0.0.0', port=port, debug=True, use_reloader=False)
    import sys; sys.exit(0)

    '''
    scaffold code
    '''
    # Only for debugging while developing
    # app.run(port=80, debug=True)
