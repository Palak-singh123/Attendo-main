import ast
import json

import cv2
import numpy as np
import streamlit as st

from insightface.app import FaceAnalysis

from src.database.config import supabase


# Load InsightFace model
@st.cache_resource
def load_face_model():

    model = FaceAnalysis(
        name="buffalo_l",
        providers=[
            "CoreMLExecutionProvider",
            "CPUExecutionProvider"
        ]
    )

    model.prepare(
        ctx_id=0,
        det_size=(640, 640)
    )

    return model


# Convert image to numpy array
def image_to_numpy(image):

    if image is None:
        return None

    if hasattr(image, "convert"):

        return np.array(
            image.convert("RGB")
        )

    if hasattr(image, "getvalue"):

        image_bytes = image.getvalue()

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if image is None:
            return None

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

    image = np.asarray(image)

    if image.ndim == 3:
        return image

    return None


# Normalize embedding
def normalize_embedding(embedding):

    embedding = np.asarray(
        embedding,
        dtype=np.float32
    ).flatten()

    norm = np.linalg.norm(embedding)

    if norm == 0:
        return None

    return embedding / norm


# Get face embeddings
def get_face_embeddings(image):

    image = image_to_numpy(image)

    if image is None:
        return []

    model = load_face_model()

    faces = model.get(image)

    embeddings = []

    for face in faces:

        embedding = normalize_embedding(
            face.embedding
        )

        if embedding is not None:
            embeddings.append(embedding)

    return embeddings


# Parse stored embedding
def parse_embedding(value):

    if value is None:
        return []

    if isinstance(value, np.ndarray):

        if value.ndim == 1:

            embedding = normalize_embedding(value)

            if embedding is not None:
                return [embedding]

            return []

        embeddings = []

        for item in value:

            embedding = normalize_embedding(item)

            if embedding is not None:
                embeddings.append(embedding)

        return embeddings

    if isinstance(value, list):

        if not value:
            return []

        if isinstance(
            value[0],
            (int, float)
        ):

            embedding = normalize_embedding(value)

            if embedding is not None:
                return [embedding]

            return []

        embeddings = []

        for item in value:

            embedding = normalize_embedding(item)

            if embedding is not None:
                embeddings.append(embedding)

        return embeddings

    if isinstance(value, str):

        try:

            parsed = json.loads(value)

        except Exception:

            try:

                parsed = ast.literal_eval(value)

            except Exception:

                return []

        return parse_embedding(parsed)

    return []


# Calculate cosine similarity
def cosine_similarity(
    embedding1,
    embedding2
):

    embedding1 = normalize_embedding(
        embedding1
    )

    embedding2 = normalize_embedding(
        embedding2
    )

    if embedding1 is None:
        return -1

    if embedding2 is None:
        return -1

    if embedding1.shape != embedding2.shape:
        return -1

    return float(
        np.dot(
            embedding1,
            embedding2
        )
    )


# Get registered students
@st.cache_data(ttl=60)
def get_student_embeddings():

    response = (
        supabase
        .table("students")
        .select(
            "student_id,name,face_embedding"
        )
        .execute()
    )

    students = []

    for student in response.data:

        embeddings = parse_embedding(
            student.get("face_embedding")
        )

        if not embeddings:
            continue

        students.append(
            {
                "student_id": student.get(
                    "student_id"
                ),
                "name": student.get(
                    "name"
                ),
                "embeddings": embeddings
            }
        )

    return students


# Find best matching student
def match_face(
    query_embedding,
    students,
    threshold=0.48,
    margin=0.05
):

    query_embedding = normalize_embedding(
        query_embedding
    )

    if query_embedding is None:
        return None

    candidates = []

    for student in students:

        similarities = []

        for stored_embedding in student["embeddings"]:

            similarity = cosine_similarity(
                query_embedding,
                stored_embedding
            )

            if similarity >= 0:
                similarities.append(
                    similarity
                )

        if not similarities:
            continue

        similarities.sort(
            reverse=True
        )

        best_similarity = similarities[0]

        if len(similarities) >= 2:

            score = (
                similarities[0] * 0.7
                + similarities[1] * 0.3
            )

        else:

            score = best_similarity

        candidates.append(
            {
                "student_id": student["student_id"],
                "name": student["name"],
                "similarity": best_similarity,
                "score": score
            }
        )

    if not candidates:
        return None

    candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    best = candidates[0]

    if best["score"] < threshold:
        return None

    if len(candidates) > 1:

        difference = (
            best["score"]
            - candidates[1]["score"]
        )

        if difference < margin:
            return None

    return best


# Check whether face is already registered
def check_duplicate_face(
    face_embedding,
    threshold=0.48
):

    students = get_student_embeddings()

    if not students:
        return None

    match = match_face(
        face_embedding,
        students,
        threshold=threshold,
        margin=0
    )

    return match


# Predict attendance
def predict_attendance(
    image,
    threshold=0.48
):

    image_array = image_to_numpy(image)

    if image_array is None:
        return {}, [], 0

    model = load_face_model()

    faces = model.get(image_array)

    num_faces = len(faces)

    if num_faces == 0:
        return {}, [], 0

    students = get_student_embeddings()

    detected = {}

    all_ids = []

    for face in faces:

        embedding = normalize_embedding(
            face.embedding
        )

        if embedding is None:
            continue

        match = match_face(
            embedding,
            students,
            threshold=threshold
        )

        if match is None:
            continue

        student_id = match["student_id"]

        detected[student_id] = {
            "student_id": student_id,
            "name": match["name"],
            "similarity": round(
                match["similarity"],
                4
            ),
            "score": round(
                match["score"],
                4
            )
        }

        all_ids.append(student_id)

    return detected, all_ids, num_faces


# Refresh student embeddings
def train_classifier():

    get_student_embeddings.clear()

    return get_student_embeddings()


# Clear student embedding cache
def clear_face_cache():

    get_student_embeddings.clear()