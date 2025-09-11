from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from io import BytesIO
import uuid
import os

app = Flask(__name__)

# ----------------------
# DATABASE CONFIGURATION
# ----------------------
# Use DATABASE_URL from environment in production, else fallback to external Render URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg2://business_visit_db_user:Q71xLb5KKA9qbnNv6yafOXym8GJc3ySU@dpg-d30m5jh5pdvs7386gq00-a.oregon-postgres.render.com:5432/business_visit_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------
# DATABASE MODEL
# ----------------------
class Visit(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID as ID
    company_name = db.Column(db.String(200))
    primary_name = db.Column(db.String(100))
    primary_position = db.Column(db.String(100))
    primary_contact = db.Column(db.String(50))
    primary_email = db.Column(db.String(100))
    secondary_name = db.Column(db.String(100))
    secondary_position = db.Column(db.String(100))
    secondary_contact = db.Column(db.String(50))
    secondary_email = db.Column(db.String(100))
    purpose = db.Column(db.String(200))
    outcome = db.Column(db.String(200))
    next_meeting = db.Column(db.String(100))
    notes = db.Column(db.Text)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ----------------------
# ROUTES
# ----------------------
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    record_id = str(uuid.uuid4())  # Unique ID
    visit = Visit(
        id=record_id,
        company_name=request.form.get("company_name"),
        primary_name=request.form.get("primary_name"),
        primary_position=request.form.get("primary_position"),
        primary_contact=request.form.get("primary_contact"),
        primary_email=request.form.get("primary_email"),
        secondary_name=request.form.get("secondary_name"),
        secondary_position=request.form.get("secondary_position"),
        secondary_contact=request.form.get("secondary_contact"),
        secondary_email=request.form.get("secondary_email"),
        purpose=request.form.get("purpose"),
        outcome=request.form.get("outcome"),
        next_meeting=request.form.get("next_meeting"),
        notes=request.form.get("notes"),
        location=request.form.get("location")
    )
    db.session.add(visit)
    db.session.commit()
    return redirect(url_for('view_records'))

@app.route('/view')
def view_records():
    visits = Visit.query.order_by(Visit.created_at.desc()).all()
    return render_template('view.html', records=visits)

@app.route('/delete/<record_id>', methods=['POST'])
def delete_record(record_id):
    visit = Visit.query.get(record_id)
    if visit:
        db.session.delete(visit)
        db.session.commit()
    return redirect(url_for('view_records'))

@app.route('/record/<record_id>')
def record_details(record_id):
    visit = Visit.query.get(record_id)
    if not visit:
        return "Record not found", 404
    return jsonify({c.name: getattr(visit, c.name) for c in visit.__table__.columns})

# ----------------------
# DOWNLOAD SINGLE RECORD
# ----------------------
@app.route('/download/<record_id>')
def download_record(record_id):
    visit = Visit.query.get(record_id)
    if not visit:
        return "Record not found", 404

    df = pd.DataFrame([{c.name: getattr(visit, c.name) for c in visit.__table__.columns}])
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        download_name=f"business_visit_{record_id}.xlsx",
        as_attachment=True
    )

# ----------------------
# DOWNLOAD ALL RECORDS
# ----------------------
@app.route('/download-all')
def download_all():
    visits = Visit.query.order_by(Visit.created_at.desc()).all()
    if not visits:
        return "No records to download", 404

    df = pd.DataFrame([{c.name: getattr(v, c.name) for c in v.__table__.columns} for v in visits])
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        download_name="all_business_visits.xlsx",
        as_attachment=True
    )

# ----------------------
# RUN APP
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
