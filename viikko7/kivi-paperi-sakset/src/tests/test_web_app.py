import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from web_app import app
import config


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client


@pytest.fixture
def session_client():
    """Create a test client with session tracking."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess.clear()
        yield client


class TestHomePage:
    """Test the home page functionality."""
    
    def test_home_page_loads(self, client):
        """Home page should load successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi' in response.data
        assert b'Paperi' in response.data
        assert b'Sakset' in response.data
    
    def test_home_page_clears_session(self, session_client):
        """Home page should clear any existing session."""
        with session_client.session_transaction() as sess:
            sess['mode'] = 'a'
            sess['tuomari_state'] = {'eka': 5, 'toka': 3, 'tie': 1}
        
        session_client.get('/')
        
        with session_client.session_transaction() as sess:
            assert 'mode' not in sess
            assert 'tuomari_state' not in sess


class TestGameModes:
    """Test different game mode selections."""
    
    def test_start_pvp_mode(self, session_client):
        """Starting PvP mode should set session and redirect."""
        response = session_client.post('/start', data={'mode': config.PVP})
        assert response.status_code == 302
        assert '/play' in response.location
        
        with session_client.session_transaction() as sess:
            assert sess['mode'] == config.PVP
            assert sess['tuomari_state'] == {'eka': 0, 'toka': 0, 'tie': 0}
    
    def test_start_ai_mode(self, session_client):
        """Starting AI mode should initialize AI state."""
        response = session_client.post('/start', data={'mode': config.AI})
        assert response.status_code == 302
        
        with session_client.session_transaction() as sess:
            assert sess['mode'] == config.AI
            assert 'ai_state' in sess
            assert sess['ai_state']['type'] == 'simple'
    
    def test_start_improved_ai_mode(self, session_client):
        """Starting improved AI mode should initialize parannettu AI state."""
        response = session_client.post('/start', data={'mode': config.PAREMPI_AI})
        assert response.status_code == 302
        
        with session_client.session_transaction() as sess:
            assert sess['mode'] == config.PAREMPI_AI
            assert 'ai_state' in sess
            assert sess['ai_state']['type'] == 'parannettu'
            assert len(sess['ai_state']['muisti']) == config.MUISTI
    
    def test_start_invalid_mode_redirects(self, session_client):
        """Invalid mode should redirect to home."""
        response = session_client.post('/start', data={'mode': 'invalid'})
        assert response.status_code == 302
        assert response.location == '/'


class TestPlayPage:
    """Test the play page display."""
    
    def test_play_without_mode_redirects(self, client):
        """Accessing play without mode should redirect to home."""
        response = client.get('/play')
        assert response.status_code == 302
        assert response.location == '/'
    
    def test_play_displays_score(self, session_client):
        """Play page should display current scores."""
        with session_client.session_transaction() as sess:
            sess['mode'] = config.PVP
            sess['tuomari_state'] = {'eka': 3, 'toka': 2, 'tie': 1}
        
        response = session_client.get('/play')
        assert response.status_code == 200
        assert b'3' in response.data  # Player 1 score
        assert b'2' in response.data  # Player 2 score
        assert b'1' in response.data  # Ties


class TestPvPGameplay:
    """Test Player vs Player gameplay."""
    
    def test_pvp_valid_moves(self, session_client):
        """Valid PvP moves should update scores."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Player 1 plays rock, Player 2 plays scissors - Player 1 wins
        response = session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        assert response.status_code == 302
        
        with session_client.session_transaction() as sess:
            assert sess['tuomari_state']['eka'] == 1
            assert sess['tuomari_state']['toka'] == 0
            assert sess['last']['message'] == 'Voitit!'
    
    def test_pvp_tie(self, session_client):
        """Same moves should result in tie."""
        session_client.post('/start', data={'mode': config.PVP})
        
        session_client.post('/move', data={'eka': 'p', 'toka': 'p'})
        
        with session_client.session_transaction() as sess:
            assert sess['tuomari_state']['tie'] == 1
            assert sess['last']['message'] == 'Tasapeli'
    
    def test_pvp_player2_wins(self, session_client):
        """Player 2 can win."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Player 1 plays scissors, Player 2 plays rock - Player 2 wins
        session_client.post('/move', data={'eka': 's', 'toka': 'k'})
        
        with session_client.session_transaction() as sess:
            assert sess['tuomari_state']['toka'] == 1
            assert sess['last']['message'] == 'Hävisit'
    
    def test_pvp_invalid_first_move(self, session_client):
        """Invalid first player move should show error."""
        session_client.post('/start', data={'mode': config.PVP})
        
        session_client.post('/move', data={'eka': 'x', 'toka': 'k'})
        
        with session_client.session_transaction() as sess:
            assert 'Virheellinen siirto!' in sess['last']['message']
    
    def test_pvp_invalid_second_move(self, session_client):
        """Invalid second player move should show error."""
        session_client.post('/start', data={'mode': config.PVP})
        
        session_client.post('/move', data={'eka': 'k', 'toka': 'invalid'})
        
        with session_client.session_transaction() as sess:
            assert 'Virheellinen siirto!' in sess['last']['message']


