package com.vectalai.skier

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Rect

class ScoreDisplay {
    private val textPaint = Paint().apply {
        color = Color.BLACK
        textSize = 64f
        textAlign = Paint.Align.LEFT
        isFakeBoldText = true
        setShadowLayer(2f, 2f, 2f, Color.WHITE)
    }
    
    private val bounds = Rect()
    
    fun draw(canvas: Canvas, score: Int) {
        val scoreText = "Score: $score"
        
        // Get text bounds for positioning
        textPaint.getTextBounds(scoreText, 0, scoreText.length, bounds)
        
        // Draw score in top-left corner with padding
        canvas.drawText(
            scoreText,
            20f, // X padding
            bounds.height() + 20f, // Y padding + text height
            textPaint
        )
    }
} 