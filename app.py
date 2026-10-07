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

# ANAGRAFICA COMPLETA DEI 235 DIPENDENTI
DEFAULT_USERS = [
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Abu Taleb",
        "nome": "Mays",
        "email": "mays.abutaleb@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Borghetti",
        "nome": "Matteo",
        "email": "matteo.borghetti@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "DIREZIONE OPERATIVA",
        "team": "DIREZIONE",
        "referente": "Verga"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Ferrario",
        "nome": "Massimiliano",
        "email": "massimiliano.ferrario@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PM CANTIERE",
        "referente": "Ferrero"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Fraudet",
        "nome": "Fabien",
        "email": "fabien.fraudet@hqcon.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PM CANTIERE",
        "referente": "Borghetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Antenozio",
        "nome": "Rebecca",
        "email": "rebecca.antenozio@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "HR",
        "team": "HR",
        "referente": "Pizzorno"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Palma",
        "nome": "Gloria",
        "email": "gloria.palma@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "COMMERCIALE",
        "team": "PM",
        "referente": "Borghetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Anzani",
        "nome": "Alessandro",
        "email": "alessandro.anzani@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Petrizzi",
        "nome": "Sandro",
        "email": "sandro.petrizzi@hqcon.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "COMMERCIALE",
        "team": "PM",
        "referente": "Borghetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Avendano",
        "nome": "Rolando",
        "email": "rolando.avendano@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Vergani",
        "nome": "Davide",
        "email": "davide.vergani@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PM CANTIERE",
        "referente": "Borghetti"
    },
    {
        "azienda": "HQ ENGINEERING ITALIA S.R.L.",
        "cognome": "Barbera",
        "nome": "Francesco",
        "email": "francesco.barbera@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DIREZIONE",
        "referente": "Villa"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Amiri",
        "nome": "Elina",
        "email": "elina.amiri@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Prezioso"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Angaroni",
        "nome": "Claudio",
        "email": "claudio.angaroni@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Antonini",
        "nome": "Federica",
        "email": "federica.antonini@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "SEDE ROMA",
        "team": "DL&SIC",
        "referente": "Tomassini"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Arcuri",
        "nome": "Pasquale",
        "email": "pasquale.arcuri@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Avila",
        "nome": "David",
        "email": "david.avila@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Prezioso"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bagnasco",
        "nome": "Giovanni",
        "email": "giovanni.bagnasco@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Ballerio",
        "nome": "Alessio",
        "email": "alessio.ballerio@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PM",
        "referente": "Barbera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bernazzani",
        "nome": "Luca",
        "email": "luca.bernazzani@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "LOS + SOPR.",
        "referente": "Loddo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Berti",
        "nome": "Federico",
        "email": "federico.berti@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "ACQUISIZIONE",
        "referente": "Bosetto"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Baraggia",
        "nome": "Fausto",
        "email": "fausto.baraggia@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "LOS + SOPR.",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bianchim",
        "nome": "Manlio",
        "email": "manlio.bianchi@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DIREZIONE",
        "referente": "Barbera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bigio",
        "nome": "Valentina",
        "email": "valentina.bigio@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bartole",
        "nome": "Diego",
        "email": "diego.bartole@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "ACQUISIZIONE",
        "referente": "Villa"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bollasina",
        "nome": "Elena",
        "email": "elena.bollasina@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "PERMESSI",
        "referente": "Villa"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bologna",
        "nome": "Alessandro",
        "email": "alessandro.bologna@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bolzoni",
        "nome": "Alessio",
        "email": "alessio.bolzoni@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bonettini",
        "nome": "Andrea",
        "email": "andrea.bonettini@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Borgato",
        "nome": "Emanuele",
        "email": "emanuele.borgato@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bellardini",
        "nome": "Gian Marco",
        "email": "gianmarco.bellardini@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "SEDE ROMA",
        "team": "DL&SIC",
        "referente": "Tomassini"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Beshir",
        "nome": "Aya",
        "email": "aya.beshir@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "PERMESSI",
        "referente": "Bollasina"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Blasi",
        "nome": "Valeria",
        "email": "valeria.blasi@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Borruto",
        "nome": "Alessia",
        "email": "alessia.borruto@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bosetto",
        "nome": "Elena",
        "email": "elena.bosetto@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "ACQUISIZIONE",
        "referente": "Villa"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Bozzolo",
        "nome": "Paolo",
        "email": "paolo.bozzolo@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Bracale",
        "nome": "Samuele",
        "email": "samuele.bracale@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Brancato",
        "nome": "Chiara",
        "email": "chiara.brancato@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Caputo",
        "nome": "Filippo",
        "email": "filippo.caputo@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "SERVIZI GENERALI",
        "referente": "Redaelli"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Caracozza",
        "nome": "Daniele",
        "email": "daniele.caracozza@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "FATTURAZIONE",
        "referente": "Redaelli"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Brevi",
        "nome": "Filippo",
        "email": "filippo.brevi@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Prezioso"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Cardozo",
        "nome": "Antonella",
        "email": "antonella.cardozo@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Buonvino",
        "nome": "Lara",
        "email": "lara.buonvino@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Cammelli",
        "nome": "Sonia",
        "email": "sonia.cammelli@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Prezioso"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Cannavo'",
        "nome": "Fabiana",
        "email": "fabiana.cannavo@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DL&SIC",
        "referente": "Maragno"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Caruso",
        "nome": "Alida",
        "email": "alida.caruso@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Castellazzi",
        "nome": "Stefano",
        "email": "stefano.castellazzi@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Cazzulli",
        "nome": "Monica",
        "email": "monica.cazzulli@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "QUALIFICHE E GARE",
        "team": "QUALIFICHE E GARE",
        "referente": "Verga"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Cigalotti",
        "nome": "Giada",
        "email": "giada.cigalotti@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PM",
        "referente": "Barbera"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Caruso",
        "nome": "Giovanni",
        "email": "giovanni.caruso@qtech.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "COMMERCIALE",
        "team": "COMMERCIALE",
        "referente": "Verga"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Carusos",
        "nome": "Simone",
        "email": "simone.caruso@qtech.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Cipolla",
        "nome": "Marco",
        "email": "marco.cipolla@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Castoldi",
        "nome": "Ivan",
        "email": "ivan.castoldi@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Catroppa",
        "nome": "Rocco",
        "email": "rocco.catroppa@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Coccia",
        "nome": "Roberto",
        "email": "roberto.coccia@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "PM (AI SPECIALIST)",
        "referente": "Cracchiolo"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Cerpelloni Qtech",
        "nome": "Giovanni",
        "email": "giovanni.cerpelloni@qtech.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Cesari",
        "nome": "Martina",
        "email": "martina.cesari@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "PERMESSI",
        "referente": "Bollasina"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Chahine",
        "nome": "Marwan",
        "email": "marwan.chahine@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Concolato",
        "nome": "Marco",
        "email": "marco.concolato@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Contesi",
        "nome": "Lorenzo",
        "email": "lorenzo.contesi@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PM",
        "referente": "Barbera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Ciricosta",
        "nome": "Francesco",
        "email": "francesco.ciricosta@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "SEDE ROMA",
        "team": "PROG.&SOPR.",
        "referente": "Tomassini"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Corradi",
        "nome": "Luca",
        "email": "luca.corradi@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "De Cicco",
        "nome": "Alessandro",
        "email": "alessandro.decicco@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "ACQUISIZIONE",
        "referente": "Fontana"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "De Maria",
        "nome": "Francesco Adriano",
        "email": "adriano.demaria@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "COMMERCIALE",
        "referente": "Verga"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Condori",
        "nome": "Adrian",
        "email": "adrian.condori@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DL&SIC",
        "referente": "Maragno"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Di Nunno",
        "nome": "Simone",
        "email": "simone.dinunno@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Di Salvatore",
        "nome": "Jacopo",
        "email": "jacopo.disalvatore@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "SEDE ROMA",
        "team": "DL&SIC",
        "referente": "Tomassini"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Corso",
        "nome": "Linda",
        "email": "linda.corso@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "SEDE GENOVA",
        "team": "SEDE GENOVA",
        "referente": "Sampaolesi"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Daoud",
        "nome": "El Shaymaa",
        "email": "daoud.elshaymaa@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "SEDE GENOVA",
        "team": "SEDE GENOVA",
        "referente": "Sampaolesi"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "De Araujo Lobato",
        "nome": "Brayan",
        "email": "brayan.dearaujo@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "LOS + SOPR.",
        "referente": "Loddo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Di Vito",
        "nome": "Daniela",
        "email": "daniela.divito@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "FATTURAZIONE",
        "referente": "Redaelli"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Dicosimo",
        "nome": "Paola",
        "email": "paola.dicosimo@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "SEDE ROMA",
        "team": "ACQUISIZIONE",
        "referente": "Tomassini"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Disabella",
        "nome": "Jacopo",
        "email": "jacopo.disabella@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "De Masi",
        "nome": "Silvia",
        "email": "silvia.demasi@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "SEDE ROMA",
        "team": "DL&SIC",
        "referente": "Tomassini"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Degrada",
        "nome": "Andrea",
        "email": "andrea.degrada@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "D'Italia",
        "nome": "Michael Alberto",
        "email": "michael.ditalia@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "LOS + SOPR.",
        "referente": "Baraggia"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Dell'Orto",
        "nome": "Denise",
        "email": "denise.dellorto@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "PERMESSI",
        "referente": "Bollasina"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Depalma",
        "nome": "Luigi",
        "email": "luigi.depalma@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Fabiano",
        "nome": "Mario",
        "email": "mario.fabiano@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Fontana",
        "nome": "Debora",
        "email": "debora.fontana@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "ACQUISIZIONE",
        "referente": "Borghetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Formenti",
        "nome": "Barbara",
        "email": "barbara.formenti@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Girelli",
        "nome": "Paolo Maria Giovanni",
        "email": "paolo.girelli@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "ACQUISIZIONE",
        "referente": "Mazzucchelli"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Gisotti",
        "nome": "Eduardo",
        "email": "eduardo.gisotti@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DL&SIC",
        "referente": "Maragno"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Gucciardi",
        "nome": "Claudio",
        "email": "claudio.gucciardi@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "AIE",
        "referente": "Lucera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Durante",
        "nome": "Alessio",
        "email": "alessio.durante@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Guo",
        "nome": "Zhong Yi",
        "email": "zhongyi.guo@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "TOPOGRAFIA",
        "referente": "Pasqualotto"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Guzzo",
        "nome": "Genoveffa",
        "email": "genoveffa.guzzo@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "UFFICIO TECNICO",
        "referente": "Russo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Hannaf",
        "nome": "Fadi",
        "email": "hanna.fadi@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PM CANTIERE",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Felici",
        "nome": "Celine",
        "email": "celine.felici@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "SEDE ROMA",
        "team": "DL&SIC",
        "referente": "Tomassini"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Fernandez",
        "nome": "Braython",
        "email": "braython.fernandez@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "TOPOGRAFIA",
        "referente": "Pasqualotto"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Ferrari",
        "nome": "Roberto",
        "email": "roberto.ferrari@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "PM (AI SPECIALIST)",
        "referente": "Cracchiolo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Landro",
        "nome": "Marietta",
        "email": "marietta.landro@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Bosetto"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Ferrero",
        "nome": "Renato",
        "email": "renato.ferrero@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PM CANTIERE",
        "referente": "Borghetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Loddo",
        "nome": "Alessandro",
        "email": "alessandro.loddo@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Losito",
        "nome": "Costantino",
        "email": "costantino.losito@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Forgione",
        "nome": "Stefano",
        "email": "stefano.forgione@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Luccini",
        "nome": "Gianluca",
        "email": "gianluca.luccini@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "HR",
        "team": "HR",
        "referente": "Pizzorno"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Lucera",
        "nome": "Stefano",
        "email": "stefano.lucera@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "AIE",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Fuse'",
        "nome": "Filippo",
        "email": "filippo.fuse@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "DL&SIC",
        "referente": "Bollasina"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Ganz",
        "nome": "Sandro",
        "email": "sandro.ganz@qtech.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Garau",
        "nome": "Nicola",
        "email": "nicola.garau@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "UFFICIO TECNICO",
        "referente": "Russo"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Garavaglia",
        "nome": "Federico",
        "email": "federico.garavaglia@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "UFFICIO TECNICO",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Ghanimi",
        "nome": "Ghazal",
        "email": "ghanimi.ghazal@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "SEDE ROMA",
        "team": "PERMESSI",
        "referente": "Tomassini"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Luo",
        "nome": "Hang Dan Giacomo",
        "email": "giacomo.luo@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "AIE",
        "referente": "Lucera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Maceroni",
        "nome": "Andrea",
        "email": "andrea.maceroni@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Macri",
        "nome": "Leonardo",
        "email": "leonardo.macri@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "VINCOLI",
        "referente": "Bosetto"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Maenza",
        "nome": "Alessandro",
        "email": "alessandro.maenza@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Mahato",
        "nome": "Arvind",
        "email": "arvind.mahato@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Malcotti",
        "nome": "Pietro",
        "email": "pietro.malcotti@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "HR",
        "team": "HR",
        "referente": "Pizzorno"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Hamid",
        "nome": "Narges",
        "email": "narges.hamid@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Hanna",
        "nome": "Abanoub",
        "email": "abanoub.hanna@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Mallano",
        "nome": "Barbara",
        "email": "barbara.mallano@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Imbriano",
        "nome": "Matteo",
        "email": "matteo.imbriano@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Inga",
        "nome": "Rolando",
        "email": "rolando.inga@qtech.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Khan",
        "nome": "Seerat",
        "email": "seerat.khan@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "QUALIFICHE E GARE",
        "team": "QUALIFICHE E GARE",
        "referente": "Verga"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Maruffi",
        "nome": "Fabrizio",
        "email": "fabrizio.maruffi@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "AMMINISTRAZIONE",
        "referente": "Redaelli"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Lijoi",
        "nome": "Daniele",
        "email": "daniele.lijoi@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Lo Cricchio",
        "nome": "Luca",
        "email": "luca.locricchio@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "LOS + SOPR.",
        "referente": "Loddo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Lobascio",
        "nome": "Fedele",
        "email": "fedele.lobascio@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "SEDE GENOVA",
        "team": "SEDE GENOVA",
        "referente": "Sampaolesi"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Matanguihan",
        "nome": "Jeffrey",
        "email": "jeffrey.matanguihan@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Prezioso"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Lopez",
        "nome": "Patrick",
        "email": "patrick.lopez@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "AIE",
        "referente": "Lucera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Mazzucchelli",
        "nome": "Gaia Donata",
        "email": "gaia.mazzucchelli@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "ACQUISIZIONE",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Lovecchio",
        "nome": "Michele",
        "email": "michele.lovecchio@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Melis",
        "nome": "Luigi Elia",
        "email": "luigi.melis@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Morolla",
        "nome": "Damiano",
        "email": "damiano.morolla@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DIREZIONE",
        "referente": "Barbera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Nicoli",
        "nome": "Laura",
        "email": "laura.nicoli@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "PERMESSI",
        "referente": "Bollasina"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Parini",
        "nome": "Fabio",
        "email": "fabio.parini@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Prezioso"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Pavan",
        "nome": "Alessandro",
        "email": "alessandro.pavan@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Piccolino",
        "nome": "Giuseppe",
        "email": "giuseppe.piccolino@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PM CANTIERE",
        "referente": "Ferrero"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Pizzoni",
        "nome": "Luca",
        "email": "luca.pizzoni@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "AIE",
        "referente": "Lucera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Maiocchi",
        "nome": "Filippo",
        "email": "filippo.maiocchi@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DL&SIC",
        "referente": "Maragno"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Pizzorno",
        "nome": "Chiara",
        "email": "chiara.pizzorno@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "HR",
        "team": "HR",
        "referente": "Barbera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Poire'",
        "nome": "Massimo",
        "email": "massimo.poire@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "AMMINISTRAZIONE",
        "referente": "Redaelli"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Manfredi",
        "nome": "Alice",
        "email": "alice.manfredi@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "SEDE GENOVA",
        "team": "SEDE GENOVA",
        "referente": "Sampaolesi"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Maragno",
        "nome": "Luigi",
        "email": "luigi.maragno@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DL&SIC",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Marano",
        "nome": "Carlo",
        "email": "carloalberto.marano@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DL&SIC",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Prezioso",
        "nome": "Ivan",
        "email": "ivan.prezioso@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Borghetti"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Marra",
        "nome": "Armando",
        "email": "armando.marra@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Martino",
        "nome": "Giuseppe",
        "email": "giuseppe.martino@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "PERMESSI",
        "referente": "Bollasina"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Quistelli",
        "nome": "Andrea",
        "email": "andrea.quistelli@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DL&SIC",
        "referente": "Maragno"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Romano",
        "nome": "Daniele",
        "email": "daniele.romano@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Saini",
        "nome": "Gabriele",
        "email": "gabriele.saini@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "LOS + SOPR.",
        "referente": "Loddo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Sampaolesi",
        "nome": "Federica",
        "email": "federica.sampaolesi@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "SEDE GENOVA",
        "team": "SEDE GENOVA",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Scurati",
        "nome": "Martina",
        "email": "martina.scurati@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "PERMESSI",
        "referente": "Bosetto"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Siviero",
        "nome": "Gianluca",
        "email": "gianluca.siviero@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PM CANTIERE",
        "referente": "Ferrero"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Menna",
        "nome": "Antonio",
        "email": "antonio.menna@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Miliziano",
        "nome": "Stefano",
        "email": "stefano.miliziano@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "ACQUISIZIONE",
        "referente": "Mazzucchelli"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Mingrone",
        "nome": "Mattia",
        "email": "mattia.mingrone@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Mohamed",
        "nome": "Randa Hassan Abdelmonem",
        "email": "randa.mohamed@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Mohammadi",
        "nome": "Zeinab",
        "email": "zeinab.mohammadi@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Castoldi"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Molinelli",
        "nome": "Cesare",
        "email": "cesare.molinelli@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "UFFICIO TECNICO",
        "referente": "Russo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Montesano",
        "nome": "Tatiana",
        "email": "tatiana.montesano@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "PERMESSI",
        "referente": "Bollasina"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Tarantino",
        "nome": "Andrea",
        "email": "andrea.tarantino@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Teti",
        "nome": "Romina",
        "email": "romina.teti@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Tirellig",
        "nome": "Gianmarco",
        "email": "gianmarco.tirelli@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "PERMESSI",
        "referente": "Bollasina"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Tomassini",
        "nome": "Manilo",
        "email": "manilo.tomassini@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "SEDE ROMA",
        "team": "RESPONSABILE DI SEDE",
        "referente": "Barbera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Toso",
        "nome": "Lorenzo",
        "email": "lorenzo.toso@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "UFFICIO TECNICO",
        "referente": "Russo"
    },
    {
        "azienda": "nan",
        "cognome": "Oselin",
        "nome": "Sebastiano",
        "email": "sebastiano.oselin@qtech.it",
        "inquadramento": "nan",
        "maxDays": 4,
        "bu": "VERONA",
        "team": "VERONA",
        "referente": "Tosatto"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Paleari",
        "nome": "Riccardo",
        "email": "riccardo.paleari@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PM",
        "referente": "Barbera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Pallante",
        "nome": "Veronica",
        "email": "veronica.pallante@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Vellotti",
        "nome": "Andrea",
        "email": "andrea.vellotti@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "SEDE PADOVA",
        "team": "SEDE PADOVA",
        "referente": "Barbera"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Palmal",
        "nome": "Luigi",
        "email": "luigi.palma@hqe.it",
        "inquadramento": "nan",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Pandolfini",
        "nome": "Elisabetta",
        "email": "elisabetta.pandolfini@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "SEDE GENOVA",
        "team": "SEDE GENOVA",
        "referente": "Sampaolesi"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Villajunior",
        "nome": "Alberto",
        "email": "operations@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "LOS + SOPR.",
        "referente": "Baraggia"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Pasqualotto",
        "nome": "Daniele",
        "email": "daniele.pasqualotto@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "TOPOGRAFIA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Zerzeri",
        "nome": "Karim",
        "email": "karim.zerzeri@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "PROGETTAZIONE ELETTRICA",
        "referente": "Tirelli"
    },
    {
        "azienda": "HQ INDUSTRIAL ASSETS S.R.L.",
        "cognome": "Andreozzi",
        "nome": "Veronica",
        "email": "veronica.andreozzi@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "ACQUISTI",
        "referente": "Redaelli"
    },
    {
        "azienda": "HQ INDUSTRIAL ASSETS S.R.L.",
        "cognome": "Redaelli",
        "nome": "Luca",
        "email": "luca.redaelli@hqe.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "AMMINISTRAZIONE",
        "referente": "Villa"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Baracchi",
        "nome": "Mauro",
        "email": "mauro.baracchi@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Benelli",
        "nome": "Filippo",
        "email": "filippo.benelli@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Piasentini",
        "nome": "Chiara",
        "email": "chiara.piasentini@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Borruto",
        "nome": "David",
        "email": "david.borruto@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Pisanu",
        "nome": "Andrea",
        "email": "andrea.pisanu@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Bottin",
        "nome": "Andrea",
        "email": "andrea.bottin@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Brambilla",
        "nome": "Marco",
        "email": "marco.brambilla@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Brandi",
        "nome": "Luca",
        "email": "luca.brandi@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Briguglio",
        "nome": "Simona",
        "email": "simona.briguglio@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "AMMINISTRAZIONE",
        "referente": "Borghetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Collura",
        "nome": "Luigi",
        "email": "luigi.collura@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Procopio",
        "nome": "Gerardo",
        "email": "gerardo.procopio@qtech.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Proietti",
        "nome": "Giulia",
        "email": "giulia.proietti @hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Prosperi",
        "nome": "Andrea",
        "email": "andrea.prosperi@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Puddu",
        "nome": "Francesca",
        "email": "francesca.puddu@hqe.it",
        "inquadramento": "PartitaIVA(01/04/2026-31/12/2026)",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Quadrante",
        "nome": "Daniela",
        "email": "daniela.quadrante@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "De Blasio",
        "nome": "Giuseppe",
        "email": "giuseppe.deblasio@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Raimondi",
        "nome": "Giorgio",
        "email": "giorgio.raimondi@qtech.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Rasia",
        "nome": "Silvia",
        "email": "silvia.rasia@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Dell'Acqua",
        "nome": "Fabio",
        "email": "fabio.dellacqua@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Rho",
        "nome": "Enrico",
        "email": "enrico.rho@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PROGETTAZIONE ESECUTIVA",
        "referente": "Russo"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "El Allami",
        "nome": "Mohamed",
        "email": "mohamed.elallami@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Faedda",
        "nome": "Gianluca",
        "email": "gianluca.faedda@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "VERONA",
        "team": "VERONA",
        "referente": "Tosatto"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Ferrighetto",
        "nome": "Tullio",
        "email": "tullio.ferrighetto@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "VERONA",
        "team": "VERONA",
        "referente": "Tosatto"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Rosati",
        "nome": "Roberta",
        "email": "roberta.rosati@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Prezioso"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Rosi",
        "nome": "Alessandra",
        "email": "alessandra.rosi@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "VINCOLI",
        "referente": "Bosetto"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Russo",
        "nome": "Franco",
        "email": "franco.russo@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "UFFICIO TECNICO",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Graziano",
        "nome": "Samuel",
        "email": "samuel.graziano@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Marchini",
        "nome": "Andrea",
        "email": "andrea.marchini@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Mato Obregon",
        "nome": "Juan Carlos",
        "email": "juancarlos.matoobregon@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Sampietro",
        "nome": "Domenica",
        "email": "domenica.sampietro@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Prezioso"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Sandrini",
        "nome": "Cristian",
        "email": "cristian.sandrini@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DL&SIC",
        "referente": "Maragno"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Sanguineti",
        "nome": "Antonio",
        "email": "antonio.sanguineti@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "SEDE GENOVA",
        "team": "DL&SIC",
        "referente": "Sampaolesi"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Mendolaro",
        "nome": "Giuseppe",
        "email": "giuseppe.mendolaro@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Sava",
        "nome": "Giampaolo",
        "email": "giampaolo.sava@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "SEDE ROMA",
        "team": "DL&SIC",
        "referente": "Tomassini"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Scardovelli",
        "nome": "Cracchiolo",
        "email": "m.cracchiolo@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "PM (AI SPECIALIST)",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Murgo",
        "nome": "Lorenzo",
        "email": "lorenzo.murgo@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Noreddine",
        "nome": "Adil",
        "email": "adil.noreddine@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Sertogullarindan",
        "nome": "Merve",
        "email": "merve.sertogullarindan@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Prezioso"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Oselin",
        "nome": "Sebastiano",
        "email": "sebastiano.oselin@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "VERONA",
        "team": "VERONA",
        "referente": "Tosatto"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Simoncini",
        "nome": "Luca",
        "email": "luca.simoncini@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "MOBILITA' ELETTRICA",
        "team": "PERMESSI",
        "referente": "Prezioso"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Simonelli",
        "nome": "Cristina",
        "email": "cristina.simonelli@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Patrascu",
        "nome": "Dorinel",
        "email": "dorinel.patrascu@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Suma",
        "nome": "Carlo",
        "email": "carlo.suma@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "DL&SIC",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Perego",
        "nome": "Silvio",
        "email": "silvio.perego@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "AMMINISTRAZIONE",
        "referente": "Redaelli"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Testa",
        "nome": "Marco",
        "email": "marco.testa@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "UFFICIO TECNICO",
        "referente": "Russo"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Perfetti",
        "nome": "Matteo",
        "email": "matteo.perfetti@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Villa"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Thomas",
        "nome": "Ashlin",
        "email": "ashlin.thomas@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "PROGETTAZIONE ELETTRICA",
        "referente": "Tirelli"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Tirelli",
        "nome": "Csillag",
        "email": "matteo.tirelli@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "PROGETTAZIONE ELETTRICA",
        "referente": "Villa"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Pozzi",
        "nome": "Attilio",
        "email": "attilio.pozzi@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Rodriguez Gamboa",
        "nome": "Max Anders",
        "email": "maxrodriguez.gamboa@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Romano",
        "nome": "Ottavio",
        "email": "ottavio.romano@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "HSE",
        "team": "HSE",
        "referente": "Pisanu"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Russo",
        "nome": "Roberto",
        "email": "roberto.russo@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Toure",
        "nome": "Alassane Youssouf",
        "email": "youssouf.toure@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "PM (AI SPECIALIST)",
        "referente": "Scardovelli"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Santagata",
        "nome": "Iolanda Domenica",
        "email": "iolanda.santagata@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "AMMINISTRAZIONE",
        "referente": "Redaelli"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Tuttobene",
        "nome": "Cristofero",
        "email": "cristofero.tuttobene@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Uzoma",
        "nome": "Daniela",
        "email": "daniela.uzoma@hqcon.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "AMMINISTRAZIONE",
        "team": "AMMINISTRAZIONE",
        "referente": "Briguglio"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Semeraro",
        "nome": "Giuseppe",
        "email": "giuseppe.semeraro@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Shabi",
        "nome": "Aurid",
        "email": "aurid.shabi@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "VERONA",
        "team": "VERONA",
        "referente": "Tosatto"
    },
    {
        "azienda": "CONSORZIO HQ",
        "cognome": "Verga",
        "nome": "Claudio",
        "email": "claudio.verga@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "DIREZIONE",
        "referente": "Verga"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Tosatto",
        "nome": "Gabriele",
        "email": "gabriele.tosatto@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "VERONA",
        "team": "VERONA",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Vieni",
        "nome": "Giuseppe",
        "email": "giuseppe.vieni@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "RINNOVABILI",
        "team": "ACQUISIZIONE",
        "referente": "Bosetto"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Villa",
        "nome": "Alberto",
        "email": "alberto.villa@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "GRUPPO",
        "team": "DIREZIONE",
        "referente": "Barbera"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Trotta",
        "nome": "Nicola",
        "email": "nicola.trotta@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Villalun",
        "nome": "Jovana",
        "email": "jovana.villalun@hqe.it",
        "inquadramento": "CoCoCo",
        "maxDays": 4,
        "bu": "RADIOMOBILE",
        "team": "PERMESSI",
        "referente": "Pisanu"
    },
    {
        "azienda": "HQ ENGINEERING SRL",
        "cognome": "Vincenti",
        "nome": "Luisella",
        "email": "luisella.vincenti@hqe.it",
        "inquadramento": "PartitaIVA",
        "maxDays": 4,
        "bu": "SEDE PADOVA",
        "team": "SEDE PADOVA",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Vadori",
        "nome": "Riccardo",
        "email": "riccardo.vadori@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Perfetti"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Zanga",
        "nome": "Gianluca",
        "email": "gianluca.zanga@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "MILANO",
        "team": "MILANO",
        "referente": "Morolla"
    },
    {
        "azienda": "QTECH SRL",
        "cognome": "Zavoli",
        "nome": "Sandro",
        "email": "sandro.zavoli@qtech.it",
        "inquadramento": "Dipendente",
        "maxDays": 4,
        "bu": "CONSULENZA",
        "team": "CONSULENZA",
        "referente": "Morolla"
    }
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
