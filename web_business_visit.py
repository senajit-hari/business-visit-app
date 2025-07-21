
from flask import Flask, render_template, request, jsonify, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = 'visits.csv'
FIELDNAMES = [
    "Timestamp",
    "Company Name",
    "Primary Contact Person Name",
    "Primary Contact Position",
    "Primary Contact Number",
    "Primary Email",
    "Secondary Contact Person Name",
    "Secondary Contact Position",
    "Secondary Contact Number",
    "Secondary Email",
    "Purpose of Visit",
    "Meeting Outcome",
    "Follow-up Actions",
    "Next Meeting Date",
    "Additional Notes",
    "Location"
]

# Ensure CSV exists with headers
def ensure_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

# Read all records
def read_records():
    ensure_csv()
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Write all records (overwrite)
def write_records(records):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)

@app.route('/')
def home():
    return redirect(url_for('new_entry'))

@app.route('/new-entry')
def new_entry():
    return render_template('form.html')

@app.route('/view')
def view_entries():
    data = read_records()
    return render_template('view.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        form = request.form
        record = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Company Name": form.get("company_name", "").strip(),
            "Primary Contact Person Name": form.get("primary_contact_name", "").strip(),
            "Primary Contact Position": form.get("primary_contact_position", "").strip(),
            "Primary Contact Number": form.get("primary_contact_number", "").strip(),
            "Primary Email": form.get("primary_email", "").strip(),
            "Secondary Contact Person Name": form.get("secondary_contact_name", "").strip(),
            "Secondary Contact Position": form.get("secondary_contact_position", "").strip(),
            "Secondary Contact Number": form.get("secondary_contact_number", "").strip(),
            "Secondary Email": form.get("secondary_email", "").strip(),
            "Purpose of Visit": form.get("purpose", "").strip(),
            "Meeting Outcome": form.get("outcome", "").strip(),
            "Follow-up Actions": form.get("followup", "").strip(),
            "Next Meeting Date": form.get("next_date", "").strip(),
            "Additional Notes": form.get("notes", "").strip(),
            "Location": form.get("location", "").strip()
        }
        records = read_records()
        records.append(record)
        write_records(records)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/delete', methods=['POST'])
def delete():
    try:
        data = request.get_json()
        timestamp = data.get('timestamp')
        if not timestamp:
            return jsonify(success=False, error="Missing timestamp")
        records = read_records()
        filtered = [r for r in records if r['Timestamp'] != timestamp]
        if len(records) == len(filtered):
            return jsonify(success=False, error="Record not found")
        write_records(filtered)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/get_location')
def get_location():
    # This is a dummy implementation. You would replace it with actual location fetching logic.
    # For example, using IP geolocation or browser Geolocation API in frontend.
    # Here we simulate a fixed location response.
    dummy_location = {
        "success": True,
        "location": {
            "address": "123 Business Street, Riyadh",
            "coordinates": "24.7136° N, 46.6753° E",
            "city": "Riyadh",
            "state": "Riyadh Province",
            "country": "Saudi Arabia"
        }
    }
    return jsonify(dummy_location)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = 'visits.csv'
FIELDNAMES = [
    "Timestamp",
    "Company Name",
    "Primary Contact Person Name",
    "Primary Contact Position",
    "Primary Contact Number",
    "Primary Email",
    "Secondary Contact Person Name",
    "Secondary Contact Position",
    "Secondary Contact Number",
    "Secondary Email",
    "Purpose of Visit",
    "Meeting Outcome",
    "Follow-up Actions",
    "Next Meeting Date",
    "Additional Notes",
    "Location"
]

# Ensure CSV exists with headers
def ensure_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

# Read all records
def read_records():
    ensure_csv()
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Write all records (overwrite)
def write_records(records):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)

@app.route('/')
def home():
    return redirect(url_for('new_entry'))

@app.route('/new-entry')
def new_entry():
    return render_template('form.html')

@app.route('/view')
def view_entries():
    data = read_records()
    return render_template('view.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        form = request.form
        record = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Company Name": form.get("company_name", "").strip(),
            "Primary Contact Person Name": form.get("primary_contact_name", "").strip(),
            "Primary Contact Position": form.get("primary_contact_position", "").strip(),
            "Primary Contact Number": form.get("primary_contact_number", "").strip(),
            "Primary Email": form.get("primary_email", "").strip(),
            "Secondary Contact Person Name": form.get("secondary_contact_name", "").strip(),
            "Secondary Contact Position": form.get("secondary_contact_position", "").strip(),
            "Secondary Contact Number": form.get("secondary_contact_number", "").strip(),
            "Secondary Email": form.get("secondary_email", "").strip(),
            "Purpose of Visit": form.get("purpose", "").strip(),
            "Meeting Outcome": form.get("outcome", "").strip(),
            "Follow-up Actions": form.get("followup", "").strip(),
            "Next Meeting Date": form.get("next_date", "").strip(),
            "Additional Notes": form.get("notes", "").strip(),
            "Location": form.get("location", "").strip()
        }
        records = read_records()
        records.append(record)
        write_records(records)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/delete', methods=['POST'])
def delete():
    try:
        data = request.get_json()
        timestamp = data.get('timestamp')
        if not timestamp:
            return jsonify(success=False, error="Missing timestamp")
        records = read_records()
        filtered = [r for r in records if r['Timestamp'] != timestamp]
        if len(records) == len(filtered):
            return jsonify(success=False, error="Record not found")
        write_records(filtered)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/get_location')
def get_location():
    # This is a dummy implementation. You would replace it with actual location fetching logic.
    # For example, using IP geolocation or browser Geolocation API in frontend.
    # Here we simulate a fixed location response.
    dummy_location = {
        "success": True,
        "location": {
            "address": "123 Business Street, Riyadh",
            "coordinates": "24.7136° N, 46.6753° E",
            "city": "Riyadh",
            "state": "Riyadh Province",
            "country": "Saudi Arabia"
        }
    }
    return jsonify(dummy_location)

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run()
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get PORT from env or default 5000 locally
    app.run(host='0.0.0.0', port=port)

