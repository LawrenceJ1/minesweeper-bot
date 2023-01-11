# minesweeper-bot
https://user-images.githubusercontent.com/89532734/211936261-89066b0c-d771-4222-94ee-4fe4d1925379.mp4

## Introduction

This is still currently a work in progress.  
The minesweeper-bot is able to play a game of minesweeper on minesweeperonline.com and win with decent speed.  
This bot currently only works on monitors with resolution 1920x1080, and settings of zoom 200% for minesweeperonline.com.  
Please ensure that minesweeperonline.com is open on your primary monitor.  

## Running the program

1. Clone the repository  
`git clone https://github.com/LawrenceJ1/minesweeper-bot.git`  
  
2. Install the necessary requirements.  
`pip install -r requirements.txt`  
  
3. Run the main script with minesweeperonline.com open on your primary monitor.  
`python main.py`  
  
## WIP

Currently the bot isn't the smartest. It can't look multiple moves into the future, which makes it pretty weak. It can still win games on beginner and intermediate, but it frequently gets stuck on expert. There is also a bug with the number detection, as sometimes the number 4 is processed as 8.
