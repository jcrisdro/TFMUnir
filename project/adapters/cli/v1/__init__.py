import argparse
from pdb import run


from project.adapters.cli.v1.run_models import RunModelsCliAdapter

def setup_args():
    """
    Setup the arguments for the CLI
    """
    parser_args = argparse.ArgumentParser(description='Files CLI')
    parser_args.add_argument('-m', '--model', type=str, choices=['vsmodel', 'hamodel'], required=True)
    parser_args.add_argument('-t', '--task', type=bool, choices=['train'], required=False)
    parser_args.add_argument('-c', '--cam', type=bool, default=False)
    parser_args.add_argument('-p', '--path', type=str, )
    parser_args.add_argument('-S', '--sentences', type=str, default=None)
    return parser_args


def handle_args(args: dict = None):
    run_models_cli_adapter = RunModelsCliAdapter()
    if args.model == 'vsmodel':
        run_models_cli_adapter.vsmodel()
    else:
        if args.path:
            run_models_cli_adapter.hamodel(path=args.path)
        if args.sentences:
            run_models_cli_adapter.hamodel(sentences = args.sentences)


if __name__ == "__main__":
    """ main function """
    parser = setup_args()
    handle_args(parser.parse_args())
