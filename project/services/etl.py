import cv2
import os
import whisper

from moviepy.editor import VideoFileClip


class ETL:

    def set_file_path(self, file_path) -> None:
        self.file_path = file_path

    def split(self, root_path: str = None, file_path: str = None, folder_name: str = None):
        try:
            os.mkdir(f"{root_path}/resources/uploads/{folder_name}")
            os.mkdir(f"{root_path}/resources/uploads/{folder_name}/frames")
        except Exception as e:
            print(f"Exception: {e}")

        try:
            movie = VideoFileClip(f"{root_path}/{file_path}")
            audio = movie.audio
            audio_path = f"/resources/uploads/{folder_name}/{folder_name}.mp3"
            audio.write_audiofile(f"{root_path}/{audio_path}")
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            movie.close()
            audio.close()
            print(f"Finish audio from video... {audio_path}")

        try:
            capture = cv2.VideoCapture(f"{root_path}/{file_path}")
            frames = 0
            while(capture.isOpened()):
                ret, frame = capture.read()
                if ret is True:
                    frames += 1
                    cv2.imwrite(f"{root_path}/resources/uploads/{folder_name}/frames/{frames}.jpg", frame)
                else:
                    break
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            print("Finish getting frames...")

        text = {}
        try:
            whisper_model = whisper.load_model("base")
            text = whisper_model.transcribe(f"{root_path}/resources/uploads/{folder_name}/{folder_name}.mp3")
            with open(f"{root_path}/resources/uploads/{folder_name}/{folder_name}.txt", "w") as file:
                file.write(text.get('text', 'No transcription found'))
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            print("Finish transcrypting video...")

        response = {'frames': frames, 'key': folder_name, 'language': text.get('language', 'No language found')}
        return response
