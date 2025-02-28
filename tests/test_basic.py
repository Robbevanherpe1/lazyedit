import pytest
from lazyedit.terminal import Terminal

def test_basic_import():
    terminal = Terminal()
    assert terminal is not None
