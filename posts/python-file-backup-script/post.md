title: "Python File Backup Script"
date: 2020-08-14
category: Tools
tags: [python, backup]
feature: feature.png
description: "This script allows you to backup a file or folder as a zip file into a backup folder. It is designed to be run periodically for backing up something like an SQLite database."

[TOC]

## Background
Yesterday I may have dropped a few too many rows from a demo-prod database as I was frantically trying to fix crazy response times from the demo instance of [hit-counter](https://github.com/brentvollebregt/hit-counter). After figuring out the crazy response times were due to the amount of traffic coming in, and sorting it out, I thought it would be a good idea to clean the database of URLs that had less than 3 counts against it in hope to improve performance on the home page (a good 2/3 of the database).

I downloaded the database, performed some operations and uploaded it to the server for it to immediately start being used (overwriting over the older version). I'm still not quite sure what went wrong; I probably deleted the SQLite WAL file or my SQLite client played me - but whatever it was, I had lost a significant amount of data at some point because when I viewed the stats on the home page after reloading the server, it looked very wrong.

I tried to think when I last backed up this database and remembered it was a couple of months ago and I had put the SQLite file in Google Drive. Using the version of the database I had just butchered and this embarrassingly old backup, I took the max counts for all URLs from both databases to try to reconstruct what I could of the original. This was probably the best result I could get at the time.

> Although, at the time of writing this, I have just remembered that the recycling bin exists for this exact reason... Identifying the database I originally downloaded and performing some operations on the current database has helped me reconstruct the original database that only excludes counts from the time I was originally modifying it. I'm much happier with the result now.

Did I learn my lesson? Yes.

 1. Run `PRAGMA schema.wal_checkpoint;` before deleting WAL files.
 2. Copy SQLite files before you try to do some dangerous operations on them and delete them when you are confident all is well.
 3. Keep backups of the database in the first place!

## What This Script Does
This script is lesson #3 - backup the database. This script will take a folder or file, zip it, and store it in a different directory with the timestamp. A maximum backup count has also been added to delete older backups when a limit is reached.

This script is designed to be run periodically by something like CRON and works on both Linux and Windows.

The script takes three parameters that are hard-coded as constants at the top of the script:

- `OBJECT_TO_BACKUP`: The file or folder to be zipped up and put into `BACKUP_DIRECTORY`.
- `BACKUP_DIRECTORY`: The directory to store the backup zips in.
- `MAX_BACKUP_AMOUNT`: The maximum about of backed-up zips to have in `BACKUP_DIRECTORY`.
 
This script follows a basic process:

1. Validate that the file/folder we are about to backup exists.
2. Validate the backup directory exists and create if required.
3. Gets the amount of past backup zips in the backup directory already and removes the oldest files if required to be under `MAX_BACKUP_AMOUNT`.
4. Create the zip for the file/folder in `BACKUP_DIRECTORY`.

> Python 3.6+ is required to run this file due to the usage of f-strings and pathlib

## Script

```python
from datetime import datetime
from pathlib import Path
import zipfile


OBJECT_TO_BACKUP = '/home/server/data.db'  # The file or directory to backup
BACKUP_DIRECTORY = '/home/server/backup'  # The location to store the backups in
MAX_BACKUP_AMOUNT = 5  # The maximum amount of backups to have in BACKUP_DIRECTORY


object_to_backup_path = Path(OBJECT_TO_BACKUP)
backup_directory_path = Path(BACKUP_DIRECTORY)
assert object_to_backup_path.exists()  # Validate the object we are about to backup exists before we continue

# Validate the backup directory exists and create if required
backup_directory_path.mkdir(parents=True, exist_ok=True)

# Get the amount of past backup zips in the backup directory already
existing_backups = [
    x for x in backup_directory_path.iterdir()
    if x.is_file() and x.suffix == '.zip' and x.name.startswith('backup-')
]

# Enforce max backups and delete oldest if there will be too many after the new backup
oldest_to_newest_backup_by_name = list(sorted(existing_backups, key=lambda f: f.name))
while len(oldest_to_newest_backup_by_name) >= MAX_BACKUP_AMOUNT:  # >= because we will have another soon
    backup_to_delete = oldest_to_newest_backup_by_name.pop(0)
    backup_to_delete.unlink()

# Create zip file (for both file and folder options)
backup_file_name = f'backup-{datetime.now().strftime("%Y%m%d%H%M%S")}-{object_to_backup_path.name}.zip'
zip_file = zipfile.ZipFile(str(backup_directory_path / backup_file_name), mode='w')
if object_to_backup_path.is_file():
    # If the object to write is a file, write the file
    zip_file.write(
        object_to_backup_path.absolute(),
        arcname=object_to_backup_path.name,
        compress_type=zipfile.ZIP_DEFLATED
    )
elif object_to_backup_path.is_dir():
    # If the object to write is a directory, write all the files
    for file in object_to_backup_path.glob('**/*'):
        if file.is_file():
            zip_file.write(
                file.absolute(),
                arcname=str(file.relative_to(object_to_backup_path)),
                compress_type=zipfile.ZIP_DEFLATED
            )
# Close the created zip file
zip_file.close()
```
