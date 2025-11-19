import os

def save_files_to_generator_folder(html: str, js: str, backend_code: str):
    base_path = "generator/"
    os.makedirs(base_path, exist_ok=True)
    os.makedirs(os.path.join(base_path, "api"), exist_ok=True)

    # HTML / JS
    with open(os.path.join(base_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(base_path, "app.js"), "w", encoding="utf-8") as f:
        f.write(js)

    # Backend 함수
    with open(os.path.join(base_path, "api/server.py"), "w", encoding="utf-8") as f:
        f.write(backend_code)
