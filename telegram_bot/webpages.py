from flask import Flask, request, render_template_string, jsonify
import os
import json

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
    user_data = {
        "chat_id": request.form.get('chat-info'),
        "all_reminders": json.loads(request.form.get('all_reminders')),
    }
    reminders = []
    for reminder in user_data['all_reminders']:
        days = reminder['days'].split(',')
        topics = reminder['products'].split(',')
        rem = {
            'id': reminder['id']
            , 'week_days': days
            , 'topics': topics
            , 'reminder_time': reminder['time']
            , 'reminder_end_dt': reminder['date']
        }
        reminders.append(rem)

    user_data['reminders'] = reminders
    del user_data['all_reminders']

    return jsonify({'success': True, 'data':user_data}), 200

def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()