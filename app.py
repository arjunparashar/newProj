from flask import Flask, render_template, request, url_for, flash,session
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

#Local import for model
from models import db, Customer, Professional, Service, ServiceRequest

#Instance relative config is very important
app = Flask(__name__, instance_relative_config=True)

adminuser='admin'
adminpass='admin'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

#Why not instantiate app with db why not the other way around?
db.init_app(app)


#This creates the tables in the db
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customerdashboard')
def customerdashboard():
    if 'user_id' not in session:
        flash('Please Login to Continue')
        return redirect(url_for('login'))

    return render_template('customerdashboard.html',customer=Customer.query.get(session['user_id']))

@app.route('/professionaldashboard')
def professionaldashboard():
    if 'user_id' not in session:
        flash('Please Login to Continue')
        return redirect(url_for('login'))
    return render_template('professionaldashboard.html',professional=Professional.query.get(session['user_id']))

@app.route('/professionaldashboard/search')
def professionaldashboard_search():
    if 'user_id' not in session:
        flash('Please Login to Continue')
        return redirect(url_for('login'))
    return render_template('professionaldashboardsearch.html',professional=Professional.query.get(session['user_id']))

@app.route('/professional/summary')
def pro_summary():
    return render_template('professionalsummary.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    if username=='' or password == '':
        flash('Username or Password can not be Empty')
        return redirect(url_for('custlogin_process'))
    if username==adminuser or password == adminpass:
        print('admin login')
        return redirect(url_for('admin_dashboard'))
    print('not null')
    customer=Customer.query.filter_by(username=username).first()
    if not customer:
        professional=Professional.query.filter_by(username=username).first()
        if not professional:
            flash('No Account Found, Please Register')
            return redirect(url_for('login'))
        if not professional.check_password(password):
            flash('Incorrect Password')
            return redirect(url_for('login'))
        session['user_id'] = professional.id
        return redirect(url_for('professionaldashboard'))
    if not customer.check_password(password):
        flash('Incorrect Password')
        return redirect(url_for('login'))
    print('Correct Password')
    session['user_id']=customer.id
    return redirect(url_for('customerdashboard'))


@app.route('/registerCustomer')
def register_customer():
    return render_template('registerCustomer.html')

@app.route('/registerCustomer' , methods=['POST'])
def register_customer_post():
    username=request.form.get('username')
    password=request.form.get('password')
    name=request.form.get('name')
    address=request.form.get('address')
    pincode = request.form.get('pincode')
    if username=='' or password == '':
        flash('Username or Password can not be Empty')
        return redirect(url_for('register_customer'))
    if Customer.query.filter_by(username=username).first():
        flash('User with this username Already Exists, Please Choose another Username')
        return redirect(url_for('register_customer'))
    customer=Customer(username=username,passhash=generate_password_hash(password),name=name,address=address,pincode=pincode)
    db.session.add(customer)
    db.session.commit()
    flash('Customer Successfully Registered.')
    return redirect(url_for('customerlogin'))

@app.route('/registerProfessional')
def register_professional():
    return render_template('registerProfessional.html')

@app.route('/registerProfessional' , methods=['POST'])
def register_professional_post():
    username=request.form.get('username')
    password=request.form.get('password')
    name=request.form.get('name')
    servicetype=request.form.get('servicetype')
    description=request.form.get('description')
    experience=request.form.get('experience')
    if username=='' or password == '':
        flash('Username or Password can not be Empty')
        return redirect(url_for('register_professional'))
    if Professional.query.filter_by(username=username).first():
        flash('User with this username Already Exists, Please Choose another Username')
        return redirect(url_for('register_professional'))
    professional = Professional(username=username, passhash=generate_password_hash(password), name=name, servicetype=servicetype, description=description,experience=experience)
    db.session.add(professional)
    db.session.commit()
    flash('Professional Successfully Registered.')
    return redirect(url_for('login'))


    @app.route('/logout')
    def logout():
        session.pop('user_id',None)

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admindashboard.html')

@app.route('/admin/dashboard/search')
def admin_dashboard_search():
    return render_template('admindashboardsearch.html')

@app.route('/admin/summary')
def admin_summary():
    return render_template('adminsummary.html')

if __name__ == '__main__':


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '2Y2974132HRDIUEWHD932RYD98H32D28CE2DBJHIFC2ECHIUDBEQWHIWD32CH2'
    app.run(debug = True)
