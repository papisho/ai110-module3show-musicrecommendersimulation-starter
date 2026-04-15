from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    score_song_energy_focused,
    score_song_genre_first,
    score_song_mood_first,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_mode_scoring_shifts_preference_between_genre_and_mood_matches():
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }
    genre_match_song = {
        "title": "Genre Match",
        "genre": "pop",
        "mood": "calm",
        "energy": 0.8,
        "acousticness": 0.2,
    }
    mood_match_song = {
        "title": "Mood Match",
        "genre": "rock",
        "mood": "happy",
        "energy": 0.8,
        "acousticness": 0.2,
    }

    genre_first_genre_song_score, _ = score_song_genre_first(user_prefs, genre_match_song)
    genre_first_mood_song_score, _ = score_song_genre_first(user_prefs, mood_match_song)
    assert genre_first_genre_song_score > genre_first_mood_song_score

    mood_first_genre_song_score, _ = score_song_mood_first(user_prefs, genre_match_song)
    mood_first_mood_song_score, _ = score_song_mood_first(user_prefs, mood_match_song)
    assert mood_first_mood_song_score > mood_first_genre_song_score


def test_mode_explanations_reflect_strategy_logic_only():
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }
    song = {
        "title": "Mode Test Song",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "acousticness": 0.2,
    }

    _, genre_first_reasons = score_song_genre_first(user_prefs, song)
    assert "genre match (+2.0)" in genre_first_reasons
    assert "mood match (+0.5)" in genre_first_reasons

    _, mood_first_reasons = score_song_mood_first(user_prefs, song)
    assert "mood match (+2.0)" in mood_first_reasons
    assert "genre match (+0.5)" in mood_first_reasons

    _, energy_focused_reasons = score_song_energy_focused(user_prefs, song)
    assert any("energy proximity" in reason for reason in energy_focused_reasons)
    assert any("acousticness preference" in reason for reason in energy_focused_reasons)
    assert not any("genre match" in reason for reason in energy_focused_reasons)
    assert not any("mood match" in reason for reason in energy_focused_reasons)
