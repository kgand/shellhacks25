# -------------------------------
# Transcriber Functions
# -------------------------------


async def transcribe_audio(audio_frames: list[float]) -> dict[str, any]:
    if not audio_frames:
        return {"transcript": "", "confidence": 0.0}

    transcript = await simulate_transcription(audio_frames)
    confidence = 0.9
    return {
        "transcript": transcript,
        "confidence": confidence,
        "timestamp": datetime.utcnow().isoformat(),
    }


async def simulate_transcription(audio_frames: list[float]) -> str:
    return "This is a simulated transcription of the audio content."


# -------------------------------
# Summarizer Functions
# -------------------------------


async def summarize_conversation(utterances: list[dict]) -> dict[str, any]:
    if not utterances:
        return {"summary": "", "key_points": []}

    summary = await generate_summary(utterances)
    key_points = await extract_key_points(utterances)
    return {
        "summary": summary,
        "key_points": key_points,
        "timestamp": datetime.utcnow().isoformat(),
    }


async def generate_summary(utterances: list[dict]) -> str:
    return "This is a simulated summary of the conversation."


async def extract_key_points(utterances: list[dict]) -> list[str]:
    return ["Key point 1", "Key point 2", "Key point 3"]


# -------------------------------
# Action Planner Functions
# -------------------------------


async def extract_actions(utterances: list[dict]) -> dict[str, any]:
    if not utterances:
        return {"actions": []}

    actions = await _extract_actions_internal(utterances)
    return {"actions": actions, "timestamp": datetime.utcnow().isoformat()}


async def _extract_actions_internal(utterances: list[dict]) -> list[dict]:
    return [
        {
            "description": "Follow up on discussed topic",
            "owner": "user",
            "due_hint": "next week",
            "priority": "medium",
        }
    ]


# -------------------------------
# Relationship Miner Functions
# -------------------------------


async def extract_relationships(utterances: list[dict]) -> dict[str, any]:
    if not utterances:
        return {"relationships": []}

    relationships = await _extract_relationships_internal(utterances)
    return {"relationships": relationships, "timestamp": datetime.utcnow().isoformat()}


async def _extract_relationships_internal(utterances: list[dict]) -> list[dict]:
    return [
        {
            "person1": "Alice",
            "person2": "Bob",
            "relationship_type": "colleague",
            "evidence": "mentioned working together",
        }
    ]


# -------------------------------
# Store Insights Function
# -------------------------------


async def store_insights(insights: dict[str, any]) -> bool:
    """Store insights to Firestore DB (stub)"""
    # This will use your GOOGLE_APPLICATION_CREDENTIALS env variable for auth
    db = firestore.Client()
    # Auto-generated document ID
    doc_ref = db.collection("people_insights").document()  # random ID
    doc_ref.set(insights)
