from flask import Flask, render_template, request, session, redirect, url_for
import config
from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

app = Flask(__name__)
app.secret_key = 'kivi-paperi-sakset-secret-key-2025'

MODE_LABELS = {
    config.PVP: "Pelaaja vs Pelaaja",
    config.AI: "Pelaaja vs Tekoäly",
    config.PAREMPI_AI: "Pelaaja vs Parannettu Tekoäly"
}

def get_tuomari():
    if 'tuomari_state' not in session:
        session['tuomari_state'] = {'eka': 0, 'toka': 0, 'tie': 0}
    state = session['tuomari_state']
    tuomari = Tuomari()
    tuomari.ekan_pisteet = state['eka']
    tuomari.tokan_pisteet = state['toka']
    tuomari.tasapelit = state['tie']
    return tuomari

def save_tuomari(tuomari):
    session['tuomari_state'] = {
        'eka': tuomari.ekan_pisteet,
        'toka': tuomari.tokan_pisteet,
        'tie': tuomari.tasapelit
    }

def get_ai():
    mode = session.get('mode')
    if mode == config.AI:
        if 'ai_state' not in session:
            session['ai_state'] = {'type': 'simple', 'siirto': 0}
        ai = Tekoaly()
        ai._siirto = session['ai_state']['siirto']
        return ai
    elif mode == config.PAREMPI_AI:
        if 'ai_state' not in session:
            session['ai_state'] = {'type': 'parannettu', 'muisti': [None] * config.MUISTI, 'index': 0}
        ai = TekoalyParannettu(config.MUISTI)
        state = session['ai_state']
        # Ensure muisti is properly sized list
        if len(state['muisti']) < config.MUISTI:
            state['muisti'] = (state['muisti'] + [None] * config.MUISTI)[:config.MUISTI]
        ai._muisti = state['muisti']
        ai._vapaa_muisti_indeksi = state['index']
        return ai
    return None

def save_ai(ai):
    if isinstance(ai, Tekoaly):
        session['ai_state'] = {'type': 'simple', 'siirto': ai._siirto}
    elif isinstance(ai, TekoalyParannettu):
        session['ai_state'] = {
            'type': 'parannettu',
            'muisti': ai._muisti,
            'index': ai._vapaa_muisti_indeksi
        }

def valid_move(move):
    return move in (config.KIVI, config.PAPERI, config.SAKSET)

def get_overall_stats():
    """Get or initialize overall statistics."""
    if 'overall_stats' not in session:
        session['overall_stats'] = {
            config.PVP: {'wins': 0, 'losses': 0},
            config.AI: {'wins': 0, 'losses': 0},
            config.PAREMPI_AI: {'wins': 0, 'losses': 0}
        }
    return session['overall_stats']

@app.route('/')
def home():
    stats = get_overall_stats()
    # Clear game state but preserve overall stats
    overall = session.get('overall_stats', {})
    session.clear()
    session['overall_stats'] = overall
    return render_template('home.html', overall_stats=stats)

@app.route('/start', methods=['POST'])
def start():
    mode = request.form.get('mode')
    if mode not in (config.PVP, config.AI, config.PAREMPI_AI):
        return redirect(url_for('home'))
    session['mode'] = mode
    session['tuomari_state'] = {'eka': 0, 'toka': 0, 'tie': 0}
    if mode in (config.AI, config.PAREMPI_AI):
        get_ai()  # Initialize AI state
    return redirect(url_for('play'))

@app.route('/play')
def play():
    mode = session.get('mode')
    if not mode:
        return redirect(url_for('home'))
    
    tuomari = get_tuomari()
    last = session.get('last')
    game_over = session.get('game_over')
    overall_stats = get_overall_stats()
    
    return render_template(
        'play.html',
        mode=mode,
        mode_label=MODE_LABELS.get(mode, "Peli"),
        score_eka=tuomari.ekan_pisteet,
        score_toka=tuomari.tokan_pisteet,
        score_tie=tuomari.tasapelit,
        last=last,
        game_over=game_over,
        overall_stats=overall_stats
    )

@app.route('/move', methods=['POST'])
def move():
    mode = session.get('mode')
    if not mode:
        return redirect(url_for('home'))
    
    # Check if game is already over
    if session.get('game_over'):
        return redirect(url_for('play'))
    
    eka_move = request.form.get('eka')
    
    if not valid_move(eka_move):
        session['last'] = {'message': 'Virheellinen siirto!', 'eka': eka_move or '?', 'toka': ''}
        return redirect(url_for('play'))
    
    # Get second move
    if mode == config.PVP:
        toka_move = request.form.get('toka')
        if not valid_move(toka_move):
            session['last'] = {'message': 'Virheellinen siirto!', 'eka': eka_move, 'toka': toka_move or '?'}
            return redirect(url_for('play'))
    else:
        ai = get_ai()
        toka_move = ai.anna_siirto()
        ai.aseta_siirto(eka_move)
        save_ai(ai)
    
    # Judge the round
    tuomari = get_tuomari()
    tuomari.kirjaa_siirto(eka_move, toka_move)
    save_tuomari(tuomari)
    
    # Determine result message
    if eka_move == toka_move:
        result_msg = "Tasapeli"
    elif (eka_move == config.KIVI and toka_move == config.SAKSET) or \
         (eka_move == config.SAKSET and toka_move == config.PAPERI) or \
         (eka_move == config.PAPERI and toka_move == config.KIVI):
        result_msg = "Voitit!"
    else:
        result_msg = "Hävisit"
    
    session['last'] = {
        'eka': eka_move,
        'toka': toka_move,
        'message': result_msg
    }
    
    # Check for game over (3 wins)
    if tuomari.ekan_pisteet >= 3:
        session['game_over'] = {
            'winner': 'player1',
            'message': 'Pelaaja 1 voitti pelin!',
            'final_score': f"{tuomari.ekan_pisteet} - {tuomari.tokan_pisteet}"
        }
        # Update overall statistics
        overall_stats = get_overall_stats()
        overall_stats[mode]['wins'] += 1
        session['overall_stats'] = overall_stats
    elif tuomari.tokan_pisteet >= 3:
        opponent_name = 'Pelaaja 2' if mode == config.PVP else 'Tekoäly'
        session['game_over'] = {
            'winner': 'player2',
            'message': f'{opponent_name} voitti pelin!',
            'final_score': f"{tuomari.ekan_pisteet} - {tuomari.tokan_pisteet}"
        }
        # Update overall statistics
        overall_stats = get_overall_stats()
        overall_stats[mode]['losses'] += 1
        session['overall_stats'] = overall_stats
    
    return redirect(url_for('play'))

@app.route('/reset')
def reset():
    mode = session.get('mode')
    overall_stats = get_overall_stats()
    session.clear()
    if mode:
        session['mode'] = mode
        session['overall_stats'] = overall_stats
        if mode in (config.AI, config.PAREMPI_AI):
            get_ai()
    return redirect(url_for('play'))

if __name__ == '__main__':
    print("Starting Kivi-Paperi-Sakset web app...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, host='127.0.0.1', port=5000)
