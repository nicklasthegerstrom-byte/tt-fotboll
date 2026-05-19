# core/processor.py

# Ordlista för TT:s standardförkortningar på klubbar (fyll på här efter hand)
KLUBB_REPLACEMENTS = {
    "Laholms FK": "Laholms",
    "Rosengård": "Rosengårds",
    "Djurgården": "Djurgårdens",
    "Malmö FF": "Malmös",
    "AIK": "AIKs",
    "Hammarby": "Hammarbys"  # Bara som exempel!
}

def process_match_data(raw_data):
    """
    Tar emot rå JSON från bokmärket, städar lagnamnen,
    och separerar spelarna i startelva och avbytare.
    """
    match_id = raw_data.get("matchId", "Okänt ID")
    raw_teams = raw_data.get("teams", [])
    
    cleaned_teams = []
    
    for team in raw_teams:
        raw_name = team.get("team", "")
        # Kör TT:s namn-replacement om det finns, annars behåll originalnamnet
        tt_team_name = KLUBB_REPLACEMENTS.get(raw_name, raw_name)
        
        # Vi skapar en renare struktur för varje lag
        team_obj = {
            "name": tt_team_name,
            "startelva": [],
            "avbytare": []
        }
        
        # Gå igenom alla spelare i laget
        for player in team.get("players", []):
            # En spelare är avbytare om "image" saknas eller om ni vill styra 
            # baserat på SvFF:s dolda logik (i din JSON är alla samlade i en lista).
            # SvFF:s XML sätter oftast de 11 första som startelva, eller använder positions-attribut.
            # För tillfället lägger vi alla i startelvan så fixar vi sorteringen sen!
            team_obj["startelva"].append({
                "id": player.get("id"),
                "number": player.get("number"),
                "firstName": player.get("firstName"),
                "lastName": player.get("lastName"),
                "captain": player.get("captain", False),
                "goalkeeper": player.get("goalkeeper", False),
                "goals": player.get("goals", 0),
                "assists": player.get("assists", 0)
            })
            
        cleaned_teams.append(team_box := team_obj)
        
    return {
        "matchId": match_id,
        "teams": cleaned_teams
    }