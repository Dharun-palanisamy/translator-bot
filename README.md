# <p align="center">Translator Bot</p>

<div align="right">
<a href="LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg" target="_blank" >
</a>
</div>

This is telegram bot to translate text to any language. This bot uses python library `googletrans` to translate the text.

## ✨ How it Works

You have to initialize by `/start` command. Enter `/help` for list all command.
To translate just enter the text. To translate to specific language enter the text in following format

> Lang Code | Text

for example

> hi | Hi im a language translator bot

This will translate the text to Hindi. \
Same format follows for inline translation. /list command will list all the language code.

## 🚀 Usage

### Prerequisites

It is presumed that you have obtained an API token with [@BotFather](https://core.telegram.org/bots#botfather). Refer [here](https://core.telegram.org/bots#6-botfather) for more info.

### Installation

You need to install following python package : `python-telegram-bot`, `googletrans`,`python-telegram-bot[ext]`

```bash
pip install -r requirements.txt
```

## 📝 License

Copyright © 2023 [Dharun A P](https://github.com/mr-u0b0dy). \
This project is [MIT](LICENSE) licensed.
