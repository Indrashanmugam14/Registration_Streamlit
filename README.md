
It allows candidates to register for job opportunities by submitting their personal details, selecting job preferences, and uploading their resume (PDF format).  
The app supports multiple consecutive registrations and prevents duplicate registrations based on email or phone number. I used sqlite to store the information in table format we can view in streamlit page and we can install the DB Browser and import candidate.db and then we view the Registered candidate information in table.

Features 

1. Collects candidate information:  
  - Full Name  
  - Email Address  
  - Phone Number  
  - Preferred Job Roles (Multiple selection)  
  - Resume Upload (PDF)

2. Validates input fields to ensure all data is provided.

3. Prevents duplicate registrations by checking existing records (based on email or phone).

4. Saves candidate information and resume in a local folder.

5. Automatically clears the form after each successful registration, allowing easy registration of multiple persons.

How to Run  

Install Streamlit:  
   pip install streamlit
Run the application:
   streamlit run job_registration_app.py
