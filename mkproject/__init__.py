import argparse

__version__ = '0.0.0'

def main():
    cfg = {}
    parser = argparse.ArgumentParser()

    parser.add_argument('name')
    args = parser.parse_args()
    cfg['name'] = args.name

    print('cfg: {}'.format(cfg))

    return 0
