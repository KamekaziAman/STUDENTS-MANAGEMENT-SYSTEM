# ====================================================STUDENTS MANAGEMENT SYSTEM====================================================
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Function to fetch data from the database
def fetch_data():
    con = None
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="21664391",
            database="studentdb"
        )
        curr = con.cursor()
        curr.execute("SELECT * FROM data")
        rows = curr.fetchall()
        if len(rows) != 0:
            student_table.delete(*student_table.get_children())
            for row in rows:
                student_table.insert('', tk.END, values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
    finally:
        if con and con.is_connected():
            con.close()

def add_func():
    # Validate inputs
    if rollno_ent.get().strip() == "" or not rollno_ent.get().isdigit():
        messagebox.showerror("Error", "Roll Number must be a valid number!")
        return
    if name_ent.get().strip() == "" or course_ent.get().strip() == "":
        messagebox.showerror("Error", "Please fill all the fields!")
        return

    # Get the date of birth directly from the entry as a string
    dob = dob_ent.get().strip()  # Just like any other entry

    try:
        # Insert data into the database
        con = mysql.connector.connect(
            host="localhost", user="root", password="21664391", database="studentdb"
        )
        curr = con.cursor()
        curr.execute(
            "INSERT INTO data (rollno, name, course, phoneno, emailid, fathersname, address, gender, dob) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                int(rollno_ent.get().strip()),
                name_ent.get().strip(),
                course_ent.get().strip(),
                phoneno_ent.get().strip(),
                emailid_ent.get().strip(),
                fathersname_ent.get().strip(),
                address_ent.get().strip(),
                gender_combobox.get(),
                dob,
            )
        )
        con.commit()
        fetch_data()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Failed to insert data into database. Error: {e}")
    finally:
        if con.is_connected():
            con.close()
            
def clear_entries():
    rollno_ent.delete(0, tk.END)
    name_ent.delete(0, tk.END)
    course_ent.delete(0, tk.END)
    phoneno_ent.delete(0, tk.END)
    emailid_ent.delete(0, tk.END)
    fathersname_ent.delete(0, tk.END)
    address_ent.delete(0, tk.END)
    dob_ent.delete(0, tk.END)  # Clear the date of birth entry

    # Reset the gender combobox to its default value
    gender_combobox.set("Select Gender")
    
def fetch_cursor(event):
    cursor_row = student_table.focus()
    content = student_table.item(cursor_row)
    row = content["values"]
    rollno.set(row[0])
    name.set(row[1])
    course.set(row[2])
    phoneno.set(row[3])
    emailid.set(row[4])
    fathersname.set(row[5])
    address.set(row[6])
    gender.set(row[7])
    dob.set(row[8])

def update_func():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="21664391",
            database="studentdb"
        )
        curr = con.cursor()
        curr.execute(
            "UPDATE data SET name=%s, course=%s, phoneno=%s, emailid=%s, fathersname=%s, address=%s, gender=%s, dob=%s WHERE rollno=%s",
            (
                name_ent.get(),
                course_ent.get(),
                phoneno_ent.get(),
                emailid.get(),
                fathersname_ent.get(),
                address_ent.get(),
                gender_combobox.get(),
                dob_ent.get(),
                rollno_ent.get()
            )
        )
        con.commit()
        messagebox.showinfo("Success", "Student record updated successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to update data. Error: {err}")
    finally:
        con.close()
        fetch_data()
        clear_entries()
        
def fetch_cursor2(event=None):
    selected_item = student_table.focus()
    row_data = student_table.item(selected_item, 'values')
    if row_data:
        message = (
            f"Roll No: {row_data[0]}\n"
            f"Name: {row_data[1]}\n"
            f"Course: {row_data[2]}\n"
            f"Phone No: {row_data[3]}\n"
            f"Email ID: {row_data[4]}\n"
            f"Father's Name: {row_data[5]}\n"
            f"Address: {row_data[6]}\n"
            f"Gender: {row_data[7]}\n"
            f"D.O.B: {row_data[8]}"
        )
        messagebox.showinfo("Student Details", message)
        
def delete_row():
    selected_item = student_table.focus()
    if selected_item:
        rollno_to_delete = student_table.item(selected_item, 'values')[0]
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="21664391",
                database="studentdb"
            )
            curr = con.cursor()
            curr.execute("DELETE FROM data WHERE rollno = %s", (rollno_to_delete,))
            con.commit()
            student_table.delete(selected_item)
            messagebox.showinfo("Success", "Record deleted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete data. Error: {err}")
        finally:
            con.close()
    else:
        messagebox.showerror("Error", "Please select a row to delete.")

