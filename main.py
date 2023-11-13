import sys
import piper 
import subprocess

# speakers
# speaker_id

import regex as re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

book = epub.read_epub("test.epub")
items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

chapters = filter(lambda i: i.get_name() != 'chapter', items)

# see if the text contains tags for references
# ...
# elif the text contains footnotes
# ...
# elif the text contains inline referencing
# 

def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
    for a in soup.find_all('a'):
        a.replace_with('')
    text = [para.get_text() for para in soup.find_all('p')]
    text = ' '.join(text)
    text = re.sub(r'\(\d+-?\d*\)', '', text)
    return text

texts = {}
for c in chapters:
    texts[c.get_name()] = chapter_to_str(c)
    # stream text to piper
    # p.communicate(texts[c.get_name()].encode('utf-8'))

# TODO: multispeaker mode for things like emphasis
# TODO: multispeaker (map 'said' synonyms to speaker_id's)

import argparse
import logging
import os
import subprocess

# define the command line arguments
parser = argparse.ArgumentParser(description="Piper command line interface")
parser.add_argument("-m", "--model", required=True, help="Path to the ONNX model file")
parser.add_argument("-c", "--config", required=True, help="Path to the configuration file")
parser.add_argument("-o", "--output-dir", required=True, help="Path to the output directory")
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")

# parse the command line arguments
args = parser.parse_args()

# configure the logging
logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
_LOGGER = logging.getLogger(__name__)

def texts_to_wav(texts, output_dir):
    for name, text in texts.items():
        # call Piper as a bash process
        cmd = f"echo '{text}' | piper -m {args.model} -c {args.config} -f wav -r 22050 -o {os.path.join(args.output_dir, f'{name}.wav')}"
        subprocess.run(cmd, shell=True, check=True)
        _LOGGER.info(f"Saved audio file to {os.path.join(args.output_dir, f'{name}.wav')}")
# synthesize the text and save the audio files