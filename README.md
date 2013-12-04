python-pil-metaballs
====================

This is based on the code found at http://www.niksula.cs.hut.fi/~hkankaan/Homepages/metaballs.html and in fact borrows heavily from to code posted there. I've made a few modifications/improvements to fix a few issues where the rendering would lock up under certain conditions. I also converted this to use PIL/Pillow instead of pygame.

There are still bugs in the rendering and sometimes output isn't generated as the code gets stuck in a loop. I'm hoping that by posting this here others can help speed the code up and/or fix the various issues that I've run into.
