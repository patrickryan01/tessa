package com.example.tessa_tablet

import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import java.util.*

class MainActivity : AppCompatActivity(), RecognitionListener, TextToSpeech.OnInitListener {
    private lateinit var voiceInput: EditText
    private lateinit var voiceOutput: TextView
    private lateinit var voiceButton: Button
    private lateinit var statusIcon: TextView
    private lateinit var statusText: TextView
    private lateinit var lightsButton: Button
    private lateinit var temperatureButton: Button
    private lateinit var musicButton: Button
    private lateinit var speechRecognizer: SpeechRecognizer
    private lateinit var textToSpeech: TextToSpeech
    private var lightsOn = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        voiceInput = findViewById(R.id.voice_input)
        voiceOutput = findViewById(R.id.voice_output)
        voiceButton = findViewById(R.id.voice_button)
        statusIcon = findViewById(R.id.status_icon)
        statusText = findViewById(R.id.status_text)
        lightsButton = findViewById(R.id.lights_button)
        temperatureButton = findViewById(R.id.temperature_button)
        musicButton = findViewById(R.id.music_button)

        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
        speechRecognizer.setRecognitionListener(this)

        textToSpeech = TextToSpeech(this, this)

        voiceButton.setOnClickListener {
            if (voiceButton.text == "Stop") {
                speechRecognizer.stopListening()
                voiceButton.text = "Speak"
            } else {
                val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
                intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak here...")
                speechRecognizer.startListening(intent)
                voiceButton.text = "Stop"
            }
        }

        lightsButton.setOnClickListener {
            if (lightsOn) {
                lightsOn = false
                statusIcon.text = "✔️"
                statusText.text = "All systems are operational."
            } else {
                lightsOn = true
                statusIcon.text = "⚠️"
                statusText.text = "Lights are on."
            }
        }

        temperatureButton.setOnClickListener {
            val temperature = promptTemperature()
            if (temperature != null) {
                statusIcon.text = "⚠️"
                statusText.text = "Temperature set to $temperature degrees."
            }
        }

        musicButton.setOnClickListener {
            statusIcon.text = "⚠️"
            statusText.text = "Playing music."
        }
    }

    override fun onReadyForSpeech(params: Bundle?) {}

    override fun onBeginningOfSpeech() {}

    override fun onRmsChanged(rmsdB: Float) {}

    override fun onBufferReceived(buffer: ByteArray?) {}

    override fun onEndOfSpeech() {}

    override fun onError(error: Int) {}

    override fun onResults(results: Bundle?) {
        val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
        if (matches != null) {
            val transcript = matches[0]
            voiceInput.setText(transcript)
            voiceOutput.append("You said: $transcript\n")
            // Add your response logic here
        }
        voiceButton.text = "Speak"
    }

    override fun onPartialResults(partialResults: Bundle?) {}

    override fun onEvent(eventType: Int, params: Bundle?) {}

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            textToSpeech.language = Locale.US
        }
    }

    private fun promptTemperature(): Int? {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Set Temperature")
        val input = EditText(this)
        input.inputType = InputType.TYPE_CLASS_NUMBER
        builder.setView(input)
        builder.setPositiveButton("OK") { _, _ ->
            val temperature = input.text.toString().toIntOrNull()
            if (temperature != null) {
                statusIcon.text = "⚠️"
                statusText.text = "Temperature set to $temperature degrees."
            }
        }
        builder.setNegativeButton("Cancel") { dialog, _ -> dialog.cancel() }
        builder.show()
        return null
    }
}