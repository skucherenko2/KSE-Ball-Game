from abc import abstractmethod
from datetime import datetime

from pygame import Color, Vector2, Surface

from Source.config import default_font, PLAYER_SIZE


class DecorativeObject:
    def __init__(self):
        self.spawn_time = datetime.now()
        self.position = Vector2(0, 0)

    @abstractmethod
    def render(self, screen, dt):
        pass

class DecorativeSprite(DecorativeObject):
    def __init__(self, surface: Surface, initial_position: Vector2, time: float, velocity: Vector2):
        super().__init__()
        self.surface = surface
        move_vector = velocity.normalize().copy()
        self.position = initial_position - move_vector * PLAYER_SIZE
        self.time = time
        self.velocity = velocity

    def render(self, screen, dt):
        live_time = (datetime.now() - self.spawn_time).total_seconds()
        if live_time > self.time:
            del self
            return
        self.position += -self.velocity * dt
        self.velocity = self.velocity * 0.95

        time_percentage = live_time / self.time

        self.surface.set_alpha(min(int((1 - time_percentage) * 255), 100))

        screen.blit(self.surface, self.position - Vector2(self.surface.get_size()) / 2)


class DecorativeText(DecorativeObject):
    def __init__(self, text: str, color: Color, time: float, initial_position: Vector2):
        super().__init__()
        self.text = text
        self.color = color
        self.time = time
        self.position = initial_position

    def render(self, screen, dt):
        live_time = (datetime.now() - self.spawn_time).total_seconds()
        if live_time > self.time:
            del self
            return
        self.position.y -= 25 * dt

        render_text = default_font.render(f"{self.text}", False, self.color)
        render_text.set_alpha(255 - max(0.2, live_time / self.time) * 255)
        screen.blit(render_text, self.position - Vector2(default_font.size(self.text)) / 2)