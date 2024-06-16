import sounddevice as sd
import speech_recognition as sr

from scipy.io.wavfile import write

from project.services.explode import ExplodeService
from project.services.hamodel import HAModelService
from constants import IO_AUDIO, ROOT_PROJECT, HA_MODEL


class InputService:

    def __init__(self) -> None:
        # print("InputService started")
        self.explode = ExplodeService()
        self.hamodel = HAModelService(type_model=HA_MODEL['type'], corpus=HA_MODEL['corpus'], 
                                      transformer=HA_MODEL['transformer'], distance=HA_MODEL['distance'])
        self.audio_data = []

    def __del__(self) -> None:
        print("InputService stopped")

    def audio_callback(self, indata, frames, tiem, status):
        """ Called when new audio data is ready """
        pass

    def capture_audio(self, languages: str = None, cycle: int = 0, folder_name: str = None):
        file_audio_path = f"{ROOT_PROJECT}/uploads/{folder_name}/{folder_name}_{cycle}.mp3"
        file_text_path = f"{ROOT_PROJECT}/uploads/{folder_name}/{folder_name}_{cycle}.txt"
        myrecording = sd.rec(int(IO_AUDIO['sample_rate'] * IO_AUDIO['duration']), samplerate=IO_AUDIO['sample_rate'], 
                             channels=IO_AUDIO['channels'])
        sd.wait()
        write(file_audio_path, IO_AUDIO['sample_rate'], myrecording)
        text = self.explode.get_text(file_audio_path=file_audio_path, file_text_path=file_text_path, 
                                     languages=languages)
        response = self.hamodel.predict(sentence=text.get('text', 'No transcription found'))
        response['INPUT_TEXT'] = text.get('text')
        print(f"Cycle {cycle} : {response}")
        return response

    def capture_video(self):
        print("capture_video")
