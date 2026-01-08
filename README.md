# Google Keep Takeout Helper

A simple tool to convert Google Keep notes from [Google Takeout](https://takeout.google.com/) (HTML + JSON) into clean Markdown files.

## Prerequisites

* Python 3.x
* `pip` (Python package manager)

## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies:
```bash
pip install beautifulsoup4 html2text
```

## Configuration

1. Create a local configuration file by copying the example:
```bash
cp config.example.py config.py
```

2. Open `config.py` in your text editor and update the path to point to your unzipped Google Keep Takeout folder.

## Usage

Run the script to begin the conversion:

```bash
python GoogleKeepTakeoutHelper.py
```
Or:

```bash
python3 GoogleKeepTakeoutHelper.py
```