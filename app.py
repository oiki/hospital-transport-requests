
from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/history/<service>')
def history(service):
    transports = []
    with open('transport_requests.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Departure Service'] == service:
                transports.append(row)
    return render_template('history.html', transports=transports, service=service)

@app.route('/pending/<service>')
def pending(service):
    transports = []
    with open('transport_requests.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Departure Service'] == service and not row.get('Handled', False):
                transports.append(row)
    return render_template('pending.html', transports=transports, service=service)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    dob = request.form['dob']
    appointment_location = request.form['appointment_location']
    appointment_date = request.form['appointment_date']
    appointment_time = request.form['appointment_time']
    room_number = request.form['room_number']
    departure_service = request.form['departure_service']
    
    # Here you can process the data, e.g., store it in a database or a file
    # Path to the CSV file
    csv_file = 'transport_requests.csv'
    
    # Check if the file exists
    file_exists = os.path.isfile(csv_file)
    
    # Write the data to the CSV file
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write the header if the file does not exist
            writer.writerow(['Name', 'Date of Birth', 'Appointment Location', 'Appointment Date', 'Appointment Time', 'Room Number', 'Departure Service'])
        writer.writerow([name, dob, appointment_location, appointment_date, appointment_time, room_number, departure_service])
    
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(port=5000)
