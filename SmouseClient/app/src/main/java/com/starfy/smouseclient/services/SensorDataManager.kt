package com.starfy.smouseclient.services

import android.content.Context
import android.content.Context.SENSOR_SERVICE
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import kotlinx.coroutines.channels.Channel

class SensorDataManager(context: Context) : SensorEventListener {
    private val sensorManager: SensorManager =
        context.getSystemService(SENSOR_SERVICE) as SensorManager
    private val socketManager: SocketManager = SocketManager()

    init {
        val accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION)

        socketManager.connect()

        sensorManager.registerListener(
            this,
            accelerometer,
            SensorManager.SENSOR_DELAY_FASTEST,
            SensorManager.SENSOR_STATUS_ACCURACY_HIGH
        )
    }

    val data: Channel<SensorData> = Channel(Channel.UNLIMITED)

    override fun onSensorChanged(event: SensorEvent?) {

        event?.let {
            val (xAccel, yAccel, zAccel) = it.values
            if (socketManager.isConnected()) {
                println("sending")
                socketManager.emit(xAccel, yAccel, zAccel, it.timestamp)
            }
        }
//        data.trySend(
//            SensorData(
//                xAccel =
//            )
//        )
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}

    fun cancel() {
        sensorManager.unregisterListener(this)
        socketManager.disconnect()
    }

    data class SensorData(
        val xAccel: Float, val yAccel: Float, val zAccel: Float
    )
}