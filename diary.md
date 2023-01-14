# 2023

## January

### 14

Had some experimentation with pyglet, which supposed to be faster 
and more advanced than pygame.
It was promising, e.g.: already have a comprehensive GUI system that I need
to implement atop of pygame.

However, pyglet proven to be very immature. It took me two days to get a simple
logo screen running. I did the same in a few hours in PyGame. The code is missing
any type hints which makes it less convenient to use with modern IDEs.

It also heavily relies on OpenGL which is practically deprecated on most 
systems.

I reverted most of the changes, but now I have a basic dependency inversion 
system.