def search_student():
    search_by = selected_value.get().lower()  # Get the search criteria
    search_value = search_entry.get().strip()  # Get the search term and strip whitespace
    if search_value == "":
        messagebox.showerror("Error", "Please enter a search term.")
        return
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="21664391",
            database="studentdb"
        )
        curr = con.cursor()
        # Enclose the search_by variable in backticks to avoid syntax errors
        query = f"SELECT * FROM data WHERE `{search_by}` LIKE %s"  
        curr.execute(query, ('%' + search_value + '%',))  # Use parameterized query
        results = curr.fetchall()
        
        # Clear the Treeview before displaying new results
        for row in student_table.get_children():
            student_table.delete(row)
        
        # Insert the search results into the Treeview
        for row in results:
            student_table.insert("", "end", values=row)
        
        # Inform the user if no results were found
        if len(results) == 0:
            messagebox.showinfo("No Results", f"No results found for {search_by}: {search_value}.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"An error occurred while searching: {err}")
    finally:
        if con.is_connected():
            con.close()  # Ensure the connection is closed

def show_all_students():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="21664391",
            database="studentdb"
        )
        curr = con.cursor()
        curr.execute("SELECT * FROM data")
        results = curr.fetchall()
        
        # Clear the Treeview before displaying all results
        for row in student_table.get_children():
            student_table.delete(row)
        
        # Insert all student records into the Treeview
        for row in results:
            student_table.insert("", "end", values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"An error occurred while fetching all students: {err}")
    finally:
        if con.is_connected():
            con.close()  # Ensure the connection is closed
        

# Main application code
root = tk.Tk()
root.title("Student Management System")
root.iconbitmap("icon.ico")
root.geometry("1280x650")
root.resizable(False, False)

#============ variable ===============
rollno = tk.StringVar()
name = tk.StringVar()
course = tk.StringVar()
phoneno = tk.StringVar()
emailid = tk.StringVar()
fathersname = tk.StringVar()
address = tk.StringVar()
gender = tk.StringVar()
dob = tk.StringVar()
selected_value = tk.StringVar()

# =========== LABEL ==================
title_label = tk.Label(root, text="Student Management System by Kamekazi ⭐", font=("Ariel", 30, "bold"), border=12, relief=tk.GROOVE, bg="lightgrey")
title_label.pack(side=tk.TOP, fill=tk.X)

# =========== Frames =================
detail_frame = tk.LabelFrame(root, text="Enter Details", font=("Ariel", 20), bd=12, relief=tk.GROOVE, bg="lightgrey")
detail_frame.place(x=20, y=90, width=420, height=545)

data_frame = tk.Frame(root, bd=12, bg="lightgrey", relief=tk.GROOVE)
data_frame.place(x=460, y=90, width=800, height=545)

btn_frame = tk.Frame(detail_frame, bg="lightgrey", bd=10, relief=tk.GROOVE)
btn_frame.place(x=20, y=400, width=345, height=75)

#=========== Entry ==================
rollno_lbl = tk.Label(detail_frame, text="Roll No", font=("Ariel", 15), bg="lightgrey")
rollno_lbl.grid(row=0, column=0, padx=2, pady=2)

rollno_ent = tk.Entry(detail_frame, bd=7, font=("Ariel", 15), textvariable=rollno)
rollno_ent.grid(row=0, column=1, padx=2, pady=2)

name_lbl = tk.Label(detail_frame, text="Name", font=("Ariel", 15), bg="lightgrey")
name_lbl.grid(row=1, column=0, padx=2, pady=2)

name_ent = tk.Entry(detail_frame, bd=7, font=("Ariel", 15), textvariable=name)
name_ent.grid(row=1, column=1, padx=2, pady=2)

# Entry for Course
course_lbl = tk.Label(detail_frame, text="Course", font=("Ariel", 15), bg="lightgrey")
course_lbl.grid(row=2, column=0, padx=2, pady=2)

course_ent = tk.Entry(detail_frame, bd=7, font=("Ariel", 15), textvariable=course)
course_ent.grid(row=2, column=1, padx=2, pady=2)

# Entry for Phone No
phoneno_lbl = tk.Label(detail_frame, text="Phone No", font=("Ariel", 15), bg="lightgrey")
phoneno_lbl.grid(row=3, column=0, padx=2, pady=2)

phoneno_ent = tk.Entry(detail_frame, bd=7, font=("Ariel", 15), textvariable=phoneno)
phoneno_ent.grid(row=3, column=1, padx=2, pady=2)

# Entry for Email ID
emailid_lbl = tk.Label(detail_frame, text="Email ID", font=("Ariel", 15), bg="lightgrey")
emailid_lbl.grid(row=4, column=0, padx=2, pady=2)

emailid_ent = tk.Entry(detail_frame, bd=7, font=("Ariel", 15), textvariable=emailid)
emailid_ent.grid(row=4, column=1, padx=2, pady=2)

