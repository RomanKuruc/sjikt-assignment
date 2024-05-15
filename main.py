# Difficulty: ★★☆☆☆

# Code made by Roman Kuruc. Any sharing or copying this code is
# understandable, since im hella good at this
# --------------------------------------------------------------------------
# COPYRIGHT © 2023 Roman Kuruc, student of University of Zilina, faculty of
# Electrical Engineering and Information Technology, field of study
# Communication and information technologies
# All rights reserved
# --------------------------------------------------------------------------

import cv2
import os
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


def resized_image_save(image, width, height, file_path, new_name, file_extension, selected_folder):
    #   protections
    #   checks if string with new name contains any special character
    name = new_name
    name.split()
    character = False
    special_character = '[@_!#$%^&*()<>?/|}{~:]\\'  # special character set
    for i in range(len(name)):
        # checking if any special character is present in given string or not
        if name[i] in special_character:
            character = True  # if special character found then add 1 to the c
            break

    if character:
        messagebox.showwarning("WARNING", "INVALID CHARACTER")
        return
    #   protection if string new_name is empty
    if not new_name:
        messagebox.showwarning("WARNING", "ENTER NEW NAME OF THE FILE")
        return
    #   protection if string file_extension is empty
    if not file_extension:
        messagebox.showwarning("WARNING", "SELECT FILE EXTENSION")
        return
    #   protection if no folder was selected
    if not selected_folder:
        messagebox.showwarning("WARNING", "SELECT FOLDER")
        return

    #   creates path to original picture
    image = os.path.join(file_path, image).replace("\\", "/")
    #   creates string containing selected folder, new name and file extension
    new_name = selected_folder + "/" + new_name + file_extension
    image = Image.open(image)
    resize = (width, height)
    image = image.resize(resize)
    image = image.save(new_name)


