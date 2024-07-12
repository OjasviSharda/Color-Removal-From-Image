from PIL import Image


def remove_color_from_image(input_image_path, output_image_path, target_color):
    # Open the image
    image = Image.open(input_image_path)

    # Modify and correct the target_color
    target_color = tuple(map(lambda x: x, target_color))

    # Get the image data as a list of pixels
    pixel_data = list(image.getdata())

    # Create a new list to store the modified pixel data
    modified_pixel_data = []

    # Iterate through the pixel data and remove the target color
    for pixel in pixel_data:
        pixel_color = tuple(map(lambda x: x, pixel[:3]))
        modified_pixel = []
        for p_color, t_color in zip(pixel_color, target_color):
            val = p_color - t_color
            if val > 255:
                val = 255
            elif val < 0:
                val = 0
            modified_pixel.append(val)

        modified_pixel_data.append(tuple(modified_pixel))

    # Create a new image with the modified pixel data
    modified_image = Image.new(image.mode, image.size)
    modified_image.putdata(modified_pixel_data)

    # Save the modified image to the specified output path
    modified_image.save(output_image_path)

    # Close the images
    image.close()
    modified_image.close()


# Example usage:
input_image_path = 'input_image.jpg'  # Replace with the path to your input image
output_image_path = 'output_image.png'  # Replace with the desired output path
target_color = (0, 0, 255)  # Replace with the RGB color you want to remove

remove_color_from_image(input_image_path, output_image_path, target_color)