# Entry for Father's Name
father_lbl = tk.Label(detail_frame, text="Father's Name", font=("Ariel", 15), bg="lightgrey")
father_lbl.grid(row=5, column=0, padx=2, pady=2)

fathersname_ent = tk.Entry(detail_frame, bd=7, font=("Ariel", 15), textvariable=fathersname)
fathersname_ent.grid(row=5, column=1, padx=2, pady=2)

# Entry for Address
address_lbl = tk.Label(detail_frame, text="Address", font=("Ariel", 15), bg="lightgrey")
address_lbl.grid(row=6, column=0, padx=2, pady=2)

address_ent = tk.Entry(detail_frame, bd=7, font=("Ariel", 15), textvariable=address)
address_ent.grid(row=6, column=1, padx=2, pady=2)

# Gender Combobox
gender_lbl = tk.Label(detail_frame, text="Gender", font=("Ariel", 15), bg="lightgrey")
gender_lbl.grid(row=7, column=0, padx=2, pady=2)

gender_combobox = ttk.Combobox(detail_frame, textvariable=gender, font=("Ariel", 14,))
gender_combobox['values'] = ("MALE", "FEMALE", "Others")
gender_combobox['state'] = 'readonly'
gender_combobox.grid(row=7, column=1, padx=2, pady=2)
gender_combobox.set("Select Gender")

# Entry for Date of Birth
dob_lbl = tk.Label(detail_frame, text="D.O.B", font=("Ariel", 15), bg="lightgrey")
dob_lbl.grid(row=8, column=0, padx=2, pady=2)

dob_ent = tk.Entry(detail_frame, bd=7, font=("Ariel", 15), textvariable=dob)
dob_ent.grid(row=8, column=1, padx=2, pady=2)

# =============== Buttons =======================
submit_btn = tk.Button(btn_frame, text="Submit", font=("Ariel", 12), command=add_func)
submit_btn.grid(row=2, column=0, padx=10, pady=10)

update_btn = tk.Button(btn_frame, text="Update", font=("Ariel", 12), command=update_func)
update_btn.grid(row=2, column=1, padx=10, pady=10)

delete_btn = tk.Button(btn_frame, text="Delete", font=("Ariel", 12), command=delete_row)
delete_btn.grid(row=2, column=2, padx=10, pady=10)

clear_btn = tk.Button(btn_frame, text="Clear", font=("Ariel", 12), command=clear_entries)
clear_btn.grid(row=2, column=3, padx=10, pady=10)

# =============== Search Section ===================
search_frame = tk.Frame(data_frame, bg="lightgrey", bd=10)
search_frame.place(x=10, y=20, width=760, height=50)

search_lbl = tk.Label(search_frame, text="Search By:", font=("Ariel", 15), bg="lightgrey")
search_lbl.grid(row=0, column=0, padx=5, pady=5)


search_combo = ttk.Combobox(search_frame, font=("Ariel", 14), textvariable=selected_value, state="readonly", width=12)
search_combo['values'] = ("rollno", "name", "course", "phoneno", "emailid", "fathersname", "address", "gender", "dob")
search_combo.grid(row=0, column=1, padx=5, pady=5)
search_combo.set("rollno")


search_entry = tk.Entry(search_frame, font=("Ariel", 12), bd=7, width=24)
search_entry.grid(row=0, column=2, padx=5, pady=5)

search_btn = tk.Button(search_frame, text="Search", font=("Ariel", 12), width=10, command=search_student)
search_btn.grid(row=0, column=3, padx=5, pady=5)

show_all_btn = tk.Button(search_frame, text="Show All", font=("Ariel", 12), width=10, command=show_all_students)
show_all_btn.grid(row=0, column=4, padx=5, pady=5)

# ============ Treeview for Data ==================
main_frame = tk.Frame(data_frame, bg="lightgrey", bd=10)
main_frame.place(x=20, y=90, width=740, height=430)

y_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
x_scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)

student_table = ttk.Treeview(
    main_frame,
    columns=("Roll No", "Name", "Course", "Phone no", "Email ID", "Father's Name", "Address", "Gender", "D.O.B"),
    yscrollcommand=y_scroll.set,
    xscrollcommand=x_scroll.set,
)

y_scroll.config(command=student_table.yview)
x_scroll.config(command=student_table.xview)

y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

student_table.pack(fill=tk.BOTH, expand=True)

# Setting headings for columns
for col in student_table["columns"]:
    student_table.heading(col, text=col)
    student_table.column(col, width=100)

student_table["show"] = "headings"

fetch_data()
student_table.bind("<ButtonRelease-1>",fetch_cursor)
student_table.bind("<Double-1>", fetch_cursor2)

root.mainloop()