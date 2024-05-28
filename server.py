from flask import Flask, render_template, url_for, request, redirect
from flask_analytics import Analytics
import csv

app = Flask(__name__)
Analytics(app)
app.config['ANALYTICS'] = {'GAUGES': {'SITE_ID': '234599346'}}

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def index(page_name):
    return render_template(page_name)

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except Exception as err:
            # Log the error here if needed
            print(f"Error: {err}")
            return 'Did not save to database. Please try again later.'
    else:
        return 'Something went wrong. Please try again.'

if __name__ == "__main__":
    app.run(debug=True)
