import cv2

from constants import ROOT_PROJECT, HOW2SIGN_DIRECTORY


class OutputService:
    """ output service """

    def __init__(self) -> None:
        self.position_top = (10, 26)
        self.position_bottom = (10, 52)
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.font_scale = 1
        self.font_color = (255, 255, 255)
        self.line_type = 2

    def __del__(self) -> None:
        pass

    def show_video(self, list_videos: list = None, folder_name: str = None):
        """ show video """
        out = cv2.VideoWriter(
            f"{ROOT_PROJECT}/uploads/{folder_name}/output.avi", cv2.VideoWriter_fourcc(*'DIVX'), 20.0, (640, 480))

        for video in list_videos:
            _ = cv2.VideoCapture(f"{ROOT_PROJECT}/{HOW2SIGN_DIRECTORY}/{video['SENTENCE_NAME']}.mp4")
            while _.isOpened():
                ret, frame = _.read()
                if ret:
                    cv2.putText(
                        frame, f"Input: {video['INPUT_TEXT']}", self.position_top, self.font, self.font_scale,
                        self.font_color, self.line_type)
                    cv2.putText(
                        frame, f"Output: {video['SENTENCE']}", self.position_bottom, self.font, self.font_scale,
                        self.font_color, self.line_type)
                    out.write(frame)
                    cv2.imshow('Video', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            _.release()
