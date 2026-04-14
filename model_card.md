# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeMatch Lite 1.0

---

## 2. Intended Use  

This recommender suggests the top 5 songs from a small class dataset.
It uses one user profile with genre, mood, energy, and acoustic preference.
It assumes the user has one main taste at a time.
This project is for classroom exploration, not real production use.

---

## 3. How the Model Works  

Each song is compared to the user profile.
The model gives points for genre match, mood match, energy closeness, and acoustic fit.
Energy now has the biggest weight, so energy can strongly change the ranking.
Genre still matters, but less than before.
The model sorts songs by total score and returns the top songs.

---

## 4. Data  

The catalog has 18 songs.
It includes genres like pop, lofi, rock, ambient, jazz, metal, and others.
It includes moods like happy, chill, intense, relaxed, romantic, and more.
I did not add or remove songs.
The data is small, so many styles are missing or underrepresented.

---

## 5. Strengths  

The system works well when the user profile matches common patterns in the dataset.
It gives understandable reasons for each recommendation.
High-Energy Pop and Chill Lofi produced results that mostly matched expectations.
Changing profile settings clearly changes the top results.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

The dataset is imbalanced, so some users get better matches than others.
For example, lofi appears 3 times, but many genres appear only once.
If a user picks a missing genre like k-pop, genre match is impossible.
Then the model falls back to energy and mood, which can feel inaccurate.
The model can also over-focus on energy because energy has the strongest weight.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested three profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock.
I compared the top 5 songs for each profile.
I checked whether the results changed in ways that made sense.
I also ran a logic experiment by increasing energy weight and reducing genre weight.
A surprise was that Gym Hero still ranked high for different profiles because energy strongly affects score.

---

## 8. Future Work  

I would add more songs so each genre and mood has better coverage.
I would add partial matches for similar genres and related moods.
I would add diversity rules so the top 5 are less repetitive.
I would support multi-style users instead of one fixed profile.
I would improve explanations so users can see trade-offs more clearly.

---

## 9. Personal Reflection  

My biggest learning moment was seeing how one weight change shifted many results.
When I doubled energy and reduced genre weight, the ranking changed fast, and songs like Gym Hero showed up for very different users.
AI tools helped me move faster by suggesting tests, edge cases, and cleaner wording, but I still had to double-check outputs against the CSV and real score math.
I learned that even a simple point system can feel personal because it reacts to user inputs and explains why songs were chosen.
If I extend this project, I want to add more songs, partial genre/mood matching, and a diversity rule so the top 5 recommendations are less repetitive.
