# Pizza Sprite
# Demonstrates creating a sprite 

from livewires import games

games.init(screen_width = 640, screen_height = 480, fps = 50)

wall_image = games.load_image("wall.jpg", transparent = False)
games.screen.background = wall_image

pizza_image = games.load_image("pizza.bmp")
pizza = games.Sprite(image = pizza_image, x = 320, y = 240)
games.screen.add(pizza)

games.screen.mainloop()
