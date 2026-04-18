from tkinter import *
from tkinter import ttk

from db import insert_student, delete_student

WIDTH = 800
HEIGHT = 600
DEF_FONT = "Inter"

rootWindow = Tk()
status_after_id = None

def clear_status():
    global status_after_id
    status_label.config(text="")
    status_after_id = None


def set_status(text, fg):
    global status_after_id
    status_label.config(text=text, fg=fg)
    if status_after_id:
        rootWindow.after_cancel(status_after_id)
    status_after_id = rootWindow.after(2500, clear_status)


def hide_all_frames():
    dashboard_frame.pack_forget()
    student_frame.pack_forget()
    delete_frame.pack_forget()
    view_frame.pack_forget()

def show_dashboard():
    hide_all_frames()
    dashboard_frame.pack(fill="both", expand=True)

def show_student():
    hide_all_frames()
    student_frame.pack(fill="both", expand=True)

def show_delete():
    hide_all_frames()
    delete_frame.pack(fill="both", expand=True)

def show_view():
    set_status("View is not available yet.", "#ff5555")

def make_back_button(parent):
    return Button(
        parent,
        text="Back",
        font=(DEF_FONT, 12, "bold"),
        bg="#ff5555",
        fg="#ffffff",
        bd=1,
        padx=15,
        pady=6,
        command=show_dashboard,
    )

def handle_submit():
    for entry in entries.values():
        if not entry.get().strip():
            set_status("All fields are required!", "#ff5555")
            return

    try:
        reg_no = entries["Register No"].get().strip()
        name = entries["Name"].get().strip()
        age = int(entries["Age"].get().strip())
        marks = float(entries["Marks"].get().strip())
        cgpa = float(entries["CGPA"].get().strip())
        grade = entries["Grade"].get().strip()

        success, msg = insert_student(
            reg_no, name, age, marks, cgpa, grade
        )

        if success:
            set_status(msg, "#50fa7b")

            for e in entries.values():
                e.delete(0, END)

        else:
            set_status(msg, "#ff5555")

    except ValueError:
        set_status("Invalid input type!", "#ff5555")

scr_width = rootWindow.winfo_screenwidth()
scr_height = rootWindow.winfo_screenheight()

xcord = (scr_width - WIDTH) // 2
ycord = (scr_height - HEIGHT) // 2

newGeometry = f"{WIDTH}x{HEIGHT}+{xcord}+{ycord}"

rootWindow.title("Student Management System")
rootWindow.geometry(newGeometry)
rootWindow.resizable(False, False)
rootWindow.configure(bg="#1e1e2f")

header_frame = Frame(rootWindow, bg="#2c2f4a", height=30)
dashboard_frame = Frame(rootWindow, bg="#1e1e2f")
student_frame = Frame(rootWindow, bg="#282a36")
delete_frame = Frame(rootWindow, bg="#282a36")
view_frame = Frame(rootWindow, bg="#282a36")

header_frame.pack(fill="x", side="top")

Label(
    header_frame,
    text="Student Management",
    font=(DEF_FONT, 18, "bold"),
    bg="#2c2f4a",
    fg="#ffffff",
).pack(pady=15)

status_label = Label(
    rootWindow,
    text="",
    bg="#1e1e2f",
    fg="#ffffff",
    font=(DEF_FONT, 11),
)
status_label.pack(pady=6)

# main dashboard
dashboard_frame.pack(fill="both", expand=True)

Label(
    dashboard_frame,
    text='''Welcome to the Dashboard!
    Manage and organize student records with ease.''',
    font=(DEF_FONT, 22, "italic"),
    bg="#1e1e2f",
    fg="#ffffff"
).pack(pady=80)

button_frame = Frame(dashboard_frame, bg="#1e1e2f")
button_frame.pack(pady=20)

# dashboard - buttons
Button(
    button_frame,
    text="+ Add Student",
    font=(DEF_FONT, 12, "bold"),
    bg="#4CAF50",
    fg="#ffffff",
    padx=16,
    pady=8,
    bd=1,
    command=show_student
).grid(row=0, column=0, padx=10)

Button(
    button_frame,
    text="- Delete Student",
    font=(DEF_FONT, 12, "bold"),
    bg="#ff5555",
    fg="#ffffff",
    padx=16,
    pady=8,
    bd=1,
    command=show_delete
).grid(row=0, column=1, padx=10)

