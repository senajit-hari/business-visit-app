from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import pandas as pd 
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data.json'

# Load data from file
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/download/<record_id>')
def download_record(record_id):
    data = load_data()
    record = next((rec for rec in data if rec["id"] == record_id), None)
    if not record:
        return "Record not found", 404

    # Convert the single record into a DataFrame
    df = pd.DataFrame([record])

    # Create filename
    filename = f"business_visit_{record_id}.xlsx"
    filepath = os.path.join("downloads", filename)

    # Make downloads folder if it doesn't exist
    os.makedirs("downloads", exist_ok=True)

    # Save Excel file
    df.to_excel(filepath, index=False)

    # Send file to user
    from flask import send_file
    return send_file(filepath, as_attachment=True)


@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = load_data()

    form_data = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "company_name": request.form.get("company_name"),
        "primary_name": request.form.get("primary_name"),
        "primary_position": request.form.get("primary_position"),
        "primary_contact": request.form.get("primary_contact"),
        "primary_email": request.form.get("primary_email"),
        "secondary_name": request.form.get("secondary_name"),
        "secondary_position": request.form.get("secondary_position"),
        "secondary_contact": request.form.get("secondary_contact"),
        "secondary_email": request.form.get("secondary_email"),
        "purpose": request.form.get("purpose"),
        "outcome": request.form.get("outcome"),
        "next_meeting": request.form.get("next_meeting"),
        "notes": request.form.get("notes"),
        "location": request.form.get("location"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data.append(form_data)
    save_data(data)

    return redirect(url_for('view_records'))

@app.route('/view')
def view_records():
    data = load_data()
    return render_template('view.html', records=data)

@app.route('/delete/<record_id>', methods=['POST'])
def delete_record(record_id):
    data = load_data()
    data = [rec for rec in data if rec["id"] != record_id]
    save_data(data)
    return redirect(url_for('view_records'))

@app.route('/record/<record_id>')
def record_details(record_id):
    data = load_data()
    record = next((rec for rec in data if rec["id"] == record_id), None)
    if not record:
        return "Record not found", 404
    return jsonify(record)

@app.route('/download-all')
def download_all():
    data = load_data()
    if not data:
        return "No records to download", 404

    import pandas as pd
    df = pd.DataFrame(data)

    filename = "all_business_visits.xlsx"
    filepath = os.path.join("downloads", filename)

    os.makedirs("downloads", exist_ok=True)
    df.to_excel(filepath, index=False)

    from flask import send_file
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
