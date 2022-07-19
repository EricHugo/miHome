#!/usr/bin/env python3

import sys
import json
import re
import pickle
import cv2 
import face_recognition

WEBCAM = cv2.VideoCapture(0)

def create_embeddings(ref, n=5):
    for _ in range(n):
        print("Press 'C' to capture image, 'Q' to quit without saving")
        while True:
            check, frame = WEBCAM.read()
            if not check:
                raise RuntimeError("Webcam failed check.")
            resized_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            cv2.imshow("Capturing", resized_frame)
            key = cv2.waitKey(1)
            # print(key)
            if key == -1:
                continue
            elif re.match("[Cc]", chr(key)):
                face_locs = face_recognition.face_locations(resized_frame)
                if face_locs:
                    face_encoding = face_recognition.face_encodings(frame)[0]
                    print(face_encoding)
                    if ref in embeddings:
                        embeddings[ref] += [face_encoding]
                    else:
                        embeddings[ref] = [face_encoding]
                break
            elif re.match("[Qq]", chr(key)):
                print("quit")
                return 
    return embeddings


if __name__ == "__main__":
    name = sys.argv[1]
    try:
        with open("people.json") as f:
            people = json.load(f)
        ref = 1 + int(max(list(people.keys())))
    except FileNotFoundError:
        people = {}
        ref = 0
    try:
        with open("embeddings.pkl") as f:
            embeddings = pickle.load(f)
    except FileNotFoundError:
        embeddings = {}

    people[ref] = name
    with open("people.json", "w") as outfile:
        json.dump(people, outfile)

    new_embeddings = create_embeddings(ref)
    embeddings.update(new_embeddings)
    with open("embeddings.pkl", "wb") as embed_file:
        pickle.dump(embeddings, embed_file)
    WEBCAM.release()
    cv2.destroyAllWindows()