def watermark(image, folder, width, height, placement):
    image_path = os.path.join(folder, image).replace("\\", "/")
    width = int(width)
    height = int(height)
    watermarked_image = tkinter.Toplevel()
    watermarked_image.title("Watermark")
    font = ("Times", 22)

    left = Frame(watermarked_image, bg="#64C7FF", width=width, height=height)
    right = Frame(watermarked_image, bg="#64C7FF", width=200, height=height)

    left.grid(row=0, column=0, sticky="nsew")
    right.grid(row=0, column=1, sticky="nsew")

    img = Image.open(image_path)
    resize = (width, height)
    img = img.resize(resize)

    # Get the image watermark that already prepared
    logo = Image.open("watermark.png")

    # Resizing the watermark into desired size
    size = (100, 100)
    logo.thumbnail(size)

    if placement == "top-left":
        x = 0
        y = 0
    elif placement == "top":
        x = int((width - 100) // 2)
        y = 0
    elif placement == "top-right":
        x = width - 100
        y = 0
    elif placement == "center-left":
        x = 0
        y = int((height - 100) // 2)
    elif placement == "center":
        x = int((width - 100) // 2)
        y = int((height - 100) // 2)
    elif placement == "center-right":
        x = width - 100
        y = int((height - 100) // 2)
    elif placement == "bottom-left":
        x = 0
        y = height - 100
    elif placement == "bottom":
        x = int((width - 100) // 2)
        y = height - 100
    else:
        x = width - 100
        y = height - 100

    # Integrate the image watermark into the watermark position
    img.paste(logo, (x, y))

    # Convert PIL image to ImageTk format
    watermark_img = ImageTk.PhotoImage(image=img)

    image_label = tkinter.Label(left, image=watermark_img)
    image_label.grid(column=0, row=0)

    resize_padx = 5
    resize_pady = 10

    save_label = tkinter.Label(right, text="Enter name", font=("times", 12), bg="#64C7FF")
    save_label.grid(column=0, row=0)
    entry_save = tkinter.Entry(right, font=font, width=12)
    entry_save.grid(column=0, row=1, padx=resize_padx, pady=resize_pady)

    file_extension_label = tkinter.Label(right, text="select file extension", font=("times", 12), bg="#64C7FF")
    file_extension_label.grid(column=0, row=2)
    n = tkinter.StringVar()
    file_extension_combobox = ttk.Combobox(right, width=5, textvariable=n, state="readonly")
    file_extension_combobox['values'] = ('.jpg', '.png', '.bmp')
    file_extension_combobox.grid(column=0, row=3, padx=resize_padx, pady=resize_pady)
    file_extension_combobox.current()

    list_of_folders_label = tkinter.Label(right, text="select folder", font=("times", 12), bg="#64C7FF")
    list_of_folders_label.grid(column=0, row=4)
    n = tkinter.StringVar()
    list_of_folders = ttk.Combobox(right, textvariable=n, state="readonly", width=8)
    fill_combobox(list_of_folders)
    list_of_folders.grid(column=0, row=5, padx=resize_padx, pady=resize_pady)
    file_extension_combobox.current()

    button_save = tkinter.Button(right, text="Save", font=font, width=8,
                                 command=lambda: img.save(list_of_folders.get() + "/" + entry_save.get() + file_extension_combobox.get()))
    button_save.grid(column=0, row=6, padx=resize_padx, pady=resize_pady)
    button_save.bind("<Button-1>")

    watermarked_image.mainloop()


def histogram(img_full_name, file_path):
    #   Creating path to image
    img_path = os.path.join(file_path, img_full_name).replace("\\", "/")
    #   reading image
    image = cv2.imread(img_path)

    #   calculates values of blue, red and green
    blue = cv2.calcHist([image], [0], None, [256], [0, 256])
    red = cv2.calcHist([image], [1], None, [256], [0, 256])
    green = cv2.calcHist([image], [2], None, [256], [0, 256])

    # plots histogram of calculated colors
    plt.title("Histogram of all RGB Colors")
    plt.plot(blue, color="blue")
    plt.plot(green, color="green")
    plt.plot(red, color="red")
    plt.legend(['Blue', 'Green', 'Red'])
    plt.show()


def bilateral_filter(full_name, width, height, input_diameter, input_sigmacolor, input_sigmaspace, file_path):
    #   protection in case input values are not numeric
    if not input_diameter.get().isnumeric() or not input_sigmaspace.get().isnumeric() or not input_sigmacolor.get().isnumeric():
        messagebox.showwarning("WARNING", "INPUTS ARE NOT NUMBERS")
        return

    #   converting string to integer
    diameter = int(input_diameter.get())
    sigma_color = int(input_sigmacolor.get())
    sigma_space = int(input_sigmaspace.get())

    down_points = (int(width), int(height))
    img_path = os.path.join(file_path, full_name).replace("\\", "/")
    bilateral_filter_window = tkinter.Toplevel()
    bilateral_filter_window.title("Bilateral filter")

    left = Frame(bilateral_filter_window, bg="#64C7FF", width=width, height=height)
    right = Frame(bilateral_filter_window, bg="#64C7FF", width=200, height=height)
    font = ("times", 22)

    left.grid(row=0, column=0, sticky="nsew")
    right.grid(row=0, column=1, sticky="nsew")

    #   reads image
    picture = cv2.imread(img_path)

    # Convert BGR to RGB
    picture = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)

    # Resize image
    picture = cv2.resize(picture, down_points, interpolation=cv2.INTER_LINEAR)
    # Apply bilateral filter
    picture = cv2.bilateralFilter(picture, diameter, sigma_color, sigma_space)

    # Convert the filtered image to PIL format
    pil_image = Image.fromarray(picture)
    # Convert PIL image to ImageTk format
    photo = ImageTk.PhotoImage(image=pil_image)

    # Attach the photo to the Tkinter window object to prevent it from being garbage collected
    bilateral_filter_window.photo = photo
    bilateral_image = tkinter.Label(left, image=photo)
    bilateral_image.grid(column=0, row=1, padx=5, pady=5)

    resize_padx = 5
    resize_pady = 10

    save_label = tkinter.Label(right, text="Enter name", font=("times", 12), bg="#64C7FF")
    save_label.grid(column=0, row=0)
    entry_save = tkinter.Entry(right, font=font, width=12)
    entry_save.grid(column=0, row=1, padx=resize_padx, pady=resize_pady)

    file_extension_label = tkinter.Label(right, text="select file extension", font=("times", 12), bg="#64C7FF")
    file_extension_label.grid(column=0, row=2)
    n = tkinter.StringVar()
    file_extension_combobox = ttk.Combobox(right, width=5, textvariable=n, state="readonly")
    file_extension_combobox['values'] = ('.jpg', '.png', '.bmp')
    file_extension_combobox.grid(column=0, row=3, padx=resize_padx, pady=resize_pady)
    file_extension_combobox.current()

    list_of_folders_label = tkinter.Label(right, text="select folder", font=("times", 12), bg="#64C7FF")
    list_of_folders_label.grid(column=0, row=4)
    n = tkinter.StringVar()
    list_of_folders = ttk.Combobox(right, textvariable=n, state="readonly", width=8)
    fill_combobox(list_of_folders)
    list_of_folders.grid(column=0, row=5, padx=resize_padx, pady=resize_pady)
    file_extension_combobox.current()

    button_save = tkinter.Button(right, text="Save", font=font, width=8,
                                 command=lambda: pil_image.save(list_of_folders.get() + "/" + entry_save.get() + file_extension_combobox.get()))
    button_save.grid(column=0, row=6, padx=resize_padx, pady=resize_pady)
    button_save.bind("<Button-1>")

    bilateral_filter_window.mainloop()


def options(full_name, width, height, file_path):
    options_window = tkinter.Toplevel()
    options_window.title("Options")
    options_window.config(bg="#64C7FF")
    font = ("Times", 14)

    #   file_path = "pictures"
    img_path = os.path.join(file_path, full_name).replace("\\", "/")
    #   labels for main window
    #   left side
    left = Frame(options_window, bg='#64C7FF')
    left.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    right = Frame(options_window, bg='white')
    right.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

    #   creates original image label
    top_label = tkinter.Label(left, text="OPTIONS", font=font, bg="#64C7FF")
    top_label.grid(row=0, column=0, padx=5, pady=5)
    width = int(width)
    height = int(height)
    down_points = (width, height)

    # creates resized picture on the left
    img_right = cv2.imread(img_path)
    #   converts the image from BGR to RGB
    img_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2RGB)
    #   resizes image
    img_right = cv2.resize(img_right, down_points, interpolation=cv2.INTER_LINEAR)
    #   coverts the image to ImageTk format
    img_right = Image.fromarray(img_right)
    img_original = ImageTk.PhotoImage(image=img_right)
    picture_right = tkinter.Label(right, image=img_original)
    picture_right.grid(row=1, column=0, padx=5, pady=5)

    options_bar = Frame(left, bg="#64C7FF")
    options_bar.grid(row=2, column=0, padx=0, pady=0)

    resize_padx = 5
    resize_pady = 10

    #   labels for bilateral filter
    button_bilateral = tkinter.Button(options_bar, text="bilateralfilter", font=font, width=10,
                                      command=lambda: bilateral_filter(full_name, width, height, entry_diameter,
                                                                      entry_sigma_color, entry_sigma_space, file_path))
    button_bilateral.grid(column=0, row=1, padx=resize_padx, pady=resize_pady)
    button_bilateral.bind("<Button-1>")

    text_diameter = tkinter.Label(options_bar, text="Diameter", font=("Times", 10), bg="#64C7FF")
    text_diameter.grid(column=1, row=0)
    text_sigma_color = tkinter.Label(options_bar, text="Sigma Color", font=("Times", 10), bg="#64C7FF")
    text_sigma_color.grid(column=2, row=0)
    text_sigma_space = tkinter.Label(options_bar, text="Sigma space", font=("Times", 10), bg="#64C7FF")
    text_sigma_space.grid(column=3, row=0)

    entry_diameter = tkinter.Entry(options_bar, font=font, width=5)
    entry_diameter.grid(column=1, row=1, padx=resize_padx, pady=resize_pady)
    entry_sigma_color = tkinter.Entry(options_bar, font=font, width=5)
    entry_sigma_color.grid(column=2, row=1, padx=resize_padx, pady=resize_pady)
    entry_sigma_space = tkinter.Entry(options_bar, font=font, width=5)
    entry_sigma_space.grid(column=3, row=1, padx=resize_padx, pady=resize_pady)

    #   combobox for logo placement
    n = tkinter.StringVar()
    placement_combobox = ttk.Combobox(options_bar, width = 10, textvariable=n)
    placement_combobox['values'] = ('top-left',
                                    'top',
                                    'top-right',
                                    'center-left',
                                    'center',
                                    'center-right',
                                    'bottom-left',
                                    'bottom',
                                    'bottom-right')
    placement_combobox.grid(column=1, row=3, padx=resize_padx, pady=resize_pady)
    placement_combobox.current()
    text_watermark = tkinter.Label(options_bar, text="logo placement", font=("Times", 10), bg="#64C7FF")
    text_watermark.grid(column=1, row=2)
    button_watermark = tkinter.Button(options_bar, text="watermark", font=font, width=10,
                                      command=lambda: watermark(full_name, file_path, width, height,
                                                                placement_combobox.get()))
    button_watermark.grid(column=0, row=3, padx=resize_padx, pady=resize_pady)
    button_watermark.bind("<Button-1>")

    #   labels for image histogram
    button_histogram = tkinter.Button(options_bar, text="histogram", font=font, width=10,
                                      command=lambda: histogram(full_name, file_path))
    button_histogram.grid(column=0, row=4, padx=resize_padx, pady=resize_pady)
    button_histogram.bind("<Button-1>")

    label_name = tkinter.Label(options_bar, text="New name", font=("Times", 10), bg="#64C7FF")
    label_name.grid(column=1, row=5)
    file_extension_text = tkinter.Label(options_bar, text="Select file extension", font=("Times", 10), bg="#64C7FF")
    file_extension_text.grid(column=2, row=5)
    folder_text = tkinter.Label(options_bar, text="Select folder", font=("Times", 10), bg="#64C7FF")
    folder_text.grid(column=3, row=5)

    button_save = tkinter.Button(options_bar, text="Save", font=font, width=10,
                                 command=lambda: resized_image_save(full_name, width, height, file_path, entry_save.get(),
                                                                    file_extension_combobox.get(), list_of_folders.get()))
    button_save.grid(column=0, row=6, padx=resize_padx, pady=resize_pady)
    button_save.bind("<Button-1>")
    entry_save = tkinter.Entry(options_bar, font=font, width=10)
    entry_save.grid(column=1, row=6, padx=resize_padx, pady=resize_pady)

    #   combobox for file extensions
    n = tkinter.StringVar()
    file_extension_combobox = ttk.Combobox(options_bar, width=5, textvariable=n, state="readonly")
    file_extension_combobox['values'] = ('.jpg', '.png', '.bmp')
    file_extension_combobox.grid(column=2, row=6, padx=resize_padx, pady=resize_pady)
    file_extension_combobox.current()

    n = tkinter.StringVar()
    list_of_folders = ttk.Combobox(options_bar, textvariable=n, state="readonly", width=8)
    fill_combobox(list_of_folders)
    list_of_folders.grid(column=3, row=6, padx=resize_padx, pady=resize_pady)
    file_extension_combobox.current()

    options_window.mainloop()


def gallery(extension, folder_path):
    #   function loads picture from list and displays it
    def load_image(image_paths, current_image_index, images):
        image_path = image_paths[current_image_index]
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (854, 480))  # Resize to 854x480
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)
        images.config(image=photo)
        images.image = photo  # Keep reference to avoid garbage collection

    #   after button next is pressed, it displays next picture
    def next_image(image_paths, images):
        global current_image_index
        #   it increases value by 1, once it reaches end of the list,
        #   the modulo operation ensures that the index will be 0
        #   it creates loop behaviour
        current_image_index = (current_image_index + 1) % len(image_paths)
        load_image(image_paths, current_image_index, images)

    global current_image_index
    current_image_index = 0
    gallery_window = tkinter.Toplevel()
    gallery_window.title("Gallery")
    gallery_window.config(bg="#64C7FF")
    font = ("Times", 22)
    image_paths = []
    #   loads all images with correct extension and saves them to list
    for filename in os.listdir(folder_path):
        if filename.endswith(extension):
            image_paths.append(os.path.join(folder_path, filename).replace("\\", "/"))

    # Load the first image
    images = tkinter.Label(gallery_window)
    images.pack()
    load_image(image_paths, current_image_index, images)

    # Create buttons
    next_button = tkinter.Button(gallery_window, text="Next", height=1, width=10, font=font,
                                 command=lambda: next_image(image_paths, images))
    next_button.pack()

    gallery_window.mainloop()


#   simple slide show
def slide_show(extension, images_folder):
    #   images_folder = "pictures"
    slideshow_duration = 1000  # milliseconds
    # Get the list of image files in the folders
    image_files = [f for f in os.listdir(images_folder) if f.endswith(extension)]
    # Iterate through each image and display it for slideshow_duration milliseconds
    for image_file in image_files:
        # Create a window for displaying the slideshow
        cv2.namedWindow("Slideshow", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Slideshow", 854, 480)
        image_path = os.path.join(images_folder, image_file)
        image = cv2.imread(image_path)
        cv2.imshow("Slideshow", image)
        cv2.waitKey(slideshow_duration)
    cv2.destroyAllWindows()


#   applies selected values and checks if all conditions are true
def on_apply(extension, input_filename, input_width, input_height, folder_path, selection_window):
    filename = input_filename.get()
    width = input_width.get()
    height = input_height.get()
    full_file = filename + extension
    was_file_found = False

    #   checks if size of the image is less or equal to 1920x1080
    if not width.isnumeric() or not height.isnumeric():
        messagebox.showwarning("WARNING", "WIDTH OR HEIGHT ARE NOT NUMBERS")
        return

    if int(width) > 1920 or int(height) > 1080:
        messagebox.showwarning("WARNING", "WIDTH OR HEIGHT ARE MORE THAN 1920x1080")
        return

    for filename in os.listdir(folder_path):
        if filename == full_file:
            selection_window.destroy()
            was_file_found = True
            options(full_file, width, height, folder_path)

    #   if file wasn't found, it'll show error
    if not was_file_found:
        messagebox.showwarning("WARNING", "NO FILE WAS FOUND FILE OR WIDTH AND HEIGHT ARE NOT NUMBERS")
        selection_window.destroy()


#   this function allows user to select file, height and weight, as well as show gallery and slideshow
def selection_of_file(extension, folder):
    #   checks whether folder was selected or not
    if folder == "":
        messagebox.showwarning("WARNING", "NO FOLDER WAS SELECTED")
        return

    color = "#64C7FF"
    selection_window = tkinter.Tk()
    selection_window.title("Select image")
    selection_window.config(bg=color)
    font = ("Times", 14)
    resize_padx = 5
    resize_pady = 5

    message_name = tkinter.Label(selection_window, text="Type file name", font=font, bg=color)
    message_name.grid(column=0, row=0, padx=resize_padx, pady=resize_pady)

    message_width = tkinter.Label(selection_window, text="Width (px)", font=font, bg=color)
    message_width.grid(column=1, row=0, padx=resize_padx, pady=resize_pady)

    message_height = tkinter.Label(selection_window, text="Height (px)", font=font, bg=color)
    message_height.grid(column=2, row=0, padx=resize_padx, pady=resize_pady)

    entry_name = tkinter.Entry(selection_window, font=font)
    entry_name.grid(column=0, row=1, padx=resize_padx, pady=resize_pady)

    entry_width = tkinter.Entry(selection_window, font=font, width=5)
    entry_width.grid(column=1, row=1, padx=resize_padx, pady=resize_pady)

    entry_height = tkinter.Entry(selection_window, font=font, width=5)
    entry_height.grid(column=2, row=1, padx=resize_padx, pady=resize_pady)

    button_apply = tkinter.Button(selection_window, text="Apply", font=font, width=18, anchor="center",
                                  command=lambda: on_apply(extension, entry_name, entry_width, entry_height, folder,
                                                           selection_window))
    button_apply.grid(column=0, row=2, padx=resize_padx, pady=resize_pady)

    button_slideshow = tkinter.Button(selection_window, text="Slideshow", font=font,
                                      command=lambda: slide_show(extension, folder))
    button_slideshow.grid(column=0, row=3, padx=resize_padx, pady=resize_pady)

    button_gallery = tkinter.Button(selection_window, text="Gallery", font=font,
                                    command=lambda: gallery(extension, folder))
    button_gallery.grid(column=1, row=3)

    selection_window.mainloop()


#   first creating combobox
#   this function will return list of all folders in current directory
def get_folders_in_current_directory():
    folders = []
    current_directory = '.'  # Represents the current directory
    for item in os.listdir(current_directory):
        #   if it's folder, then it appends to a list which is then returned
        if os.path.isdir(item):
            folders.append(item)
    return folders


def fill_combobox(combobox):
    #   fills combobox with names of the folders in current directory
    folders = get_folders_in_current_directory()
    for folder in folders:
        #   the star unpacks the existing values from  the Combobox into a tuple,
        #   and then it's added to the folder tuple (google and friends helped me with this
        combobox['values'] = (*combobox['values'], folder)


#   main function
def main():
    main_window = tkinter.Tk()
    main_window.title("MAIN WINDOW")
    font = ("Times", 18)

    #   labels for main window
    #   left side
    left = Frame(main_window, bg="#64C7FF", width=250, height=350)
    right = Frame(main_window, bg="#64C7FF", width=250, height=350)

    left.grid(row=0, column=0, sticky="nsew")
    right.grid(row=0, column=1, sticky="nsew")

    folder_label = tkinter.Label(left, text="Select folder", font=("Times", 12), bg="#64C7FF")
    folder_label.grid(column=0, row=3)
    n = tkinter.StringVar()
    list_of_folders = ttk.Combobox(left, textvariable=n, state="readonly")
    list_of_folders.grid(column=0, row=4, padx=50, pady=10)
    fill_combobox(list_of_folders)

    button_jpg = tkinter.Button(left, text="JPG", font=font, command=lambda: selection_of_file(".jpg", list_of_folders.get()))
    button_jpg.grid(column=0, row=0, padx=50, pady=10)

    button_png = tkinter.Button(left, text="PNG", font=font, command=lambda: selection_of_file(".png", list_of_folders.get()))
    button_png.grid(column=0, row=1, padx=50, pady=10)

    button_jpeg = tkinter.Button(left, text="BMP", font=font, command=lambda: selection_of_file(".bmp", list_of_folders.get()))
    button_jpeg.grid(column=0, row=2, padx=50, pady=10)

    down_points = (480, 270)
    img_right = cv2.imread("myCreation.png")
    #   converts the image from BGR to RGB
    img_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2RGB)
    #   resizes image to 480x270
    img_right = cv2.resize(img_right, down_points, interpolation=cv2.INTER_LINEAR)
    #   coverts the image to ImageTk format
    img_right = Image.fromarray(img_right)
    img_original = ImageTk.PhotoImage(image=img_right)
    picture_right = tkinter.Label(right, image=img_original)
    picture_right.grid(row=0, column=0, padx=5, pady=5)

    main_window.mainloop()


if __name__ == "__main__":
    main()
