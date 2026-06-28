import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from core.memory_engine import MemoryEngine

chat_file = os.path.join(PROJECT_ROOT, "input_chat.txt")

if not os.path.exists(chat_file):
    print("❌ input_chat.txt not found")
    raise SystemExit(1)

with open(chat_file, "r", encoding="utf-8") as f:
    text = f.read()

engine = MemoryEngine(text)
result = engine.extract()

print("\n🧠 PIPELINE RESULT\n")
print(result)

memory_dir = os.path.join(PROJECT_ROOT, "memory")
os.makedirs(memory_dir, exist_ok=True)

latest_path = os.path.join(memory_dir, "latest.md")

with open(latest_path, "w", encoding="utf-8") as f:
    f.write("# CRME Latest Memory\n\n")
    f.write(str(result))

print("\n✔ latest.md updated")


