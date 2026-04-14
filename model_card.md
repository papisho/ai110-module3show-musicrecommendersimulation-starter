# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

One weakness from my experiments is catalog-driven filter bubble behavior. The dataset is imbalanced (for example, lofi is 3 of 18 songs while most genres appear only once), so users in common genres get more chances for high-ranked matches. Users with a missing favorite genre get no genre points at all and are pushed toward whichever songs happen to share energy or mood, which can feel off-target. This effect was clear in a cold-start test with favorite genre set to k-pop, where the top results were pop, indie pop, synthwave, and rock tracks because energy and mood dominated when genre match was unavailable.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested the recommender with three profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock, and compared the top 5 results for each profile. I looked for whether songs changed in ways a listener would expect when I changed genre, mood, energy, and acoustic preference. One surprise was that Gym Hero kept showing up even when genre did not match, because its very high energy score can outweigh missing genre points after the weight experiment. I also ran a logic experiment where I doubled energy weight and halved genre weight, and the ranking became more sensitive to energy than to genre labels. This helped confirm that the model is responsive, but it can over-prioritize “how energetic” a song is over “what type of song” a user asked for.

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
