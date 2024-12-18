import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Apply lomographic filters to an image.')
    parser.add_argument('filename', help='File containing the image')
    args = parser.parse_args()
    return args