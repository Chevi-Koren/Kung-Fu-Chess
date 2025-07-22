import pytest
from KeyboardInput import KeyboardProcessor

class FakeEvent:
    def __init__(self, name):
        self.name = name
        self.event_type = "down"

@pytest.fixture
def keymap1():
    return {
        'w': 'up',
        's': 'down',
        'a': 'left',
        'd': 'right',
        'enter': 'choose',
        '+': 'jump'
    }

def test_initial_position_and_get_cursor(keymap1):
    kp = KeyboardProcessor(8, 8, keymap1)
    assert kp.get_cursor() == (0, 0)

def test_cursor_moves_and_wraps(keymap1):
    kp = KeyboardProcessor(2, 3, keymap1)
    kp.process_key(FakeEvent('w'))  # up from (0,0) → stays (0,0)
    assert kp.get_cursor() == (0, 0)
    kp.process_key(FakeEvent('s'))  # down → (1,0)
    assert kp.get_cursor() == (1, 0)
    kp.process_key(FakeEvent('s'))  # down again → still (1,0)
    assert kp.get_cursor() == (1, 0)
    kp.process_key(FakeEvent('a'))  # left → (1,0) stays (0)
    assert kp.get_cursor() == (1, 0)
    kp.process_key(FakeEvent('d'))  # right → (1,1)
    assert kp.get_cursor() == (1, 1)

def test_choose_and_jump_return_actions(keymap1):
    kp = KeyboardProcessor(5, 5, keymap1)
    kp._cursor = [3, 4]
    choice = kp.process_key(FakeEvent('enter'))
    assert choice == 'choose'
    jump = kp.process_key(FakeEvent('+'))
    assert jump == 'jump'
    assert kp.process_key(FakeEvent('w')) == 'up'
    assert kp.process_key(FakeEvent('x')) is None  # unknown key

def test_custom_keymaps():
    km2 = {
        'i': 'up',
        'k': 'down',
        'j': 'left',
        'l': 'right',
        'o': 'choose',
        'p': 'jump'
    }
    kp = KeyboardProcessor(5, 5, km2)
    kp.process_key(FakeEvent('i'))  # up → (0,0) stays (0,0)
    assert kp.get_cursor() == (0, 0)
    kp.process_key(FakeEvent('k'))  # down → (1,0)
    assert kp.get_cursor() == (1, 0)
    kp._cursor = [2, 2]
    assert kp.process_key(FakeEvent('o')) == 'choose'
    assert kp.process_key(FakeEvent('p')) == 'jump'
