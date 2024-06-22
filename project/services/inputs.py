import sounddevice as sd

from scipy.io.wavfile import write

from project.services.explode import ExplodeService
from project.services.hamodel import HAModelService
from project.services.vsmodel import VSModelService
from constants import IO_AUDIO, ROOT_PROJECT, HA_MODEL


class InputService:
    """ input service """

    def __init__(self) -> None:
        self.explode = ExplodeService()
        self.hamodel = HAModelService(
            type_model=HA_MODEL['type'], corpus=HA_MODEL['corpus'], transformer=HA_MODEL['transformer'])
        self.vsmodel = VSModelService()
        self.audio_data = []

    def __del__(self) -> None:
        print("InputService stopped")

    def capture_audio(self, cycle: int = 0, folder_name: str = None):
        """ capture audio """
        file_audio_path = f"{ROOT_PROJECT}/uploads/{folder_name}/{folder_name}_{cycle}.mp3"
        file_text_path = f"{ROOT_PROJECT}/uploads/{folder_name}/{folder_name}_{cycle}.txt"
        myrecording = sd.rec(
            int(IO_AUDIO['sample_rate'] * IO_AUDIO['duration']), samplerate=IO_AUDIO['sample_rate'],
            channels=IO_AUDIO['channels'])
        sd.wait()
        write(file_audio_path, IO_AUDIO['sample_rate'], myrecording)
        text = self.explode.get_text(file_audio_path=file_audio_path, file_text_path=file_text_path)
        response = self.hamodel.predict(sentence=text.get('text', 'No transcription found'))
        response['INPUT_TEXT'] = text.get('text')
        print(f"Cycle {cycle} : {response}")
        return response

    def capture_video(self, frame):
        """ capture video """
        df, frame = self.vsmodel.predict(frame=frame)
        return self.vsmodel.process(df=df, frame=frame)
