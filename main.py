# Hayden Berberich
# 11/11/24

import cv2
import sys
from utils import parse_arguments
from filters import on_color_trackbar, on_halo_trackbar, apply_halo_effect

def main():
    global image, original_image, color_filtered_image, halo_filtered_image
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Load the image
        original_image = cv2.imread(args.filename)
        if original_image is None:
            print(f"Error: Unable to load image {args.filename}")
            sys.exit(1)
        
        # Make copies of the original image
        image = original_image.copy()
        color_filtered_image = original_image.copy()
        halo_filtered_image = original_image.copy()
        
        # Create a window
        cv2.namedWindow('Lomographic Filter')
        # Create trackbars for color and halo effects
        cv2.createTrackbar('Color Effect', 'Lomographic Filter', 10, 20, lambda val: on_color_trackbar(val, original_image, color_filtered_image, halo_filtered_image))
        cv2.createTrackbar('Halo Effect', 'Lomographic Filter', 100, 100, lambda val: on_halo_trackbar(val, color_filtered_image))
        
        # Show the initial image
        cv2.imshow('Lomographic Filter', image)
        
        while True:
            # Wait for a key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save the modified image if 's' is pressed
                apply_halo_effect(cv2.getTrackbarPos('Halo Effect', 'Lomographic Filter'), color_filtered_image, True)
                break
        
        # Destroy all windows
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()