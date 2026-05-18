from graphics import TextButton

class StartMenuModel:
    def __init__(self):
        self._buttons = [
        TextButton(48, 48, "Play", 1),
        TextButton(48, 96, "Settings", 1)
        ]
        self._states = ["play", "settings"]
        self._current_tick = 1
        self._is_current_screen = True
        self._state = self.base_state

    @property
    def is_current_screen(self):
        return self._is_current_screen

    @property
    def buttons(self):
        return self._buttons
    
    @property
    def state(self):
        return self._state

    @property
    def current_tick(self):
        return self._current_tick

    @property
    def base_state(self):
        return "main"

    def update(self, clicked_idx):
        if self._is_current_screen:
            self._current_tick += 1
            if clicked_idx is not None:
                self.change_screen(self._states[clicked_idx])

    def change_screen(self, state):
        self._is_current_screen = False
        self._current_tick = 1
        self._state = state

    def start_screen(self):
        self._is_current_screen = True
        self._current_tick = 1
        self._state = "main"