# Skier Game

A simple Android skiing game built with Kotlin.

## Project Structure

```
skier/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/vectalai/skier/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── GameView.kt
│   │   │   │   └── GameLoop.kt
│   │   │   ├── res/
│   │   │   │   └── values/
│   │   │   └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
└── settings.gradle
```

## Setup

1. Open the project in Android Studio
2. Sync project with Gradle files
3. Run the app on an emulator or physical device

## Development

The game uses a standard game loop pattern with:
- `GameView`: Handles rendering and surface management
- `GameLoop`: Manages game timing and updates
- `MainActivity`: Entry point for the application

## Requirements

- Android Studio Arctic Fox or newer
- Android SDK 24 or higher
- Kotlin 1.9.22 or higher 