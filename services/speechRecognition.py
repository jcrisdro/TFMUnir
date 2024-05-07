import speech_recognition as sr
import spacy
import es_core_news_sm
import moviepy.editor as editor
import cv2 
from unidecode import unidecode

class SpeechRecognition:
    
    #CONSTANTES
    END = "ADIOS"

    def __init__(self) -> None:
        print("Initializing audio recognizer...")
        # Initializing variables
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.nlp = es_core_news_sm.load()


    def listen(self):
        print("Checking audio permissions...\n")
   
        looping = True
        while(looping):

            try:
                with self.mic as source:
                    # Adjust micro to ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)

                    print("Habla ahora")

                    # Listen
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    print("Fin del audio. Transcribiendo...")

                # Convert audio to text with google
                text = self.ecognizer.recognize_google(audio, language="ES")

                # Convert text into Doc of tokens
                sentence = self.nlp(text)
                print(sentence)

                # If end of conversation -> Stop
                if unidecode(sentence.text.upper()) == self.END:
                    looping = False
                    print("Finalizando programa...")
                
            # Exceptions control
            except sr.RequestError as e:
                print(f"Error en el request {e}")

            except sr.UnknownValueError as e:
                print(f"No se escuchó nada {e}")

            except sr.WaitTimeoutError as e:
                print(f"Tiempo de espera excedido {e}")


        def videos():
            # Loading videos
            clip1 = editor.VideoFileClip("/Users/Vicll/OneDrive - UNIR/MASTER/SEMESTRE_2/TFM/SCRIPTS/videos/prueba1.gif")
            clip2 = editor.VideoFileClip("/Users/Vicll/OneDrive - UNIR/MASTER/SEMESTRE_2/TFM/SCRIPTS/videos/prueba2.gif")
            
            # Concatenating both the clips
            final = editor.concatenate_videoclips([clip1, clip2])
            
            # Prepare window
            final.ipython_display(width = 480)

            # Write video
            final_url = "/Users/Vicll/OneDrive - UNIR/MASTER/SEMESTRE_2/TFM/SCRIPTS/videos/merged.webm"
            final.write_videofile(final_url)

            # Showing final clip
            showVideo(final_url)


        def showVideo(url):
            cap = cv2.VideoCapture(url) 

            while(cap.isOpened()):
                success, frame = cap.read()
                if success:
                    cv2.imshow('Video Player', frame)
                    quitButton = cv2.waitKey(25) & 0xFF == ord('q')
                    closeButton = cv2.getWindowProperty('Video Player', cv2.WND_PROP_VISIBLE) < 1

                    if quitButton or closeButton: 
                        break
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()

