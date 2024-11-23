#!/usr/bin/env python3

from argparse import ArgumentParser
from os import path, makedirs
from magic import Magic

from subprocess import Popen, PIPE
from datetime import datetime
from tqdm import tqdm


###############################################################################
def run_sub_cmds(command):
    # Run the command
    process = Popen(command, stdout=PIPE, stderr=PIPE)

    # Capture the output and error
    stdout, stderr = process.communicate()

    # Decode byte strings to normal strings
    if "HandBrakeCLI" in command:
        stderr = stderr.decode()
    else: 
        stdout = stdout.decode()

    # So we only care about the stderr because thats how handbrakecli works
    return stdout, stderr


###############################################################################
def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "input",
        help = "Input file to parse into chapters"
    )

    parser.add_argument(
        "-l",
        "--episode_length",
        required = False,
        help = "Average Episode length",
        default = 24 # roundabout time in minutes
    )

    parser.add_argument(
        "-c",
        "--chapters",
        required = False,
        default = 0,
        help = "Chapters per episode"
    )

    parser.add_argument(
        "-o",
        "--output",
        required = False,
        help = "output directory location",
        default = "Episodes"
    )

    parser.add_argument(
        "-d",
        "--debug",
        required = False,
        help = "Enable debugging to see chapters and episodes",
        default = False,
        action = "store_true"
    )

    args = parser.parse_args()
    return vars(args)


###############################################################################
def check_bytes(filename):
    with open(filename, 'rb') as file:
        result = bytearray()
        while True:
            byte = file.read(1)
            if not byte or len(result) == 6:  # EOF / Len of read needed
                break
            if byte != b'\x00':
                result.append(byte[0])  # Append the non-zero byte to result

    if b"CD001" in result:
        return True

    return False


###############################################################################
def check_exists(filename):
    if path.isfile(filename):
        if check_bytes(filename):
            return
    print("\033[91;5mPlease try again with a valid file\033[0m")
    exit()


###############################################################################
def get_title_location(filename): 
    command = ["lsdvd", filename]
    lsdvd_output, _ = run_sub_cmds(command)
    title_location = lsdvd_output.split("\n")[-2].split()[-1]
    return title_location

###############################################################################
def get_chapters(filename, title_location):
    command = ["HandBrakeCLI", "-i", filename, "-t", title_location, "--scan"]
    _, handbrake_output = run_sub_cmds(command)

    chapters = []
    for line in handbrake_output.split("\n"):
        if "scan: chap" in line:
            chapter_base = line.split('chap ')[1].split(', ')
            chapter_number = int(chapter_base[0])
            chapter_length = int(chapter_base[1].split()[0])
            chapters.append([chapter_number, chapter_length])
    return chapters


###############################################################################
def get_episode_chapters(chapters, episode_length, chapter_len=0):
    episodes = {}

    episode_number = 1

    if chapter_len == 0:
        running_total = 0
        tmp_chapters = []

        for chapter in chapters:
            running_total += chapter[1]
            tmp_chapters.append(chapter[0])
            if running_total >= episode_length:
                episodes[episode_number] = tmp_chapters

                episode_number += 1
                running_total = 0
                tmp_chapters = []
    else:
        count = 1
        placeholder = 1
        for chapter in chapters:
            if count % chapter_len+1 == 1:
                tmp = chapter[0]
                episodes[episode_number] = [i for i in range(placeholder, tmp+1, 1)]
                placeholder = tmp + 1
                episode_number += 1
            count += 1

    return episodes


###############################################################################
def create_episodes(input_iso, title_location, output, episodes):
    input_name = input_iso.split(".")[0].split("/")[-1]

    if not path.isdir(output):
        makedirs(output)

    #for episode in episodes:
    for episode in tqdm(episodes):
        episode_name = f"{input_name}_EPISODE_{episode}.m4v"
        command = [
            "HandBrakeCLI", "-i", input_iso, "-t", title_location,
            "-c", f"{episodes[episode][0]}-{episodes[episode][-1]}",
            "-o", f"{output}/{episode_name}"
        ]

        run_sub_cmds(command)

        # Convert to mp4
        command = ["ffmpeg", "-i", f"{output}/{episode_name}",
                   "-codec", "copy",
                    f"{output}/{episode_name.replace('m4v', 'mp4')}"]

        run_sub_cmds(command)

        command = ["rm", f"{output}/{episode_name}"]
        run_sub_cmds(command)
    return

###############################################################################
def main():
    args = get_args()
    input_iso = args["input"]
    chapter_len = int(args["chapters"])
    output = args["output"]
    debug = args["debug"]
    # total ms = minutes * 60 seconds * 1000ms
    episode_length = int(args["episode_length"]) * 60 * 1000  # minutes to ms

    check_exists(input_iso)
    title_location = get_title_location(input_iso)
    chapters = get_chapters(input_iso, title_location)

    if debug: print(chapters)

    if chapter_len != 0:
        episodes = get_episode_chapters(chapters, episode_length, chapter_len)
    else:
        episodes = get_episode_chapters(chapters, episode_length)
        if debug: print(episodes)

    create_episodes(input_iso, title_location, output, episodes)

    return


###############################################################################
if __name__ == '__main__':
    exit(main())
