Deck Building Card Game 
-------------------------------
[![Build Status](https://travis-ci.com/nikos912000/sd-card-game.svg?token=zU6ptnBBwDGu1jzbrQNz&branch=master)](https://travis-ci.com/nikos912000/sd-card-game)

Final version of the Deck Building Card game. 

This assignment has been completed under the "Software Development" course at the University of Edinburgh.

## LICENSE
Copyright (c) 2016 Nikos Katirtzis - All rights reserved

## Assignment Description

The objective of the coursework is to analyse and improve a prototype version of a deck building card game written in Python. Deck building games are where players are provided with a set of initial starting cards and using these they can "buy" additional cards from a shared deck to augment their own sets.

Depending on the type of game, each card defines quantities such as strength, health, wealth and the cost
to buy the card. Buying cards allows a player to improve their strength to attack their opposing players
or to increase some other quantity, like their wealth. Each player can build a deck according to their own
play style and what cards are available at each step of the game.

In the deck building game used in this coursework, each player starts with a health level. The goal is for
a player to increase their wealth and strength, by buying cards, and playing these cards to "attack" their
opponent to reduce their health. A player wins if they reduce their opponent’s health to zero.

Each card in this game has four values associated with it:
* Name - what the card is called e.g. Squire, Serf, Baker, Thug etc.
* Strength - the contribution of this card to an attack.
* Money - the contribution of this card to the available funds to buy new cards.
* Cost - how much money it costs to buy this card.

An example card is Squire:
* Name - Squire
* Strength - 1
* Money - 0
* Cost - 0

Another example card is Serf:
* Name - Serf
* Strength - 0
* Money - 1
* Cost - 0

Each player starts with a deck of 10 cards, and each player has the same starting deck of 2 Squires and 8
Serfs. These provide each player with a small amount of money and attack strength.

Between the players there lies central line of 5 cards. The remaining cards are held within a main deck.
Players can buy cards from the central line, and, if a card is bought, then it is replaced by the next card
from the main deck, if there are any cards left.

The game continues until either the central line of available cards is empty or one player is reduced to
zero or less health.

Each player has:

* Deck - where a player draws their cards from. Initially the deck is 10 cards, but they may buy
more.
* Hand - the cards (normally 5), that a player has available to play during their turn. These are drawn
from the player’s deck.
* Active Area - the cards played by the player during their turn (where players put cards into play).
The player can play 1 or more cards from their hand.
* Discard Pile - where played cards are put at the end of the player’s turn and where cards the player
has bought are also put.
When it is a player’s turn, they have the following options:
* Play one or more cards - the player puts 1 or more cards from their hand into the active area.
Money to buy more cards and attack strength to attack opponents is calculated by the sum of these
quantities on the cards in the active area for the player.
* Attack - this will attack their opponent, reducing health by the current attack strength (the sum of
the strength of cards in the active area for the player).
* Buy - buy one of more cards from the central line based on current money value (the sum of the
money on the cards in the active area for the player). Any bought card is put into the player’s
discard pile.
* End Turn - pass turn to the opponent - all the player’s cards in the active area are put into their
discard pile, and the player draws a new hand from their deck. If their deck is empty, then the
discard pile is shuffled and moved to the deck.

To attack the opponent or buy cards, a player must have cards in their active area.

As an example of a player’s turn, imagine that the central line of cards has the following cards:

* Name Caravan costing 5 with attack 1 and money 5
* Name Tailor costing 3 with attack 0 and money 4
* Name Baker costing 2 with attack 0 and money 3
* Name Baker costing 2 with attack 0 and money 3
* Name Thug costing 1 with attack 2 and money 0

Player One has a hand with 2 Squires and 3 Serfs and decides to play all of these. They move these cards
into the active area. Together, these cards give the player Attack Strength 2 and Money 3.

Player One chooses to buy the Tailor card. This card is transferred from the central line into the player’s
discard pile.

Player One then chooses to attack their opponent. Their opponent’s health is reduced by the active attack
strength of 2.

Player One now decides to end their turn. They put all the cards from the active area into their discard
pile. They then draw a new hand from their deck.
