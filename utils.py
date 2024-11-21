import os
import time
from PIL import Image
from psd_tools import PSDImage
from psd_tools.api.layers import Layer, PixelLayer, Group
from psd_tools.constants import Compression, BlendMode


def parse_file(psdFile, pngFile, parseOutFolder):
    psd = PSDImage.open(psdFile)
    psd.composite().save(pngFile)  # save in a png file
    bboxAll = []
    lefttop = []
    layerNameAll = []
    for layer in psd:
        bboxAll.append(layer.bbox) # Get the (left, top, right, bottom) position of a layer
        bbox = layer.bbox
        lefttop.append(bbox[:2])
        #layerNameAll.append(os.path.join(parseOutFolder, layer.name + '.png')) # layer name is also the PNG image name
        layerNameAll.append(layer.name + '.png')  # layer name is also the PNG image name .png
        layer_image = layer.composite()
        layer_image.save(os.path.join(parseOutFolder,'%s.png') % layer.name) # .png
        time.sleep(1)
    return bboxAll, layerNameAll, lefttop

def load_images(imgPath, files):
    images = []
    for file in files:
        image = Image.open(os.path.join(imgPath, file)).convert('RGBA')
        images.append({'pil_image':image, 'name':file.split('.')[0]})
    return images

def images_to_layers(psd, images, lefttop):
    for i in range(0, len(images)):
        image = images[i]
        psd.append(PixelLayer.frompil(image['pil_image'], psd, image['name'], lefttop[i][1], lefttop[i][0], Compression.RLE))
    return psd

def set_opacity_blend_mode(psd):
    for layer in psd[1:]:
        layer.opacity = 128
        layer.blend_mode = BlendMode.DARKEN
    return psd

def image_to_psd(image_obj: Image, save_path):
    # Convert an image to RGBA
    if image_obj.mode != "RGBA":
        image_obj = image_obj.convert("RGBA")

    # Create a new PSD document from PIL Image
    psd = PSDImage.frompil(image_obj)

    # Creates a PixelLayer from a PIL image for a given psd file.
    pixel_layer = PixelLayer.frompil(image_obj, psd)
    pixel_layer.visible = True  # Set a layer to be visible

    psd.append(pixel_layer)  # Add a layer to the psd file
    psd.save(save_path)  # Save the psd file
