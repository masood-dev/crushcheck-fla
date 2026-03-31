import os

from flask import Flask, jsonify, render_template, request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

from flames_app.database import init_db, create_note, get_note, verify_password, cleanup_expired_notes

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024

MAX_MESSAGE_LENGTH = 500
MAX_SENDER_NAME_LENGTH = 30
MAX_NAME_LENGTH = 50
MIN_PASSWORD_LENGTH = 4

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri='memory://',
    default_limits=['120 per hour']
)

init_db()
cleanup_expired_notes()

ZODIAC_SIGNS = {
    "Aries": {"element": "Fire", "date": "Mar 21 - Apr 19"},
    "Taurus": {"element": "Earth", "date": "Apr 20 - May 20"},
    "Gemini": {"element": "Air", "date": "May 21 - Jun 20"},
    "Cancer": {"element": "Water", "date": "Jun 21 - Jul 22"},
    "Leo": {"element": "Fire", "date": "Jul 23 - Aug 22"},
    "Virgo": {"element": "Earth", "date": "Aug 23 - Sep 22"},
    "Libra": {"element": "Air", "date": "Sep 23 - Oct 22"},
    "Scorpio": {"element": "Water", "date": "Oct 23 - Nov 21"},
    "Sagittarius": {"element": "Fire", "date": "Nov 22 - Dec 21"},
    "Capricorn": {"element": "Earth", "date": "Dec 22 - Jan 19"},
    "Aquarius": {"element": "Air", "date": "Jan 20 - Feb 18"},
    "Pisces": {"element": "Water", "date": "Feb 19 - Mar 20"}
}

ELEMENT_COMPATIBILITY = {
    "same": 88,
    frozenset(["Fire", "Air"]): 82,
    frozenset(["Earth", "Water"]): 80,
    frozenset(["Fire", "Earth"]): 70,
    frozenset(["Water", "Air"]): 68,
    frozenset(["Fire", "Water"]): 62,
    frozenset(["Earth", "Air"]): 64
}


@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com data:; "
        "img-src 'self' data: https:; "
        "connect-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'"
    )
    if request.is_secure:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


def clean_text(value, max_length):
    if value is None:
        return ''
    return str(value).strip()[:max_length]

def calculate_flames(name1, name2):
    name1_list = list(name1.lower().replace(" ", ""))
    name2_list = list(name2.lower().replace(" ", ""))
    
    # Remove matching characters
    for char in name1_list[:]:
        if char in name2_list:
            name1_list.remove(char)
            name2_list.remove(char)
            
    count = len(name1_list) + len(name2_list)
    
    if count == 0:
        return "No Characters Left", "Try with different names!"
        
    result_list = ['Friendship', 'Love', 'Affection', 'Marriage', 'Enemy', 'Siblings']
    
    while len(result_list) > 1:
        split_index = (count % len(result_list)) - 1
        
        if split_index >= 0:
            right = result_list[split_index + 1:]
            left = result_list[:split_index]
            result_list = right + left
        else:
            result_list = result_list[:len(result_list) - 1]
            
    return result_list[0], f"Your relationship is {result_list[0]}!"

def normalize_sign(sign):
    if not sign:
        return None
    cleaned = sign.strip().lower()
    for name in ZODIAC_SIGNS:
        if cleaned == name.lower():
            return name
    return None

def calculate_zodiac_compatibility(sign1, sign2):
    element1 = ZODIAC_SIGNS[sign1]["element"]
    element2 = ZODIAC_SIGNS[sign2]["element"]

    if element1 == element2:
        score = ELEMENT_COMPATIBILITY["same"]
    else:
        score = ELEMENT_COMPATIBILITY.get(frozenset([element1, element2]), 70)

    if score >= 85:
        vibe = "Cosmic Match"
        insight = f"{element1} and {element2} energy blends with ease and spark."
    elif score >= 75:
        vibe = "Magnetic Glow"
        insight = f"{element1} meets {element2} with a warm, steady pull."
    elif score >= 65:
        vibe = "Sweet Sync"
        insight = f"{element1} and {element2} balance each other when you lean in."
    elif score >= 55:
        vibe = "Curious Chemistry"
        insight = f"{element1} and {element2} need a little extra patience to align."
    else:
        vibe = "Learning Curve"
        insight = f"{element1} and {element2} move differently, but growth is possible."

    return score, vibe, insight


