import argparse
import os
import cv2

from datetime import datetime
from pynput import keyboard as kb
from colorama import init, Fore, Back, Style

from project.adapters.cli.v1.run_models import RunModelsCliAdapter
from project.services.inputs import InputService
from project.services.outputs import OutputService
from constants import ROOT_PROJECT


def setup_args():
    """
    Setup the arguments for the CLI
    """
    parser_args = argparse.ArgumentParser(description='Files CLI')
    parser_args.add_argument('-m', '--model', type=str, choices=['vsmodel', 'hamodel'], required=True)
    parser_args.add_argument('-t', '--task', type=bool, choices=['train'], required=False)
    parser_args.add_argument('-c', '--cam', type=bool, default=False)
    parser_args.add_argument('-a', '--audio', type=bool, default=False)
    parser_args.add_argument('-p', '--path', type=str, )
    parser_args.add_argument('-S', '--sentences', type=str, default=None)
    parser_args.add_argument('-L', '--languages', type=str, default='es')
    parser_args.add_argument('-Ta', '--test_audio', type=str)
    return parser_args


def handle_args(args: dict = None):
    def pull(key):
        pass

    def push(key):
        if key == kb.KeyCode.from_char('q') or key == kb.Key.esc:
            print(f"Exiting {key}")
            return False

    folder_name = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    print(Style.BRIGHT + Fore.YELLOW + f"making directory {ROOT_PROJECT}/uploads/{folder_name}")
    os.mkdir(f"{ROOT_PROJECT}/uploads/{folder_name}")
    cycle = 0
    if args.model == 'vsmodel':
        input_service = InputService()
        output_service = OutputService()
        run_models_cli_adapter = RunModelsCliAdapter()
        run_models_cli_adapter.vsmodel()
        if args.cam:
            capture = cv2.VideoCapture(0)
            while capture.isOpened():
                status, frame = capture.read()
                if not status or (cv2.waitKey(10) & 0xFF == ord('q')):
                    break
                _ = input_service.capture_video(frame=frame)
    elif args.model == 'hamodel':
        input_service = InputService()
        output_service = OutputService()
        if args.audio:
            print(Back.YELLOW + Fore.WHITE + "press Q for exit" + Style.RESET_ALL)
            segment = []
            my_listener = kb.Listener(pull, push)
            my_listener.start()
            while my_listener.is_alive():
                segment.append(input_service.capture_audio(cycle=cycle, folder_name=folder_name))
                output_service.show_video(list_videos=segment, folder_name=folder_name)
                cycle = cycle + 1
            print(Back.RED + Fore.WHITE + "destroyed all windows")
            cv2.destroyAllWindows()
        elif args.test_audio:
            test_video = [{
                'VIDEO_NAME': '-0N0jbyBW6g-5-rgb_front',
                'SENTENCE_NAME': '-0N0jbyBW6g_0-5-rgb_front',
                'SENTENCE': 'Hello.',
                'EMBEDDINGS_DISTANCES': 0.3518511652946472,
                'START_REALIGNED': 1.79,
                'END_REALIGNED': 2.27,
                'VIDEO_ID': '-0N0jbyBW6g',
                'INPUT_TEXT': ' Hello, that is good.'
            }, {
                'VIDEO_NAME': 'FadLsYNd2tk-5-rgb_front',
                'SENTENCE_NAME': '_0-JkwZ9o4Q_5-5-rgb_front',
                'SENTENCE': "Good, that's very good.",
                'EMBEDDINGS_DISTANCES': 0.36733341217041016,
                'START_REALIGNED': 68.5,
                'END_REALIGNED': 70.55,
                'VIDEO_ID': 'FadLsYNd2tk',
                'INPUT_TEXT': ' Hello, that is good. Hello, that is good.'
            }]
            output_service.show_video(list_videos=test_video, folder_name='test')
        else:
            if args.path:
                run_models_cli_adapter = RunModelsCliAdapter()
                run_models_cli_adapter.hamodel(path=args.path)
            elif args.sentences:
                run_models_cli_adapter = RunModelsCliAdapter()
                run_models_cli_adapter.hamodel(sentences=args.sentences)
            else:
                print("Please select a valida option")
    else:
        print("Please select a valid model")


if __name__ == "__main__":
    """ main function """
    init()
    print(Style.BRIGHT + Fore.YELLOW + "Preparing project")
    parser = setup_args()
    handle_args(parser.parse_args())
