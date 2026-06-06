from .model_settings import SettingsModel
from .view_settings import SettingsView
from graphics import Screen, TextButton
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_FONT_SIZE


class SettingsController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def get_clicked_screen_change_button(self):
        actions = ["main_menu", "save"] 
        clicked_btn = self._view.get_clicked_button(self._model.screen_change_buttons)
        if clicked_btn is not None:
            if actions[clicked_btn] == "save":
                self._model.save()
            return actions[clicked_btn]

    def update(self):
        clicked_idx = self._view.get_clicked_button(self._model.screen_change_buttons)
        self._update_lives()
        self._update_enemies()
        self._update_regenerator()
        self._update_chameleon()
        self._update_smooth_movement()
        self._model.update(clicked_idx)

    def _update_lives(self):
        if self._model.lives_decrease_button.is_left_clicked():
            self._model.decrease_lives()
        if self._model.lives_increase_button.is_left_clicked():
            self._model.increase_lives()
    
    def _update_enemies(self):
        if self._model.enemies_decrease_button.is_left_clicked():
            self._model.decrease_enemies()
        if self._model.enemies_increase_button.is_left_clicked():
            self._model.increase_enemies()
    
    def _update_regenerator(self):
        if self._model.regenerator_decrease_button.is_left_clicked():
            self._model.decrease_regenerator()
        if self._model.regenerator_increase_button.is_left_clicked():
            self._model.increase_regenerator()
    
    def _update_chameleon(self):
        if self._model.chameleon_decrease_button.is_left_clicked():
            self._model.decrease_chameleon()
        if self._model.chameleon_increase_button.is_left_clicked():
            self._model.increase_chameleon()
    
    def _update_smooth_movement(self):
        if self._view.is_smooth_movement_clicked():
            self._model.toggle_smooth_movement()

    def draw(self):
        self._view.reset_screen()
        self._view.draw_background()
        self._view.draw_buttons(self._model.screen_change_buttons)
        self._draw_lives_buttons()
        self._draw_enemies_buttons()
        self._draw_regenerator_buttons()
        self._draw_chameleon_buttons()
        self._view.draw_smooth_movement(self._model.smooth_movement)
    
    def _draw_lives_buttons(self):
        self._view.draw_buttons([self._model.lives_decrease_button, self._model.lives_increase_button])  
        self._view.draw_lives_label(self._model.lives)
    
    def _draw_enemies_buttons(self):
        self._view.draw_buttons([self._model.enemies_decrease_button, self._model.enemies_increase_button])  
        self._view.draw_enemies_label(self._model.enemies)
    
    def _draw_regenerator_buttons(self):
        self._view.draw_buttons([self._model.regenerator_decrease_button, self._model.regenerator_increase_button])  
        self._view.draw_regenerator_label(self._model.regenerator_interval)

    def _draw_chameleon_buttons(self):
        self._view.draw_buttons([self._model.chameleon_decrease_button, self._model.chameleon_increase_button])  
        self._view.draw_chameleon_label(self._model.chameleon_interval)

model = SettingsModel()


view = SettingsView(SCREEN_WIDTH, SCREEN_HEIGHT)
controller = SettingsController(model, view)

SettingsScreen = Screen(model, view, controller)