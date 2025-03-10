package com.vectalai.skier

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import kotlin.math.cos
import kotlin.math.sin

class Player(screenWidth: Int, screenHeight: Int) {
    private var x: Float = screenWidth / 2f
    private var y: Float = screenHeight / 3f
    private var angle: Float = 0f // 0 degrees is straight down
    private var speed: Float = 5f
    private val paint = Paint().apply {
        color = Color.BLUE
        style = Paint.Style.FILL
    }
    
    // Size of the skier triangle
    private val size = 40f
    
    // Score tracking
    private var distanceTraveled: Float = 0f
    private var score: Int = 0
    private var collisionPenalty: Int = 0
    private var isInvulnerable = false
    private var invulnerabilityTimer = 0f
    private val invulnerabilityDuration = 1.5f // seconds
    
    fun update(deltaTime: Float, leftPressed: Boolean, rightPressed: Boolean) {
        // Update invulnerability
        if (isInvulnerable) {
            invulnerabilityTimer += deltaTime
            if (invulnerabilityTimer >= invulnerabilityDuration) {
                isInvulnerable = false
                invulnerabilityTimer = 0f
            }
        }
        
        // Update angle based on input
        when {
            leftPressed && !rightPressed -> angle -= 2f
            rightPressed && !leftPressed -> angle += 2f
        }
        
        // Clamp angle to prevent going uphill (-60 to 60 degrees)
        angle = angle.coerceIn(-60f, 60f)
        
        // Move player based on angle and speed
        val angleRadians = Math.toRadians(angle.toDouble()).toFloat()
        val dx = sin(angleRadians) * speed
        val dy = cos(angleRadians) * speed
        
        x += dx
        y += dy
        
        // Update distance traveled and score
        val distanceThisFrame = kotlin.math.sqrt((dx * dx + dy * dy).toDouble()).toFloat()
        distanceTraveled += distanceThisFrame
        score = (distanceTraveled / 10).toInt() - collisionPenalty
    }
    
    fun draw(canvas: Canvas) {
        canvas.save()
        
        // Translate to player position and rotate
        canvas.translate(x, y)
        canvas.rotate(angle)
        
        // Draw skier as a triangle
        val path = Path()
        path.moveTo(0f, -size)    // Top
        path.lineTo(-size/2, size) // Bottom left
        path.lineTo(size/2, size)  // Bottom right
        path.close()
        
        // Flash the player when invulnerable
        if (isInvulnerable && (invulnerabilityTimer * 1000).toInt() % 200 < 100) {
            paint.alpha = 128
        } else {
            paint.alpha = 255
        }
        
        canvas.drawPath(path, paint)
        
        canvas.restore()
    }
    
    fun handleCollision() {
        if (!isInvulnerable) {
            collisionPenalty += 50 // Lose 50 points per collision
            isInvulnerable = true
            invulnerabilityTimer = 0f
        }
    }
    
    fun reset(screenWidth: Int, screenHeight: Int) {
        x = screenWidth / 2f
        y = screenHeight / 3f
        angle = 0f
        distanceTraveled = 0f
        score = 0
        collisionPenalty = 0
        isInvulnerable = false
        invulnerabilityTimer = 0f
    }
    
    fun getScore(): Int = score
    fun getSize(): Float = size
    fun getX(): Float = x
    fun getY(): Float = y
    fun isInvulnerable(): Boolean = isInvulnerable
} 