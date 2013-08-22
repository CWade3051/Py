# Slippery Pizza Program
# Demonstrates testing for sprite collisions

from livewires import games
import random

games.init(screen_width = 640, screen_height = 480, fps = 50)


class Pan(games.Sprite):
    """" A pan controlled by the mouse. """
    def update(self):
        """ Move to mouse position. """
        self.x = games.mouse.x
        self.y = games.mouse.y
        self.check_collide()
 
    def check_collide(self):
        """ Check for collision with pizza. """
        for pizza in self.overlapping_sprites:
            pizza.handle_collide()


class Pizza(games.Sprite):
    """" A slippery pizza. """
    def handle_collide(self):
        """ Move to a random screen location. """
        self.x = random.randrange(games.screen.width)
        self.y = random.randrange(games.screen.height)


def main():
    wall_image = games.load_image("wall.jpg", transparent = False)
    games.screen.background = wall_image

    pizza_image = games.load_image("pizza.bmp")
    pizza_x = random.randrange(games.screen.width)
    pizza_y = random.randrange(games.screen.height)
    the_pizza = Pizza(image = pizza_image, x = pizza_x, y = pizza_y)
    games.screen.add(the_pizza)

    pan_image = games.load_image("pan.bmp")
    the_pan = Pan(image = pan_image,
                  x = games.mouse.x,
                  y = games.mouse.y)
    games.screen.add(the_pan)

    games.mouse.is_visible = False

    games.screen.event_grab = True

    games.screen.mainloop()

# kick it off!
main()
