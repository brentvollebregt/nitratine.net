---
layout: post
title: "Monopoly Money"
date: 2017-12-21
categories: Projects
tags: Python Flask
---

* content
{:toc}

A web app that allows players to keep track of their Monopoly balances securely in an internet banking like system. The server is built in Flask which can support unlimited games on one server. Each game has one banker amd can have as many players as needed.

[Find the project on GitHub here](https://github.com/brentvollebregt/monopoly-money)

## What is this?
This project is a substitution for cash/credit cards in the game of Monopoly. A banker creates a game on the server and players then join. The banker can spawn in money and pass it to other players. Players can send money to each other, see how much money is in free parking, see their own amount and see all events that occur (money passed). All events are shown to all players to stop cheating as everyone will know where money goes.

## Demonstration and Screenshots
![Player type selection screen](/images/monopoly-money-game1.png)
![Pin input screen](/images/monopoly-money-game2.png)
![Banker screen](/images/monopoly-money-game3.png)
![Player screen](/images/monopoly-money-game4.png)

<!-- more -->

## Installation and Setup
1. Install Python
2. Install Flask (pip install Flask)
3. Download or clone the repository at [https://github.com/brentvollebregt/monopoly-money](https://github.com/brentvollebregt/monopoly-money)
4. Visit address displayed
5. Choose if you are the banker or another player and supply your name
6. If you are a player, enter the pin supplied by your banker

## Usage
After the server has been started, the player who is going to be the banker can visit the address displayed on the console, enter their name and click banker.

By clicking on the bank icon in the top left side, the banker can switch between the bank and their account.

For other players, go to the address displayed, enter your name and click player. This will now ask for a pin, this can be received from the banker.

When all players have joined the game, the banker can lock the game by going to the banking screen and clicking the button on the bottom left. This will make sure no one else can join the game. This can be clicked again to open the game back up to more players.

The banker can now give money to everyone and play the game as it normally would be played.

Players can send money by selecting what player they want to send money to, changing the amount and clicking go.

The top of the banker screen allows the banker to send money to a player. Under that allows the banker to send free parking to a particular player. Under than the banker can manage players. Next the banker can set a players balance and finally the "Who starts first?" button will select a player at random and display their name. The "Open/Close" button manages if the game is open or closes to more players and the "End" button will end the game.

## Features
### Server
- Games that generate when a player makes themself a banker
- Free parking
- Log that says what has happened (Shows all money values in K)

### Players
- Easily join a game using a pin
- Auto refresh in the background (still manual button in /play/ if its too slow)
- Self chosen names (can be changed by banker)
- Simple to send money to players/bank/free parking
- Clicking on amounts with 'M' or 'k' will switch them.

### Banker
- Banker can edit player names and remove people
- Ask who starts first (random selection of current players)
- Can set players balances
- Lock the game so no one else can come in while you are in the middle of a game
- End game easily
