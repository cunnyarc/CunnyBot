<h1 align="center">
    <img src="./assets/Logo.png">
</h1>
<h4 align="center">A Reddit to Discord/Twitter bot</h4>
<h1 align="center">
    <a href="https://liberapay.com/GlitchyChan/donate">
        <img src="https://img.shields.io/badge/Liberapay-F6C915?style=for-the-badge&logo=liberapay&logoColor=black" alt="liberapay" />
    </a>
    <a href="https://discord.gg/ZxbYHEh">
        <img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=fff&style=for-the-badge" alt="Discord" />
    </a>
    <a href="https://twitter.com/cutemoebot">
        <img src="https://img.shields.io/badge/twitter-%2300acee?&style=for-the-badge&logo=twitter&logoColor=white" alt="twitter" />
    </a>
</h1>

<p align="center">
    <a href="#about">About</a> •
    <a href="#features">Features</a> •
    <a href="#development">Development</a> •
    <a href="#deploy">Deploy</a>
</p>

## **About**
This bot that takes a random subreddit from <a href="https://codeberg.org/Waifu-Tech/Moe-Bot/src/branch/master/subreddits.txt">subreddits.txt</a> takes a random post and then posts the image to Discord and Twitter

## **Features**
- ✅ Fully Async
- ✅ Proper Logging for any errors
- ✅ Easily Extendable with more Subreddits

## **Development**
Dependencies:
- Python < 3.10
- [Yarn](https://yarnpkg.com/)

Fill out your own `.env` file using <a href="https://codeberg.org/Waifu-Tech/Moe-Bot/src/branch/master/example.ev">example.env</a> as a reference

Then simply run
```bash
poetry install
```


## **Deploy**
Install dependencies in <a href="#development">development</a> then on linux to run every hour and follow the instructions

```bash
crontab -e
```
then type in 
```bash
0 * * * * PATH/TO/POETRY/ENV/bin/python  /PATH/TO/app.py
```
