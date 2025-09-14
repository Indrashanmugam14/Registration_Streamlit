import streamlit as st
import os

SAVE_FOLDER = "job_registrations"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def is_already_registered(email, phone):
    # Check all existing files for duplicate email or phone
    for file in os.listdir(SAVE_FOLDER):
        if file.endswith("_info.txt"):
            with open(os.path.join(SAVE_FOLDER, file), 'r') as f:
                content = f.read()
                if email in content or phone in content:
                    return True
    return False

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
                    # Save resume and info
                    resume_filename = os.path.join(SAVE_FOLDER, f"{name.replace(' ', '_')}_resume.pdf")
                    with open(resume_filename, "wb") as f:
                        f.write(resume.getbuffer())

                    info_filename = os.path.join(SAVE_FOLDER, f"{name.replace(' ', '_')}_info.txt")
                    with open(info_filename, "w") as f:
                        f.write(f"Name: {name}\n")
                        f.write(f"Email: {email}\n")
                        f.write(f"Phone: {phone}\n")
                        f.write(f"Preferred Roles: {', '.join(preferred_roles)}\n")
                        f.write(f"Resume File: {resume_filename}\n")

                    st.success(f"{name} has been registered successfully!")
                    st.info(f"✅ Data saved in `{SAVE_FOLDER}` folder.")

    st.info("ℹ️ After registration, fill the form again to register another person.")

if __name__ == '__main__':
    job_registration()


