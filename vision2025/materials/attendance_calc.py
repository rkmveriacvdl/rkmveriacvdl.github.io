import os
import re
from collections import defaultdict

def parse_attendance(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    student_data = []
    record_started = False
    
    for line in lines:
        if "Name" in line and "Roll Number" in line:
            record_started = True
            continue
        if record_started and "----" in line:
            continue
        if record_started and line.strip():
            parts = re.split(r'\s{2,}', line.strip())
            if len(parts) == 5:  # Ensuring valid student entry
                name, dept, roll, status_type, presence = parts
                student_data.append((name, roll, status_type, dept, presence))
    
    return student_data

def compute_attendance():
    attendance_records = defaultdict(lambda: {"name": "", "department": "", "status_type": "", "present": 0, "total": 0})
    
    for folder in os.listdir():
        if re.match(r"Lecture\d+", folder) and os.path.isdir(folder):
            file_path = os.path.join(folder, "attendance.txt")
            if os.path.exists(file_path):
                student_data = parse_attendance(file_path)
                for name, roll, status_type, dept, presence in student_data:
                    attendance_records[roll]["name"] = name
                    attendance_records[roll]["department"] = dept
                    attendance_records[roll]["status_type"] = status_type
                    attendance_records[roll]["total"] += 1
                    if presence.lower() == "present":
                        attendance_records[roll]["present"] += 1
    
    sorted_attendance = sorted(attendance_records.items(), key=lambda x: (x[1]["present"] / x[1]["total"]), reverse=True)
    
    print(f"{'Name':<25} {'Roll Number':<15} {'Credit/Audit':<15} {'Department':<15} {'Attendance %':<15}")
    print("-" * 85)
    for roll, stats in sorted_attendance:
        percentage = (stats["present"] / stats["total"]) * 100
        print(f"{stats['name']:<25} {roll:<15} {stats['status_type']:<15} {stats['department']:<15} {percentage:<14.2f}%")

if __name__ == "__main__":
    compute_attendance()
