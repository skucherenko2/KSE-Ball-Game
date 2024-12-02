import os.path


def register_score(score: int):
    prev_score = get_highscore()
    if score > prev_score:
        with open('score.txt', 'w') as file:
            file.write(str(score))

def get_highscore() -> int | None:
    if not os.path.exists("score.txt"):
        return None
    with open('score.txt', 'r') as file:
        return int(file.read())
