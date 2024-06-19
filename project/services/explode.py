import cv2
import os
import whisper

from moviepy.editor import VideoFileClip


class ExplodeService:
    """ service to explode video """

    def __init__(self) -> None:
        self.file_path = None

    def __del__(self) -> None:
        print("ExplodeService stopped")

    def set_file_path(self, file_path: str = None) -> None:
        """ set file path """
        self.file_path = file_path

    def get_text(self, file_audio_path: str = None, file_text_path: str = None) -> str:
        """ get text """
        text = {}
        try:
            whisper_model = whisper.load_model("base")
            text = whisper_model.transcribe(file_audio_path)
            with open(file_text_path, "w") as file:
                file.write(text.get('text', 'No transcription found'))
            return text
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            print("Finish transcrypting video...")

    def split(self, root_path: str = None, file_path: str = None, folder_name: str = None):
        """ split video """
        try:
            os.mkdir(f"{root_path}/uploads/{folder_name}")
            os.mkdir(f"{root_path}/uploads/{folder_name}/frames")
        except Exception as e:
            print(f"Exception: {e}")

        try:
            movie = VideoFileClip(f"{root_path}/{file_path}")
            audio = movie.audio
            audio.write_audiofile(f"{root_path}/uploads/{folder_name}/{folder_name}.mp3")
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            movie.close()
            audio.close()

        try:
            capture = cv2.VideoCapture(f"{root_path}/{file_path}")
            frames = 0
            while capture.isOpened():
                ret, frame = capture.read()
                if ret is True:
                    frames += 1
                    cv2.imwrite(f"{root_path}/uploads/{folder_name}/frames/{frames}.jpg", frame)
                else:
                    break
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            print("Finish getting frames...")

        text = self.get_text(
            f"{root_path}/uploads/{folder_name}/{folder_name}.mp3", 
            f"{root_path}/uploads/{folder_name}/{folder_name}.txt")

        response = {'frames': frames, 'key': folder_name, 'language': text.get('language', 'No language found'),
                    'transcription': text.get('text', 'No transcription found').split(',')}
        return response
