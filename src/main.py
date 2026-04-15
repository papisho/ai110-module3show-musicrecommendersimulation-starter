"""Test runner to compare all scoring modes with the same user profile."""

from typing import Callable, Dict, List, Tuple
import textwrap

from recommender import (
    load_songs,
    score_song_energy_focused,
    score_song_genre_first,
    score_song_mood_first,
)


def _top_k_for_mode(
    songs: List[Dict],
    user_prefs: Dict,
    scorer: Callable[[Dict, Dict], Tuple[float, List[str]]],
    k: int = 3,
) -> List[Tuple[Dict, float, List[str]]]:
    scored: List[Tuple[Dict, float, List[str]]] = []
    for song in songs:
        score, reasons = scorer(user_prefs, song)
        scored.append((song, score, reasons))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]


def _wrap_cell(value: str, width: int) -> List[str]:
    wrapped = textwrap.wrap(str(value), width=width) if value else [""]
    return wrapped or [""]


def _print_table(rows: List[Tuple[str, str, str, str, List[str]]]) -> None:
    widths = {
        "title": 22,
        "artist": 18,
        "genre": 10,
        "score": 8,
        "reasons": 54,
    }

    headers = ["Title", "Artist", "Genre", "Score", "Reasons"]
    line = (
        f"| {headers[0]:<{widths['title']}} "
        f"| {headers[1]:<{widths['artist']}} "
        f"| {headers[2]:<{widths['genre']}} "
        f"| {headers[3]:<{widths['score']}} "
        f"| {headers[4]:<{widths['reasons']}} |"
    )
    separator = (
        f"|-{'-' * widths['title']}-"
        f"|-{'-' * widths['artist']}-"
        f"|-{'-' * widths['genre']}-"
        f"|-{'-' * widths['score']}-"
        f"|-{'-' * widths['reasons']}-|"
    )

    print(line)
    print(separator)

    for title, artist, genre, score, reasons in rows:
        title_lines = _wrap_cell(title, widths["title"])
        artist_lines = _wrap_cell(artist, widths["artist"])
        genre_lines = _wrap_cell(genre, widths["genre"])
        score_lines = _wrap_cell(score, widths["score"])
        reason_lines: List[str] = []
        for reason in reasons:
            wrapped_reason = textwrap.wrap(reason, width=widths["reasons"] - 2) or [""]
            for index, part in enumerate(wrapped_reason):
                prefix = "• " if index == 0 else "  "
                reason_lines.append(f"{prefix}{part}")
        if not reason_lines:
            reason_lines = [""]

        row_height = max(
            len(title_lines),
            len(artist_lines),
            len(genre_lines),
            len(score_lines),
            len(reason_lines),
        )

        for i in range(row_height):
            print(
                f"| {title_lines[i] if i < len(title_lines) else '':<{widths['title']}} "
                f"| {artist_lines[i] if i < len(artist_lines) else '':<{widths['artist']}} "
                f"| {genre_lines[i] if i < len(genre_lines) else '':<{widths['genre']}} "
                f"| {score_lines[i] if i < len(score_lines) else '':<{widths['score']}} "
                f"| {reason_lines[i] if i < len(reason_lines) else '':<{widths['reasons']}} |"
            )

        print(separator)


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    mode_scorers = [
        ("genre-first", score_song_genre_first),
        ("mood-first", score_song_mood_first),
        ("energy-focused", score_song_energy_focused),
    ]

    print("\nProfile for mode comparison:")
    print(user_prefs)

    for mode_name, scorer in mode_scorers:
        print(f"\n=== Mode: {mode_name} ===")
        top_results = _top_k_for_mode(songs, user_prefs, scorer, k=3)

        table_rows = [
            (
                song["title"],
                song["artist"],
                song["genre"],
                f"{score:.2f}",
                reasons,
            )
            for song, score, reasons in top_results
        ]
        _print_table(table_rows)


if __name__ == "__main__":
    main()
