from dataclasses import dataclass
from pathlib import Path
import os
import sys
from typing import List

from ..config import FREEZE_DESTINATION


@dataclass
class FileStats:
    path: Path
    extension: str
    file_type: str
    size: int


def __get_file_type(extension: str) -> str:
    if extension == '.html':
        return 'html'
    elif extension == '.png' or extension == '.jpeg' or extension == '.jpg' or extension == '.ico' or extension == '.gif':
        return 'image'
    elif extension == '.svg':
        return 'svg'
    elif extension == '.js':
        return 'js'
    elif extension == '.css':
        return 'css'
    elif extension == '.xml':
        return 'xml'
    elif extension == '.txt':
        return 'txt'
    elif extension == '.py':
        return 'python'
    elif extension == '.mp4':
        return 'mp4'
    elif extension == '.ui':
        return 'ui'
    elif extension == '':
        return '[None]'
    return extension


def __bytes_to_human_readable(size, precision=2):
    """ From https://stackoverflow.com/a/32009595/ """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffix_index = 0
    while size > 1024 and suffix_index < 4:
        suffix_index += 1  # increment the index of the suffix
        size = size/1024.0  # apply the division
    return "%.*f%s" % (precision, size, suffixes[suffix_index])


def print_build_stats():
    """ Output stats of the latest build """
    # Validate build exists
    if not FREEZE_DESTINATION.exists():
        print('No build found')
        sys.exit(1)

    # Get all files in the output directory
    all_files: List[FileStats] = []
    for root, dirs, files in os.walk(FREEZE_DESTINATION, topdown=False):
        root_path = Path(root)
        for file in files:
            path = root_path / file
            extension = path.suffix

            file_stats = FileStats(
                path,
                extension,
                __get_file_type(extension),
                path.stat().st_size
            )
            all_files.append(file_stats)

    # Output total size
    total_files = len(all_files)
    total_size = sum(map(lambda x: x.size, all_files))
    print(f'Total files: {total_files}')
    print(f'Total size: {__bytes_to_human_readable(total_size)}')
    print()

    # Output grouped by extension
    file_type_groupings = {}
    for file in all_files:
        if file.file_type in file_type_groupings:
            file_type_groupings[file.file_type]['size'] += file.size
            file_type_groupings[file.file_type]['count'] += 1
        else:
            file_type_groupings[file.file_type] = {
                'size': file.size,
                'count': 1
            }
    file_type_groupings_ordered_by_size = {k: v for k, v in sorted(file_type_groupings.items(), key=lambda item: item[1]['size'], reverse=True)}
    print(f'|{"Extension":^14}|{"Size":^11}|{"%":^7}|{"Count":^7}|')
    print(f'|{("-"*14):^14}|{("-"*11):^11}|{("-"*7):^7}|{("-"*7):^7}|')
    for file_type in file_type_groupings_ordered_by_size:
        size = file_type_groupings[file_type]['size']
        percentage = (size / total_size) * 100
        count = file_type_groupings[file_type]['count']
        print(f'|{file_type:^14}|{__bytes_to_human_readable(size):^11}|{round(percentage, 2):^7}|{count:^7}|')
