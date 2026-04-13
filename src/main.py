"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, profile: dict, songs: list) -> None:
    recommendations = recommend_songs(profile, songs, k=5)
    divider = "-" * 44
    print(f"\n{'TOP RECOMMENDATIONS':^44}")
    print(f"  Profile: {label}")
    print(divider)
    for i, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f" #{i}  {song['title']:<28} Score: {score:.2f}")
        print(divider)
        for reason in reasons:
            print(f"      {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Profile A: upbeat indie listener — moderate energy, some acoustic warmth, danceable
    indie_listener = {
        "genre": "indie pop",
        "mood": "happy",
        "energy": 0.72,
        "acousticness": 0.35,
        "valence": 0.80,
        "danceability": 0.78,
    }

    # Profile B: high-intensity listener — hard rock energy, raw sound, low valence
    intense_listener = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.90,
        "acousticness": 0.08,
        "valence": 0.45,
        "danceability": 0.65,
    }

    # Profile C: study/focus listener — quiet, acoustic, calm mood, minimal danceability
    study_listener = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "acousticness": 0.82,
        "valence": 0.60,
        "danceability": 0.58,
    }

    # Profile D: extremes — all numerics maxed; acousticness contradicts high energy
    max_everything = {
        "genre": "pop",
        "mood": "intense",
        "energy": 1.0,
        "acousticness": 1.0,
        "valence": 1.0,
        "danceability": 1.0,
    }

    # Profile E: all numeric prefs at zero
    silent_listener = {
        "genre": "ambient",
        "mood": "chill",
        "energy": 0.0,
        "acousticness": 0.0,
        "valence": 0.0,
        "danceability": 0.0,
    }

    # Profile F: genre/mood contradict numeric prefs (lofi label, intense numbers)
    contradictory_listener = {
        "genre": "lofi",
        "mood": "intense",
        "energy": 0.95,
        "acousticness": 0.05,
        "valence": 0.30,
        "danceability": 0.90,
    }

    # Profile G: genre and mood that appear nowhere in the catalog
    ghost_listener = {
        "genre": "classical",
        "mood": "epic",
        "energy": 0.60,
        "acousticness": 0.50,
        "valence": 0.50,
        "danceability": 0.50,
    }

    # Profile H: all numerics at 0.5 — designed to create near-ties
    middle_ground = {
        "genre": "synthwave",
        "mood": "moody",
        "energy": 0.5,
        "acousticness": 0.5,
        "valence": 0.5,
        "danceability": 0.5,
    }

    # Profile I: only categorical prefs, no numeric fields
    minimal_listener = {
        "genre": "jazz",
        "mood": "relaxed",
    }

    profiles = [
        ("A — indie listener",       indie_listener),
        ("B — intense listener",     intense_listener),
        ("C — study listener",       study_listener),
        ("D — max everything",       max_everything),
        ("E — silent listener",      silent_listener),
        ("F — contradictory",        contradictory_listener),
        ("G — ghost genre/mood",     ghost_listener),
        ("H — middle ground / ties", middle_ground),
        ("I — minimal (no numerics)", minimal_listener),
    ]

    for label, profile in profiles:
        print_recommendations(label, profile, songs)


if __name__ == "__main__":
    main()
