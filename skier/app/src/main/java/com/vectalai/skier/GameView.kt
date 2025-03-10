package com.vectalai.skier

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.view.MotionEvent
import android.view.SurfaceHolder
import android.view.SurfaceView

class GameView(context: Context) : SurfaceView(context), SurfaceHolder.Callback, Runnable {
    private var thread: Thread? = null
    private var running = false
    private val gameLoop = GameLoop()
    private lateinit var player: Player
    private val scoreDisplay = ScoreDisplay()
    
    // Touch control states
    private var leftPressed = false
    private var rightPressed = false
    
    init {
        holder.addCallback(this)
        isFocusable = true
    }

    override fun surfaceCreated(holder: SurfaceHolder) {
        player = Player(width, height)
        running = true
        thread = Thread(this)
        thread?.start()
    }

    override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {
        player = Player(width, height)
    }

    override fun surfaceDestroyed(holder: SurfaceHolder) {
        running = false
        thread?.join()
    }

    override fun run() {
        while (running) {
            gameLoop.update()
            update(gameLoop.getDeltaTime())
            draw()
            
            // Reset player if they go off screen
            if (isPlayerOffScreen()) {
                player.reset(width, height)
            }
        }
    }

    private fun update(deltaTime: Float) {
        player.update(deltaTime, leftPressed, rightPressed)
    }

    private fun draw() {
        val canvas: Canvas? = holder.lockCanvas()
        canvas?.let {
            // Clear the background
            it.drawColor(Color.WHITE)
            
            // Draw the player
            player.draw(it)
            
            // Draw the score
            scoreDisplay.draw(it, player.getScore())
            
            holder.unlockCanvasAndPost(it)
        }
    }
    
    private fun isPlayerOffScreen(): Boolean {
        return player.getX() < -50 || 
               player.getX() > width + 50 || 
               player.getY() < -50 || 
               player.getY() > height + 50
    }
    
    override fun onTouchEvent(event: MotionEvent): Boolean {
        val halfWidth = width / 2
        
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN,
            MotionEvent.ACTION_POINTER_DOWN -> {
                handleTouchDown(event, halfWidth)
            }
            MotionEvent.ACTION_UP,
            MotionEvent.ACTION_POINTER_UP -> {
                handleTouchUp(event, halfWidth)
            }
            MotionEvent.ACTION_MOVE -> {
                // Reset states
                leftPressed = false
                rightPressed = false
                // Check all active touch points
                for (i in 0 until event.pointerCount) {
                    if (event.getX(i) < halfWidth) {
                        leftPressed = true
                    } else {
                        rightPressed = true
                    }
                }
            }
        }
        return true
    }
    
    private fun handleTouchDown(event: MotionEvent, halfWidth: Int) {
        val pointerIndex = event.actionIndex
        val x = event.getX(pointerIndex)
        if (x < halfWidth) {
            leftPressed = true
        } else {
            rightPressed = true
        }
    }
    
    private fun handleTouchUp(event: MotionEvent, halfWidth: Int) {
        val pointerIndex = event.actionIndex
        val x = event.getX(pointerIndex)
        if (x < halfWidth) {
            leftPressed = false
        } else {
            rightPressed = false
        }
    }
} 