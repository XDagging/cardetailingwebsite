from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
import requests

import os
from flask_bootstrap import Bootstrap



import smtplib, ssl



SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)
service_options = ("Full Detail","Interior Detail","Exterior Detail")
yes_no = ("Yes","No")

class AppointmentForm(FlaskForm):
  name = StringField(label="Name:", validators=[DataRequired()])
  address = StringField(label="Address:", validators=[DataRequired()])
  phone_number = StringField(label="Phone number:", validators=[DataRequired()])
  email = StringField(label="Email", validators=[DataRequired()])
  type_of_car = StringField(label="Type of car (ex. Sedan):", validators=[DataRequired()])
  service = SelectField(label="Service:", validators=[DataRequired()], choices=service_options)
  car_material = SelectField(label="Is the Car seat interior made of leather:", validators=[DataRequired()], choices=yes_no)
  submit = SubmitField(label="Submit")
  



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/book_an_appointment", methods=["GET","POST"])
def booking_an_appointment():
    appointment_form = AppointmentForm()
    if appointment_form.validate_on_submit():
      c_name = appointment_form.name.data
      c_email = appointment_form.email.data
      c_address = appointment_form.address.data
      c_phone = appointment_form.phone_number.data
      c_type_of_car = appointment_form.type_of_car.data
      c_service = appointment_form.service.data
      c_car_material = appointment_form.car_material.data
      sender='noreplypython0@gmail.com' 
      
      port = 587  # For starttls
      smtp_server = "smtp.gmail.com"
      sender_email = "noreplypython0@gmail.com"
      receiver_email = "maracuchoamericano@gmail.com"
      password = "dielepwyvzykhvti"
      message = f"A new customer has signed up for your service. Here are the details. Name. {c_name}\n Email. {c_email}\n Address. {c_address}\n Phone Number. {c_phone}\n Type of car. {c_type_of_car}\n Service Requested. {c_service}\n Car seat material. {c_car_material}"

      context = ssl.create_default_context()
      with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo() 
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg=message)

      return render_template("success.html")
    return render_template("book.html", form=appointment_form)







app.run(host='0.0.0.0', debug=True)
