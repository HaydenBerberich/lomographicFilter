import cv2
import numpy as np

def on_color_trackbar(val, original_image, color_filtered_image, halo_filtered_image):
    global image
    try:
        # Calculate the sigmoid function parameter
        s = max(val / 100.0, 0.08)
        
        # Create a lookup table for the sigmoid function
        lut = np.array([256 / (1 + np.exp(-((i / 256.0) - 0.5) / s)) for i in range(256)], dtype=np.uint8)
        
        # Split the image into its color channels
        b, g, r = cv2.split(original_image)
        
        # Apply the lookup table to the red channel
        r = cv2.LUT(r, lut)
        
        # Merge the channels back together
        color_filtered_image[:] = cv2.merge((b, g, r))
        
        # Apply the halo effect with the current trackbar value
        apply_halo_effect(cv2.getTrackbarPos('Halo Effect', 'Lomographic Filter'), color_filtered_image, False)
    except Exception as e:
        print(f"Error in on_color_trackbar: {e}")

def on_halo_trackbar(val, color_filtered_image):
    try:
        # Apply the halo effect with the new trackbar value
        apply_halo_effect(val, color_filtered_image, False)
    except Exception as e:
        print(f"Error in on_halo_trackbar: {e}")

def apply_halo_effect(val, color_filtered_image, save_image):
    global image
    try:
        # Create a halo effect mask
        halo = np.full_like(color_filtered_image, 1.0, dtype=np.float32)
        
        # Get the dimensions of the image
        rows, cols = color_filtered_image.shape[:2]
        max_radius = min(rows, cols) // 2
        
        # Calculate the radius of the halo effect
        radius = int(max_radius * (val / 100.0))
        
        # Ensure the radius is odd
        if radius % 2 == 0:
            radius += 1
        
        # Draw a black circle in the center of the halo mask
        cv2.circle(halo, (cols // 2, rows // 2), radius, (0, 0, 0), -1)
        
        # Invert the halo mask
        halo = 1 - halo
        
        # Apply a Gaussian blur to the halo mask
        halo = cv2.GaussianBlur(halo, (radius, radius), 0)
        
        # Convert the color filtered image to float
        color_filtered_float = color_filtered_image.astype(np.float32) / 255.0
        
        # Apply the halo effect
        halo_effect = cv2.multiply(color_filtered_float, halo)
        
        # Blend the halo effect with the original image
        alpha = 0.5
        blended = cv2.addWeighted(color_filtered_float, alpha, halo_effect, 1 - alpha, 0)
        
        # Convert the result back to uint8
        image = (blended * 255).astype(np.uint8)
        
        if save_image:
            cv2.imwrite('output.jpg', image)
        
        # Show the image with the halo effect
        cv2.imshow('Lomographic Filter', image)
    except Exception as e:
        print(f"Error in apply_halo_effect: {e}")