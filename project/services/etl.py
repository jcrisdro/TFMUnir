import cv2
import os

from moviepy.editor import VideoFileClip


class ETL:

    def set_file_path(self, file_path) -> None:
        self.file_path = file_path

    def split(self, root_path: str = None, file_path: str = None, folder_name: str = None):
        try:
            os.mkdir(f"{root_path}/resources/uploads/{folder_name}")
        except Exception as e:
            print(f"Exception: {e}")

        try:
            movie = VideoFileClip(f"{root_path}/{file_path}")
            audio = movie.audio
            audio_path = f"/resources/uploads/{folder_name}/audio.mp3"
            audio.write_audiofile(f"{root_path}/{audio_path}")
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            movie.close()
            audio.close()
        print(f"getting audio from video... {audio_path}")

        try:
            capture = cv2.VideoCapture(f"{root_path}/{file_path}")
            cont = 0
            while(capture.isOpened()):
                ret, frame = capture.read()
                if ret is True:
                    cont += 1
                    cv2.imwrite(f"{root_path}/resources/uploads/{folder_name}/frame_{cont}.jpg", frame)
                else:
                    break
        except Exception as e:
            print(f"Exception: {e}")
        print(f"getting frames from video... {file_path}")
        return cont, audio_path