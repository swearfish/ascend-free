# Free Ascendancy

Welcome to __Free Ascendancy__ project, a free and open source re-implementation of 
an old [4X space strategy game](https://en.wikipedia.org/wiki/4X) video game from 
[The Logic Factory](https://en.wikipedia.org/wiki/The_Logic_Factory): 
[Ascendancy](https://en.wikipedia.org/wiki/Ascendancy_(video_game))

## How to make it work

1. Obtain Ascendancy game from [Abandonware sites](#ascendancy-itself)
2. Default location for game assets are ../assets (relative to ascendancy.py), 
but you may override it using [command line arguments](#command-line-arguments)
3. Copy *.COB and COB.CFG from Ascendancy directory into {ascend-dir} (../assets/cob by default)
4. Run [main.py](./ascendancy.py)
5. Enjoy

### Command line arguments

| Argument        | Description                                                   | Default         |
|-----------------|---------------------------------------------------------------|-----------------|
| --assets-dir    | Base directory for all assets                                 | ../assets       |
| --ascend-dir    | Path to Ascendancy files (*.cob)                              | ../assets/cob   |
| --cache-dir     | A writeable directory to store converted game assets          | ../assets/cache |
| --extract-all   | Extract and convert all files from COBs into cache on startup | False           | 
| --save-dir      | Path to game save files                                       | ../save         |
| --display-scale | Display scaling factor (relative to original 640x480)         | 1.5             |
| --skip-logo     | Skip the logo screen                                          | False           |
| --resume-game   | Skip main menu, immediately resume last game                  | False           |
| --nougat-lf     | Enable cheat codes                                            | False           |


## Table of contents

- [Disclaimer](./DISCLAIMER.md)
- [License agreement](./LICENSE.md)
- [House rules for wannabe contributors](./RULES.md)
- [TODO](./TODO.md)

## Introduction

### Ascendancy itself

The Logic Factory, the creator of Ascendancy is now officially dead.

Their most recent release was the iPhone version of Ascendancy which
solved lots of issues, but was never ported to other platforms: no release for iPad, macOS, Android, Windows.
Even the iPhone version is unavailable due to lack of updates and incompatibility with recent
versions of iOS.

_As of today, there is no legal way to purchase Ascendancy_. No Gog, no App Store, Steam or whatever version. 
The Logic Factory website is also down, so you can no longer download the demo version either.

> You may find the game on _abandonware_ sites, but please note: these are not official or legal sources.  
> E.g.: [My Abandonware](https://www.myabandonware.com/game/ascendancy-2qs) has a copy of the 
game, and they also offer the original user manual and a useful handbook.

### COB files, Ascendancy tools

Ascendancy as most games of its era used its own file formats.
I've used an open sourced tool from GitHub: https://github.com/daumiller/ascendancy 

### Other useful sources

* https://b-sting.nl/ascendancy/about.html
<br>A fan-made guide for Ascendancy

* https://mikefay.info/wiki/index.php?title=Game-Ascendancy
<br>A comprehensive analysis of the Ascendancy game. Very useful for understanding game mechanics without reverse engineering 

* https://github.com/btigi/iiAscendancyLib
<br>C# implementation for decoding Ascendancy files, not only game assets, but also save games.

* https://github.com/PetePete1984/godot-SpaceRace/tree/master
<br>An unfinished, yet playable reimplementation of the same game, but using Godot engine. 
A better option if you plan to modernize the game.

## Motivation

Ascendancy was a childhood favourite for me. Unfortunately I had no access to the
game itself for a long time, so I could play it once a year when we visited our
friends in northern Hungary. Maybe this limitation made the game so precious to me,
but I still play it sometimes.

The game has a beautiful atmosphere, I love the music, the graphics, and the gameplay 
in general. It's easy to get working on modern computers: since the game was designed 
to run on 486 computers in DOS, you can easily run it in DosBox not just on
any PCs, but even on a mobile phone or tablet.

However, the game can be really annoying even for a devoted fan like me.
The micromanagement makes the gameplay very repetitive,
especially when playing on bigger star maps. 

The AI is also extremely dumb, which caused the game to fail on the market.
The Logic Factory later released a patch, the so-called "Antagonizer AI", which makes
the AI play a bit more aggressive, but far from challenging. 

# Goals

1. Reimplement the game in Python using PyGame
2. Make some optional UI changes, e.g:
    - Remember the last position in lists (e.g.: buildings, ship parts) so the user won't have to scroll down every time
    - Copy existing ships in ship designer, so you won't need to start from scratch for each ship
    - Make possible to sort lists in different ways, e.g.: show the most recent buildings on top
    - Organize buildings by type in project list (similarly to ship parts)
    - Display if a planet is self-managed on the planet management screen (only visible in the list of planets)
    - List of events for each turn instead of popups
    - Display how a building or project will affect the industrial/research/fertility score of a planet
    - Display inventions for research projects
    - Display home systems for ships
    - Display estimated travel time for star lanes
3. Implement clever planetary management AI that can be used by self-managed planets and AI players
    - Add different planet roles: industrial (ship building), research, military
    - Upgrade buildings on planets
    - Use Habitats, Metroplexes instead of Outposts
    - Replace existing Outposts when possible
    - Automate buildings when possible
4. Implement a more challenging AI
    - Scrap or refit obsolete ships
    - Build fleet, don't send ships one by one
    - Better balance between ship building and planetary development
    - Don't use special abilities against yourself (e.g.: block your exit from your home system)
    - Use diplomacy with/against player and other AI controlled empires
    - Escape from battles before losing valuable ships
5. Gameplay changes (optional)
    - Share food capacities across planets
    - Make late game with lots of controlled systems less frustrating
      - Share industrial resources between planets (require research and special buildings)
      - Build artificial star lanes, star gates
      - Research jump drive (immediate jump to any known star system)
6. Use deep learning for AI

## Why Python?

Why not? I wrote dozens of games (indie and commercial) in C++ using own, licensed
or open source game engines. I don't want to learn a new technology now. I want
the same fun I had as teenage programmer: just open an IDE, start writing code,
have fast build, run, fail and fix rounds, like in Turbo Pascal.

