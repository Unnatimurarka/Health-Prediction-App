from gemini_service import generate_health_prediction
from flask import Flask, render_template, request, redirect, url_for
from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Import models AFTER db initialization
from datetime import datetime
from models import Patient

@app.route("/")
def home():

    patients = Patient.query.all()

    return render_template(
        "index.html",
        patients=patients
    )

@app.route("/add", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        full_name = request.form["full_name"]

        date_of_birth = datetime.strptime(
            request.form["date_of_birth"],
            "%Y-%m-%d"
        ).date()

        email = request.form["email"]

        glucose = float(request.form["glucose"])

        haemoglobin = float(request.form["haemoglobin"])

        cholesterol = float(request.form["cholesterol"])

        remarks = generate_health_prediction(
            glucose,
            haemoglobin,
            cholesterol
        )

        patient = Patient(
            full_name=full_name,
            date_of_birth=date_of_birth,
            email=email,
            glucose=glucose,
            haemoglobin=haemoglobin,
            cholesterol=cholesterol,
            remarks=remarks
        )

        db.session.add(patient)

        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add_patient.html")

@app.route("/delete/<int:id>")
def delete_patient(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)

    db.session.commit()

    return redirect(url_for("home"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):

    patient = Patient.query.get_or_404(id)

    if request.method == "POST":

        patient.full_name = request.form["full_name"]

        patient.date_of_birth = datetime.strptime(
            request.form["date_of_birth"],
            "%Y-%m-%d"
        ).date()

        patient.email = request.form["email"]

        patient.glucose = float(request.form["glucose"])
        patient.haemoglobin = float(request.form["haemoglobin"])
        patient.cholesterol = float(request.form["cholesterol"])

        try:
            patient.remarks = generate_health_prediction(
                patient.glucose,
                patient.haemoglobin,
                patient.cholesterol
            )
        except Exception:
            patient.remarks = "AI prediction unavailable."

        db.session.commit()

        return redirect(url_for("home"))

    return render_template(
        "edit_patient.html",
        patient=patient
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)