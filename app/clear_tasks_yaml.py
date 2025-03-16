import os
import re

yaml_path = os.path.join(os.path.dirname(__file__), "tasks.yaml")

with open(yaml_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

cleaned_lines = [line for line in lines if re.match(r"^\s*#", line) or line.strip() == ""]

with open(yaml_path, "w", encoding="utf-8") as file:
    file.writelines(cleaned_lines)

print("tasks.yaml cleared, comments preserved!")
