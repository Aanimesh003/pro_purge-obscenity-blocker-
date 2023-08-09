from PIL import Image as pil_image

with pil_image.open("pic.png") as im:
    width, height = im.size
    quarters = [(0, 0, width / 2, height / 2), (width / 2, 0, width, height / 2), (0, height / 2, width / 2, height), (width / 2, height / 2, width, height)]

    # Looping over the quarters
    for i, q in enumerate(quarters):
        # Cropping the image
        im_crop = im.crop(q)

        # Saving the cropped image to a file
        im_crop.save(f"image_{i+1}.png")
