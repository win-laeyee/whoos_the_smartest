import google.generativeai as genai


import logging


def cleanup_file(file):
    genai.delete_file(file.name)
    logging.info(f'Deleted file {file.uri}')