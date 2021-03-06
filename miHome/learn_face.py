#!/usr/bin/env python3

import sys
import json
import re
import pickle
import cv2 
import face_recognition

WEBCAM = cv2.VideoCapture(0)

def get_person(curr_people, new_name):
    """
    Check if name exists in dict.

    :param curr_people: dict of current refences and corresponding names
    :param new_name: name to be checked in curr_people values
    :returns: if name exists returns corresponding reference else None
    """
    for reference, corr_name in curr_people:
        if new_name == corr_name:
            return reference
    return None

def create_embeddings(ref, n=5):
    """
    Creates and returns dict of embeddings based on n images taken by 
    WEBCAM.

    :param ref: reference num corresponding to embeddings.
    :param n: number of images to create embeddings from.
    :returns: dict with key ref and value embeddings.
    :raises RuntimeError: webcam not responding.
    """
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
        ref = get_person(people, name)
        if not ref:
            ref = 1 + int(max(list(people.keys())))
        else:
            print("Replacing " + name)
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
