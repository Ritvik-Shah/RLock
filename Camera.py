import cv2
import os

def capture_frame(save_path=None, show_preview=True, window_name="Camera", camera_index=0):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("Could not open camera.")

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    frame_captured = None
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if show_preview:
                cv2.imshow(window_name, frame)
            key = cv2.waitKey(20) & 0xFF
            if key == ord('s'):
                print("✅ Frame captured in-app:",
                    type(frame), frame.shape, frame.dtype,
                    "min:", frame.min(), "max:", frame.max())
                frame_captured = frame.copy()
                if save_path:
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    cv2.imwrite(save_path, frame_captured)
                break
            elif key in (ord('q'), ord('c')):
                frame_captured = None
                break
    finally:
        cap.release()
        cv2.destroyWindow(window_name)
    return frame_captured
