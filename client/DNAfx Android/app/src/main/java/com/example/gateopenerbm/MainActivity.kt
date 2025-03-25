package com.example.gateopenerbm

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.ButtonDefaults
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import kotlinx.coroutines.*
import java.io.PrintWriter
import java.net.Socket
import java.util.UUID
import androidx.lifecycle.lifecycleScope

class MainActivity : ComponentActivity() {
    private val defaultServerIP = "192.168.43.22"
    private val serverPort = 12345
    private val sharedPrefs: SharedPreferences by lazy {
        getSharedPreferences("GateOpenerPrefs", Context.MODE_PRIVATE)
    }
    // Socket persistente
    @Volatile private var socket: Socket? = null
    // Job per gestire le connessioni
    private var connectionJob: Job? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val initialIP = loadServerIP() // Carica l'IP salvato
        val initialButtons = loadButtons() // Carica i pulsanti salvati

        // Non esegue una connessione automatica qui!

        setContent {
            MainContent(
                serverIP = initialIP,
                onConnect = { newIP ->
                    saveServerIP(newIP)
                    // Cancella eventuali tentativi di connessione in corso
                    connectionJob?.cancel()
                    connectionJob = lifecycleScope.launch(Dispatchers.IO) {
                        socket = connectToServerSuspend(newIP)
                    }
                },
                onCommandSend = { command -> sendMessage(command) },
                initialButtons = initialButtons,
                onButtonsUpdate = { updatedButtons -> saveButtons(updatedButtons) }
            )
        }
    }

    // Funzione sospesa per stabilire la connessione
    private suspend fun connectToServerSuspend(ip: String): Socket? = withContext(Dispatchers.IO) {
        try {
            socket?.close()
        } catch (e: Exception) {
            e.printStackTrace()
        }
        try {
            val newSocket = Socket(ip, serverPort)
            runOnUiThread {
                Toast.makeText(this@MainActivity, "Connected to $ip", Toast.LENGTH_SHORT).show()
            }
            newSocket
        } catch (e: Exception) {
            e.printStackTrace()
            runOnUiThread {
                Toast.makeText(this@MainActivity, "Failed to connect to $ip", Toast.LENGTH_SHORT).show()
            }
            null
        }
    }

    // Invia il comando usando la connessione persistente, riconnettendo se necessario
    private fun sendMessage(command: String) {
        lifecycleScope.launch(Dispatchers.IO) {
            try {
                if (socket == null || socket!!.isClosed) {
                    // Se non sei connesso, non inviare nulla
                    runOnUiThread {
                        Toast.makeText(this@MainActivity, "Non connesso", Toast.LENGTH_SHORT).show()
                    }
                    return@launch
                }
                socket?.let { sock ->
                    val writer = PrintWriter(sock.getOutputStream(), true)
                    writer.println(command)
                }
            } catch (e: Exception) {
                e.printStackTrace()
                runOnUiThread {
                    Toast.makeText(this@MainActivity, "Failed to send: $command", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    private fun saveServerIP(ip: String) {
        sharedPrefs.edit().putString("serverIP", ip).apply()
    }

    private fun loadServerIP(): String {
        return sharedPrefs.getString("serverIP", defaultServerIP) ?: defaultServerIP
    }

    private fun saveButtons(buttons: List<ButtonData>) {
        val gson = Gson()
        val json = gson.toJson(buttons)
        sharedPrefs.edit().putString("buttons", json).apply()
    }

    private fun loadButtons(): List<ButtonData> {
        val gson = Gson()
        val json = sharedPrefs.getString("buttons", null)
        if (json != null) {
            val type = object : TypeToken<List<ButtonData>>() {}.type
            return gson.fromJson(json, type)
        }
        return emptyList()
    }
}

data class ButtonData(val id: String, val text: String, val position: Offset)

@Composable
fun MainContent(
    serverIP: String,
    onConnect: (String) -> Unit,
    onCommandSend: (String) -> Unit,
    initialButtons: List<ButtonData>,
    onButtonsUpdate: (List<ButtonData>) -> Unit
) {
    var buttons by remember { mutableStateOf(initialButtons) }
    var currentServerIP by remember { mutableStateOf(serverIP) }

    LaunchedEffect(buttons) {
        onButtonsUpdate(buttons)
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            // Titolo
            Box(
                modifier = Modifier
                    .padding(bottom = 16.dp)
                    .shadow(4.dp, shape = RoundedCornerShape(8.dp))
                    .border(width = 2.dp, color = Color.Black, shape = RoundedCornerShape(8.dp))
                    .padding(8.dp)
            ) {
                Text(
                    text = "DNAfx Android",
                    fontSize = 24.sp
                )
            }
            // Campo IP e pulsante di connessione
            IPTextBox(
                serverIP = currentServerIP,
                onIPChange = { newIP -> currentServerIP = newIP },
                onConnectClick = { onConnect(currentServerIP) }
            )
            Spacer(modifier = Modifier.height(24.dp))
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
            ) {
                buttons.forEach { buttonData ->
                    MovableEditableButton(
                        text = buttonData.text,
                        position = buttonData.position,
                        onDrag = { newOffset ->
                            buttons = buttons.map {
                                if (it.id == buttonData.id) it.copy(position = newOffset) else it
                            }
                        },
                        onNameChange = { newName ->
                            buttons = buttons.map {
                                if (it.id == buttonData.id) it.copy(text = newName) else it
                            }
                        },
                        onDelete = {
                            buttons = buttons.filter { it.id != buttonData.id }
                        },
                        onClick = { onCommandSend(buttonData.text) }
                    )
                }
            }
        }

        Column(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Button(
                onClick = {
                    buttons = buttons + ButtonData(UUID.randomUUID().toString(), "New Effect", Offset(100f, 100f))
                },
                modifier = Modifier.padding(8.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color.Black)
            ) {
                Text("+", color = Color.White)
            }
            Row(
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Button(
                    onClick = { onCommandSend("-") },
                    modifier = Modifier.padding(8.dp)
                ) {
                    Text("<-- Prev")
                }
                Button(
                    onClick = { onCommandSend("") },
                    modifier = Modifier.padding(8.dp)
                ) {
                    Text("Next -->")
                }
            }
        }
    }
}

@Composable
fun IPTextBox(
    serverIP: String,
    onIPChange: (String) -> Unit,
    onConnectClick: () -> Unit
) {
    var ipInput by remember { mutableStateOf(serverIP) }

    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(text = "Server IP:", fontSize = 16.sp)
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Box(
                modifier = Modifier
                    .weight(1f)
                    .background(Color.LightGray)
                    .padding(8.dp)
            ) {
                BasicTextField(
                    value = ipInput,
                    onValueChange = { newValue ->
                        ipInput = newValue
                        onIPChange(newValue)
                    },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    textStyle = TextStyle(fontSize = 16.sp, color = Color.Black)
                )
            }
            Button(onClick = onConnectClick) {
                Text("Connect")
            }
        }
    }
}

