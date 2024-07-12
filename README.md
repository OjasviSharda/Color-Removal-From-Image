# Remove particular color from an image in Python
A package that can be used to remove particular color from an image in Python.

## Setup
***
#### _Installing the base package_
    /Note:/ Better to use GUI as it uses openCV which is majorly supported. 

<br/>

> ###### RAW CODE ONLY : _(ColorRemoval.py)_
> `python -m pip install --upgrade Pillow`<br>

> ###### GUI ONLY : _(GUI.py)_
> `pip install opencv-python`<br>
> `pip install PySimpleGUI`
>
> _Run 'GUI.py' directly._

## How to use
***

### ColorRemoval.py

```python
import ColorRemoval

input_image_path = 'input_image.jpg'  # Replace with the path to your input image
output_image_path = 'output_image.png'  # Replace with the desired output path
target_color = (255, 0, 0)  # Replace with the RGB color you want to remove

ColorRemoval.remove_color_from_image(input_image_path, output_image_path, target_color)
```
