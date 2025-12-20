# Kivi-Paperi-Sakset Web App - Testing

## Running the Tests

To run the complete test suite:

```powershell
poetry run pytest src/tests/ -v
```

For a quick test run without verbose output:

```powershell
poetry run pytest src/tests/
```

To run with coverage report:

```powershell
poetry run pytest src/tests/ --cov=src --cov-report=html
```

## Test Coverage

The test suite includes **38 comprehensive tests** covering:

### 1. Home Page (2 tests)
- Page loads successfully
- Session cleared on home page access

### 2. Game Modes (4 tests)
- PvP mode initialization
- Simple AI mode initialization
- Improved AI mode initialization
- Invalid mode handling

### 3. Play Page (2 tests)
- Redirect when no mode selected
- Score display

### 4. PvP Gameplay (5 tests)
- Valid moves and scoring
- Tie detection
- Win/loss scenarios
- Invalid move validation (both players)

### 5. AI Gameplay (3 tests)
- AI move generation
- AI state persistence
- Invalid player move handling

### 6. Improved AI Gameplay (2 tests)
- Move generation
- Memory/learning functionality

### 7. Score Tracking (2 tests)
- Score accumulation over rounds
- All winning combinations (rock/paper/scissors)

### 8. Victory Condition (6 tests)
- Player 1 wins at 5 victories
- Player 2/AI wins at 5 victories
- No moves allowed after game over
- Victory screen displays correctly
- Game continues before 5 wins
- AI can reach victory

### 9. Reset Functionality (3 tests)
- Score reset while preserving mode
- Game over state cleared on reset
- Reset behavior without active mode

### 10. Session Management (2 tests)
- Move without mode redirects
- Session isolation between clients

### 11. Overall Statistics (7 tests)
- Statistics initialization on first visit
- Win counter incrementation
- Loss counter incrementation
- Stats persistence across multiple games
- Stats preservation when returning home
- Different mode stats tracked separately
- Stats display on home page

## Test Strategy

Tests use Flask's test client to simulate HTTP requests without running a server. Each test is isolated with fresh sessions to ensure no state bleeding between tests.

### Key Testing Patterns

- **Fixtures**: `client` and `session_client` provide test clients
- **Session testing**: Direct session manipulation to verify state management
- **Integration**: Tests verify full request/response cycles
- **Edge cases**: Invalid inputs, missing sessions, boundary conditions
- **Victory logic**: Ensures games end at 5 wins and display victory screen
- **Statistics tracking**: Verifies persistent win/loss tracking across games

## Continuous Integration

Run tests after any code change to verify functionality:

```powershell
# After editing web_app.py
poetry run pytest src/tests/ -v

# After editing templates or static files
poetry run pytest src/tests/ -v
```

All 38 tests should pass before deploying changes.
