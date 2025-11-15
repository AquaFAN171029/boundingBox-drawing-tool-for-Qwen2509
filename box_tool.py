import cv2
import os

# settings
# ================
IMAGE_DIR = "."
CLASS_ID = 0

OUTPUT_BOXED_DIR = "boxed"
OUTPUT_LABEL_DIR = "labels"
# ==================

os.makedirs(OUTPUT_BOXED_DIR, exist_ok=True)
os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

image_files = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
]

image_files.sort()

if not image_files:
    print("no image files found in the dir. ")
    exit(0)

print(f"totally {len(image_files)} image found.")

base_img = None      # original image
boxes = []           # all boxes on the image [(x1,y1,x2,y2), (x3,y3,x4,y4)...]
drawing = False
ix, iy = -1, -1


def redraw(preview_box=None):
    global base_img, boxes
    img_show = base_img.copy()

    # existing boxes
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(img_show, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # drawing boxes
    if preview_box is not None:
        (px1, py1, px2, py2) = preview_box
        cv2.rectangle(img_show, (px1, py1), (px2, py2), (0, 0, 255), 1)

    cv2.imshow("image", img_show)


def mouse_callback(event, x, y, flags, param):
   
    global ix, iy, drawing, boxes, base_img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # preview box
            px1, px2 = sorted([ix, x])
            py1, py2 = sorted([iy, y])
            redraw(preview_box=(px1, py1, px2, py2))

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x1, x2 = sorted([ix, x])
        y1, y2 = sorted([iy, y])

        # only add valid boxes
        if x2 > x1 and y2 > y1:
            boxes.append((x1, y1, x2, y2))

        redraw()


def save_annotation(img_name):
    global base_img, boxes, CLASS_ID

    h, w = base_img.shape[:2]
    name_no_ext, ext = os.path.splitext(img_name)

    boxed_path = os.path.join(OUTPUT_BOXED_DIR, name_no_ext + "_boxed" + ext)
    label_path = os.path.join(OUTPUT_LABEL_DIR, name_no_ext + ".txt")

    # save the txt file
    with open(label_path, "w") as f:
        for (x1, y1, x2, y2) in boxes:
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            bw = x2 - x1
            bh = y2 - y1

            cx_norm = cx / w
            cy_norm = cy / h
            bw_norm = bw / w
            bh_norm = bh / h

            line = f"{CLASS_ID} {cx_norm:.6f} {cy_norm:.6f} {bw_norm:.6f} {bh_norm:.6f}\n"
            f.write(line)

    # Draw and save boxed images
    img_boxed = base_img.copy()
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(img_boxed, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imwrite(boxed_path, img_boxed)

    print(f"[Saved] {img_name}")
    print(f" Image with bounding boxes: {boxed_path}")
    print(f"  - YOLO text file: {label_path}")


cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_callback)

print("Instructions:")
print("  Mouse: left-click and drag = draw a box (can draw multiple boxes)")
print("  Keys:  s = save current image and go to the next one")
print("         d = skip current image without saving")
print("         z = undo the last box")
print("         r = remove all boxes on the current image")
print("         q = quit the program")

running = True
idx = 0

while idx < len(image_files) and running:
    img_name = image_files[idx]
    img_path = os.path.join(IMAGE_DIR, img_name)

    base_img = cv2.imread(img_path)
    if base_img is None:
        print(f"[Skiped] Cannot load the image: {img_path}")
        idx += 1
        continue

    boxes = []
    print(f"\n=== {idx+1}/{len(image_files)} images drawed: {img_name} ===")

    redraw()

    while True:
        key = cv2.waitKey(20) & 0xFF

        if key == ord('q'):
            running = False
            break

        elif key == ord('s'):
            if boxes:
                save_annotation(img_name)
            else:
                print(f"[Key] Cannot find any bounding box on {img_name} ,skiped.")
            idx += 1
            break

        elif key == ord('d'):
            print(f"[Skiped] {img_name} (without save)")
            idx += 1
            break

        elif key == ord('z'):
            if boxes:
                boxes.pop()
                print("Withdrew the last box")
                redraw()
            else:
                print("There is no box to withdraw")

        elif key == ord('r'):
            if boxes:
                boxes = []
                print("Cleared all boxes on the image")
                redraw()
            else:
                print("There is no box to clear")

cv2.destroyAllWindows()
print("Program ended.")
