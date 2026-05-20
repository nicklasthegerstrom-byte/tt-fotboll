# web/routes.py
import json
from flask import Blueprint, render_template, request

# Vi importerar tvättmaskinen vi just byggde i core
from core.processor import process_match_data

# Vi behåller din Blueprint exakt som den är
web_bp = Blueprint('web', __name__, template_folder='templates')

@web_bp.route('/')
def index():
    """Visar den tomma startvyn om man bara surfar direkt till sajten"""
    return render_template('index.html', data=None)

@web_bp.route('/api/match', methods=['POST'])
def motta_match():
    """Denna rutt tar emot matchen från bokmärket och visar verktyget direkt"""
    
    # Hämta JSON-strängen som bokmärket skickade i formuläret
    raw_json_string = request.form.get('match_data')
    
    if not raw_json_string:
        return "Ingen matchdata mottogs", 400
        
    try:
        # Gör om strängen till ett Python-dictionary
        raw_data = json.loads(raw_json_string)
        
        # Kör datan genom vår processor (städar namn, etc.)
        cleaned_data = process_match_data(raw_data)
        
        # BÄSTA BITEN: Vi skippar redirect och sessions helt!
        # Vi ritar ut gränssnittet direkt till just den här användaren.
        # Det gör att matchen bara existerar i den här specifika fliken just nu.
        return render_template('index.html', data=cleaned_data)
        
    except Exception as e:
        return f"Ett fel uppstod vid databehandlingen: {str(e)}", 500