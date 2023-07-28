import random
import os
import json

#gets an n amount of random images from specified dir
def get_images_random(dir: str, amount: int):
    #Check if amount is in bounds
    if (amount < 1):
        return "INVALID_AMT"

    #Check if there are enough images
    n = 0
    with open(dir + "properties.json", "r") as file:
        n = json.loads(file.read())["image_n"]
        file.close()
    if (amount > n): 
        return "AMT_TOO_LARGE"

    #Generate list of paths to images
    paths = random.sample(range(0, n), amount)
    for i in range(len(paths)):
        paths[i] = dir + "images/" + str(paths[i]) + ".png"

    return paths

#gets an n amount of images from a specified dir 
def get_images_seq(dir: str, amount: int):
    #Check if amount is in bounds
    if (amount < 1):
        return "INVALID_AMT"

    #Check if there are enough images
    n = 0
    with open(dir + "properties.json", "r") as file:
        n = json.loads(file.read())["image_n"]
        file.close()
    if (amount > n): 
        return "AMT_TOO_LARGE"

    #generate list of paths to images
    paths = []
    for i in range(amount):
        paths[i] = dir + "images/" + str(i) + ".png"

    return paths

#Gets amount of images in dir
def get_image_n(dir: str):
    n = 0
    with open(dir + "properties.json", "r") as file:
        n = json.loads(file.read())["image_n"]
        file.close()
    return n

#Get random photo directory
def get_random_dir(dir: str):
    dirlist = os.listdir(dir)
    return (dir + dirlist[random.randint(0, len(dirlist)-1)] + "/")
    

