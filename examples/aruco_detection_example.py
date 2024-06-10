import cv2


def detect_aruco_markers(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load the Aruco dictionary and parameters
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    # Detect the markers in the image
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        # Draw the detected markers
        cv2.aruco.drawDetectedMarkers(image, corners, ids)

        # Display the result
        cv2.imshow("Detected Aruco Markers", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print("No Aruco markers detected.")


if __name__ == "__main__":
    image_path = "/path/to/example/aruco.png"
    detect_aruco_markers(image_path)
