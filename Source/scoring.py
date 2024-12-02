from Source import game


def apply_score_for_one_planet():
    if game.death_time is None:
        game.score += 1