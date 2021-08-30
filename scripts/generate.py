from copy import deepcopy
from json import dump
from os import listdir, remove
from os.path import isfile, join
from pathlib import Path

from constants import BRAILLE_MAPPING, COLOR_SAFE_PELLETE, METADATA_TEMPLATE
from helper import gen_primes
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "assets/fonts"
METADATA_PATH = "metadata"
OUTPUT_PATH = "generated-arts"


def init_dir(dir_path):
    """ Initilize or reset directories """
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    for f in listdir(dir_path):
        remove(join(dir_path, f))


def generate_art(start, max_primes, total, width=786, height=786):
    """ Dynmically generate art, its metadata and write to folder """

    token_id = 0

    for color_name, color_code in COLOR_SAFE_PELLETE.items():
        for prime in gen_primes(start=start, max_count=max_primes):
            for i, font_name in enumerate(listdir(FONT_PATH)):
                
                font_file = join(FONT_PATH, font_name)
                font_name = font_name[:-4]

                if not isfile(font_file):
                    continue

                img = Image.new('RGB', (width, height), color=color_code)

                text = "".join([BRAILLE_MAPPING[c] for c in str(prime)])
                
                fnt = ImageFont.truetype(font_file, int(width*0.125))
                w, h = fnt.getsize(text)
                center_pos = ((width-w)/2, (height-h)/2)

                d = ImageDraw.Draw(img)
                d.text(center_pos, text, fill=(0, 0, 0), font=fnt)

                image_name = f"{token_id+1}-prime-braille-{prime}-{color_name}-font{i+1}"
                output_image_name = f"{OUTPUT_PATH}/{image_name}.png"

                metadata = deepcopy(METADATA_TEMPLATE)

                metadata['name'] = image_name
                metadata['description'] = f"A unique braille art with prime number: {prime}, font-family: {font_name} and background-color: {color_name}"
                metadata['image'] = output_image_name

                metadata['attributes'].append(
                    {'trait_type': 'prime_number', 'value': prime})
                metadata['attributes'].append(
                    {'trait_type': 'braille_font', 'value': font_name})
                metadata['attributes'].append(
                    {'trait_type': 'bg_color', 'value': color_code})

                with open(f"{METADATA_PATH}/{image_name}.json", 'w') as f:
                    dump(metadata, f, indent=4)

                img.save(output_image_name)
                token_id += 1

        print(f"Progress: {token_id}/{total}")

    print(f"\nTotal {token_id} unique arts generated in {OUTPUT_PATH} folder.\n")


def main():

    start = int(input("\nEnter a number to start primes from (e.g. 43): "))
    max_primes = int(input("Enter a number of primes (e.g. 10): "))

    total = len(COLOR_SAFE_PELLETE) * max_primes * len(listdir(FONT_PATH))
    if input(f"\nThis script will generate {total} unique arts. Enter Y to proceed: ") not in ["Y", "y"]:
        print("Aborting..")
        return

    print("")

    init_dir(OUTPUT_PATH)
    init_dir(METADATA_PATH)
    generate_art(start, max_primes, total)


if __name__ == "__main__":
    main()
