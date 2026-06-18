import json, os

REPO = "/workspaces/itc-apne-prep"

def load_json(path):
    full = os.path.join(REPO, path)
    if not os.path.exists(full):
        return None
    with open(full, encoding="utf-8") as f:
        return json.load(f)

# ... (باقي الكود مطابق تماماً لآخر build_live.py) ...
