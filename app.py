import os
from flask import Flask, render_template, request, redirect, url_for, flash
import database

app = Flask(__name__)
# Secret key for session/flash messaging if needed
app.secret_key = 'our-magical-dreamy-blue-secret-key'

# Centralized personal names and settings - easily customizable in one single place
APP_CONFIG = {
    'site_title': 'Our Little New Beginning ♡',
    'partner_name': 'Swikriti',
    'nickname': 'Sweetu',
    'pet_name': 'Swituu',
    'year': '2026'
}

# Ensure database table is created on startup
database.init_db()

@app.context_processor
def inject_global_data():
    """Make the personalized name and website title available across all Jinja2 templates."""
    return APP_CONFIG

# PAGE 1: WELCOME (/)
@app.route('/')
def index():
    return render_template('index.html')

# PAGE 2: APOLOGY (/apology)
@app.route('/apology')
def apology():
    # Fetch latest response if user has already chosen one
    latest = database.get_latest_response()
    return render_template('apology.html', latest_response=latest)

# POST: SAVE RESPONSE (/save-response)
@app.route('/save-response', methods=['POST'])
def save_response():
    selected_choice = request.form.get('choice', '').strip()
    
    # Validate and save to SQLite
    success = database.save_response(selected_choice)
    if success:
        # Redirect directly to the magical gate with notification
        return redirect(url_for('gate', answered=1))
    
    # If invalid choice, redirect back to apology page
    return redirect(url_for('apology'))

# PAGE 3: MAGICAL OPENING GATE (/gate)
@app.route('/gate')
def gate():
    answered = request.args.get('answered', default=0, type=int)
    latest = database.get_latest_response()
    return render_template('gate.html', answered=answered, latest_response=latest)

# PAGE 4: A NEW BEGINNING (/beginning)
@app.route('/beginning')
def beginning():
    return render_template('beginning.html')

# PAGE 5: LITTLE THINGS FOR YOU (/little-things)
@app.route('/little-things')
def little_things():
    return render_template('little_things.html')

# PAGE 6: FINAL MESSAGE (/final)
@app.route('/final')
def final():
    return render_template('final.html')

if __name__ == '__main__':
    # Use PORT from environment (required for Render) or default to 5000 locally
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(host='0.0.0.0', port=port, debug=debug)
