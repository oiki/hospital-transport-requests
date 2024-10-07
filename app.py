
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

@app.route('/regulation')
def regulation():
    transports = []
    with open('transport_requests.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transports.append(row)
    return render_template('regulation.html', transports=transports)

@app.route('/assign_transporter', methods=['POST'])
def assign_transporter():
    name = request.form['name']
    dob = request.form['dob']
    transporter = request.form['transporter']
    
    # Lire les données existantes
    transports = []
    with open('transport_requests.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transports.append(row)
    
    # Mettre à jour le transporteur attribué
    for transport in transports:
        if transport['Name'] == name and transport['Date of Birth'] == dob:
            transport['Transporter'] = transporter
    
    # Écrire les données mises à jour
    with open('transport_requests.csv', mode='w', newline='') as file:
        fieldnames = ['Name', 'Date of Birth', 'Appointment Location', 'Appointment Date', 'Appointment Time', 'Room Number', 'Departure Service', 'Transporter']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transports)
    
    return redirect(url_for('regulation'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('transporter_dashboard', username=username))
    
    # Read the list of transporters from the CSV file
    transporters = set()
    with open('transport_requests.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'Transporter' in row and row['Transporter']:
                transporters.add(row['Transporter'])
    
    return render_template('login.html', transporters=transporters)

@app.route('/transporter/<username>')
def transporter_dashboard(username):
    transports = []
    with open('transport_requests.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get('Transporter') == username:
                transports.append(row)
    return render_template('transporter_dashboard.html', transports=transports, username=username)

@app.route('/transporter/<username>/history')
def transporter_history(username):
    transports = []
    with open('transport_requests.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get('Transporter') == username and row.get('Status') == 'Completed':
                transports.append(row)
    return render_template('transporter_history.html', transports=transports, username=username)

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
