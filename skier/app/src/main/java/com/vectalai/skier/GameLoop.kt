package com.vectalai.skier

class GameLoop {
    private var lastUpdateTime = System.nanoTime()
    private val targetFPS = 60
    private val targetTime = (1000000000 / targetFPS).toLong()
    private var deltaTime: Float = 0f

    fun update() {
        val currentTime = System.nanoTime()
        deltaTime = (currentTime - lastUpdateTime) / 1000000000f // Convert to seconds

        // Update game logic here

        lastUpdateTime = currentTime

        // Control frame rate
        val frameTime = System.nanoTime() - currentTime
        if (frameTime < targetTime) {
            try {
                Thread.sleep((targetTime - frameTime) / 1000000)
            } catch (e: InterruptedException) {
                e.printStackTrace()
            }
        }
    }

    fun getDeltaTime(): Float = deltaTime
} 