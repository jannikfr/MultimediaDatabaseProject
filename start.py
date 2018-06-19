from flask import Flask, render_template, request
import db_connection


app = Flask(__name__)





@app.route('/', methods = ['POST', 'GET'])
def start():
    queryobject = None
    feat = None
    sim = None
    seg = None
    eigenval = None
    picanz = db_connection.get_count_images()
    return callHtmlPage(feat, sim, seg, eigenval, picanz, queryobject)




@app.route('/do_db_search', methods = ['POST', 'GET'])
def do_db_search():
    if request.method == 'POST':
        result = request.form
        queryobject = request.files
        feat = result['feature']
        seg = result['segmentation']
        sim = result['similarity']
        eigenval = result['numberEigenvalues']
        picanz = db_connection.get_count_images()
        return callHtmlPage(feat, sim, seg, eigenval, picanz, queryobject)









def callHtmlPage(feat,sim, seg, eigenanz, picanz, qo):
    return render_template('index.html', feat=feat, sim=sim, seg=seg, eigenanz=eigenanz, picanz=picanz, qo=qo)



