import json
import os
import glob


def load_lesson(filepath: str) -> dict | None:
    """Load a single lesson JSON file. Returns None on error."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[utils] Lesson file not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"[utils] Invalid JSON in {filepath}: {e}")
        return None


def load_all_lessons(directory: str) -> list[dict]:
    """
    Scan directory for *.json files, load each as a lesson.
    Returns a list of lesson dicts sorted alphabetically by title.
    Invalid or missing files are skipped with a console warning.
    """
    pattern = os.path.join(directory, "*.json")
    paths = glob.glob(pattern)

    lessons = []
    for path in paths:
        lesson = load_lesson(path)
        if lesson is not None:
            # Ensure each lesson has a fallback id derived from its filename
            if "id" not in lesson:
                lesson["id"] = os.path.splitext(os.path.basename(path))[0]
            lessons.append(lesson)

    lessons.sort(key=lambda l: l.get("title", "").lower())
    return lessons
