import cv2
import os

# ---------------- CONFIG ----------------
CASCADE_PATH = "data/NumberPlate/haarcascade_russian_plate_number.xml"
IMAGE_PATH = "data/NumberPlate/plate_2.jpg"
SAVE_DIR = "data/NumberPlate/Resources/Scanned"

minArea = 200
color = (255, 0, 255)

os.makedirs(SAVE_DIR, exist_ok=True)

NumPlateCascade = cv2.CascadeClassifier(CASCADE_PATH)


# ---------------- FUNCTIONS ----------------
def detect_plate(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = NumPlateCascade.detectMultiScale(imgGray, 1.1, 10)

    imgRoi = None

    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            imgRoi = img[y:y + h, x:x + w]
            cv2.imshow("ROI", imgRoi)

    return img, imgRoi



mode = input("Select mode (1 = Image, 0 = Webcam): ").strip()

# ---------------- IMAGE MODE ----------------
if mode == "1":
    img = cv2.imread(IMAGE_PATH)
    count = 0

    while True:
        imgResult, imgRoi = detect_plate(img.copy())
        cv2.imshow("Result", imgResult)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') and imgRoi is not None:
            cv2.imwrite(f"{SAVE_DIR}/NoPlate_{count}.jpg", imgRoi)
            print("✅ Plate saved")
            count += 1

        if key == ord('q'):
            break

# ---------------- WEBCAM MODE ----------------
elif mode == "0":
    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        success, img = cap.read()
        if not success:
            break

        imgResult, imgRoi = detect_plate(img)
        cv2.imshow("Result", imgResult)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') and imgRoi is not None:
            cv2.imwrite(f"{SAVE_DIR}/NoPlate_{count}.jpg", imgRoi)
            print("✅ Plate saved")
            count += 1

        if key == ord('q'):
            break

    cap.release()

else:
    print("Invalid option! Use 1 for Image or 0 for Webcam.")

cv2.destroyAllWindows()
