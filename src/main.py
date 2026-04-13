"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Taste profile: upbeat, moderately energetic listener who enjoys
    # danceable tracks with some acoustic warmth. Not too intense, not too chill.
    user_prefs = {
        "genre": "indie pop",
        "mood": "happy",
        "energy": 0.72,        # prefers moderate-high energy, not extreme
        "acousticness": 0.35,  # some warmth, but not fully unplugged
        "valence": 0.80,       # strongly prefers positive, feel-good tracks
        "danceability": 0.78,  # likes music with rhythmic drive
    }
    

    recommendations = recommend_songs(user_prefs, songs, k=5)

    divider = "-" * 44
    print(f"\n{'TOP RECOMMENDATIONS':^44}")
    print(divider)

    for i, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f" #{i}  {song['title']:<28} Score: {score:.2f}")
        print(divider)
        for reason in reasons:
            print(f"      {reason}")
        print()


if __name__ == "__main__":
    main()
