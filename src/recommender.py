from typing import List, Dict, Tuple, Optional
import csv
from dataclasses import dataclass


def _normalize_label(value: Optional[str]) -> str:
    """Normalize string labels to reduce brittle exact-match failures."""
    return str(value or "").strip().lower()


def _clamp_01(value: float) -> float:
    """Clamp numeric values to [0, 1] for stable scoring."""
    return max(0.0, min(1.0, value))

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
        """This function ranks songs for a user and returns the top k Song objects."""
        scored_songs = []
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

        for song in self.songs:
            song_dict = {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "tempo_bpm": song.tempo_bpm,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            }
            score, _ = score_song(user_prefs, song_dict)
            scored_songs.append((song, score))

        scored_songs.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """This function returns a human-readable explanation for why a song matches a user profile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }
        _, reasons = score_song(user_prefs, song_dict)
        return "; ".join(reasons) if reasons else "This song is a decent match for your preferences."

def load_songs(csv_path: str) -> List[Dict]:
    """This function loads songs from a CSV file into a list of typed dictionaries."""
    songs: List[Dict] = []
    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """This function computes a weighted relevance score and reasons for one song and one user preference profile."""
    total_score = 0.0
    reasons: List[str] = []

    user_genre = _normalize_label(user_prefs.get("genre"))
    song_genre = _normalize_label(song.get("genre"))
    user_mood = _normalize_label(user_prefs.get("mood"))
    song_mood = _normalize_label(song.get("mood"))

    if song_genre == user_genre and user_genre:
        total_score += 1.0
        reasons.append("genre match (+1.0)")

    if song_mood == user_mood and user_mood:
        total_score += 1.0
        reasons.append("mood match (+1.0)")

    song_energy = _clamp_01(float(song.get("energy", 0.0)))
    target_energy = _clamp_01(float(user_prefs.get("energy", 0.0)))
    energy_score = round(2 * _clamp_01(1 - abs(song_energy - target_energy)), 2)
    total_score += energy_score
    reasons.append(f"energy proximity (+{energy_score})")

    acousticness = _clamp_01(float(song.get("acousticness", 0.0)))
    if user_prefs.get("likes_acoustic") is True:
        acoustic_score = round(0.5 * acousticness, 2)
        total_score += acoustic_score
        reasons.append(f"high acousticness preference (+{acoustic_score})")
    elif user_prefs.get("likes_acoustic") is False:
        acoustic_score = round(0.5 * (1 - acousticness), 2)
        total_score += acoustic_score
        reasons.append(f"low acousticness preference (+{acoustic_score})")

    return total_score, reasons


def score_song_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Strategy score: prioritize genre, then mood, then numeric proximity signals."""
    total_score = 0.0
    reasons: List[str] = []

    user_genre = _normalize_label(user_prefs.get("genre"))
    song_genre = _normalize_label(song.get("genre"))
    user_mood = _normalize_label(user_prefs.get("mood"))
    song_mood = _normalize_label(song.get("mood"))

    if song_genre == user_genre and user_genre:
        total_score += 2.0
        reasons.append("genre match (+2.0)")

    if song_mood == user_mood and user_mood:
        total_score += 0.5
        reasons.append("mood match (+0.5)")

    song_energy = _clamp_01(float(song.get("energy", 0.0)))
    target_energy = _clamp_01(float(user_prefs.get("energy", 0.0)))
    energy_score = round(2 * _clamp_01(1 - abs(song_energy - target_energy)), 2)
    total_score += energy_score
    reasons.append(f"energy proximity (+{energy_score})")

    acousticness = _clamp_01(float(song.get("acousticness", 0.0)))
    if user_prefs.get("likes_acoustic") is True:
        acoustic_score = round(0.5 * acousticness, 2)
        total_score += acoustic_score
        reasons.append(f"high acousticness preference (+{acoustic_score})")
    elif user_prefs.get("likes_acoustic") is False:
        acoustic_score = round(0.5 * (1 - acousticness), 2)
        total_score += acoustic_score
        reasons.append(f"low acousticness preference (+{acoustic_score})")

    return total_score, reasons


def score_song_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """This function computes a mood-first weighted relevance score and reasons for one song and one user preference profile."""
    total_score = 0.0
    reasons: List[str] = []

    user_genre = _normalize_label(user_prefs.get("genre"))
    song_genre = _normalize_label(song.get("genre"))
    user_mood = _normalize_label(user_prefs.get("mood"))
    song_mood = _normalize_label(song.get("mood"))

    if song_mood == user_mood and user_mood:
        total_score += 2.0
        reasons.append("mood match (+2.0)")

    if song_genre == user_genre and user_genre:
        total_score += 0.5
        reasons.append("genre match (+0.5)")

    song_energy = _clamp_01(float(song.get("energy", 0.0)))
    target_energy = _clamp_01(float(user_prefs.get("energy", 0.0)))
    energy_score = round(2 * _clamp_01(1 - abs(song_energy - target_energy)), 2)
    total_score += energy_score
    reasons.append(f"energy proximity (+{energy_score})")

    acousticness = _clamp_01(float(song.get("acousticness", 0.0)))
    if user_prefs.get("likes_acoustic") is True:
        acoustic_score = round(0.5 * acousticness, 2)
        total_score += acoustic_score
        reasons.append(f"high acousticness preference (+{acoustic_score})")
    elif user_prefs.get("likes_acoustic") is False:
        acoustic_score = round(0.5 * (1 - acousticness), 2)
        total_score += acoustic_score
        reasons.append(f"low acousticness preference (+{acoustic_score})")

    return total_score, reasons


def score_song_energy_focused(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """This function computes an energy-focused weighted relevance score and reasons for one song and one user preference profile."""
    total_score = 0.0
    reasons: List[str] = []

    song_energy = _clamp_01(float(song.get("energy", 0.0)))
    target_energy = _clamp_01(float(user_prefs.get("energy", 0.0)))
    energy_score = round(2 * _clamp_01(1 - abs(song_energy - target_energy)), 2)
    total_score += energy_score
    reasons.append(f"energy proximity (+{energy_score})")

    acousticness = _clamp_01(float(song.get("acousticness", 0.0)))
    if user_prefs.get("likes_acoustic") is True:
        acoustic_score = round(0.5 * acousticness, 2)
        total_score += acoustic_score
        reasons.append(f"high acousticness preference (+{acoustic_score})")
    elif user_prefs.get("likes_acoustic") is False:
        acoustic_score = round(0.5 * (1 - acousticness), 2)
        total_score += acoustic_score
        reasons.append(f"low acousticness preference (+{acoustic_score})")

    return total_score, reasons

# Maps scoring mode names to their corresponding scoring strategy functions.
SCORING_MODES = {
    "genre-first": score_song_genre_first,
    "mood-first": score_song_mood_first,
    "energy-focused": score_song_energy_focused,
}

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """This function scores all songs, sorts them by score, and returns the top k recommendation tuples."""
    scored_songs: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored_songs.append((song, score, explanation))

    ranked = sorted(scored_songs, key=lambda item: item[1], reverse=True)
    return ranked[:k]
