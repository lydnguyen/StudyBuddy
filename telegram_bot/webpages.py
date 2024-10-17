from flask import Flask, request, render_template_string, jsonify
import os
import json
from _access_source import GetData
import logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
)


app = Flask(__name__)

def get_topics_display_by_userid(userid):
    parser = GetData()
    topics = parser.gettopicsbyrights(userid)
    return topics

# Route to display the HTML form
@app.route('/')
def form():
    html_file = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'templates', 'timeslotreminder.html')
    if 'telegram_bot' in html_file:
        html_file = html_file.replace('/telegram_bot','')
    with open(html_file,'r') as f:
        html = f.read()
        f.close()
    return render_template_string(html)

@app.route('/get_topics', methods=['POST'])
def get_topics():
    # Get the chat ID sent from the frontend
    chat_id = request.get_json()
    userid = chat_id.get('chat_id')
    logging.info(f'Retrieve topics for User {userid}')  # Log the received user id
    if userid is None or userid=='':
        userid = '23'
    topics = get_topics_display_by_userid(userid)['quizlevel'].unique().tolist()
    return jsonify(topics)

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
    logging.info(f'Success update for {user_data}')
    # return jsonify({'success': True, 'data':user_data}), 200
    return 200

def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()