from google.cloud import speech
from pydub import AudioSegment
import io

def transcribe_mp3(mp3_file: str) -> None:
    """Transcrit un fichier MP3 en texte à l'aide de Google Cloud Speech-to-Text, en envoyant les données en morceaux."""

    # Convertir le MP3 en WAV
    audio = AudioSegment.from_mp3(mp3_file)
    wav_file = "temp_audio.wav"
    audio.export(wav_file, format="wav")

    # Lire le fichier WAV converti
    with open(wav_file, "rb") as audio_file:
        content = audio_file.read()

    # Diviser l'audio en morceaux (par exemple, 1 Mo par morceau)
    chunk_size = 1048576  # 1 Mo
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

    # Créer un client Speech-to-Text
    client = speech.SpeechClient()

    # Définir la configuration de reconnaissance
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Format WAV
        sample_rate_hertz=16000,  # Fréquence d'échantillonnage
        language_code="en-US",    # Langue
    )

    streaming_config = speech.StreamingRecognitionConfig(config=config)

    # Envoyer les morceaux d'audio en streaming
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in chunks)

    # Commencer la reconnaissance
    responses = client.streaming_recognize(
        config=streaming_config,
        requests=requests,
    )

    # Traiter les réponses
    for response in responses:
        for result in response.results:
            print(f"Finalisé: {result.is_final}")
            print(f"Stabilité: {result.stability}")
            alternatives = result.alternatives
            for alternative in alternatives:
                print(f"Confiance: {alternative.confidence}")
                print(f"Transcription: {alternative.transcript}")

# Appel de la fonction avec le chemin du fichier MP3
transcribe_mp3("Noa miskine.mp3")
