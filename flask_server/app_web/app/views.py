# ============================ SQL  ======================================

from app import app
from flask import render_template
from flask import request  #redirect
from flask import make_response

# =========================== IMPORTS FROM MAIN ============================

# this change is done on MAIN BRANCH


import os.path
import time

# GOOGLE API DEPENDENCIES
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
from google.oauth2 import service_account

import requests
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#Defining base directory 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Joining BASE DIRECTORY AND FILE FOR THE CREDS
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "credentials.json")

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# GETTING THE DATA FROM THE INITIAL TABLE:

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1LTejK-Oo7L1bFreBIIcEZnF1W1RCC1s_jos3EuIP0jI'
SAMPLE_RANGE_NAME = 'Лист1' # for testovoe

# INITIAL TABLE (FROM TASK): 1LTejK-Oo7L1bFreBIIcEZnF1W1RCC1s_jos3EuIP0jI

# COPIED TABLE (EDITABLE): 1vVgYyBafsp8btA4BiriKIIGFs8DFEdgz7A0xDH27sII

# TABLE WITH ADDITIONAL RUB VALUES: 1Ccs96sIRbWE0l40-r30pyy-_ohp6_q6DvxrSIOMV9DQ




SAMPLE_SPREADSHEET_ID_2 = '1vVgYyBafsp8btA4BiriKIIGFs8DFEdgz7A0xDH27sII' # COPIED TABLE (EDITABLE)
SAMPLE_RANGE_NAME_2 = 'Sheet1'


import requests
import json
import string
import math
# ======================background process FOR COPYING THE DATA TO PERSONAL GOOGLE TABLE ==============
    
@app.route('/background_process_copy_data')
def background_process_copy_data():

    global api_result_list_new

    # ============================================================================================
    # ================= GETTING THE VALUES FROM THE INITIAL TABLE ================================
    # ============================================================================================



    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    #print(result)

    values = result.get('values', [])

    # GETTING THE NESTED DICTIONARY OUT FROM THE INITIAL GOOGLE TABLE
    DICT = result.items()

    # CREATING A LIST OUT OF GOOGLE API THAT WE'LL USE LATER TO INSERT DATA FROM INITIAL TABLE TO OUR ELEPHANT DATABASE
    api_result_list = list(DICT)[2][1]
    for element in api_result_list:
        print(element)


    # ==================================================================
    # ======= COPYING THE VALUES TO THE PERSONAL GOOGLE TABLE ==========
    # ==================================================================


    #service = build('sheets', 'v4', credentials=credentials)

    # The ID of the spreadsheet to update.
    #spreadsheet_id = '1Ccs96sIRbWE0l40-r30pyy-_ohp6_q6DvxrSIOMV9DQ'  # TODO: Update placeholder value.
    spreadsheet_id = '1vVgYyBafsp8btA4BiriKIIGFs8DFEdgz7A0xDH27sII' # we copy data to this table

    # The A1 notation of the values to update.
    #range_ = 'Sheet1!A4:B5'  # TODO: Update placeholder value.
    range_ = 'Sheet1'  # TODO: Update placeholder value.


    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

    #alue_range_body = {'values':[[1,2],[3,4]]}
    value_range_body = {'values':list(DICT)[2][1]}


    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, 
                                                     range=range_, 
                                                     valueInputOption=value_input_option, 
                                                     body=value_range_body)

    response = request.execute()
    print(response)
    return ('NOTHING')