class TestAIGameplay:
    """Test Player vs AI gameplay."""
    
    def test_ai_makes_move(self, session_client):
        """AI should make a valid move."""
        session_client.post('/start', data={'mode': config.AI})
        
        response = session_client.post('/move', data={'eka': 'k'})
        assert response.status_code == 302
        
        with session_client.session_transaction() as sess:
            assert 'last' in sess
            assert sess['last']['toka'] in ['k', 'p', 's']
    
    def test_ai_state_persists(self, session_client):
        """AI state should persist between moves."""
        session_client.post('/start', data={'mode': config.AI})
        
        session_client.post('/move', data={'eka': 'k'})
        session_client.post('/move', data={'eka': 'p'})
        
        with session_client.session_transaction() as sess:
            # Simple AI cycles through moves, so state should change
            assert 'ai_state' in sess
    
    def test_ai_invalid_player_move(self, session_client):
        """Invalid player move against AI should show error."""
        session_client.post('/start', data={'mode': config.AI})
        
        session_client.post('/move', data={'eka': 'invalid'})
        
        with session_client.session_transaction() as sess:
            assert 'Virheellinen siirto!' in sess['last']['message']


class TestImprovedAIGameplay:
    """Test Player vs Improved AI gameplay."""
    
    def test_improved_ai_makes_move(self, session_client):
        """Improved AI should make a valid move."""
        session_client.post('/start', data={'mode': config.PAREMPI_AI})
        
        response = session_client.post('/move', data={'eka': 'p'})
        assert response.status_code == 302
        
        with session_client.session_transaction() as sess:
            assert 'last' in sess
            assert sess['last']['toka'] in ['k', 'p', 's']
    
    def test_improved_ai_learns(self, session_client):
        """Improved AI should update its memory."""
        session_client.post('/start', data={'mode': config.PAREMPI_AI})
        
        # Play several rounds
        for move in ['k', 'p', 's', 'k']:
            session_client.post('/move', data={'eka': move})
        
        with session_client.session_transaction() as sess:
            # Memory should have recorded moves
            assert sess['ai_state']['index'] > 0
            assert any(m is not None for m in sess['ai_state']['muisti'])


class TestScoreTracking:
    """Test score tracking across multiple rounds."""
    
    def test_score_accumulates(self, session_client):
        """Scores should accumulate over multiple rounds."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Round 1: Player 1 wins (rock beats scissors)
        session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        # Round 2: Player 2 wins (paper beats rock)
        session_client.post('/move', data={'eka': 'k', 'toka': 'p'})
        # Round 3: Tie
        session_client.post('/move', data={'eka': 's', 'toka': 's'})
        
        with session_client.session_transaction() as sess:
            assert sess['tuomari_state']['eka'] == 1
            assert sess['tuomari_state']['toka'] == 1
            assert sess['tuomari_state']['tie'] == 1
    
    def test_all_winning_combinations(self, session_client):
        """Test all possible winning combinations."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Rock beats scissors
        session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        assert session_client.get('/play').status_code == 200
        
        # Paper beats rock
        session_client.post('/move', data={'eka': 'p', 'toka': 'k'})
        
        # Scissors beats paper
        session_client.post('/move', data={'eka': 's', 'toka': 'p'})
        
        with session_client.session_transaction() as sess:
            assert sess['tuomari_state']['eka'] == 3