Button(
    button_frame,
    text="% View Students",
    font=(DEF_FONT, 12, "bold"),
    bg="#14b8a6",
    fg="#ffffff",
    padx=16,
    pady=8,
    bd=1,
    command=show_view
).grid(row=1, column=0, columnspan=2, pady=20)

########################

# student area (add records)
Label(
    student_frame,
    text="New Student",
    font=(DEF_FONT, 22, "bold"),
    bg="#282a36",
    fg="#ffffff",
).pack(pady=25)


form_container = Frame(student_frame, bg="#21222c", bd=0)
form_container.pack()

form_box = Frame(form_container, bg="#f8f8f2", padx=25, pady=25)
form_box.pack()

fields = [
    "Register No",
    "Name",
    "Age",
    "Marks",
    "CGPA",
    "Grade"
]

entries = {}

# all the fields which are required for student record
for i, field in enumerate(fields):
    Label(
        form_box,
        text=field,
        font=(DEF_FONT, 11, "bold"),
        bg="#f8f8f2",
        fg="#2c3e50"
    ).grid(row=i, column=0, sticky="w", pady=8, padx=10)

    entry = Entry(
        form_box,
        font=(DEF_FONT, 11),
        width=28,
        bd=1,
        relief="solid"
    )
    entry.grid(row=i, column=1, pady=8, padx=10)

    entries[field] = entry

button_row = Frame(form_box, bg="#f8f8f2")
button_row.grid(row=len(fields), column=0, columnspan=2, pady=20)

Button(
    button_row,
    text="Submit",
    font=(DEF_FONT, 12, "bold"),
    bg="#50fa7b",
    fg="#000000",
    bd=1,
    padx=15,
    pady=6,
    command=handle_submit
).pack(side="left", padx=8)

make_back_button(button_row).pack(side="left", padx=8)

#########################

# student area - delete records
Label(
    delete_frame,
    text="Remove Student",
    font=(DEF_FONT, 22, "bold"),
    bg="#282a36",
    fg="#ffffff",
).pack(pady=25)

field_map = {
    "Register No": "regno",
    "Name": "name",
    "Age": "age",
    "Marks": "marks",
    "CGPA": "cgpa",
    "Grade": "grade",
}

delete_checks = {}
delete_entries = {}

delete_box = Frame(
    delete_frame, 
    bg="#f8f8f2", 
    padx=25, 
    pady=20
)
delete_box.pack()

for i, field in enumerate(field_map):
    var = IntVar(value=0)
    Checkbutton(
        delete_box,
        text=field,
        variable=var,
        onvalue=1,
        offvalue=0,
        bg="#f8f8f2",
        fg="#2c3e50",
        selectcolor="#f8f8f2",
        font=(DEF_FONT, 11, "bold"),
    ).grid(row=i, column=0, sticky="w", pady=8, padx=10)
    delete_checks[field] = var

    entry = Entry(
        delete_box,
        font=(DEF_FONT, 11),
        width=28,
        bd=1,
        relief="solid",
    )
    entry.grid(row=i, column=1, pady=8, padx=10)
    delete_entries[field] = entry


def handle_delete():
    criteria = {}
    for field, column in field_map.items():
        if delete_checks[field].get():
            value = delete_entries[field].get().strip()
            if not value:
                set_status(f"{field} selected but empty", "#ff5555")
                return
            if field == "Age":
                value = int(value)
            elif field in ("Marks", "CGPA"):
                value = float(value)
            criteria[column] = value

    if not criteria:
        set_status("Select fields and enter values", "#ff5555")
        return

    success, msg = delete_student(criteria)
    if success:
        set_status(msg, "#50fa7b")
    else:
        set_status(msg, "#ff5555")

button_row = Frame(delete_box, bg="#f8f8f2")
button_row.grid(row=len(field_map), column=0, columnspan=2, pady=20)

Button(
    button_row,
    text="Delete",
    font=(DEF_FONT, 12, "bold"),
    bg="#ff5555",
    fg="#ffffff",
    bd=1,
    padx=15,
    pady=6,
    command=handle_delete,
).pack(side="left", padx=8)

make_back_button(button_row).pack(side="left", padx=8)
