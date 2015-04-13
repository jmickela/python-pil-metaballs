python-pil-metaballs
====================

This is based on the code found at http://www.niksula.cs.hut.fi/~hkankaan/Homepages/metaballs.html and in fact borrows heavily from to code posted there. I've made a few modifications/improvements to fix a few issues where the rendering would lock up under certain conditions. I also converted this to use PIL/Pillow instead of pygame.

There are still bugs in the rendering and sometimes output isn't generated as the code gets stuck in a loop. I'm hoping that by posting this here others can help speed the code up and/or fix the various issues that I've run into.

Example Usage
===============
Here's an example usage with five balls. With these values four should be connected together, one should be on its own. You can play with the goo and threshold values a bit, but small changes in those values cause large changes in the image. Smaller goo values cause the balls to merge more, which I suppose is counterintuitive. You'll probably want to leave the threshold as it is and mess with goo to adjust how the balls are drawn, very small changes in threshold cause large changes in the drawn metaballs.

```python
from PIL import Image, ImageDraw
from metaballs import MetaBallManager, Ball

WIDTH = 640
HEIGHT = 480

balls = []
size = (WIDTH, HEIGHT)
RADUIS = 3
STEP_SIZE = 1

GOO = 3.0
THRESHOLD = 0.004

image = Image.new('RGBA', size)

balls.append(Ball(100, 100, RADUIS))
balls.append(Ball(110, 110, RADUIS))
balls.append(Ball(130, 130, 6*RADUIS))
balls.append(Ball(150, 130, 16*RADUIS))
balls.append(Ball(180, 180, RADUIS))

manager = MetaBallManager(balls, GOO, THRESHOLD, (255, 0, 0), image, WIDTH*HEIGHT)

manager.DrawBalls(manager.rungeKutta2, STEP_SIZE)
image.save("image.png", "PNG")
```

Known Issues
===========================
In the above example, if you set goo to 2, the entire image will be painted red. This is because the algorithm often produces balls that aren't completely closed, so when floodfill is called to fill in the ball it fills the whole image. I don't have time to fix this right now and am no longer working on the project that I was going to use this for, so I likely wont get to this again. If you encounter this problem, mess with the goo or threshold values, change your step size, or use one of the other algorithms for tracing the ball.
