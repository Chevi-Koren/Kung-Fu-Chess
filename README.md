# Kung-Fu Chess

## Overview
Kung-Fu Chess is a real-time, multiplayer chess game with a unique twist: players can move their pieces simultaneously, introducing speed, strategy, and action to classic chess. The project features a server-client architecture using WebSocket for fast communication and supports both local and networked play.

## Features
- Real-time chess gameplay (no turns)
- Two-player support (White and Black)
- Keyboard controls for each player
- Pawn promotion, win detection, and scoring
- Sound effects and game logging
- Modular design for easy extension

## Technologies
- Python 3.8+
- OpenCV
- numpy
- keyboard
- pygame
- WebSocket (for server-client communication)

## Project Structure
- `KFC_Py/` - Main game logic, server, client, graphics, input, factories, tests
- `KungFu Chess/` - Alternative implementation (legacy or reference)
- `pieces/` - Piece state definitions and transitions
- `pub/` - Logging, pub/sub, scoring, system tests

## How to Run
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the server:**
   ```bash
   python KFC_Py/chess_server.py
   ```
3. **Start each client (in separate terminals):**
   ```bash
   python KFC_Py/chess_client.py
   ```
   - The first client is assigned White, the second Black.

## Controls
### White Player
- Move: Arrow keys
- Jump: ENTER
- Special: `+`

### Black Player
- Move: W/A/S/D
- Jump: SPACE
- Special: `g`

## Gameplay Notes
- Select a piece, then use the jump key to perform a jump.
- If you see `[WARN] Player1 tried to jump but no piece selected`, select a piece first.
- Pawn promotion and win detection are automatic.

## Testing
Run unit and integration tests from the `KFC_Py/Tests/` and `pub/` folders.

## Author
Yocheved Koren