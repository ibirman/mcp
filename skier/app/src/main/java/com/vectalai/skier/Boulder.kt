package com.vectalai.skier

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import kotlin.random.Random

class Boulder(private val x: Float, private val y: Float) {
    companion object {
        const val SIZE = 30f
        private val paint = Paint().apply {
            color = Color.DKGRAY
            style = Paint.Style.FILL
        }
        
        fun generateRandom(screenWidth: Int, screenHeight: Int, player: Player): Boulder {
            // Generate position below the player
            val x = Random.nextFloat() * (screenWidth - SIZE * 2) + SIZE
            val y = player.getY() + Random.nextFloat() * (screenHeight / 2) + screenHeight / 4
            return Boulder(x, y)
        }
    }
    
    private val collisionRadius = SIZE / 2
    
    fun draw(canvas: Canvas) {
        canvas.drawCircle(x, y, SIZE, paint)
    }
    
    fun checkCollision(playerX: Float, playerY: Float, playerSize: Float): Boolean {
        val distance = kotlin.math.sqrt(
            (x - playerX) * (x - playerX) + 
            (y - playerY) * (y - playerY)
        )
        return distance < (collisionRadius + playerSize / 2)
    }
    
    fun isOffScreen(screenHeight: Int): Boolean {
        return y < -SIZE
    }
    
    fun getX() = x
    fun getY() = y
} 