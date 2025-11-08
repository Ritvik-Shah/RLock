import os
import numpy as np
import face_recognition
import cv2
import Vars
import Database
import Camera as cam

# Config
FACE_MODEL = "hog"
DIST_THRESHOLD = 0.48
ENCODING_COUNT = 3

def _user_folder():
    """Return folder path for current device/user."""
    return Vars.database

def _embedding_path(user_id):
    """Return path for the user's stored encodings."""
    return os.path.join(_user_folder(), f"{user_id}_encodings.npy")

def _save_embeddings(user_id, encs):
    path = _embedding_path(user_id)
    np.save(path, np.array(encs))
    return path

def _load_embeddings(user_id):
    path = _embedding_path(user_id)
    if not os.path.exists(path):
        return None
    return np.load(path, allow_pickle=True)

def _compute_encodings(image):
    """Return face encodings for detected faces in image."""
    if image is None:
        print("[ERROR] No image captured from camera.")
        return []

    if not isinstance(image, np.ndarray):
        print(f"[ERROR] Invalid image type: {type(image)}")
        return []

    if image.size == 0:
        print("[ERROR] Empty image frame.")
        return []

    if image.dtype != np.uint8:
        print(f"[DEBUG] Converting dtype from {image.dtype} to uint8")
        image = np.clip(image, 0, 255).astype(np.uint8)

    if image.shape[-1] == 4:
        print("[DEBUG] Removing alpha channel (BGRA → BGR)")
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # Make sure array is contiguous in memory (important!)
    if not image.flags['C_CONTIGUOUS']:
        image = np.ascontiguousarray(image)

    try:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb = np.ascontiguousarray(rgb)
    except cv2.error as e:
        print(f"[ERROR] Failed color conversion: {e}")
        return []

    try:
        locs = face_recognition.face_locations(rgb, model=FACE_MODEL)
    except Exception as e:
        print(f"[ERROR] Face recognition failed: {e}")
        return []

    if not locs:
        print("[INFO] No faces found in frame.")
        return []

    print(f"[INFO] Found {len(locs)} face(s).")
    encs = face_recognition.face_encodings(rgb, locs)
    return encs

def register_user():
    """
    Register the current device's user (Vars.device_id).
    Captures multiple samples and stores encodings.
    """
    user_id = Vars.device_id
    if Database.check_database(Vars.database_file, user_id):
        print("[INFO] User already registered on this device.")
        return False

    enc_list = []
    print(f"[INFO] Starting registration for device ID: {user_id}")
    os.makedirs(Vars.database, exist_ok=True)

    for i in range(ENCODING_COUNT):
        print(f"--> Capture {i+1}/{ENCODING_COUNT}: Look at camera and press 's'")
        frame = cam.capture_frame(show_preview=True)
        if frame is None:
            print("[WARN] Capture canceled.")
            continue
        encs = _compute_encodings(frame)
        if not encs:
            print("[WARN] No face detected. Try again.")
            continue
        enc_list.append(encs[0])
        img_path = os.path.join(Vars.database, f"{user_id}_{i+1}.jpg")
        cv2.imwrite(img_path, frame)

    if not enc_list:
        print("[ERROR] Registration failed (no faces captured).")
        return False

    _save_embeddings(user_id, enc_list)

    Database.create_database(Vars.database, Vars.database_file, user_id)

    print(f"[SUCCESS] Registration complete for {user_id}")
    return True

def recognize_user():
    """
    Capture a frame and recognize against stored encodings.
    """
    frame = cam.capture_frame(show_preview=True)
    if frame is None:
        print("[INFO] Recognition canceled.")
        return None

    query_encs = _compute_encodings(frame)
    if not query_encs:
        print("[WARN] No face detected.")
        return None
    query = query_encs[0]

    user_id = Vars.device_id
    stored_encs = _load_embeddings(user_id)
    if stored_encs is None:
        print("[WARN] No registration found for this device.")
        return None

    dists = [np.linalg.norm(query - e) for e in stored_encs]
    best = np.min(dists)
    print(f"[DEBUG] Best distance: {best:.4f}")

    if best < DIST_THRESHOLD:
        print(f"[SUCCESS] Face recognized for {user_id}")
        return user_id
    else:
        print("[FAIL] Face not recognized.")
        return None
