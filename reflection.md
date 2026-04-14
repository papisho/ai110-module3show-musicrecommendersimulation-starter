# Reflection Comparisons

## Profiles tested

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock

## Pairwise output comparisons

### High-Energy Pop vs Chill Lofi

High-Energy Pop surfaces fast, punchy songs like Sunrise City and Gym Hero, while Chill Lofi shifts toward Library Rain, Focus Flow, and Midnight Coding. This makes sense because the Chill Lofi profile asks for lower energy and acoustic-friendly songs, so the system rewards softer tracks with higher acousticness.

### High-Energy Pop vs Deep Intense Rock

Both profiles still pull in energetic songs, so there is overlap in tracks like Gym Hero and Storm Runner. The difference is that Deep Intense Rock pushes intense/rock-adjacent songs higher, while High-Energy Pop keeps happy pop songs near the top. This makes sense because both users want high energy, but they differ on mood and genre.

### Chill Lofi vs Deep Intense Rock

These two profiles produce the biggest split: Chill Lofi recommends calm study-like songs, while Deep Intense Rock recommends loud, aggressive tracks. This is expected because the target energy values are far apart and the acoustic preference moves in opposite directions.

## Plain-language takeaway

If someone asks for Happy Pop, Gym Hero can still appear because it has extremely high energy and low acousticness, which score strongly in the current formula. In simple terms, the model sometimes hears "high energy" louder than it hears "exact genre."
