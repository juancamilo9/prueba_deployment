from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date, datetime


class Appointment:

    def __init__(self, data):
        self.id = data['id']
        self.task = data['task']
        self.date = data['date']
        self.status = data['status']
        self.created_at = ['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO appointments (task,date,status,user_id) VALUES (%(task)s, %(date)s, %(status)s,%(user_id)s);"
        result = connectToMySQL('appointments').query_db(query, data)
        return result

    @classmethod
    def show_all(cls, data):
        query = "SELECT * FROM appointments join users on users.id = appointments.user_id where users.id = %(id)s;"
        results = connectToMySQL('appointments').query_db(query, data)  # Lista de diccionarios
        appointments = []
        for x in results:
            appointments.append(cls(x))

        return appointments

    @classmethod
    def show_appointment_missed(cls, data):
        query = "SELECT * FROM appointments left join users on users.id = appointments.user_id where users.id = %(id)s and status = 'Missed';"
        results = connectToMySQL('appointments').query_db(query, data)  # Lista de diccionarios
        appointments = []
        for x in results:
            appointments.append(cls(x))

        return appointments

    @classmethod
    def get_appointment(cls, data):
        query = "select * from appointments where id = %(id)s"
        result = connectToMySQL('appointments').query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE appointments SET task=%(task)s, date=%(date)s, status=%(status)s, user_id=%(user_id)s where id = %(id)s"
        result = connectToMySQL('appointments').query_db(query, data)
        return result

    @classmethod
    def delete(cls, formulario):  # Recibe formulario con id de receta a borrar
        query = "DELETE FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('appointments').query_db(query, formulario)
        return result

    @staticmethod
    def validate_appointment(data):
        today = datetime.now()
        is_valid = True
        if len(data['task']) < 3:
            flash('The Task to have more than three characters', 'appointments')
            is_valid = False
        date_today = datetime.strptime(data['date'], '%Y-%m-%d')
        print(date_today)
        print(today)
        if date_today <= today:
            flash('The date cannot be before today', 'appointments')
            is_valid = False

        if data['status'] == "":
            flash('The State must not be empty', 'appointments')
            is_valid = False

        return is_valid





