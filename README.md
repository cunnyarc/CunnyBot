<p align="center">
    <img src="./assets/Logo.png">
</p>
<h3 align="center">A Curated Gelbooru to Twitter / Discord Bot</h3>
<p align="center">
    <a href="https://liberapay.com/GlitchyChan/donate">
        <img src="https://img.shields.io/badge/Liberapay-F6C915?style=for-the-badge&logo=liberapay&logoColor=black" alt="liberapay" />
    </a>
    <a href="https://discord.gg/ZxbYHEh">
        <img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=fff&style=for-the-badge" alt="Discord" />
    </a>
    <a href="https://twitter.com/cutemoebot">
        <img src="https://img.shields.io/badge/twitter-%2300acee?&style=for-the-badge&logo=twitter&logoColor=white" alt="twitter" />
    </a>
</p>

<p align="center">
    <a href="#about">About</a> •
    <a href="#features">Features</a> •
    <a href="#development">Development</a> •
    <a href="#deploy">Deploy</a>
</p>

## **About**
This script takes a random image from <a href="https://gelbooru.com">Gelbooru</a> using curated tags and posts it to Discord / Twitter

## **Features**
- 💀 Overkill
- 🔁 Asyncio
- 🔥 Blazingly Fast™️
- 📝 Pretty logging with <a href="https://github.com/Delgan/loguru">Loguru</a>
- ⚙️ Easily editable with simple variable changes

## **Development**
Dependencies:
- Python < 3.10
- [Poetry](https://python-poetry.org/)

Fill out your own `.env` file using <a href="https://codeberg.org/Waifu-Tech/Moe-Bot/src/branch/master/example.ev">example.env</a> as a reference

Then simply run
```bash
poetry install
```

To install all needed dependencies


## **Deploy**
Install dependencies in <a href="#development">development</a> then on linux to run every hour and follow the instructions

```bash
crontab -e
```
then type in
```bash
0 * * * * PATH/TO/POETRY/ENV/bin/python  /PATH/TO/app.py
```
