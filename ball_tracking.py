import cv2
import numpy as np
from collections import defaultdict

def load_video(video_file_path):
    """Loads a video from the specified file path."""
    return cv2.VideoCapture(video_file_path)

def define_quadrants(frame):
    """Divides the frame into four equal quadrants."""
    height, width = frame.shape[:2]
    return [
        ((0, 0), (width // 2, height // 2)),  # Top-left quadrant
        ((width // 2, 0), (width, height // 2)),  # Top-right quadrant
        ((0, height // 2), (width // 2, height)),  # Bottom-left quadrant
        ((width // 2, height // 2), (width, height))  # Bottom-right quadrant
    ]

def detect_balls(frame):
    """Detects balls of different colors in the frame."""
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges for different ball colors
    color_ranges = {
        'yellow': ([20, 100, 100], [30, 255, 255]),
        'green': ([40, 40, 40], [80, 255, 255]),
        'white': ([0, 0, 200], [180, 30, 255]),
        'orange': ([5, 100, 100], [15, 255, 255])
    }

    detected_balls = []
    for color, (lower_hsv, upper_hsv) in color_ranges.items():
        # Create a mask for the current color
        color_mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)

        # Find contours in the mask
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filter out small noise
                moments = cv2.moments(contour)
                if moments["m00"] != 0:
                    center_x = int(moments["m10"] / moments["m00"])
                    center_y = int(moments["m01"] / moments["m00"])
                    detected_balls.append((center_x, center_y, color))
    return detected_balls

def track_balls(previous_positions, current_detections):
    """Tracks ball positions across frames."""
    # ... implementation of ball tracking logic

def check_events(ball_positions, quadrants, current_time):
    """Checks for ball entry and exit events in quadrants."""
    # ... implementation of event checking logic

def create_overlay(frame, events):
    """Creates an overlay with event information."""
    # ... implementation of overlay creation logic

def save_output(events, output_path):
    """Saves event data to a text file."""
    # ... implementation of output saving logic

def main():
    video_path = "D:\\project\\AI Assignment video.mp4"
    video_capture = load_video(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    quadrants = None
    ball_positions = {}
    all_events = []

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter('output.mp4', fourcc, fps, (int(video_capture.get(3)), int(video_capture.get(4))))

    ball_quadrants = {}  # To store current quadrant of each ball

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        if quadrants is None:
            quadrants = define_quadrants(frame)

        current_time = frame_count / fps
        current_detections = detect_balls(frame)
        ball_positions = track_balls(ball_positions, current_detections)
        new_events = check_events(ball_positions, quadrants, current_time)
        all_events.extend(new_events)

        processed_frame = create_overlay(frame.copy(), new_events)
        output_video.write(processed_frame)

        frame_count += 1

    video_capture.release()
    output_video.release()
    save_output(all_events, 'output_events.txt')

if __name__ == "__main__":
    main()
