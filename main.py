from PIL import Image, ImageDraw, ImageFont
import cv2
import textwrap
import os

def CreateImage(text, font, index=0, image_size=(1920, 1080), bg_color=(255, 255, 255), fontColor=(0, 0, 0), saveLocation="./Lib/tmp"):
    fontSize = font.size
    # text treatment
    text = textwrap.wrap(text, width=fontSize)
    # drawing text on image
    MAX_W, MAX_H = image_size
    img = Image.new('RGB', image_size, bg_color)
    draw = ImageDraw.Draw(img)
    # drawing lines in text with padding
    current_h, pad = MAX_H/2 - ((len(text)*fontSize/2)), 10
    for line in text:
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, current_h), line,
                  font=font, fill=fontColor, encoding="UTF")
        current_h += h + pad
    # saving image
    path = f"{saveLocation}/{index}.png"
    img.save(path)
    return path

def getFileContent(fileName):
    try:
        file = open(fileName, 'r')
        lines = file.read().split('\n')
        return lines
    except Exception as e:
        print(e)

def createVideoFrames(images, fps=30, duration_per_frame=3):
    img_array = []
    for filename in images:
        img = cv2.imread(filename)
        for i in range(fps*duration_per_frame):
            img_array.append(img)
    return img_array

def saveFramesToVideo(frames, dimensions, outputFile, fps=30):
    try:
        video = cv2.VideoWriter(
            outputFile, cv2.VideoWriter_fourcc(*'DIVX'), fps, dimensions)
        for frame in frames:
            video.write(frame)
        video.release()

    except Exception as e:
        print(e)

def removeTempFiles(files):
    for file in files:
        os.unlink(file)

if __name__ == "__main__":
    # create images from text
    dimensions = (1920, 1080)
    framesPerSec = 10
    fontSize = 50
    font = ImageFont.truetype('./Lib/Urbanist.ttf', fontSize)
    sentences = getFileContent("text.txt")
    images = []
    for idx, sentence in enumerate(sentences):
        imagePath = CreateImage(
            sentence, font, idx+1, image_size=dimensions)
        images.append(imagePath)
    # read all images
    frames = createVideoFrames(images, fps=framesPerSec, duration_per_frame=2)
    saveFramesToVideo(frames, dimensions, "output.avi", fps=framesPerSec)
    removeTempFiles(images)
