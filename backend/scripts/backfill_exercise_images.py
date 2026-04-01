import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.models.exercise import Exercise


KEYWORD_IMAGE_MAP: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"supino|peito|flex[aã]o|crucifixo|crossover|peck deck", re.IGNORECASE), "https://images.pexels.com/photos/3838389/pexels-photo-3838389.jpeg?auto=compress&cs=tinysrgb&w=600"),
    (re.compile(r"remada|puxada|barra fixa|pull|costas|deadlift|terra", re.IGNORECASE), "https://images.pexels.com/photos/949129/pexels-photo-949129.jpeg?auto=compress&cs=tinysrgb&w=600"),
    (re.compile(r"agachamento|leg press|afundo|lunge|quadr[ií]ceps|panturrilha|stiff", re.IGNORECASE), "https://images.pexels.com/photos/6456307/pexels-photo-6456307.jpeg?auto=compress&cs=tinysrgb&w=600"),
    (re.compile(r"ombro|eleva[cç][aã]o lateral|desenvolvimento|shoulder|arnold", re.IGNORECASE), "https://images.pexels.com/photos/4162585/pexels-photo-4162585.jpeg?auto=compress&cs=tinysrgb&w=600"),
    (re.compile(r"b[ií]ceps|rosca|curl", re.IGNORECASE), "https://images.pexels.com/photos/5327543/pexels-photo-5327543.jpeg?auto=compress&cs=tinysrgb&w=600"),
    (re.compile(r"tr[ií]ceps|paralela|mergulho|skull crusher", re.IGNORECASE), "https://images.pexels.com/photos/6550854/pexels-photo-6550854.jpeg?auto=compress&cs=tinysrgb&w=600"),
    (re.compile(r"abd[oô]men|prancha|core|ab wheel", re.IGNORECASE), "https://images.pexels.com/photos/6456141/pexels-photo-6456141.jpeg?auto=compress&cs=tinysrgb&w=600"),
    (re.compile(r"gl[uú]teo|hip thrust|ponte", re.IGNORECASE), "https://images.pexels.com/photos/6551410/pexels-photo-6551410.jpeg?auto=compress&cs=tinysrgb&w=600"),
    (re.compile(r"cardio|corrida|esteira|bike|el[ií]ptico|remo", re.IGNORECASE), "https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg?auto=compress&cs=tinysrgb&w=600"),
]

MUSCLE_GROUP_IMAGE_MAP: dict[str, str] = {
    "peito": "https://images.pexels.com/photos/3838389/pexels-photo-3838389.jpeg?auto=compress&cs=tinysrgb&w=600",
    "costas": "https://images.pexels.com/photos/949129/pexels-photo-949129.jpeg?auto=compress&cs=tinysrgb&w=600",
    "quadriceps": "https://images.pexels.com/photos/6456307/pexels-photo-6456307.jpeg?auto=compress&cs=tinysrgb&w=600",
    "posterior": "https://images.pexels.com/photos/6456307/pexels-photo-6456307.jpeg?auto=compress&cs=tinysrgb&w=600",
    "gluteos": "https://images.pexels.com/photos/6551410/pexels-photo-6551410.jpeg?auto=compress&cs=tinysrgb&w=600",
    "ombros": "https://images.pexels.com/photos/4162585/pexels-photo-4162585.jpeg?auto=compress&cs=tinysrgb&w=600",
    "biceps": "https://images.pexels.com/photos/5327543/pexels-photo-5327543.jpeg?auto=compress&cs=tinysrgb&w=600",
    "triceps": "https://images.pexels.com/photos/6550854/pexels-photo-6550854.jpeg?auto=compress&cs=tinysrgb&w=600",
    "abdomen": "https://images.pexels.com/photos/6456141/pexels-photo-6456141.jpeg?auto=compress&cs=tinysrgb&w=600",
    "panturrilha": "https://images.pexels.com/photos/6456307/pexels-photo-6456307.jpeg?auto=compress&cs=tinysrgb&w=600",
    "cardio": "https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg?auto=compress&cs=tinysrgb&w=600",
}

DEFAULT_IMAGE = "https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg?auto=compress&cs=tinysrgb&w=600"


def resolve_image_url(name: str, muscle_group: str) -> str:
    for pattern, url in KEYWORD_IMAGE_MAP:
        if pattern.search(name):
            return url
    return MUSCLE_GROUP_IMAGE_MAP.get(muscle_group, DEFAULT_IMAGE)


def main() -> None:
    db = SessionLocal()
    try:
        exercises = db.query(Exercise).all()
        updated = 0
        for exercise in exercises:
            resolved = resolve_image_url(exercise.name, exercise.muscle_group)
            if exercise.image_url != resolved:
                exercise.image_url = resolved
                updated += 1
        db.commit()
        print(f"Exercícios atualizados com imagem: {updated}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
