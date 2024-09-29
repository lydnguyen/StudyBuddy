import json

from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Route to display the HTML form
@app.route('/')
def form():
    html_file = os.path.join(os.getcwd(), 'templates', 'timeslotreminder.html')
    with open(html_file,'r') as f:
        html = f.read()
        f.close()
    return render_template_string(html)


@app.route('/submit', methods=['POST'])
def submit():
    # Get the user input from text fields and message
    all_reminders = request.form.get('all_reminders')
    print(json.dumps(all_reminders, indent=4))



def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()