import os

# 🔥 Get project root dynamically
CURRENT_DIR = os.path.dirname(__file__)

# core/tools → go up 2 levels → project root
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def file_reader(file_name: str):
    try:
        file_path = os.path.join(DATA_DIR, file_name)

        print("📂 Trying path:", file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "file_path": file_path,
            "content": content[:2000]
        }

    except Exception as e:
        return {
            "error": str(e)
        }