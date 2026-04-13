# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**ScoreMatch 1.0**

---

## 2. Intended Use  

ScoreMatch 1.0 suggests up to five songs from a small catalog based on a user's stated genre preference, mood, and four numeric taste dimensions. It is designed for classroom exploration of how rule-based recommender systems work — not for deployment with real users. The system assumes a single, stable taste profile per run and makes no attempt to learn from listening history or adapt over time.

---

## 3. How the Model Works  

Each song in the catalog is described by six attributes: its genre (such as "lofi" or "rock"), its mood (such as "chill" or "intense"), and four numbers between 0 and 1 measuring energy, acousticness, valence, and danceability. A user profile stores one preferred value for each of those same six attributes.

To compare a song to a user, the system checks whether the genre and mood match exactly — a match gives full credit, a mismatch gives none. For the four numeric attributes it measures how close the song's value is to the user's preference: a perfect match scores the maximum, and the score decreases the further apart the two values are.

Those six individual scores are then combined into one final number using fixed weights. Genre counts for 30% of the total and mood for 25%, so together the two label-based checks determine more than half the final score. Energy contributes 18%, acousticness 12%, valence 10%, and danceability 5%. Every song in the catalog gets scored this way, the list is sorted from highest to lowest, and the top five are returned along with a breakdown showing how each feature contributed.

---

## 4. Data  

The catalog contains 18 songs stored in `data/songs.csv`. Genres represented include pop, rock, lofi, ambient, jazz, synthwave, indie pop, metal, edm, r&b, reggae, and folk. Moods include happy, chill, intense, focused, relaxed, moody, romantic, uplifting, dark, euphoric, and melancholic. Most genres appear only once or twice, which means a user whose preferred genre isn't well-represented will never receive a strong genre-match recommendation. The dataset was not modified from the starter version. Notably absent are classical, country, hip-hop, and most non-Western music traditions, and the numeric values reflect Western popular music production conventions.

---

## 5. Strengths  

The system works best when the user's genre and mood align closely with songs already in the catalog. The study listener (lofi / chill) and intense listener (rock / intense) profiles both returned a clear #1 result scoring above 0.97, with an obvious drop-off to the #2 result — which is the behavior you'd want from a confident recommendation. The scoring is also fully transparent: every feature contribution is printed alongside the result, so it's easy to understand exactly why a song ranked where it did. That explainability is a genuine advantage over black-box approaches.

---

## 6. Limitations and Bias  

The catalog is too small to serve most profiles well. Any genre or mood that appears in fewer than two songs will produce at most one strong match, forcing the remaining four recommendations to be genre and mood mismatches regardless of how good the numeric fit is.

The high weight on genre and mood (55% combined) creates a systematic disadvantage for cross-genre listeners. A user who loves high-energy acoustic folk, for example, will consistently see folk songs ranked above stylistically closer songs from other genres. This same dynamic plays out in production systems whenever category labels are over-weighted relative to acoustic or behavioral similarity.

The profile model assumes a single fixed preference vector, which doesn't capture the reality that most people want different things in different contexts. A user who listens to ambient music while studying and metal while working out cannot be represented by one profile, and any single-profile run will produce mediocre results for at least one of those contexts. There is also no mechanism for representing intensity of preference — liking a genre a little versus a lot produces the same score.

---

## 7. Evaluation  

Nine user profiles were tested: three baseline profiles (indie listener, intense listener, study listener) and six adversarial cases designed to expose edge behavior. For the baseline profiles, the expected top result appeared at #1 in all three cases with scores above 0.95. The adversarial tests confirmed several specific behaviors: the ghost profile (a genre and mood absent from the catalog) still returned five results with no errors, with rankings driven entirely by numeric proximity and a maximum possible score of 0.45. The contradictory profile (lofi genre paired with high-energy numeric preferences) always surfaced lofi songs at the top, confirming that categorical weights override numeric signals. The minimal profile (no numeric fields) completed without a `KeyError`, confirming the guard in the scoring function works. The all-zeros and all-ones profiles both produced valid output without negative scores.

---

## 8. Future Work  

The most impactful improvement would be expanding the catalog — 18 songs is too few for the ranking to be meaningful for most profiles. Beyond size, adding tempo range as a preference (rather than treating tempo as an ignored field) would give the system a more complete picture of energy feel. Softening the genre and mood matching from a binary exact-match to a similarity-based score (for example, treating "lofi" and "ambient" as closer than "lofi" and "metal") would reduce the cliff between a genre match and a mismatch. Introducing a diversity penalty to prevent the top five from clustering around one genre would also make recommendations more useful in practice. Longer term, replacing the static profile with one that updates based on which recommendations the user accepts would move the system from rule-based toward adaptive.

---

## 9. Personal Reflection  

The most surprising thing was how much the fixed weights determine the output before any numeric comparison even happens. Writing the weights down as explicit numbers made it obvious that this is a design choice with real consequences — changing genre from 0.30 to 0.15 would produce meaningfully different recommendations for cross-genre listeners. Real music apps make the same kind of choice, but the weights are learned from data and never shown to users, which makes them much harder to question or audit. Building a toy version where every decision is visible made it clearer why transparency in AI systems matters: you can't push back on a bias you can't see.
