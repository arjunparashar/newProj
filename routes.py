from flask import Flask,render_template,request,redirect,url_for,flash

from models import db,Customer,Service,ServiceRequest,Professional

from app import app

@app.route('/home')
def index():
    return render_template('index.html')