@app.route('/background_process_start_script')
def background_process_start_script():

    while True:
        global api_result_list_new
        global cbr_rate

        # === GETTNG CBR RATE + ADDING DATA FROM THE PERSONAL TABLE TO ELEPHANT DATABE ==================================

        # ============================================================================================
        # ================= PART 1. GETTING THE CENTRAL BANK EXCHANGE RATE =====================
        # ============================================================================================
        
        # the page with the latest rates
        url = "https://www.cbr.ru/currency_base/daily/"


        import datetime
        from datetime import date
        #global api_result_list

        index = -1 # -1 means that we did not find the rate on the page yet
        x=0 # x = number of retries
        while index==-1: # while the page has no "Доллар" line, proceed trying

            if x<5:
                x+=1

                #page = requests.get(url, headers={"Content-Type":"application/xhtml+xml"}).content
                page = requests.get(url).content


                soup = BeautifulSoup(page,"html.parser")

                # finding the rate for 'USD' 
                # finding the position of "dollar line" in the text we got using BS
                index = str(soup).find('Доллар США') #</td><td>number</td>
                print("==== RETRIES NUMBER IS:", x , '============')
            else:
                print('MAX RETRIES EXCEEDED, COULD NOT GET FULL HTMLS PAGE')
                break

        if index!=-1:
            needed_text = str(soup)[index+14:index+35]
            index_2 = needed_text.find("<td>")
            index_3 = needed_text.find("</td>")

            # making a float number out of the string and round to 2 digits after floating point
            cbr_rate = float(needed_text[index_2+4:index_3].replace(',','.'))
        else:
            cbr_rate = 54.12345 # setting my favourite rate in case BS could not get the value

        print("Today's CBR RATE FOR USD IS:", cbr_rate)


        # ============================================================================================
        # ================= GETTING THE VALUES FROM THE ***PERSONAL*** TABLE =========================
        # ============================================================================================

        # SAMPLE_SPREADSHEET_ID_2 = 1vVgYyBafsp8btA4BiriKIIGFs8DFEdgz7A0xDH27sII
        # SAMPLE_RANGE_NAME_2 = 'Sheet1'

        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_2,
                                    range=SAMPLE_RANGE_NAME_2).execute()
        #print(result)

        values = result.get('values', [])

        # GETTING THE NESTED DICTIONARY OUT FROM THE INITIAL GOOGLE TABLE
        DICT = result.items()

        # CREATING A LIST OUT OF GOOGLE API THAT WE'LL USE LATER TO INSERT DATA FROM INITIAL TABLE TO OUR ELEPHANT DATABASE
        api_result_list = list(DICT)[2][1]
        for element in api_result_list:
            print(element)

        # ============================================================================================
        # ================= MODIFYING THE LIST WITH ROWS FOR THE DATABASE ============================
        # ============================================================================================

        # MAKING THE LIST SHORTER SINCE WE DON"T NEED THE FIRST ROW WITH COLUMN NAMES
        api_result_list.pop(0)

        # ADDING NEW VALUE TO THE LIST THAT REPRESENTS PRICE IN RUBLES 
        # AND CHANGING THE TYPE OF DATE FROM STR TO DATE


        api_result_list_new = [] # creating new list to store values
        index_for_key = 1 # defining the index for № value
        for element in api_result_list:
            if len(element)!=0: # checking that the row in the table is NOT empty
                element.insert(3, round(int(element[2])*cbr_rate,2))
                # also let's round up the value to 2 digits after floating point

                api_result_list_new.append(element)
                index_for_key +=1
            
            else: # in case the row is empty --> create empty values and proceed with the loop
                element.extend((0,0,0,0,'NONE'))
                api_result_list_new.append(element)
                index_for_key +=1
                continue

        
        print("====================FINAL LIST IS:================", api_result_list_new)


        #==============================================================
        # ======  PART 2. CONNECTING TO THE ELEPHANT DATABASE  ========
        #==============================================================


        import psycopg2
        #from config import config

        conn = None

        conn = psycopg2.connect(
                        host="tyke.db.elephantsql.com",
                        database="ibkaamrw",
                        user="ibkaamrw",
                        password="IL7gcksdhTvxqWRK-b3XPGhfvwLcDoCr")

        # CREDS FOR ELEPHANT: https://api.elephantsql.com/console/cdacc8bb-857c-4eda-883d-fd7176819475/details

        try:

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            
            # create a cursor
            cur = conn.cursor()
            
            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version for testing
            db_version = cur.fetchone()
            print(db_version)
           

            # DROPPING THE TABLE AND THEN CREATING IT IN THE ELEPHANT DB
            # we drop it cause we wanna be sure that the data is always updated
            # each time we run script

            cur.execute ("DROP TABLE elephant_orders")
            \
            cur.execute ('CREATE TABLE elephant_orders (\
                                "№" SERIAL, \
                                "заказ №" INTEGER, \
                                "стоимость,$" FLOAT,\
                                "стоимость в руб." FLOAT,\
                                "срок поставки" VARCHAR (20) NOT NULL\
                                )')\

            # cur.execute(DROP TABLE elephant_orders;\
            #     CREATE TABLE elephant_orders (\
            #             № serial, \
            #             заказ_№ integer, \
            #             стоимость_$ float,\
            #             стоимость_₽ float,\
            #             'срок поставки' VARCHAR (20) NOT NULL\
            #             ))

            # LET'S RESET PRIMARY KEY TO "1"

            cur.execute("ALTER SEQUENCE elephant_orders_№_seq RESTART WITH 1")\

            #cur.execute("SET DATESTYLE to SQL,DMY;")

            # ADDING UPDATED LIST TO THE ELEPHANT DB --> table is called elephant_orders

            for row in api_result_list_new:
                cur.execute('INSERT INTO \
                            elephant_orders ("№", "заказ №", "стоимость,$", "стоимость в руб.", "срок поставки") \
                            VALUES (%s, %s, %s, %s, %s)', 
                            row)


            # Query the database and obtain data as Python objects
            cur.execute("SELECT * FROM elephant_orders;")
            db_data = cur.fetchone()
            print("DATABASE DATA FIRST ROW:", db_data )


            # Make the changes to the database persistent

            conn.commit()

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

        #return str(cbr_rate)

        time.sleep(10)

    
        



# ===========================FLASK FIRST PAGE ===============================


@app.route("/google_api", methods=["GET", "POST"])
def google_api():

    return render_template("google_api.html")


# ========= SHOWING THE RESULTS ON THE WEB PAGE: =======================

@app.route("/google_api_result", methods=["GET", "POST"])
def google_api_result():
    first_row = []
    global api_result_list_new
    if api_result_list_new[0][0]!='№': 
    # in case this is the first display of the table - we define the first row with column names
        first_row = ['№', 'заказ №', 'стоимость, $', 'стоимость в руб.', "срок поставки"]
        api_result_list_new.insert(0, first_row)
    else:
    # otherwise:
        pass

    return render_template("google_api_result.html",
                            cbr_rate = cbr_rate,
                            api_result_list_new = api_result_list_new,
                            first_row = first_row)
    