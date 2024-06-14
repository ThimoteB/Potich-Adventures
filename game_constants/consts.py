"""
Constants for the project.
"""

ZOOM_FACTOR = 2
GRAPHICAL_TILE_SIZE = 16 * ZOOM_FACTOR
TICK_RATE = 60
TICK_DURATION_MS = int(1 / TICK_RATE * 1000)
SOUND = False

# Network constants (used by server and client)
PAYLOAD_SIZE = 123456

# Server constants (server.py)
HOST: str = "0.0.0.0"
PORT: int = 44440

# Card constants (card.py)
CARD_SLOT_WIDTH = 150
CARD_SLOT_HEIGHT = 220

# Key constants (key.py)
KEY_SLOT_WIDTH = 80
KEY_SLOT_HEIGHT = 80
