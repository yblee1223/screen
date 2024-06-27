from PIL import ImageGrab

screeb = ImageGrab.grab()

screeb.save("screenshot.png")

screeb.show()

screeb.close()