from datetime import datetime
from math import exp, cos, pi

from pygame import Vector2


class Shake:
    def __init__(self, max_time, power):
        self.max_time = max_time
        self.power = power
        self.start_time = datetime.now()

current_shakes: list[Shake] = []

def add_shake(time: float, power: float):
    current_shakes.append(Shake(time, power))

def oscillation(time: float) -> float:
    return exp(-time) * cos(2 * pi * time)

def get_shake_summ() -> Vector2:
    final_shake = Vector2(0, 0)
    for shake in current_shakes:
        delta_seconds = ((datetime.now() - shake.start_time).total_seconds() - shake.power / 10) / shake.max_time

        final_shake += Vector2(oscillation(delta_seconds) * 15,
                   oscillation(delta_seconds) * 15,
                   )

        if (datetime.now() - shake.start_time).total_seconds() > shake.max_time * 3:
            current_shakes.remove(shake)

    return final_shake
