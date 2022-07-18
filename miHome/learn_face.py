#!/usr/bin/env python3

import sys
import json
import pickle
import cv2 
import face_recognition


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
