title: "How to Clone or Export an Azure SQL Database Using SqlPackage"
date: 2022-09-26
category: Tutorials
tags: [azure, database]
feature: feature.png
description: "In this tutorial, we go over how to use SqlPackage to clone or export (.BACPAC) a database from an Azure SQL Database."

[TOC]

## What is SqlPackage and Why Use it?

[SqlPackage](https://learn.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage?view=sql-server-ver16) is a command-line utility provided by Microsoft that automates some database development tasks like exporting, importing and running scripts.

In this tutorial, we're using SqlPackage instead of SQL Management Studio (SSMS) as SSMS is much larger than what we need and if you're reading this tutorial to get a job done quick, you probably don't want to install a large application.

### Installing / Setup

SqlPackage can be obtained from [this Microsoft page](https://learn.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage-download?view=sql-server-ver16). On this page, you can get a msi installer if you want to install the application on your machine or you can download the zip file if you don't want to go through an installation process / are running this in a pipeline.

If you downloaded the zip, unzip it, move it to whatever special place you want it in and add that folder to your PATH environment variable. If you're unsure of how to add a folder to your PATH environment variable, [read this article](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

## Exporting/Backing up a Database

To export a database, you need the connection string to the source Azure SQL database; you can get this by going to the Azure portal and going to the database you want to export. Once you're on the database page, go to "Settings" -> "Connection strings" and copy the connection string (ADO.NET).

Now running this script will export the database to a .bacpac file:

```powershell
sqlpackage.exe /a:Export /tf:"backup.bacpac" /scs:"<connection string>"
```

The file backup.bacpac will now be in the current working directory and can be used to restore the database later.

## Cloning a Database

On top of exporting a database, we can use a similar method to clone the database.

To clone your Azure SQL database to another database, you will need the following:

- Connection string of the source database
- Connection string of the destination database (might look something like `Server=localhost,1433;Initial Catalog=DestinationDatabase;Integrated Security=False;User Id=sa;Password=MyPass@word;`)

Before you start cloning, you will need to make sure the destination database is completely clear. I usually do this by running the following in the `master` database (the one that you are not copying to but is on the same database server):

```sql
DROP DATABASE DestinationDatabase;
CREATE DATABASE DestinationDatabase;
```

After making sure your destination database is clear, export the source database:

```powershell
sqlpackage.exe /a:Export /tf:"backup.bacpac" /scs:"<source database connection string>"
```

Now we restore this .bacpac file into the destination database:

```powershell
sqlpackage.exe /a:Import /sf:"backup.bacpac" /tcs:"<destination database connection string>"
```
