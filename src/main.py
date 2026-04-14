"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Example user profiles
    user_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "calm",
            "energy": 0.3,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.85,
            "likes_acoustic": False,
        },
    }

    selected_profile = "High-Energy Pop"
    user_prefs = user_profiles[selected_profile]

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nProfile: {selected_profile}")

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - {song['artist']}")
        print(f"Score: {score:.2f}")
        reasons = explanation.split(", ") if explanation else ["No explanation available"]
        for reason in reasons:
            print(f"  - {reason}")
        print("---")
        print()


if __name__ == "__main__":
    main()
