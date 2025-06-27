import cv2
import os


class SlideShow:

    def __init__(self):
        pass

    def display_images(self, folder):

        files = sorted(
            [f for f in os.listdir(folder) if f.endswith((".png", ".jpg", ".jpeg"))]
        )

        index = 0
        while True:
            file = files[index]
            path = os.path.join(folder, file)
            img = cv2.imread(path)

            # Add filename as overlay text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            color = (255, 255, 255)
            thickness = 2
            position = (10, 30)

            cv2.putText(
                img, file, position, font, font_scale, color, thickness, cv2.LINE_AA
            )

            cv2.imshow("Slideshow", img)

            key = cv2.waitKey(0)  # Wait for key press
            if key == 27:  # ESC to exit
                break

            index = (index + 1) % len(files)  # Loop back to 0 when reaching the end

        cv2.destroyAllWindows()
