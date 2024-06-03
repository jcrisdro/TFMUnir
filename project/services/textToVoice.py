from gtts import gTTS
import IPython
import soundfile as sf
import io
import google.auth as auth
from google.cloud import aiplatform
from google.cloud import texttospeech
from playsound import playsound

class Speaker:

    PROJECT_ID = "airy-cogency-419614"
    LOCATION = "us-central1"
    json_path = "./credentials/application_default_credentials.json"
    ruta_output = "./output/"

    def __init__(self, language="es-ES") -> None:
        self.loginGoogle()
        self.language = language

    '''
    def generateWithGTTS(self, text):
        tts = gTTS(text=text,lang='es')
        tts.save('saludos.mp3')
        data, rate = sf.read('saludos.mp3')
        IPython.display.Audio(data=data, rate=rate)
    '''


    def generateWithGoogle(self, text):
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.language, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        # The response's audio_content is binary.
        ruta_archivo = self.ruta_output + "output.mp3"
        print("Writing audio file in ")
        with open(ruta_archivo, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')

        playsound(ruta_archivo)


    # Importante!! Hacer login antes de generar voz
    def loginGoogle(self):
        #Sign in Google
        auth.load_credentials_from_file(self.json_path)
        aiplatform.init(project=self.PROJECT_ID, location=self.LOCATION)
        print("Loged succesfully in Google")
        