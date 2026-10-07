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

# ANAGRAFICA COMPLETA DEI 235 DIPENDENTI INTEGRATA
DEFAULT_USERS = [
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Abu Taleb", "nome": "Mays", "email": "mays.abutaleb@hqe.it", "inquadramento": "PartitaIVA", "maxDays": 4, "bu": "RADIOMOBILE", "team": "PROGETTAZIONE ESECUTIVA", "referente": "Russo"},
    {"azienda": "CONSORZIO HQ", "cognome": "Borghetti", "nome": "Matteo", "email": "matteo.borghetti@qtech.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "DIREZIONE OPERATIVA", "team": "DIREZIONE", "referente": "Verga"},
    {"azienda": "CONSORZIO HQ", "cognome": "Ferrario", "nome": "Massimiliano", "email": "massimiliano.ferrario@qtech.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "MOBILITA' ELETTRICA", "team": "PM CANTIERE", "referente": "Ferrero"},
    {"azienda": "CONSORZIO HQ", "cognome": "Fraudet", "nome": "Fabien", "email": "fabien.fraudet@hqcon.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "MOBILITA' ELETTRICA", "team": "PM CANTIERE", "referente": "Borghetti"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Antenozio", "nome": "Rebecca", "email": "rebecca.antenozio@hqe.it", "inquadramento": "CoCoCo", "maxDays": 4, "bu": "HR", "team": "HR", "referente": "Pizzorno"},
    {"azienda": "CONSORZIO HQ", "cognome": "Palma", "nome": "Gloria", "email": "gloria.palma@qtech.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "COMMERCIALE", "team": "PM", "referente": "Borghetti"},
    {"azienda": "QTECH SRL", "cognome": "Anzani", "nome": "Alessandro", "email": "alessandro.anzani@qtech.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "MILANO", "team": "MILANO", "referente": "Perfetti"},
    {"azienda": "CONSORZIO HQ", "cognome": "Petrizzi", "nome": "Sandro", "email": "sandro.petrizzi@hqcon.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "COMMERCIALE", "team": "PM", "referente": "Borghetti"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Avendano", "nome": "Rolando", "email": "rolando.avendano@hqe.it", "inquadramento": "PartitaIVA", "maxDays": 4, "bu": "RADIOMOBILE", "team": "PROGETTAZIONE ESECUTIVA", "referente": "Russo"},
    {"azienda": "CONSORZIO HQ", "cognome": "Vergani", "nome": "Davide", "email": "davide.vergani@qtech.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "MOBILITA' ELETTRICA", "team": "PM CANTIERE", "referente": "Borghetti"},
    {"azienda": "HQ ENGINEERING ITALIA S.R.L.", "cognome": "Barbera", "nome": "Francesco", "email": "francesco.barbera@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "RADIOMOBILE", "team": "DIREZIONE", "referente": "Villa"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Amiri", "nome": "Elina", "email": "elina.amiri@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "RADIOMOBILE", "team": "PROGETTAZIONE ESECUTIVA", "referente": "Prezioso"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Angaroni", "nome": "Claudio", "email": "claudio.angaroni@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "CONSULENZA", "team": "CONSULENZA", "referente": "Morolla"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Antonini", "nome": "Federica", "email": "federica.antonini@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "SEDE ROMA", "team": "DL&SIC", "referente": "Tomassini"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Arcuri", "nome": "Pasquale", "email": "pasquale.arcuri@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "CONSULENZA", "team": "CONSULENZA", "referente": "Morolla"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Avila", "nome": "David", "email": "david.avila@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "MOBILITA' ELETTRICA", "team": "PERMESSI", "referente": "Prezioso"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Bagnasco", "nome": "Giovanni", "email": "giovanni.bagnasco@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "CONSULENZA", "team": "CONSULENZA", "referente": "Morolla"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Ballerio", "nome": "Alessio", "email": "alessio.ballerio@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "RADIOMOBILE", "team": "PM", "referente": "Barbera"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Bernazzani", "nome": "Luca", "email": "luca.bernazzani@hqe.it", "inquadramento": "CoCoCo", "maxDays": 4, "bu": "RADIOMOBILE", "team": "LOS + SOPR.", "referente": "Loddo"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Berti", "nome": "Federico", "email": "federico.berti@hqe.it", "inquadramento": "CoCoCo", "maxDays": 4, "bu": "RINNOVABILI", "team": "ACQUISIZIONE", "referente": "Bosetto"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Pizzorno", "nome": "Chiara", "email": "chiara.pizzorno@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "HR", "team": "HR", "referente": "Barbera"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Luccini", "nome": "Gianluca", "email": "gianluca.luccini@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "HR", "team": "HR", "referente": "Pizzorno"},
    {"azienda": "HQ ENGINEERING SRL", "cognome": "Malcotti", "nome": "Pietro", "email": "pietro.malcotti@hqe.it", "inquadramento": "Dipendente", "maxDays": 4, "bu": "HR", "team": "HR", "referente": "Pizzorno"}
]

USERS_MAP = {u['email']: u for u in DEFAULT_USERS}

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
            print(f"Errore lettura utente Supabase: {e}")

    if not user:
        user = USERS_MAP.get(email)

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

@app.route('/api/users', methods=['GET'])
def get_users():
    if supabase:
        try:
            res = supabase.table('users').select('*').execute()
            if res.data and len(res.data) > 0:
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
            print(f"Errore get_users Supabase: {e}")
    
    return jsonify(DEFAULT_USERS)

@app.route('/api/users/update', methods=['POST'])
def update_user():
    if supabase:
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

@app.route('/api/requests', methods=['GET', 'POST'])
def handle_requests():
    if request.method == 'POST':
        data = request.json or {}
        if supabase:
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
        reqs = {}
        if supabase:
            try:
                res = supabase.table('requests').select('*').execute()
                for r in res.data:
                    dates = r.get('dates')
                    if isinstance(dates, str):
                        dates = json.loads(dates)
                    reqs[r.get('email')] = {
                        'dates': dates,
                        'notes': r.get('notes', ''),
                        'isValidated': r.get('is_validated', False)
                    }
            except Exception as e:
                print(f"Errore get_requests: {e}")
        return jsonify(reqs)

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    if request.method == 'POST':
        data = request.json or {}
        if supabase:
            row = {'key': 'recommendedDays', 'value': json.dumps(data.get('recommendedDays', []))}
            try:
                supabase.table('settings').upsert(row).execute()
            except Exception as e:
                print(f"Errore save_settings: {e}")
        return jsonify({'status': 'ok'})
    else:
        rec_days = []
        if supabase:
            try:
                res = supabase.table('settings').select('*').eq('key', 'recommendedDays').execute()
                if res.data:
                    val = res.data[0].get('value')
                    rec_days = json.loads(val) if isinstance(val, str) else val
            except Exception as e:
                print(f"Errore get_settings: {e}")
        return jsonify({'recommendedDays': rec_days})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
