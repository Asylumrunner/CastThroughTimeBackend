from flask import Flask
from flask_cors import CORS
from get_sets import download_sets_from_s3, download_sets_from_scryfall
from get_cards import read_cards_file

app = Flask(__name__)
CORS(app)

@app.route("/")
def health_check():
    return "Live!"

@app.route("/sets", methods=['GET'])
def get_sets():
    #try:
    return download_sets_from_s3()
    
    #except Exception as e:
    #    err_resp = ("An error occured when trying to get set data: " + str(e), 500)
    #    return err_resp

@app.route("/cards", methods=['GET'])
def get_cards(): 
    try:
        return read_cards_file()
    
    except Exception as e:
        err_resp = ("An error occured when trying to get card data: " + str(e), 500)
        return err_resp
    
@app.route("/update", methods=['GET'])
def update_s3():
    return download_sets_from_scryfall()

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)