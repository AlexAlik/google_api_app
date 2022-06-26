Hello!

INSTRUCTIONS FOR STARTING THIS APP:

1) download the archive "google_api_app", unzip archive
2) navigate to your shell
3) install packages from requirements.txt using the following commands:
  
  ---> cd into the directory where the file "requirements.txt" is located after you unzip the archive "google_api_app":\
  cd YOUR_FOLDER/google_api_app/flask_server/app_web
  ---> activate the virtualenv with command: \
  source env/bin/activate \
  ---> install required packages: \
  pip3 install -r requirements.txt
  
4) once the dependencies are installed, cd into the app folder, activate the VENV and run FLASK app:

cd Your_Folder/google_api_app/flask_server/app_web\
export FLASK_APP=app.py\
export FLASK_ENV=development\
source env/bin/activate\
flask run

====== you'll see something like this: ========= \
 * Serving Flask app 'app.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 135-035-974 \
================================================== \

5) navigate in your browser to the URL: http://localhost:5000/google_api
6) great! now you can push buttons

Available Buttons After the FLASK app started: \
1) "COPY INITIAL GOOGLE DATA" \
Once you click it, data from TESTOVOE table will be copied to the PERSONAL TABLE. \
2) "START CONTINIOUS SCRIPT" \
Once you click this button - you'll activate script which will get the data from Personal Table and add it to the Elephant DB  with additional column.
The script will run continiously each 10 seconds.
3) "RUN"  \
Once you click it, the table with resulting data will be generated and shown on the webpage.
Update the page in order to show updated results as you change the data in the PERSONAL TABLE.

Additional Comments:

THis app will:
1) get the data from the table located here:
https://docs.google.com/spreadsheets/d/1LTejK-Oo7L1bFreBIIcEZnF1W1RCC1s_jos3EuIP0jI/edit?usp=sharing
2) copy the data to the personal table located here:
https://docs.google.com/spreadsheets/d/1vVgYyBafsp8btA4BiriKIIGFs8DFEdgz7A0xDH27sII/edit#gid=0
3) Get the CBR usd rate 
4) Update the DataBase table called "elephant_orders" hosted by "elephantsql.com" with the new column "стоимость в руб."
5) Show the resulting table on a web page.


