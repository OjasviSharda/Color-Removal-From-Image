import PySimpleGUI as sg
import cv2
import colorsys

import numpy as np

sg.theme('GreenTan')
layout_color_operations = [
    [sg.Text("R:"), sg.Input(key='-R-', p=0, default_text=0, size=6, enable_events=True), ],
    [sg.Text("G:"), sg.Input(key='-G-', p=0, default_text=0, size=6, enable_events=True), ],
    [sg.Text("B:"), sg.Input(key='-B-', p=0, default_text=0, size=6, enable_events=True)],
]
layout_color_filter_l = [
    [sg.Text("R:", size=2), sg.Input(key='-l_R-', p=0, default_text=0, size=3, enable_events=True), ],
    [sg.Text("G:", size=2), sg.Input(key='-l_G-', p=0, default_text=0, size=3, enable_events=True), ],
    [sg.Text("B:", size=2), sg.Input(key='-l_B-', p=0, default_text=0, size=3, enable_events=True)],
]
layout_color_filter_r = [
    [sg.Text("R:", size=2), sg.Input(key='-r_R-', p=0, default_text=255, size=3, enable_events=True), ],
    [sg.Text("G:", size=2), sg.Input(key='-r_G-', p=0, default_text=255, size=3, enable_events=True), ],
    [sg.Text("B:", size=2), sg.Input(key='-r_B-', p=0, default_text=255, size=3, enable_events=True)],
]
layout_l = [
    [sg.Frame('Grayscale', layout=[
        [sg.Radio('Yes', "isGrey", default=False, size=(5, 1), k='-GREYSCALE-', enable_events=True),
         sg.Radio('No', "isGrey", default=True, size=(5, 1), k='-!GREYSCALE-', enable_events=True)],
    ], s=(150, 54))],
    [sg.Frame('Add/Sub Color', layout=[[
        sg.Col([
            [sg.Radio('ADD', "isColor", default=False, k='-ADD-', enable_events=True), ],
            [sg.Radio('SUB', "isColor", default=True, k='-SUB-', enable_events=True), ],
        ]),
        sg.Col(layout_color_operations)
    ]], s=(150, 100), element_justification='c')],
    [sg.Frame('Filter Color', layout=[
        [sg.Col(layout_color_filter_l),
         sg.Col(layout_color_filter_r), ],
    ], s=(150, 100), element_justification='c')],
    [sg.Frame('Convolutions', layout=[
        [sg.Frame('Blurring', layout=[
            [sg.Slider(key='-BLUR-', range=(0, 25), orientation='h', s=(15, 10), enable_events=True)],
        ])],
        [sg.Frame('Sharpening', layout=[
            [sg.Slider(key='-SHARPEN-', range=(0, 10), orientation='h', s=(15, 10), enable_events=True)],
        ])],
    ], s=(150, 150), element_justification='c')],
]
layout = [
    [sg.Button('Upload Image', p=10, s=20), sg.Push(), sg.Button("Save", p=10, s=10)],
    [sg.Col(layout_l, p=10), sg.Image(key='image', size=(10, 10))],
]

window = sg.Window('Basic Image Tools with OpenCV', layout, size=(720, 500), resizable=True, finalize=True)
# default_element_size=(12, 1),
image_path = None
image_file = None
SUPPORTED_IMAGE_TYPES = (".jpg", ".jpeg", ".jpe", ".bmp", ".png", ".webp")
event_handler = ["_IMG"]

