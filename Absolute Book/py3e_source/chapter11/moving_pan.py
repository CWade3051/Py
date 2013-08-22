# Moving Pan
# Demonstrates mouse input

from livewires import games

games.init(screen_width = 640, screen_height = 480, fps = 50)

class Pan(games.Sprite):
    """" A pan controlled by the mouse. """
    def update(self):
        """ Move to mouse coordinates. """
        self.x = games.mouse.x
        self.y = games.mouse.y

def main():
    wall_image = games.load_image("wall.jpg", transparent = False)
    games.screen.background = wall_image

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
