# import pymysql
# pymysql.install_as_MySQLdb()

from flask import Flask

app = Flask(__name__)
# from flask_mysqldb import MySQL



@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'


# from sqlalchemy import Column, String, Integer, Date

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# ORM

# engine = create_engine('mysql://reporting:faethoh1Choogeiquaki@mysql-mt4-prod-02.int.fx24.bz/live_prod')
# Session = sessionmaker(bind=engine)

# Base = declarative_base()

# app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql-mt4-prod-02.int.fx24.bz'
#
# app.config ['SQLALCHEMY_DATABASE_URI'] = \
#     'mysql://reporting:faethoh1Choogeiquaki@mysql-mt4-prod-02.int.fx24.bz/live_prod'
# # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_connecting_to_database.htm
#
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from app import views

if __name__ == "__main__":
    app.run(debug=True)