@app.errorhandler(429)
def handle_rate_limit(_error):
    return jsonify({'error': 'Too many requests. Please slow down and try again shortly.'}), 429

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/flames')
def flames_calculator():
    return render_template('flames.html')

@app.route('/zodiac')
def zodiac_compatibility():
    return render_template('zodiac.html', signs=ZODIAC_SIGNS)

@app.route('/secret-admirer')
def secret_admirer():
    return render_template('secret_admirer.html')

@app.route('/create-note', methods=['POST'])
@limiter.limit('10 per hour')
def create_secret_note():
    data = request.get_json(silent=True) or {}
    message = clean_text(data.get('message'), MAX_MESSAGE_LENGTH)
    password = str(data.get('password') or '').strip()
    sender_name = clean_text(data.get('sender_name') or 'Someone', MAX_SENDER_NAME_LENGTH)
    
    if not message or not password:
        return jsonify({'error': 'Message and password are required'}), 400
    
    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify({'error': f'Message too long (max {MAX_MESSAGE_LENGTH} characters)'}), 400

    if len(password) < MIN_PASSWORD_LENGTH:
        return jsonify({'error': f'Password must be at least {MIN_PASSWORD_LENGTH} characters long'}), 400

    if not sender_name:
        sender_name = 'Someone'
    
    note_id = create_note(message, password, sender_name)
    note_path = url_for('view_note', note_id=note_id)
    
    return jsonify({
        'success': True,
        'note_id': note_id,
        'note_path': note_path
    })

@app.route('/note/<note_id>')
def view_note(note_id):
    note = get_note(note_id)
    
    if not note:
        return render_template('note_not_found.html'), 404
    
    return render_template('view_note.html', note_id=note_id)

@app.route('/unlock-note', methods=['POST'])
@limiter.limit('5 per minute')
def unlock_note():
    data = request.get_json(silent=True) or {}
    note_id = clean_text(data.get('note_id'), 64)
    password = str(data.get('password') or '').strip()
    
    if not note_id or not password:
        return jsonify({'error': 'Missing data'}), 400
    
    if verify_password(note_id, password):
        note = get_note(note_id)
        return jsonify({
            'success': True,
            'message': note['message'],
            'sender_name': note['sender_name'],
            'view_count': note['view_count']
        })
    else:
        return jsonify({'success': False, 'error': 'Incorrect password'}), 401

@app.route('/calculate', methods=['POST'])
@limiter.limit('30 per minute')
def calculate():
    data = request.get_json(silent=True) or {}
    name1 = clean_text(data.get('name1'), MAX_NAME_LENGTH)
    name2 = clean_text(data.get('name2'), MAX_NAME_LENGTH)
    
    if not name1 or not name2:
        return jsonify({'error': 'Both names are required'}), 400
        
    result, message = calculate_flames(name1, name2)
    return jsonify({'result': result, 'message': message})

@app.route('/zodiac-check', methods=['POST'])
@limiter.limit('30 per minute')
def zodiac_check():
    data = request.get_json(silent=True) or {}
    sign1_raw = data.get('sign1')
    sign2_raw = data.get('sign2')

    sign1 = normalize_sign(sign1_raw)
    sign2 = normalize_sign(sign2_raw)

    if not sign1 or not sign2:
        return jsonify({'error': 'Both zodiac signs are required'}), 400

    score, vibe, insight = calculate_zodiac_compatibility(sign1, sign2)
    return jsonify({
        'sign1': sign1,
        'sign2': sign2,
        'element1': ZODIAC_SIGNS[sign1]['element'],
        'element2': ZODIAC_SIGNS[sign2]['element'],
        'score': score,
        'vibe': vibe,
        'insight': insight
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
