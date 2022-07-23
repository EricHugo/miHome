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
    manager = mp.Manager()
    q = manager.Queue()
