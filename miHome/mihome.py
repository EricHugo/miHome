#/usr/bin/env python3

import sys
import time
import json
import pickle
import cv2
import face_recognition
import multiprocessing as mp

WEBCAM = cv2.VideoCapture(0)

def _listener(q):
    while True:
        in_object = q.get()
        print(in_object)
        if in_onbject == "break":
            break


if __name__ == "__main__":
    with open("embeddings.pkl", "rb") as f:
        embeddings = pickle.load(f)
    known_face_refences = []
    known_face_encodings = []
    for ref, embedding_list in embeddings.items():
        # seperate into lists for the benefit of face_recognition module
        known_face_refences += [ref for _ in range(len(embedding_list))]
        known_face_encodings += [embedding for embedding in embedding_list]
    print(known_face_encodings)
    print(known_face_refences)
    with open("people.json") as f:
        known_people = json.load(f)
    print(known_people)
    manager = mp.Manager()
    q = manager.Queue()

    while True:
        check, frame = WEBCAM.read()
        if not check:
            raise RuntimeError("Webcam failed check.")
        resized_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        face_locs = face_recognition.face_locations(resized_frame)
        face_encodes = face_recognition.face_encodings(resized_frame, face_locs)
        people = []
        for face_encode in face_encodes:
            # default if no match
            person = "Unrecognised"
            matches = face_recognition.compare_faces(known_face_encodings, face_encode, tolerance=0.6)
            if True in matches:
                print(matches)
                match_ind = matches.index(True)
                person = known_people[str(match_ind)]
            people.append(person)
        print(people)

