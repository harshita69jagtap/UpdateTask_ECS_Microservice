from flask import Flask, request, redirect,jsonify, render_template
import requests
import sys, traceback

##### directory structure - 
##/root/project/updatetask.py
##/root/project/templates/base.html
##/root/project/templates/updatetask.html

###dependencies installed
### yum install -y tree python3 python3-pip
### pip3 install flask requests


app = Flask(__name__)

@app.route('/', methods=['GET']) #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
def index(): #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
    print(" HTTP GET REQUEST FROM pub-alb for health check ON PRIVATE IP - {0}".format(request.method)) #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
    return(jsonify({'status':'HEALTH CHECK FROM PUB-ALB'})) #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH

@app.route('/updatetask/<int:id>', methods=['GET','POST'])

def updatetask(id):

    if request.method == 'GET':

        try:
            r = requests.get('http://dns-name-of-priv-alb:80/dbtask', params = {'service':'updatetask','id': id})
            resp = r.json()  #converts returned json into python dict()  #resp = {'task':{'id':'','content':'date_created':''}}
            print("RECEIVED JSON RESPONSE FROM UPDATE OF DBTASK - {0} AND IT'S DATA TYPE IS - {1}".format(resp['task'],type(resp['task']))) #resp['task'] = {'content': 'Ganpati', 'date_created': '2020-10-21T03:28:29.234021', 'id': 1}
            return render_template('/updatetask.html',task = resp['task'])                                                                                           
                                         
        except Exception:
            print("EXCEPTION OCCURED IN GET /UPDATETASK/ID SERVICE")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
            return jsonify({'status':'EXCEPTION OCCURED IN GET UPDATE TASK'})

    elif request.method == 'POST':
        try:
            text = request.form.get('content')
            print("Value retrieved from form's text input post request - {0}".format(text))
            r = requests.post('http://dns-name-of-priv-alb:80/dbtask', json = {'text':text, 'service':'updatetask','id':id})
            resp = r.json()  
            print("JSON RESPONSE RECEIVED FROM POST UPDATE OF DBTASK - {0}".format(resp))
            if resp['status'] == 'updated':
                return redirect('http://dns-name-of-pub-alb:80/viewtask')
            elif resp['status'] == 'not updated':
                return jsonify({'status':'CONTENT NOT UPDATED IN TODO TABLE'})
            elif resp['status'] == 'exception':
                return jsonify({'status':'EXCEPTION OCCURED IN POST UPDATE OF DBTASK'})

        except:
            print("EXCEPTION OCCURED IN POST /UPDATETASK/ID SERVICE")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
            return jsonify({'status':'EXCEPTION OCCURED IN POST UPDATE TASK'})
            
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port='5000', debug=True)
