import os
import json
from flask import Flask, request, jsonify, send_from_directory
from supabase import create_client, Client

app = Flask(__name__, static_folder='.', static_url_path='')

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

DEFAULT_RECOMMENDED_DAYS = [
    "2026-12-28", "2026-12-29", "2026-12-30"
]

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

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
                rec_days = u.get('recommended_days')
                if isinstance(rec_days, str):
                    rec_days = json.loads(rec_days)
                user = {
                    'azienda': u.get('azienda', ''),
                    'cognome': u.get('cognome', ''),
                    'nome': u.get('nome', ''),
                    'email': u.get('email', ''),
                    'inquadramento': u.get('inquadramento', ''),
                    'maxDays': u.get('max_days', 4),
                    'bu': u.get('bu', ''),
                    'team': u.get('team', ''),
                    'referente': u.get('referente', ''),
                    'recommendedDays': rec_days if rec_days is not None else DEFAULT_RECOMMENDED_DAYS
                }
        except Exception as e:
            print(f"Errore lettura utente Supabase: {e}")

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
            'referente': 'HQ',
            'recommendedDays': DEFAULT_RECOMMENDED_DAYS
        }

    if not user:
        return jsonify({'error': 'Email non trovata in anagrafica.'}), 404

    return jsonify({'user': user, 'isAdmin': is_admin})

@app.route('/api/users', methods=['GET'])
def get_users():
    users_list = []
    if supabase:
        try:
            res = supabase.table('users').select('*').execute()
            if res.data and len(res.data) > 0:
                for u in res.data:
                    rec_days = u.get('recommended_days')
                    if isinstance(rec_days, str):
                        rec_days = json.loads(rec_days)
                    users_list.append({
                        'azienda': u.get('azienda', ''),
                        'cognome': u.get('cognome', ''),
                        'nome': u.get('nome', ''),
                        'email': u.get('email', ''),
                        'inquadramento': u.get('inquadramento', ''),
                        'maxDays': u.get('max_days', 4),
                        'bu': u.get('bu', ''),
                        'team': u.get('team', ''),
                        'referente': u.get('referente', ''),
                        'recommendedDays': rec_days if rec_days is not None else DEFAULT_RECOMMENDED_DAYS
                    })
        except Exception as e:
            print(f"Errore get_users Supabase: {e}")

    users_sorted = sorted(users_list, key=lambda x: (x.get('cognome', '').lower(), x.get('nome', '').lower()))
    return jsonify(users_sorted)

# AGGIUNTA COLLABORATORE MANUALE (SALVATAGGIO DIRETTO IN DATABASE)
@app.route('/api/users/add', methods=['POST'])
def add_user():
    u = request.json or {}
    email = u.get('email', '').strip().lower()
    if not email:
        return jsonify({'error': 'Email obbligatoria.'}), 400

    data = {
        'email': email,
        'nome': u.get('nome', '').strip().title(),
        'cognome': u.get('cognome', '').strip().title(),
        'azienda': u.get('azienda', '').strip(),
        'inquadramento': u.get('inquadramento', '').strip(),
        'max_days': int(u.get('maxDays', 4)),
        'bu': u.get('bu', '').strip(),
        'team': u.get('team', '').strip(),
        'referente': u.get('referente', '').strip(),
        'recommended_days': json.dumps(u.get('recommendedDays', DEFAULT_RECOMMENDED_DAYS))
    }

    if supabase:
        try:
            supabase.table('users').upsert(data, on_conflict='email').execute()
        except Exception as e:
            print(f"Errore add_user Supabase: {e}")
            return jsonify({'error': str(e)}), 500

    return jsonify({'status': 'ok'})

# ELIMINAZIONE COLLABORATORE
@app.route('/api/users/delete', methods=['POST'])
def delete_user():
    data = request.json or {}
    email = data.get('email', '').strip().lower()
    if supabase and email:
        try:
            supabase.table('users').delete().eq('email', email).execute()
            supabase.table('requests').delete().eq('email', email).execute()
        except Exception as e:
            print(f"Errore delete_user Supabase: {e}")
            return jsonify({'error': str(e)}), 500
    return jsonify({'status': 'ok'})

@app.route('/api/users/update', methods=['POST'])
def update_user():
    u = request.json or {}
    email = u.get('email')
    
    data = {
        'azienda': u.get('azienda', ''),
        'bu': u.get('bu', ''),
        'team': u.get('team', ''),
        'referente': u.get('referente', ''),
        'inquadramento': u.get('inquadramento', ''),
        'max_days': int(u.get('maxDays', 4))
    }

    if 'recommendedDays' in u:
        data['recommended_days'] = json.dumps(u.get('recommendedDays'))

    if supabase and email:
        try:
            supabase.table('users').update(data).eq('email', email).execute()
        except Exception as e:
            print(f"Errore update_user Supabase: {e}")

    return jsonify({'status': 'ok'})

@app.route('/api/requests', methods=['GET', 'POST'])
def handle_requests():
    if request.method == 'POST':
        data = request.json or {}
        email = data.get('email')
        dates = data.get('dates', [])
        notes = data.get('notes', '')
        is_validated = data.get('isValidated', False)

        if supabase and email:
            row = {
                'email': email,
                'dates': json.dumps(dates),
                'notes': notes,
                'is_validated': is_validated
            }
            try:
                supabase.table('requests').upsert(row, on_conflict='email').execute()
            except Exception as e:
                print(f"Errore save_request Supabase: {e}")

        return jsonify({'status': 'ok'})
    else:
        reqs = {}
        if supabase:
            try:
                res = supabase.table('requests').select('*').execute()
                for r in res.data:
                    dates = r.get('dates')
                    if isinstance(dates, str):
                        dates = json.loads(dates)
                    reqs[r.get('email')] = {
                        'dates': dates or [],
                        'notes': r.get('notes', ''),
                        'isValidated': r.get('is_validated', False)
                    }
            except Exception as e:
                print(f"Errore get_requests Supabase: {e}")
        return jsonify(reqs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
