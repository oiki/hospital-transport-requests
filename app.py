
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

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
    # For now, we'll just print it to the console
    print(f"Name: {name}")
    print(f"Date of Birth: {dob}")
    print(f"Appointment Location: {appointment_location}")
    print(f"Appointment Date: {appointment_date}")
    print(f"Appointment Time: {appointment_time}")
    print(f"Room Number: {room_number}")
    print(f"Departure Service: {departure_service}")
    
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(port=5000)