class TestVictoryCondition:
    """Test the 3-win victory condition."""
    
    def test_player1_wins_at_three(self, session_client):
        """Game should end when player 1 reaches 3 wins."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Player 1 wins 3 rounds (rock beats scissors)
        for _ in range(3):
            session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        with session_client.session_transaction() as sess:
            assert sess['tuomari_state']['eka'] == 3
            assert 'game_over' in sess
            assert sess['game_over']['winner'] == 'player1'
            assert 'Pelaaja 1 voitti' in sess['game_over']['message']
    
    def test_player2_wins_at_three_pvp(self, session_client):
        """Game should end when player 2 reaches 3 wins in PvP."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Player 2 wins 3 rounds (paper beats rock)
        for _ in range(3):
            session_client.post('/move', data={'eka': 'k', 'toka': 'p'})
        
        with session_client.session_transaction() as sess:
            assert sess['tuomari_state']['toka'] == 3
            assert 'game_over' in sess
            assert sess['game_over']['winner'] == 'player2'
            assert 'Pelaaja 2 voitti' in sess['game_over']['message']
    
    def test_ai_wins_at_three(self, session_client):
        """Game should end when AI reaches 3 wins."""
        session_client.post('/start', data={'mode': config.AI})
        
        # Simple AI pattern (increments then checks): p, s, k, p, s, k...
        # To make player lose: k (loses to p), p (loses to s), s (loses to k)
        player_losing_moves = ['k', 'p', 's', 'k', 'p', 's', 'k', 'p']
        
        for move in player_losing_moves:
            session_client.post('/move', data={'eka': move})
            with session_client.session_transaction() as sess:
                if sess.get('game_over'):
                    break
        
        with session_client.session_transaction() as sess:
            assert 'game_over' in sess
            assert sess['game_over']['winner'] == 'player2'
            assert 'Tekoäly voitti' in sess['game_over']['message']
    
    def test_no_moves_after_game_over(self, session_client):
        """Cannot make moves after game is over."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Player 1 wins 3 rounds
        for _ in range(3):
            session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        # Try to make another move
        response = session_client.post('/move', data={'eka': 'p', 'toka': 'k'})
        
        with session_client.session_transaction() as sess:
            # Score should not change
            assert sess['tuomari_state']['eka'] == 3
            assert sess['tuomari_state']['toka'] == 0
    
    def test_victory_screen_displays(self, session_client):
        """Victory screen should be shown when game ends."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Player 1 wins 3 rounds
        for _ in range(3):
            session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        response = session_client.get('/play')
        assert response.status_code == 200
        assert b'voitti pelin' in response.data or b'victory' in response.data
    
    def test_game_continues_before_three_wins(self, session_client):
        """Game should continue normally before 3 wins."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Player 1 wins 2 rounds
        for _ in range(2):
            session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        with session_client.session_transaction() as sess:
            assert sess['tuomari_state']['eka'] == 2
            assert 'game_over' not in sess
        
        # Should still be able to make moves
        response = session_client.post('/move', data={'eka': 'p', 'toka': 'k'})
        assert response.status_code == 302


class TestReset:
    """Test reset functionality."""
    
    def test_reset_clears_scores(self, session_client):
        """Reset should clear scores but keep mode."""
        session_client.post('/start', data={'mode': config.PVP})
        session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        # Reset
        response = session_client.get('/reset')
        assert response.status_code == 302
        
        with session_client.session_transaction() as sess:
            assert sess['mode'] == config.PVP
            assert sess.get('tuomari_state') is None
            assert sess.get('last') is None
            assert sess.get('game_over') is None
    
    def test_reset_clears_game_over(self, session_client):
        """Reset should clear game over state."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Win 5 rounds to trigger game over
        for _ in range(5):
            session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        with session_client.session_transaction() as sess:
            assert 'game_over' in sess
        
        # Reset
        session_client.get('/reset')
        
        with session_client.session_transaction() as sess:
            assert 'game_over' not in sess
            assert sess['mode'] == config.PVP
    
    def test_reset_without_mode_redirects(self, client):
        """Reset without active mode should redirect to play."""
        response = client.get('/reset')
        assert response.status_code == 302


