import os
from PIL import Image
from psd_tools import PSDImage
from utils import load_images, images_to_layers, image_to_psd, parse_file

if __name__ == "__main__":
    psd_File = "./sample_input.psd" # psd file will be parsed
    psdOutPath = './output_parse' # Folder for saving layers extracted from the psd file
    isExistParse = os.path.exists(psdOutPath)
    if not isExistParse:
        os.mkdir(psdOutPath)

    # Parse the psd file into layers and save them in png files
    print('Parse a PSD file: ', psd_File)
    png_File = os.path.join(psdOutPath, "png_out.png")
    bbox_All, imgName_All, lefttop_All = parse_file(psd_File, png_File, psdOutPath)

    ##########
    # Create a psd file from multiple images (extracted from the original PSD file)
    # This can be seen as the reverse process of the psd parsing one
    outputPSD = './created_output.psd'
    outputPNG = './created_output.png'
    print('Create a PSD file from images from: ', psdOutPath)
    # Convert an image to a psd file and use it as a background layer
    img = imgName_All[0] # use the first image (of the list of the extracted images) to create the background layer
    image_obj = Image.open(os.path.join(psdOutPath, imgName_All[0]))
    image_to_psd(image_obj, outputPSD) # Convert the image to an PSD file

    # Add images to layers in the psd file
    psd = PSDImage.open(outputPSD)
    images = load_images(psdOutPath, imgName_All[1:])
    psd = images_to_layers(psd, images, lefttop_All[1:])
    #psd = set_opacity_blend_mode(psd)

    psd.save(outputPSD)
    merged_image = psd.composite()
    merged_image.convert('RGB').save(outputPNG, 'PNG')
