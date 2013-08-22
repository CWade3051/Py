# Big Score
# Demonstrates displaying text on a graphics screen

from livewires import games, color

games.init(screen_width = 640, screen_height = 480, fps = 50)

wall_image = games.load_image("wall.jpg", transparent = False)
games.screen.background = wall_image

score = games.Text(value = 1756521,
                   size = 60,
                   color = color.black,
                   x = 550,
                   y = 30)
games.screen.add(score)

games.screen.mainloop()
