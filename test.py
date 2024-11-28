import pyscreenshot as ImageGrab

# fullscreen
im=ImageGrab.grab()
im.show()

# part of the screen
im=ImageGrab.grab(bbox=(10,10,500,500))
im.show()

# to file
im.save('/media/archiv/im.png')
