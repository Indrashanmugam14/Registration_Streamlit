import streamlit as st
import os
import sqlite3


SAVE_FOLDER = "job_registrations"
os.makedirs(SAVE_FOLDER, exist_ok=True)

DB_FILE = "candidates.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        phone TEXT UNIQUE NOT NULL,
                        preferred_roles TEXT NOT NULL,
                        resume_path TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def is_already_registered(email, phone):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE email=? OR phone=?", (email, phone))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_candidate(name, email, phone, preferred_roles, resume_path):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO candidates (name, email, phone, preferred_roles, resume_path)
                      VALUES (?, ?, ?, ?, ?)''',
                   (name, email, phone, preferred_roles, resume_path))
    conn.commit()
    conn.close()

def get_all_candidates():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, preferred_roles, resume_path FROM candidates")
    rows = cursor.fetchall()
    conn.close()
    return rows

#STREAMLIT APP
def job_registration():
    st.title("💼 Job Registration Portal")

    with st.form(key="registration_form", clear_on_submit=True):
        name = st.text_input("👤 Full Name")
        email = st.text_input("📧 Email Address")
        phone = st.text_input("📞 Phone Number")

        job_roles = ["Software Developer", "Data Analyst", "Project Manager", "UX Designer"]
        preferred_roles = st.multiselect("💡 Select Preferred Job Roles", job_roles)

        resume = st.file_uploader("📄 Upload Your Resume (PDF only)", type=['pdf'])

        submit_button = st.form_submit_button(label="✅ Submit Registration")

        if submit_button:
            if not name.strip() or not email.strip() or not phone.strip() or not preferred_roles or resume is None:
                st.error("⚠️ Please fill in all fields and upload the resume.")
            else:
                if is_already_registered(email, phone):
                    st.warning("⚠️ Already registered with this Email or Phone Number!")
                else:
                    # Save resume file
                    resume_filename = os.path.join(SAVE_FOLDER, f"{name.replace(' ', '_')}_resume.pdf")
                    with open(resume_filename, "wb") as f:
                        f.write(resume.getbuffer())

                    # Save data to database
                    save_candidate(name, email, phone, ", ".join(preferred_roles), resume_filename)

                    st.success(f"🎉 {name} has been registered successfully!")
                    st.info(f"✅ Data stored in `{DB_FILE}` (database).")

    st.subheader("📊 Registered Candidates")
    candidates = get_all_candidates()
    if candidates:
        import pandas as pd
        df = pd.DataFrame(candidates, columns=["ID", "Name", "Email", "Phone", "Preferred Roles", "Resume Path"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No candidates registered yet.")

    st.info("ℹ️ After registration, fill the form again to register another person.")

# MAIN 
if __name__ == '__main__':
    init_db()
    job_registration()


