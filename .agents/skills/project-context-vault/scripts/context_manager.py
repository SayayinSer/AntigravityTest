import os
import json
import shutil
from datetime import datetime
import argparse

def get_session_path(conversation_id, app_data_dir):
    return os.path.join(app_data_dir, "brain", conversation_id)

def save_context(project_root, session_path):
    context_dir = os.path.join(project_root, ".context")
    if not os.path.exists(context_dir):
        os.makedirs(context_dir)
    
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "milestone": "Active Development",
        "tasks": {"completed": [], "pending": [], "in_progress": []},
        "errors": [],
        "last_files": [],
        "session_id": os.path.basename(session_path)
    }

    # Try to extract tasks from task.md
    task_file = os.path.join(session_path, "task.md")
    if os.path.exists(task_file):
        with open(task_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("- [x]"):
                    snapshot["tasks"]["completed"].append(line[5:].strip())
                elif line.startswith("- [/]"):
                    snapshot["tasks"]["in_progress"].append(line[5:].strip())
                elif line.startswith("- [ ]"):
                    snapshot["tasks"]["pending"].append(line[5:].strip())

    # Save to JSON
    snapshot_path = os.path.join(context_dir, "last_snapshot.json")
    with open(snapshot_path, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=4)
    
    # Backup task board
    if os.path.exists(task_file):
        shutil.copy(task_file, os.path.join(context_dir, "task_board.md"))

    print(f"Context saved to {snapshot_path}")

def load_context(project_root, session_path):
    context_dir = os.path.join(project_root, ".context")
    snapshot_path = os.path.join(context_dir, "last_snapshot.json")
    
    if not os.path.exists(snapshot_path):
        print("No context snapshot found.")
        return

    with open(snapshot_path, 'r', encoding='utf-8') as f:
        snapshot = json.load(f)
    
    # Restore task.md
    task_board_path = os.path.join(context_dir, "task_board.md")
    if os.path.exists(task_board_path):
        os.makedirs(session_path, exist_ok=True)
        shutil.copy(task_board_path, os.path.join(session_path, "task.md"))
        print(f"Tasks restored to session {snapshot['session_id']}")
    
    print(f"Context loaded. Last activity: {snapshot['timestamp']}")
    print(f"Pending tasks: {len(snapshot['tasks']['pending'])}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["save", "load", "add-error"])
    parser.add_argument("--project", required=True)
    parser.add_argument("--session", required=True)
    parser.add_argument("--message", help="Error message to log")
    args = parser.parse_args()

    if args.action == "save":
        save_context(args.project, args.session)
    elif args.action == "load":
        load_context(args.project, args.session)
    elif args.action == "add-error":
        context_dir = os.path.join(args.project, ".context")
        snapshot_path = os.path.join(context_dir, "last_snapshot.json")
        if os.path.exists(snapshot_path):
            with open(snapshot_path, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data["errors"].append({
                    "timestamp": datetime.now().isoformat(),
                    "message": args.message
                })
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            print(f"Error logged: {args.message}")
