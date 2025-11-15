# Bounding Box Drawing Tool for Qwen2509

A small Python + OpenCV tool for drawing bounding boxes on images and exporting YOLO-format label files.
GitHub repo:
https://github.com/AquaFAN171029/boundingBox-drawing-tool-for-Qwen2509

## 1. Features

Scan a folder and load images one by one (sorted by filename)
Draw multiple bounding boxes per image with the mouse
Undo the last box (z) or clear all boxes (r)

Save:
A YOLO .txt label file
An image with red rectangles drawn on it for visual checking

## 2. Installation
### 2.1 Clone the repository
```bash
git clone https://github.com/AquaFAN171029/boundingBox-drawing-tool-for-Qwen2509.git
cd boundingBox-drawing-tool-for-Qwen2509
```
### 2.2 Create a virtual environment

macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 2.3 Install dependencies
```bash
pip install -r requirements.txt
```

## 3. Configuration

`IMAGE_DIR = "."`                 # folder containing images

`CLASS_ID = 0`                    # YOLO class id


`OUTPUT_BOXED_DIR = "boxed"`      # output folder for boxed images

`OUTPUT_LABEL_DIR = "labels"`     # output folder for YOLO labels

Supported image formats:

`.png  .jpg  .jpeg`

The script will find all images in `IMAGE_DIR` with these extensions and process them in sorted filename order.

## 4. Prepare Images
Put the images you want to label into IMAGE_DIR.
For example, if you use the default config:

```markdown
boundingBox-drawing-tool-for-Qwen2509/
  box_tool.py
  back1.png
  back2.png
  ...
```
## 5. Run the Tool
In the project folder:

```bash
python box_tool.py
```

An OpenCV window named image will pop up and show the first image.

## 6. Controls

### 6.1 Mouse

Left click + drag   -> draw a bounding box

Release mouse       -> confirm the box

You can draw multiple boxes on one image


### 6.2 Keyboard (make sure the image window is focused)

s  -> Save current image + labels, go to NEXT image

d  -> Skip current image WITHOUT saving, go to NEXT image

z  -> Undo the last bounding box

r  -> Remove ALL boxes on the current image

q  -> Quit the program


## 7. Outputs
For an input image:

back1.png


You will get:

boxed/back1_boxed.png   # image with red rectangles

labels/back1.txt        # YOLO label file

All coordinates are normalized to the range [0, 1], which is compatible with standard YOLO implementations.