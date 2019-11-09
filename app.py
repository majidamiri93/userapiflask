from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bozkurt/Desktop/login-register-form/database.db'


@app.route('/')
def hello_world():
    return 'hellllloo majid agha khan asdasd 1398'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
