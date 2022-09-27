title: "Import and Export files from an Azure Storage Account File Share with AzCopy"
date: 2022-09-27
category: Tutorials
tags: [azure]
feature: feature.png
description: "In this tutorial we go over how to import and export files to and from an Azure Storage Account File Share using AzCopy - a command line utility offered by Microsoft"

[TOC]

## What is AzCopy and why use it?

[AzCopy](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10) is a command-line utility offered by Microsoft that you can use to copy blobs or files to or from a storage account. Rather than using SMB, AzCopy is a much faster method to transfer files between your local machine and an Azure Storage Account File Share.

> In this tutorial, we will only look at moving files between your local machine and an Azure Storage Account File Share. AzCopy also supports blobs and functions in a similar way but is not covered in this tutorial.

## Setup

Download AzCopy from [this Microsoft page](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10#download-azcopy), when complete, unzip the .zip file to find azcopy.exe.

All commands from here on in will use this azcopy.exe file. To use the file, you can:

- You can then move this file to a location that is in your PATH environment variable so that you can run it from anywhere
- Use an absolute reference to the exe, for example in PowerShell: `& "C:/Users/USER/Downloads/azcopy_windows_amd64_10.16.0/azcopy.exe"`
- Execute your commands from the directory that the azcopy.exe file is in

## Obtaining a SAS Token

To interact with a file share, you will need a SAS token for authorization.

Generate a SAS token for the storage account by following these steps:

1. Go to the storage account in Azure portal
2. Go to "Shared access signature" under "Security + networking"
3. "Allowed services" = "File" only
4. "Allowed resource types" = all
5. "Allowed permissions" = all
6. "Start and expiry date/time" = leave start time, set end time to something close (1hr)
7. "Allowed IP addresses" = your current IP address
8. Click "Generate SAS and connection string"
9. Copy the value for "SAS token" - COPY IT BEFORE NAVIGATING AWAY

## Uploading / Importing

To upload a single file, execute:

```powershell
azcopy.exe copy ./path/to/single_file.txt "https://<storage_account_name>.file.core.windows.net/<file_share_name>?<sas_token>"
# For example,
azcopy.exe copy ./path/to/single_file.txt "https://mystorageaccount.file.core.windows.net/myfileshare?sv=2021-06-..."
```

If you want to put it somewhere other than the root, use something like:

```powershell
# Into a specific folder (destination/file/)
azcopy.exe copy ./path/to/single_file.txt "https://<storage_account_name>.file.core.windows.net/<file_share_name>/destination/file/?<sas_token>"
# Rename at the same time (specify file name - destination/file/new_file.txt)
azcopy.exe copy ./path/to/single_file.txt "https://<storage_account_name>.file.core.windows.net/<file_share_name>/destination/file/new_file.txt?<sas_token>"
```

To upload a directory, execute:

```powershell
azcopy.exe copy ./path/to/directory "https://<storage_account_name>.file.core.windows.net/<file_share_name>?<sas_token>" --recursive
```

> This will copy the folder "directory" and all of its contents to the root of the file share - it will create a new "directory" folder. You can specify a destination folder by adding it to the end of the URL, for example: `https://<storage_account_name>.file.core.windows.net/<file_share_name>/destination/folder/?<sas_token>`

To upload all files in a directory (and not create a new directory), execute:

```powershell
azcopy.exe copy ./path/to/directory/* "https://<storage_account_name>.file.core.windows.net/<file_share_name>?<sas_token>"
```

> Note the `*` at the end of the source path. This will copy all files in the directory, but not the directory itself.

## Downloading / Exporting

To copy a single file, execute:

```powershell
azcopy.exe copy "https://<storage_account_name>.file.core.windows.net/<file_share_name>/<file_name>?<sas_token>" ./path/to/single_file.txt
# For example,
azcopy.exe copy "https://<storage_account_name>.file.core.windows.net/<file_share_name>/path/to/file/filename.text?<sas_token>" ./path/to/single_file.txt
```

To copy a directory, execute:

```powershell
azcopy.exe copy "https://<storage_account_name>.file.core.windows.net/<file_share_name>/<directory_name>?<sas_token>" ./path/to/directory
```

To copy all files in a directory, execute:

```powershell
azcopy.exe copy "https://<storage_account_name>.file.core.windows.net/<file_share_name>/<directory_name>/?<sas_token>" ./path/to/directory --recursive
```

> This will copy the directory into the directory you named locally - you can get around this by using `*` like above top copy all files but not the directory itself.

## Clearing a File Share

```powershell
azcopy.exe rm "https://<storage_account_name>.file.core.windows.net/<file_share_name>?<sas_token>" --recursive
```
