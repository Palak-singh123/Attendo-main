from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    try:
        if not audio_bytes:
            st.error("No voice recording received.")
            return None

        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True
        )

        if audio is None or len(audio) == 0:
            st.error("Recorded audio is empty.")
            return None

        duration = len(audio) / sr

        if duration < 1.0:
            st.error("Voice recording is too short. Please record for at least 1 second.")
            return None

        wav = preprocess_wav(
            audio,
            source_sr=sr
        )

        if wav is None or len(wav) == 0:
            st.error("Could not process the voice recording.")
            return None

        embedding = encoder.embed_utterance(wav)

        if embedding is None:
            st.error("Voice embedding could not be generated.")
            return None

        embedding = np.asarray(
            embedding,
            dtype=np.float32
        )

        if not np.all(np.isfinite(embedding)):
            st.error("Invalid voice embedding generated.")
            return None

        return embedding.tolist()

    except Exception as e:
        st.error(f"Voice recognition error: {e}")
        return None


def identify_speaker(
    new_embedding,
    candidates_dict,
    threshold=0.65
):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    new_embedding = np.asarray(
        new_embedding,
        dtype=np.float32
    )

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():

        if not stored_embedding:
            continue

        stored_embedding = np.asarray(
            stored_embedding,
            dtype=np.float32
        )

        similarity = float(
            np.dot(new_embedding, stored_embedding)
        )

        if similarity > best_score:
            best_score = similarity
            best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(
    audio_bytes,
    candidates_dict,
    threshold=0.65
):
    try:
        if not audio_bytes:
            st.error("No classroom audio received.")
            return {}

        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True
        )

        if audio is None or len(audio) == 0:
            st.error("Classroom audio is empty.")
            return {}

        segments = librosa.effects.split(
            audio,
            top_db=30
        )

        identified_results = {}

        for start, end in segments:

            if (end - start) < sr * 0.5:
                continue

            segment_audio = audio[start:end]

            wav = preprocess_wav(
                segment_audio,
                source_sr=sr
            )

            if wav is None or len(wav) == 0:
                continue

            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(
                embedding,
                candidates_dict,
                threshold
            )

            if sid:
                if (
                    sid not in identified_results
                    or score > identified_results[sid]
                ):
                    identified_results[sid] = score

        return identified_results

    except Exception as e:
        st.error(f"Bulk voice processing error: {e}")
        return {}