@Composable
fun MovableEditableButton(
    text: String,
    position: Offset,
    onDrag: (Offset) -> Unit,
    onNameChange: (String) -> Unit,
    onDelete: () -> Unit,
    onClick: () -> Unit
) {
    var dragOffset by remember { mutableStateOf(position) }
    var buttonName by remember { mutableStateOf(text) }

    Box(
        modifier = Modifier
            .offset { IntOffset(dragOffset.x.toInt(), dragOffset.y.toInt()) }
            .pointerInput(Unit) {
                detectDragGestures { change, dragAmount ->
                    change.consume()
                    dragOffset += Offset(dragAmount.x, dragAmount.y)
                    onDrag(dragOffset)
                }
            }
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                BasicTextField(
                    value = buttonName,
                    onValueChange = { newName ->
                        buttonName = newName
                        onNameChange(newName)
                    },
                    singleLine = true,
                    textStyle = TextStyle(fontSize = 16.sp, color = Color.Black),
                    modifier = Modifier
                        .background(Color.LightGray)
                        .padding(4.dp)
                )
                Text(
                    text = "x",
                    color = Color.Red,
                    fontSize = 16.sp,
                    modifier = Modifier
                        .padding(start = 8.dp)
                        .clickable { onDelete() }
                )
            }
            Button(onClick = onClick) {
                Text("Send")
            }
        }
    }
}
