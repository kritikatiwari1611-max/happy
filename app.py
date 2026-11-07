import os
from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)
app.secret_key = 'our-magical-dreamy-blue-secret-key'

# Centralized personal names and settings
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

# SCREEN 1: A MYSTERIOUS WELCOME (/)
@app.route('/')
def index():
    return render_template('index.html')

# SCREEN 2: A LITTLE MESSAGE / PAUSE (/moment)
@app.route('/moment')
def moment():
    return render_template('moment.html')

# SCREEN 3: THE APOLOGY LETTER (/letter or /apology)
@app.route('/letter')
@app.route('/apology')
def letter():
    return render_template('letter.html')

# SCREEN 4: THE MAGICAL GATE (/gate)
@app.route('/gate')
def gate():
    return render_template('gate.html')

# SCREEN 5: SECOND-CHANCE & MEMORIES (/surprise or /beginning)
@app.route('/surprise')
@app.route('/beginning')
def surprise():
    latest = database.get_latest_response()
    return render_template('surprise.html', latest_response=latest)

# POST: SAVE RESPONSE (/save-response)
@app.route('/save-response', methods=['POST'])
def save_response():
    selected_choice = request.form.get('choice', '').strip()
    
    # Save response and timestamp to SQLite
    success = database.save_response(selected_choice)
    if success:
        # maybe -> redirect to /little-things
        if selected_choice in ['maybe', "Maybe We Can Try Again ♡", "I'm Willing to Try ♡"]:
            return redirect(url_for('little_things'))
        # more_time -> redirect to /final
        elif selected_choice in ['more_time', "I Need More Time", "I Need Some Time"]:
            return redirect(url_for('final'))
    
    # Fallback to surprise page if unrecognized
    return redirect(url_for('surprise'))

# NEW EXTENDED PAGE: LITTLE THINGS FOR YOU (/little-things)
@app.route('/little-things')
def little_things():
    return render_template('little_things.html')

# FINAL THANK YOU PAGE (/final or /thank-you)
@app.route('/thank-you')
@app.route('/final')
def final():
    latest = database.get_latest_response()
    return render_template('final.html', latest_response=latest)

if __name__ == '__main__':
    # Use PORT from environment (for Render) or default to 5000 locally
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(host='0.0.0.0', port=port, debug=debug)
