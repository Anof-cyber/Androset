# Android-Certificate-
Automated script to push Burp Suite certificate in Android 

## Prerequisites

- Python 3+ (Not verified)
- adb in system environment variables
- Burp or Other CA cert in DER


## Installation
Manual Installation

```bash
  git clone https://github.com/Anof-cyber/androset
  cd androset
  pip install -r requirements.txt
```

Install with PIP
```
pip install androset
```
## Usage/Examples

Convert and push Burp Certificate to android

```bash
python3 androset.py cert --cert cacert.der
```

Specify  ADB IP and Port
```bash
python3 androset.py cert --cert cacert.der --adbip 127.0.0.1:5555
```

Modify Android IPTable to redirect all traffic to burp

```bash
python3 androset.py burp --burpip 127.0.0.1:8080
```

```bash
python3 androset.py burp --burpip 127.0.0.1:8080 --adbip 127.0.0.1:5555
```


push burp cert and modify IP table
```bash
python3 androset.py cert burp --burpip 127.0.0.1:8080 --adbip 127.0.0.1:5555 --cert cacert.der
```


## Acknowledgements
The tool is Created using [ChatGPT](https://chat.openai.com/chat) with some custom modification. 

