title: "Monopoly Money"
date: 2020-04-18
category: Projects
tags: [react, typescript, javascript, express, lerna]
feature: feature.png
description: "A Node.js server and React frontend that helps you manage your finances in a game of Monopoly from the browser."
github: brentvollebregt/monopoly-money

<div align="center" style="padding: 20px 20px 40px 20px">
    <img src="/posts/monopoly-money/banner.png" alt="Monopoly Money Banner" style="margin-bottom: 10px;">
    <p class="text-center">Manage your finances in a game of Monopoly from the browser.</p>
    <a href="https://monopoly-money.nitratine.net/"><button class="btn btn-outline-secondary" type="button">🌐 Visit monopoly-money.nitratine.net →</button></a>
</div>

Monopoly Money is a webapp designed for mobile that allows multiple players to track their balances collectively in a game of monopoly and transfer money from one another.

## How Can This Help You?

If you have every played the credit card edition of Monopoly, you will appreciate how much faster the game moves without having to count cash. This webapp substitutes the need for cash in a game of monopoly for a mobile-banking-like solution where players can easily send each other virtual currency.

Using this method for finance management also allows you to keep a full history of your game and have clarity over every movement.

## Usage

To start using the webapp, follow the basic following steps:

- Get all participants to go to [monopoly-money.nitratine.net](https://monopoly-money.nitratine.net/) in a browser of their choosing.
- Whoever is the banker should select "New Game" to create a new game after providing their name.
- All other participants should then selected "Join Game" and using the game id provided by the banker and their name, join the game.

When everyone is in the game, the banker can then close the game to stop others joining and then start distributing out the initial balances.

## Features

- Multiple games can be hosted on the server at once
- Each player uses their own device; everyone joins one game.
- Send money between players quickly
- The person that created the game is the banker. This person can:
    - Give money to players from the bank (and take money)
    - Give free parking to players
    - Update player names
    - Delete players
    - Stop new people from joining the game
    - End the game completely
- History is recorded of each game event that can be viewed by all players
