# web/routes.py
import json
from flask import Blueprint, render_template, request, redirect, url_for

# Vi importerar tvättmaskinen vi just byggde i core
from core.processor import process_match_data

# Vi skapar en Blueprint för att hålla ordning på våra rutter separat från app.py
web_bp = Blueprint('web', __name__, template_folder='templates')

# En global (eller tillfällig) variabel i minnet för att spara matchen 
# så att redaktörerna kan titta på den efter att de skickats vidare.
# (I framtiden kan vi spara detta i en databas eller fil om vi vill).
AKTUELL_MATCH = {}

@web_bp.route('/')
def index():
    """Visar startvyn (antingen tom eller med den laddade matchen)"""
    return render_template('index.html', data=AKTUELL_MATCH)

@web_bp.route('/api/match', methods=['POST'])
def motta_match():
    """Denna rutt tar emot POST-anropet direkt från bokmärket"""
    global AKTUELL_MATCH
    
    # Hämta JSON-strängen som bokmärket skickade i formuläret
    raw_json_string = request.form.get('match_data')
    
    if not raw_json_string:
        return "Ingen matchdata mottogs", 400
        
    try:
        # Gör om strängen till ett Python-dictionary
        raw_data = json.loads(raw_json_string)
        
        # Kör datan genom vår processor (städar namn, etc.)
        cleaned_data = process_match_data(raw_data)
        
        # Spara i minnet så index-rutten kan visa den
        AKTUELL_MATCH = cleaned_data
        
        # Skicka redaktören vidare till den vanliga startsidan där gränssnittet visas
        return redirect(url_for('web.index'))
        
    except Exception as e:
        return f"Ett fel uppstod vid databehandlingen: {str(e)}", 500