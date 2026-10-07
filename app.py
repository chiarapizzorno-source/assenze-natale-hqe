import os
import json
from flask import Flask, request, jsonify, send_from_directory
from supabase import create_client, Client

app = Flask(__name__, static_folder='.', static_url_path='')

# Configurazione Credenziali Supabase dalle Variabili d'Ambiente
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Errore connessione Supabase: {e}")

ADMIN_EMAILS = [
    'chiara.pizzorno@hqe.it',
    'pietro.malcotti@hqe.it',
    'gianluca.luccini@hqe.it',
    'rebecca.antenozio@hqe.it'
]
ADMIN_PASSWORD = 'natalesulnilo'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# API LOGIN
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    is_admin = email in ADMIN_EMAILS

    if is_admin and password != ADMIN_PASSWORD:
        return jsonify({'error': 'Password Amministratore errata.'}), 401

    user = None
    if supabase:
        try:
            res = supabase.table('users').select('*').eq('email', email).execute()
            if res.data:
                u = res.data[0]
                user = {
                    'azienda': u.get('azienda'),
                    'cognome': u.get('cognome'),
                    'nome': u.get('nome'),
                    'email': u.get('email'),
                    'inquadramento': u.get('inquadramento'),
                    'maxDays': u.get('max_days', 4),
                    'bu': u.get('bu', ''),
                    'team': u.get('team', ''),
                    'referente': u.get('referente', '')
                }
        except Exception as e:
            print(f"Errore lettura utente: {e}")

    if not user and is_admin:
        user = {
            'azienda': 'HQ ENGINEERING SRL',
            'cognome': 'Admin',
            'nome': email.split('.')[0].upper(),
            'email': email,
            'inquadramento': 'Dipendente',
            'maxDays': 12,
            'bu': 'DIREZIONE',
            'team': 'HQ',
            'referente': 'HQ'
        }

    if not user:
        return jsonify({'error': 'Email non trovata in anagrafica.'}), 404

    return jsonify({'user': user, 'isAdmin': is_admin})

# API RICHIEDI UTENTI
@app.route('/api/users', methods=['GET'])
def get_users():
    if not supabase:
        return jsonify([])
    try:
        res = supabase.table('users').select('*').execute()
        users = []
        for u in res.data:
            users.append({
                'azienda': u.get('azienda'),
                'cognome': u.get('cognome'),
                'nome': u.get('nome'),
                'email': u.get('email'),
                'inquadramento': u.get('inquadramento'),
                'maxDays': u.get('max_days', 4),
                'bu': u.get('bu', ''),
                'team': u.get('team', ''),
                'referente': u.get('referente', '')
            })
        return jsonify(users)
    except Exception as e:
        print(f"Errore get_users: {e}")
        return jsonify([])

# API AGGIORNA UTENTE
@app.route('/api/users/update', methods=['POST'])
def update_user():
    if not supabase:
        return jsonify({'status': 'ok'})
    u = request.json or {}
    data = {
        'bu': u.get('bu', ''),
        'team': u.get('team', ''),
        'referente': u.get('referente', ''),
        'max_days': u.get('maxDays', 4)
    }
    try:
        supabase.table('users').update(data).eq('email', u.get('email')).execute()
    except Exception as e:
        print(f"Errore update_user: {e}")
    return jsonify({'status': 'ok'})

# API RICHIEDI E SALVA RICHIESTE ASSENZE
@app.route('/api/requests', methods=['GET', 'POST'])
def handle_requests():
    if not supabase:
        return jsonify({})

    if request.method == 'POST':
        data = request.json or {}
        row = {
            'email': data.get('email'),
            'dates': json.dumps(data.get('dates', [])),
            'notes': data.get('notes', ''),
            'is_validated': data.get('isValidated', False)
        }
        try:
            supabase.table('requests').upsert(row).execute()
        except Exception as e:
            print(f"Errore save_request: {e}")
        return jsonify({'status': 'ok'})
    else:
        try:
            res = supabase.table('requests').select('*').execute()
            reqs = {}
            for r in res.data:
                dates = r.get('dates')
                if isinstance(dates, str):
                    dates = json.loads(dates)
                reqs[r.get('email')] = {
                    'dates': dates,
                    'notes': r.get('notes', ''),
                    'isValidated': r.get('is_validated', False)
                }
            return jsonify(reqs)
        except Exception as e:
            print(f"Errore get_requests: {e}")
            return jsonify({})

# API IMPOSTAZIONI
@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    if not supabase:
        return jsonify({'recommendedDays': []})

    if request.method == 'POST':
        data = request.json or {}
        row = {'key': 'recommendedDays', 'value': json.dumps(data.get('recommendedDays', []))}
        try:
            supabase.table('settings').upsert(row).execute()
        except Exception as e:
            print(f"Errore save_settings: {e}")
        return jsonify({'status': 'ok'})
    else:
        try:
            res = supabase.table('settings').select('*').eq('key', 'recommendedDays').execute()
            rec_days = []
            if res.data:
                val = res.data[0].get('value')
                rec_days = json.loads(val) if isinstance(val, str) else val
            return jsonify({'recommendedDays': rec_days})
        except Exception as e:
            print(f"Errore get_settings: {e}")
            return jsonify({'recommendedDays': []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