class TestSessionManagement:
    """Test session state management."""
    
    def test_move_without_mode_redirects(self, client):
        """Making a move without mode should redirect."""
        response = client.post('/move', data={'eka': 'k'})
        assert response.status_code == 302
        assert response.location == '/'
    
    def test_session_isolation(self, client):
        """Each client should have isolated session."""
        # This test verifies that sessions don't bleed between requests
        response1 = client.post('/start', data={'mode': config.PVP})
        assert response1.status_code == 302
        
        # Create new client
        with app.test_client() as client2:
            response2 = client2.get('/play')
            assert response2.status_code == 302  # Should redirect (no mode)


class TestOverallStatistics:
    """Test overall game statistics tracking."""
    
    def test_stats_initialized_on_first_visit(self, session_client):
        """Overall stats should be initialized on first home visit."""
        session_client.get('/')
        
        with session_client.session_transaction() as sess:
            assert 'overall_stats' in sess
            assert config.PVP in sess['overall_stats']
            assert config.AI in sess['overall_stats']
            assert config.PAREMPI_AI in sess['overall_stats']
    
    def test_win_increments_stats(self, session_client):
        """Winning a game should increment win counter."""
        session_client.post('/start', data={'mode': config.PVP})
        
        # Player 1 wins 5 rounds
        for _ in range(5):
            session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        with session_client.session_transaction() as sess:
            assert sess['overall_stats'][config.PVP]['wins'] == 1
            assert sess['overall_stats'][config.PVP]['losses'] == 0
    
    def test_loss_increments_stats(self, session_client):
        """Losing a game should increment loss counter."""
        session_client.post('/start', data={'mode': config.AI})
        
        # Player loses 5 times
        player_losing_moves = ['k', 'p', 's', 'k', 'p', 's', 'k', 'p']
        for move in player_losing_moves:
            session_client.post('/move', data={'eka': move})
            with session_client.session_transaction() as sess:
                if sess.get('game_over'):
                    break
        
        with session_client.session_transaction() as sess:
            assert sess['overall_stats'][config.AI]['wins'] == 0
            assert sess['overall_stats'][config.AI]['losses'] == 1
    
    def test_stats_persist_across_games(self, session_client):
        """Stats should persist when starting new games."""
        # First game - win
        session_client.post('/start', data={'mode': config.PVP})
        for _ in range(5):
            session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        # Reset and play second game - lose
        session_client.get('/reset')
        for _ in range(5):
            session_client.post('/move', data={'eka': 'k', 'toka': 'p'})
        
        with session_client.session_transaction() as sess:
            assert sess['overall_stats'][config.PVP]['wins'] == 1
            assert sess['overall_stats'][config.PVP]['losses'] == 1
    
    def test_stats_preserved_when_returning_home(self, session_client):
        """Stats should be preserved when returning to home."""
        session_client.post('/start', data={'mode': config.PVP})
        for _ in range(5):
            session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        # Go home
        session_client.get('/')
        
        with session_client.session_transaction() as sess:
            assert sess['overall_stats'][config.PVP]['wins'] == 1
    
    def test_different_modes_tracked_separately(self, session_client):
        """Each mode should have separate statistics."""
        # Win in PvP
        session_client.post('/start', data={'mode': config.PVP})
        for _ in range(5):
            session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        # Go home and start AI mode
        session_client.get('/')
        session_client.post('/start', data={'mode': config.AI})
        
        with session_client.session_transaction() as sess:
            assert sess['overall_stats'][config.PVP]['wins'] == 1
            assert sess['overall_stats'][config.AI]['wins'] == 0
    
    def test_stats_display_on_home(self, session_client):
        """Home page should display overall statistics."""
        session_client.post('/start', data={'mode': config.PVP})
        for _ in range(5):
            session_client.post('/move', data={'eka': 'k', 'toka': 's'})
        
        response = session_client.get('/')
        assert response.status_code == 200
        # Should show wins/losses in some form
        assert b'Tilastot' in response.data or b'stats' in response.data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
