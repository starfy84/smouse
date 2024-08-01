package com.starfy.smouseclient.services


import io.socket.client.IO
import io.socket.client.Socket
import java.net.URISyntaxException

class SocketManager {
    private var socket: Socket? = null

    init {
        try {
            socket = IO.socket("http://192.168.0.59:5001")
        } catch (e: URISyntaxException) {
            e.printStackTrace()
        }
    }

    fun connect() {
        socket?.connect()
    }

    fun disconnect() {
        socket?.disconnect()
    }

    fun emit(x: Float, y: Float, z: Float, timestamp: Long) {
        socket?.emit("data", x, y, z, timestamp)
    }

    fun isConnected(): Boolean {
        return socket?.connected() ?: false
    }
}