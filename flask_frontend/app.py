from flask import Flask,render_template,request,redirect,url_for
import requests
from scan import post_vulns
app = Flask(__name__)

STAGING_URL = "http://localhost:8000/"
STAGING_USERNAME = 'Likhith'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    """
    Get JWT Token and store it in session
    """
    return render_template('login.html')

@app.route('/start',methods=["GET","POST"])
def start_project():
    """
    Intermediary screen to start a new project for the user
    """
    if request.method == "POST":
        return render_template('start_proj.html',scope=request.form['scope'])
    return render_template('start_proj.html')

@app.route('/initiate_project',methods=["GET","POST"])
def initiate_project():
    """
    Make request to create a project and create project for current user.
    """
    project_details_dict = {'scope':request.form['scope'],'app_name':request.form['appname']}
    print(STAGING_URL+'user/'+STAGING_USERNAME+"/project")
    data = requests.post(STAGING_URL+'user/'+STAGING_USERNAME+"/project",json = project_details_dict)
    post_vulns(int(data.text))
    return redirect(url_for('projects'))

    

@app.route('/projects')
def projects():
    """
    Display list of all projects with links to said projects
    """

    data = requests.get(STAGING_URL+'user/'+STAGING_USERNAME+"/project")
    print(data.json()[0])
    return render_template('projects.html',data = data.json())

@app.route('/project/<int:id>')
def project(id):
    """
    Display list of all vulnerabilities
    """
    print(STAGING_URL+'user/'+str(id)+'/'+"vulnerabilities")
    data = requests.get(STAGING_URL+'user/'+str(id)+'/'+"vulnerabilities")
    print(data.json())
    return render_template('project.html',data = data.json())

@app.route('/vulnerability/<int:id>')
def vulnerability(id):
    """
    Display vulnerability details
    """
    data = requests.get(STAGING_URL+"vulnerabilities/"+str(id))
    return render_template('vuln.html',vuln = data.json())

if __name__ == "__main__":
    app.run(debug=True)