# ascend-free

A free and open source re-implementation of 
an old [4X space strategy game](https://en.wikipedia.org/wiki/4X) video game from 
[The Logic Factory](https://en.wikipedia.org/wiki/The_Logic_Factory): 
[Ascendancy](https://en.wikipedia.org/wiki/Ascendancy_(video_game))

## Starters

### Ascendancy itself

Unfortunately, The Logic Factory is now finally dead. 
Their website promised Ascendancy 2 
for decades, but they only released an iOS version of Ascendancy since. 
The website is down and Ascendancy is not available for purchase anymore.

[My Abandonware](https://www.myabandonware.com/game/ascendancy-2qs) has a copy of the 
game, and they also offer the original user manual and a useful handbook.

### COB files, Ascendancy tools

Ascendancy as most games of its era used its own file formats.
I've used an open sourced tool from GitHub: https://github.com/daumiller/ascendancy 

## Motivation

Ascendancy was a childhood favourite for me. Unfortunately I had no access to the
game itself for a long time, so I could play it once a year when we visited our
friends in northern Hungary. Maybe this limitation made the game so precious to me,
but I still play it sometimes.

The game has a beautiful atmosphere, I love the music, the graphics, and the gameplay 
in general. It's easy to get working on modern computers: since the game was designed 
to run on 486 computers in DOS, you can easily run it nowdays in DosBox not just on
any PCs, but even on a mobile phone or tablet.

However, the game can be really annoying even for a devoted fan like me.
T he micromanagement makes the gameplay very repetitive,
especially when playing on bigger star maps. 

The AI is also extremely dumb, which caused the game to fail on the market.
The Logic Factory later released a patch, the so-called "Antagonizer AI", which makes
the AI play a bit mode aggressive, but far from challenging. 

# Goals

1. Reimplement the game in Python using PyGame
2. Make some optional UI changes, e.g:
    - Remember the last position in lists (e.g.: buildings, ship parts) so the user won't have to scroll down every time
    - Copy existing ships in ship designer, so you won't need to start from scratch for each ship
    - Make possible to sort lists in different ways, e.g.: show the most recent buildings on top
    - Organize buildings by type in project list (similarly to ship parts)
    - Display if a planet if self managed on the planet management screen (only visible in the list of planets)
    - List of events for each turn instead of popups
    - Display how a building or project will affect the industrial/research/fertility score of a planet
    - Display inventions for research projects
    - Display home systems for ships
    - Display estimated travel time for star lanes
3. Implement clever planetary management AI that can be used by self managed planets and AI players
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

