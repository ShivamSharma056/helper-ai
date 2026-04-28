from flask import Flask, render_template, request, jsonify, session, send_file
from flask_bcrypt import Bcrypt
import os, uuid, json, datetime
from functools import wraps
from db import db, User, Document, SharedDocument
from ai_engine import generate_ppt, generate_report, generate_notes

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'helperai-secret-2025')
# ✅ New — forces PostgreSQL on Vercel, SQLite only for local dev
database_url = os.environ.get('DATABASE_URL', 'sqlite:///helperai.db')
# Fix for older postgres URLs (Neon uses postgresql://)
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

db.init_app(app)
bcrypt = Bcrypt(app)

# ── Auth decorator ──────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

# ── Pages ────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return render_template('login.html')
    return render_template('dashboard.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('login.html')

# ── Health Check ─────────────────────────────────────────────────
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.utcnow().isoformat()})

# ── Auth API ─────────────────────────────────────────────────────
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'error': 'Name, email and password are required'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    pw_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(name=data['name'], email=data['email'], password=pw_hash)
    db.session.add(user)
    db.session.commit()
    session['user_id'] = user.id
    session['user_name'] = user.name
    return jsonify({'success': True, 'name': user.name})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    session['user_id'] = user.id
    session['user_name'] = user.name
    return jsonify({'success': True, 'name': user.name})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/me')
@login_required
def me():
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

# ── AI Generation API ─────────────────────────────────────────────
@app.route('/api/generate/ppt', methods=['POST'])
@login_required
def gen_ppt():
    data = request.json
    topic = data.get('topic', '').strip()
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    try:
        result = generate_ppt(topic)
        doc = Document(
            user_id=session['user_id'],
            title=f"{topic} — Presentation",
            doc_type='ppt',
            content=json.dumps(result),
            is_private=data.get('private', False)
        )
        db.session.add(doc)
        db.session.commit()
        return jsonify({'success': True, 'doc_id': doc.id, 'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate/report', methods=['POST'])
@login_required
def gen_report():
    data = request.json
    topic = data.get('topic', '').strip()
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    try:
        result = generate_report(topic)
        doc = Document(
            user_id=session['user_id'],
            title=f"{topic} — Report",
            doc_type='report',
            content=json.dumps(result),
            is_private=data.get('private', False)
        )
        db.session.add(doc)
        db.session.commit()
        return jsonify({'success': True, 'doc_id': doc.id, 'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate/notes', methods=['POST'])
@login_required
def gen_notes():
    data = request.json
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Input text is required'}), 400
    try:
        result = generate_notes(text)
        doc = Document(
            user_id=session['user_id'],
            title=f"Notes — {text[:40]}{'…' if len(text) > 40 else ''}",
            doc_type='notes',
            content=json.dumps(result),
            is_private=data.get('private', False)
        )
        db.session.add(doc)
        db.session.commit()
        return jsonify({'success': True, 'doc_id': doc.id, 'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── Document API ──────────────────────────────────────────────────
@app.route('/api/documents')
@login_required
def get_documents():
    docs = Document.query.filter_by(user_id=session['user_id']) \
                         .order_by(Document.created_at.desc()).limit(20).all()
    return jsonify([d.to_dict() for d in docs])

@app.route('/api/documents/<int:doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.user_id != session['user_id']:
        shared = SharedDocument.query.filter_by(
            doc_id=doc_id, shared_with=session['user_id']
        ).first()
        if not shared:
            return jsonify({'error': 'Access denied'}), 403
    return jsonify(doc.to_dict())

@app.route('/api/documents/<int:doc_id>/share', methods=['POST'])
@login_required
def share_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.user_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    share_token = str(uuid.uuid4())
    doc.share_token = share_token
    db.session.commit()
    return jsonify({'share_url': f'/shared/{share_token}', 'token': share_token})

@app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
@login_required
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.user_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    db.session.delete(doc)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/shared/<token>')
def shared_doc(token):
    doc = Document.query.filter_by(share_token=token).first_or_404()
    return render_template('shared.html', doc=doc)

# ── Init DB ────────────────────────────────────────────────────
with app.app_context():
    db.create_all()

# ── Run (development only) ─────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
