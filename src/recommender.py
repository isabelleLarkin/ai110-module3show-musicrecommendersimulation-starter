import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV of songs and return each row as a dict with numeric fields converted."""
    int_fields   = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs = []
    print(f"Loading songs from {csv_path}...")

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    print(f"Loaded {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return a weighted total with per-feature reasons."""
    reasons = []
    total = 0.0

    # Categorical features — exact match rule
    genre_score = 1.0 if song["genre"] == user_prefs.get("genre") else 0.0
    genre_contrib = 0.30 * genre_score
    total += genre_contrib
    if genre_score == 1.0:
        reasons.append(f"genre match: {song['genre']} (+{genre_contrib:.2f})")
    else:
        reasons.append(f"genre mismatch: {song['genre']} vs {user_prefs.get('genre')} (+{genre_contrib:.2f})")

    mood_score = 1.0 if song["mood"] == user_prefs.get("mood") else 0.0
    mood_contrib = 0.25 * mood_score
    total += mood_contrib
    if mood_score == 1.0:
        reasons.append(f"mood match: {song['mood']} (+{mood_contrib:.2f})")
    else:
        reasons.append(f"mood mismatch: {song['mood']} vs {user_prefs.get('mood')} (+{mood_contrib:.2f})")

    # Numeric features — inverse absolute distance rule
    numeric_features = [
        ("energy",        0.18),
        ("acousticness",  0.12),
        ("valence",       0.10),
        ("danceability",  0.05),
    ]

    for feature, weight in numeric_features:
        if feature in user_prefs:
            feat_score = 1.0 - abs(user_prefs[feature] - song[feature])
            contrib = weight * feat_score
            total += contrib
            reasons.append(
                f"{feature}: {song[feature]} vs {user_prefs[feature]} pref (+{contrib:.2f})"
            )

    return round(total, 4), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song in the catalog and return the top k results sorted by score descending."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return [
        (song, score, reasons)
        for song, score, reasons in ranked[:k]
    ]
