# Recorder for Realtime Speech-to-text Service

This is a realtime recorder to invoke [STT service API](https://github.com/Atomoxide/stt/) and invoke [FFXIV PostNamazu](https://github.com/Natsukage/PostNamazu) with converted text.

## Installation

Tested under Python 3.10

0. Deploy [STT service API](https://github.com/Atomoxide/stt/) and [FFXIV PostNamazu](https://github.com/Natsukage/PostNamazu)


1. Initiate a Python virtual environment. Must be named `.venv` to use the PowerShell Script.
```shell script
python3 -m venv .venv
```

2. Activate virtual environment (Windows)
```shell script
.\.venv\Scripts\Activate
```

3. Pip install dependencies
```shell script
pip install -r requirements.txt
```

4. Start (Windows)
```shell script
.\run.ps1
```

## To Config STT URL

modify stt_api.py