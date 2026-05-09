import os

def file_reader(file_path):
    try:
        base_path = os.path.abspath("data")
        full_path = os.path.join(base_path, file_path)

        print("📂 Trying path:", full_path)

        if not os.path.exists(full_path):
            return {"error": f"File not found: {full_path}"}

        with open(full_path, "r") as f:
            content = f.read()

        return {
            "type": "file",
            "content": content,
            "metadata": {"path": full_path}
        }

    except Exception as e:
        return {"error": str(e)}