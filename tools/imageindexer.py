#Initial image sorter, once images are sorted an updater will be made
import os
import sys
import json
from pillow_heif import register_heif_opener
from PIL import Image, ImageOps

IMAGE_FORMATS = [".jpg", ".png", ".heic"]
VIDEO_FORMATS = [".mov", ".mkv", ".mp4"]

register_heif_opener()

def format_all(path):
    for dir in os.listdir(path):
        img_n = 0
        vid_n = 0
        filelist = os.listdir(path + dir)

        #Check if images dir exists
        if (os.path.exists(path + dir + "/images")):
            img_n = len(os.listdir(path + dir + "/images"))
            filelist.pop(filelist.index("images"))
        else:
            os.mkdir(path + dir + "/images")

        #Check if videos dir exists
        if (os.path.exists(path + dir + "/videos")):
            vid_n = len(os.listdir(path + dir + "/videos"))
            filelist.pop(filelist.index("videos"))
        else:
            os.mkdir(path + dir + "/videos")

        for file in filelist:
            print("Processing: " + file)
            f, e = os.path.splitext(file)
            ifile = path + dir + "/" + file

            if (e.lower() in IMAGE_FORMATS):
                ofile = path + dir + "/images/" + str(img_n) + ".jpg"
                img_n += 1
                ImageOps.exif_transpose(Image.open(ifile)).convert('RGB').save(ofile)
                os.remove(ifile)

            elif (e.lower() in VIDEO_FORMATS):
                ofile = path + dir + "/videos/" + str(vid_n) + e
                vid_n += 1
                os.rename(ifile, ofile)

            elif (e.lower() == ".json"):
                pass

            else: 
                print("nil")
                pass

        #Update properties.json
        with open(path + dir + "/properties.json", 'w') as wfile:
            data = {
                "image_n" : img_n,
                "video_n" : vid_n,
            }
            json.dump(data, wfile, indent = 2)
            wfile.close()

    return

def format_single(path):
    img_n = 0
    vid_n = 0
    filelist = os.listdir(path)

    #Check if images dir exists
    if (os.path.exists(path + "images")):
        img_n = len(os.listdir(path + "images"))
        filelist.pop(filelist.index("images"))
    else:
        os.mkdir(path + "images")

    #Check if videos dir exists
    if (os.path.exists(path + "videos")):
        vid_n = len(os.listdir(path + "videos"))
        filelist.pop(filelist.index("videos"))
    else:
        os.mkdir(path + "videos")

    #Process images and videos
    for file in filelist:
        print("Processing: " + file)
        f, e = os.path.splitext(file)
        ifile = path + file

        if (e.lower() in IMAGE_FORMATS):
            ofile = path + "images/" + str(img_n) + ".jpg"
            img_n += 1
            ImageOps.exif_transpose(Image.open(ifile)).convert('RGB').save(ofile)
            os.remove(ifile)

        elif (e.lower() in VIDEO_FORMATS):
            ofile = path + "videos/" + str(vid_n) + e
            vid_n += 1
            os.rename(ifile, ofile)

        elif (e.lower() == ".json"):
            pass

        else: 
            print("Nil")
            pass

    #Update properties.json
    with open(path + "/properties.json", 'w') as wfile:
        data = {
            "image_n" : img_n,
            "video_n" : vid_n,
        }
        json.dump(data, wfile, indent = 2)
        wfile.close()

    return


if __name__ == "__main__":
    #check if args are valid
    n = len(sys.argv)
    modes = ["-s", "-m"]
    if ((n != 3) or (sys.argv[1] not in modes) or not (os.path.exists(sys.argv[2]))):
        print(
                '''
                Invalid arguments!
                USAGE: imageindexer -smuz [PATH TO CONTENT DIRECTORY]
                        -s: single directory)
                        -m: all directories within a directory
                '''
                )
        exit()

    match sys.argv[1]:
        case "-s":
            format_single(sys.argv[2])
        case "-m":
            format_all(sys.argv[2])
        
    #run based on different modes

     




