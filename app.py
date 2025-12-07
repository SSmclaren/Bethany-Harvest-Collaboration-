from flask import Flask, render_template, request, redirect, session, flash
import json
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

for file in ['users.json', 'notices.json', 'conversations.json']:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f)


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def get_or_create_anon_id(notice_id):
    
    session_key = f'anon_id_{notice_id}'
    if session_key not in session:
        session[session_key] = secrets.token_hex(4).upper()
    return session[session_key]

@app.route('/')
def index():
    notices = load_json('notices.json')
    
    sorted_notices = sorted(notices.items(), key=lambda x: x[1]['timestamp'], reverse=True)
    return render_template('index.html', notices=sorted_notices)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        users = load_json('users.json')
        
        if username in users:
            flash('Username already exists')
            return redirect('/register')
        
        users[username] = password
        save_json('users.json', users)
        flash('Registration successful! Please login.')
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        users = load_json('users.json')
        
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/dashboard')
        
        flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    
    notices = load_json('notices.json')
    conversations = load_json('conversations.json')
    
    user_notices = {k: v for k, v in notices.items() if v['owner'] == session['username']}
    
   
    user_conversations = {}
    for notice_id in user_notices.keys():
        if notice_id in conversations:
            user_conversations[notice_id] = conversations[notice_id]
    
    return render_template('dashboard.html', notices=user_notices, conversations=user_conversations)

@app.route('/post_notice', methods=['POST'])
def post_notice():
    if 'username' not in session:
        return redirect('/login')
    
    book_name = request.form['book_name'].strip()
    description = request.form['description'].strip()
    
    if not book_name:
        flash('Book name is required')
        return redirect('/dashboard')
    
    notices = load_json('notices.json')
    notice_id = secrets.token_hex(8)
    
    notices[notice_id] = {
        'owner': session['username'],
        'book_name': book_name,
        'description': description,
        'timestamp': datetime.now().isoformat()
    }
    
    save_json('notices.json', notices)
    flash('Notice posted successfully!')
    return redirect('/dashboard')

@app.route('/delete_notice/<notice_id>')
def delete_notice(notice_id):
    if 'username' not in session:
        return redirect('/login')
    
    notices = load_json('notices.json')
    conversations = load_json('conversations.json')
    
    if notice_id in notices and notices[notice_id]['owner'] == session['username']:
        del notices[notice_id]
        save_json('notices.json', notices)
        
        if notice_id in conversations:
            del conversations[notice_id]
            save_json('conversations.json', conversations)
        
        flash('Notice deleted successfully!')
    
    return redirect('/dashboard')

@app.route('/chat/<notice_id>')
def chat_view(notice_id):
    notices = load_json('notices.json')
    
    if notice_id not in notices:
        flash('Notice not found')
        return redirect('/')
    
    notice = notices[notice_id]
    conversations = load_json('conversations.json')
    
    
    anon_id = get_or_create_anon_id(notice_id)
    
   
    messages = []
    if notice_id in conversations and anon_id in conversations[notice_id]:
        messages = conversations[notice_id][anon_id]
    
    
    is_owner = 'username' in session and session['username'] == notice['owner']
    
    return render_template('chat.html', notice=notice, notice_id=notice_id, 
                          messages=messages, anon_id=anon_id, is_owner=is_owner)

@app.route('/send_dm/<notice_id>', methods=['POST'])
def send_dm(notice_id):
    message_text = request.form['message'].strip()
    
    if not message_text:
        flash('Message cannot be empty')
        return redirect(f'/chat/{notice_id}')
    
    notices = load_json('notices.json')
    
    if notice_id not in notices:
        flash('Notice not found')
        return redirect('/')
    
    conversations = load_json('conversations.json')
    
    
    anon_id = get_or_create_anon_id(notice_id)
    
   
    if notice_id not in conversations:
        conversations[notice_id] = {}
    
    if anon_id not in conversations[notice_id]:
        conversations[notice_id][anon_id] = []
    
    
    is_owner = 'username' in session and session['username'] == notices[notice_id]['owner']
    sender = 'owner' if is_owner else 'anonymous'
    
    conversations[notice_id][anon_id].append({
        'sender': sender,
        'text': message_text,
        'timestamp': datetime.now().isoformat()
    })
    
    save_json('conversations.json', conversations)
    return redirect(f'/chat/{notice_id}')

@app.route('/conversations/<notice_id>')
def view_conversations(notice_id):
    if 'username' not in session:
        return redirect('/login')
    
    notices = load_json('notices.json')
    
    if notice_id not in notices or notices[notice_id]['owner'] != session['username']:
        flash('Access denied')
        return redirect('/dashboard')
    
    conversations = load_json('conversations.json')
    notice = notices[notice_id]
    
    
    convos = conversations.get(notice_id, {})
    
    return render_template('conversations.html', notice=notice, notice_id=notice_id, conversations=convos)

if __name__ == '__main__':
    app.run(debug=True)