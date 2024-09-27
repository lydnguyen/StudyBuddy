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
    user_data = {
        "reminder-date": request.form.get('reminder-date'),
        "day_week": request.form.get('day_week'),
        "reminder-time": request.form.get('reminder-time')
    }

    # Get the checkbox values; we use getlist() to retrieve multiple checkbox values
    interests = request.form.getlist('products')
    response_1 = f'''
                <h1>Form Submitted Successfully</h1>
                <p><strong>reminder date:</strong> {user_data['reminder-date']}</p>
                <p><strong>week days:</strong> {user_data['day_week']}</p>
                <p><strong>Interests:</strong> {', '.join(interests) if interests else 'None'}</p>
                <p><strong>reminder time:</strong> {user_data['reminder-time']}</p>
                
                <button id="close-btn">Close</button>
                <br><br><a href="/">Go back to form</a>'''
    response_2 = '''
                <script>
                        const CloseBtn = document.getElementById('close-btn');
                        // Close functionality
                        CloseBtn.addEventListener('click', function() {
                            const confirmed = confirm("Are you sure you want to confirm and close the window?");
                            if (confirmed) {
                                window.close();
                                if (!window.closed) {
                                    alert("Window cannot be closed automatically. Please close the window manually.");
                                }
                            }
                        });
                </script>
            '''
    return response_1+response_2


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()