while True:
    event, values = window.read()
    print(event, values)
    print("Events: ", event_handler)

    # ---------------
    # REGISTER EVENTS
    # ---------------

    if event == sg.WIN_CLOSED:  # always,  always give a way out!
        break

    elif event == "Upload Image":
        print("[LOG] Clicked Open File!")
        image_path = file_loc = sg.popup_get_file('Choose your file', keep_on_top=True)
        print("[LOG] User chose file: " + str(file_loc))

    elif event == "Save":
        print("[LOG] Clicked Save File!")
        folder_loc = sg.popup_get_folder('Choose your folder', keep_on_top=True)
        print("[LOG] User chose folder: " + str(folder_loc))
        file_name = sg.popup_get_text('Enter file name', keep_on_top=True)
        if file_name and file_name.lower().endswith(SUPPORTED_IMAGE_TYPES):
            status = cv2.imwrite(str(folder_loc)+"/"+str(file_name), image_file)
            print(status)
            print(f"[LOG] Saved fileName: {str(file_name)} at {str(folder_loc)}")
        else:
            print("Invalid File Name !")

    elif event in ["-R-", "-G-", "-B-"]:
        try:
            R = max(0, min(int(values["-R-"]), 255))
            B = max(0, min(int(values["-B-"]), 255))
            G = max(0, min(int(values["-G-"]), 255))
            if ((R, G, B) != (0, 0, 0)) and "COLOR" not in event_handler:
                event_handler.append("COLOR")
            elif (R, G, B) == (0, 0, 0):
                event_handler.remove("COLOR")
        except ValueError:
            pass

    elif event in ["-l_R-", "-l_G-", "-l_B-", "-r_R-", "-r_G-", "-r_B-"]:
        try:
            l_R = max(0, min(int(values["-l_R-"]), 255))
            l_G = max(0, min(int(values["-l_G-"]), 255))
            l_B = max(0, min(int(values["-l_B-"]), 255))
            r_R = max(0, min(int(values["-r_R-"]), 255))
            r_G = max(0, min(int(values["-r_G-"]), 255))
            r_B = max(0, min(int(values["-r_B-"]), 255))
            if ((l_R, l_G, l_B, r_R, r_B, r_G) != (0, 0, 0, 255, 255, 255)) and "FILTER_COLOR" not in event_handler:
                event_handler.append("FILTER_COLOR")
            elif (l_R, l_G, l_B, r_R, r_B, r_G) == (0, 0, 0, 255, 255, 255):
                event_handler.remove("FILTER_COLOR")
        except ValueError:
            pass

    elif event == "-BLUR-":
        if "BLUR" not in event_handler and values["-BLUR-"] != 0:
            event_handler.append("BLUR")
        elif values["-BLUR-"] == 0:
            event_handler.remove("BLUR")

    elif event == "-SHARPEN-":
        if "SHARPEN" not in event_handler and values["-SHARPEN-"] != 0:
            event_handler.append("SHARPEN")
        elif values["-SHARPEN-"] == 0:
            event_handler.remove("SHARPEN")

    elif event == "-GREYSCALE-" and "GREY" not in event_handler:
        event_handler.append("GREY")
    elif event == "-!GREYSCALE-" and "GREY" in event_handler:
        event_handler.remove("GREY")

    # -------------
    # HANDLE EVENTS
    # -------------

    try:
        if image_path:
            image_file = cv2.imread(image_path)
            for ev in event_handler:

                # ADD or SUB Colors
                if ev == "COLOR":
                    R = max(0, min(int(values["-R-"]), 255))
                    B = max(0, min(int(values["-B-"]), 255))
                    G = max(0, min(int(values["-G-"]), 255))

                    img_B, img_G, img_R = cv2.split(image_file)

                    """
                    # CAPPING COLORS to 255
                    ### very slow => 3 * O(n^2)

                    if values["-ADD-"]:
                        img_B = np.ndarray([np.array([max(0, min(i_b + B, 255)) for i_b in i_B]) for i_B in img_B])
                        img_G = np.ndarray([np.array([max(0, min(i_g + G, 255)) for i_g in i_G]) for i_G in img_G])
                        img_R = np.ndarray([np.array([max(0, min(i_r + R, 255)) for i_r in i_R]) for i_R in img_R])
                    elif values["-SUB-"]:
                        img_B = np.ndarray([np.array([max(0, min(i_b - B, 255)) for i_b in i_B]) for i_B in img_B])
                        img_G = np.ndarray([np.array([max(0, min(i_g - G, 255)) for i_g in i_G]) for i_G in img_G])
                        img_R = np.ndarray([np.array([max(0, min(i_r - R, 255)) for i_r in i_R]) for i_R in img_R])

                    image_file = cv2.merge([img_B, img_G, img_R])
                    """

                    if values["-ADD-"]:
                        image_file = cv2.merge([img_B + B, img_G + G, img_R + R])
                    elif values["-SUB-"]:
                        image_file = cv2.merge([img_B - B, img_G - G, img_R - R])

                # Select Color Range
                elif ev == "FILTER_COLOR":
                    l_R = max(0, min(int(values["-l_R-"]), 255))
                    l_G = max(0, min(int(values["-l_G-"]), 255))
                    l_B = max(0, min(int(values["-l_B-"]), 255))
                    r_R = max(0, min(int(values["-r_R-"]), 255))
                    r_G = max(0, min(int(values["-r_G-"]), 255))
                    r_B = max(0, min(int(values["-r_B-"]), 255))

                    lower = colorsys.rgb_to_hsv(l_R / 255.0, l_G / 255.0, l_B / 255.0)
                    upper = colorsys.rgb_to_hsv(r_R / 255.0, r_G / 255.0, r_B / 255.0)

                    lower = [lower[0] * 179, lower[1] * 255, lower[2] * 255]
                    upper = [upper[0] * 179, upper[1] * 255, upper[2] * 255]

                    hsv_img = cv2.cvtColor(image_file, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(hsv_img, np.array(lower), np.array(upper))
                    image_file = cv2.bitwise_and(image_file, image_file, mask=mask)

                # Blur the image using Gaussian Blur
                elif ev == "BLUR":
                    size = int(values["-BLUR-"])
                    image_file = cv2.GaussianBlur(image_file, ((2 * size + 1), (2 * size + 1)), 0)

                # Sharpen the image via kernel sharpening
                elif ev == "SHARPEN":
                    size = float(values["-SHARPEN-"])
                    kernel_sharpening = np.array([[-1, -1, -1],
                                                  [-1, 9, -1],
                                                  [-1, -1, -1]]) * size

                    # applying the sharpening kernel to the image
                    image_file = cv2.filter2D(image_file, -1, kernel_sharpening)

                # Downgrade image to Grey Scale
                elif ev == "GREY":
                    image_file = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)

            img_bytes = cv2.imencode('.png', cv2.resize(image_file, (540, 400)))[1].tobytes()
            window['image'].update(data=img_bytes)
    except:
        print("Error has occurred somewhere (ಥ_ಥ) (＞︿＜)")

window.close()
