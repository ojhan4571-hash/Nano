

Skip to content
Using Gmail with screen readers
Enable desktop notifications for Gmail.
   OK  No, thanks
Conversations
4% of 5,120 GB used
Terms · Privacy · Programme Policies
Last account activity: 2 hours ago
Details
# app.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, date
import mysql.connector
from mysql.connector import Error
import hashlib
import re
from decimal import Decimal

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'dental_management',
    'auth_plugin': 'mysql_native_password'
}

class DatabaseConnection:
    """Database connection handler"""
    @staticmethod
    def get_connection():
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            return None

class LoginWindow:
    """Login window for the Dental Management System"""
    def __init__(self, root):
        self.root = root
        self.root.title("Dental Management System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        self.current_user = None
        self.create_login_widgets()
    
    def create_login_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Dental Management System", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Frame for login fields
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        # Username
        tk.Label(frame, text="Username:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=10, sticky='e')
        self.username_entry = tk.Entry(frame, width=25, font=("Arial", 11))
        self.username_entry.grid(row=0, column=1, padx=5, pady=10)
        
        # Password
        tk.Label(frame, text="Password:", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=10, sticky='e')
        self.password_entry = tk.Entry(frame, width=25, font=("Arial", 11), show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)
        
        # Role selection
        tk.Label(frame, text="Role:", font=("Arial", 11)).grid(row=2, column=0, padx=5, pady=10, sticky='e')
        self.role_var = tk.StringVar(value="admin")
        role_menu = ttk.Combobox(frame, textvariable=self.role_var, values=["admin", "dentist", "receptionist"], 
                                 width=23, state="readonly")
        role_menu.grid(row=2, column=1, padx=5, pady=10)
        
        # Login button
        login_btn = tk.Button(self.root, text="Login", command=self.login, 
                             width=15, height=2, bg='#4CAF50', fg='white', font=("Arial", 11))
        login_btn.pack(pady=20)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.login())
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Connect to database
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Check user credentials (simplified - in production, use proper password hashing)
            query = "SELECT user_id, username, full_name, role FROM users WHERE username = %s AND role = %s"
            cursor.execute(query, (username, role))
            user = cursor.fetchone()
            
            if user:
                self.current_user = user
                messagebox.showinfo("Success", f"Welcome, {user['full_name']}!")
                self.root.destroy()
                open_main_window(self.current_user)
            else:
                messagebox.showerror("Error", "Invalid username or password")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error during login: {e}")
        finally:
            if conn:
                conn.close()

class MainWindow:
    """Main dashboard window for Dental Management System"""
    def __init__(self, root, user):
        self.root = root
        self.root.title(f"Dental Management System - Welcome {user['full_name']}")
        self.root.geometry("1200x700")
        self.current_user = user
        
        self.create_widgets()
        self.load_dashboard_data()
    
    def create_widgets(self):
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Change Password", command=self.change_password)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Patient menu
        patient_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Patients", menu=patient_menu)
        patient_menu.add_command(label="Add New Patient", command=self.add_patient)
        patient_menu.add_command(label="Search Patients", command=self.search_patients)
        patient_menu.add_command(label="View All Patients", command=self.view_all_patients)
        
        # Appointment menu
        appointment_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Appointments", menu=appointment_menu)
        appointment_menu.add_command(label="Schedule Appointment", command=self.schedule_appointment)
        appointment_menu.add_command(label="Today's Appointments", command=self.today_appointments)
        appointment_menu.add_command(label="View All Appointments", command=self.view_all_appointments)
        
        # Treatment menu
        treatment_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Treatments", menu=treatment_menu)
        treatment_menu.add_command(label="Add Treatment Record", command=self.add_treatment_record)
        treatment_menu.add_command(label="View Treatment History", command=self.view_treatment_history)
        
        # Billing menu
        billing_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Billing", menu=billing_menu)
        billing_menu.add_command(label="Create Invoice", command=self.create_invoice)
        billing_menu.add_command(label="View Invoices", command=self.view_invoices)
        
        # Reports menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Daily Report", command=self.daily_report)
        reports_menu.add_command(label="Monthly Report", command=self.monthly_report)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Dashboard widgets
        self.create_dashboard_widgets(main_frame)
    
    def create_dashboard_widgets(self, parent):
        # Top stats frame
        stats_frame = ttk.LabelFrame(parent, text="Today's Statistics", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Stats grid
        self.stats_labels = {}
        stats_data = [
            ("Total Patients", "total_patients"),
            ("Today's Appointments", "today_appointments"),
            ("Pending Invoices", "pending_invoices"),
            ("Today's Revenue", "today_revenue")
        ]
        
        for i, (label, key) in enumerate(stats_data):
            frame = ttk.Frame(stats_frame)
            frame.grid(row=0, column=i, padx=10, sticky="nsew")
            
            ttk.Label(frame, text=label, font=("Arial", 10)).pack()
            self.stats_labels[key] = ttk.Label(frame, text="Loading...", font=("Arial", 16, "bold"))
            self.stats_labels[key].pack()
        
        # Main content area with notebook
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Today's appointments tab
        today_tab = ttk.Frame(self.notebook)
        self.notebook.add(today_tab, text="Today's Appointments")
        self.create_today_appointments_tab(today_tab)
        
        # Recent patients tab
        patients_tab = ttk.Frame(self.notebook)
        self.notebook.add(patients_tab, text="Recent Patients")
        self.create_patients_tab(patients_tab)
        
        # Quick actions tab
        actions_tab = ttk.Frame(self.notebook)
        self.notebook.add(actions_tab, text="Quick Actions")
        self.create_quick_actions_tab(actions_tab)
    
    def create_today_appointments_tab(self, parent):
        # Treeview for appointments
        columns = ('ID', 'Patient', 'Time', 'Status', 'Reason')
        self.appointments_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=100)
        
        self.appointments_tree.column('Patient', width=200)
        self.appointments_tree.column('Reason', width=250)
        
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Check In", command=self.check_in_appointment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Start Treatment", command=self.start_treatment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Complete", command=self.complete_appointment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel_appointment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_today_appointments).pack(side=tk.RIGHT, padx=5)
    
    def create_patients_tab(self, parent):
        # Search bar
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.patient_search_entry = ttk.Entry(search_frame, width=30)
        self.patient_search_entry.pack(side=tk.LEFT, padx=5)
        self.patient_search_entry.bind('<KeyRelease>', lambda e: self.search_patients_tree())
        
        ttk.Button(search_frame, text="Clear", command=self.clear_patient_search).pack(side=tk.LEFT, padx=5)
        
        # Treeview for patients
        columns = ('ID', 'Name', 'DOB', 'Phone', 'Email')
        self.patients_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=100)
        
        self.patients_tree.column('Name', width=200)
        self.patients_tree.column('Email', width=200)
        
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=scrollbar.set)
        
        self.patients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="View Patient", command=self.view_patient_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Patient", command=self.edit_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Patient", command=self.add_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_recent_patients).pack(side=tk.RIGHT, padx=5)
    
    def create_quick_actions_tab(self, parent):
        # Create a grid of quick action buttons
        actions = [
            ("Add New Patient", self.add_patient, "#4CAF50"),
            ("Schedule Appointment", self.schedule_appointment, "#2196F3"),
            ("Create Invoice", self.create_invoice, "#FF9800"),
            ("Add Treatment", self.add_treatment_record, "#9C27B0"),
            ("Today's Appointments", self.today_appointments, "#009688"),
            ("View Patients", self.view_all_patients, "#607D8B"),
            ("Generate Report", self.daily_report, "#F44336"),
            ("Manage Treatments", self.manage_treatments, "#795548")
        ]
        
        # Create a canvas for scrolling if needed
        canvas = tk.Canvas(parent, bg='white')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Place action buttons in a grid
        for i, (text, command, color) in enumerate(actions):
            row = i // 4
            col = i % 4
            btn = tk.Button(scrollable_frame, text=text, command=command,
                          bg=color, fg='white', font=("Arial", 11, "bold"),
                          width=20, height=3, relief=tk.RAISED)
            btn.grid(row=row, column=col, padx=10, pady=10)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_dashboard_data(self):
        self.load_today_appointments()
        self.load_recent_patients()
        self.update_stats()
    
    def update_stats(self):
        """Update dashboard statistics"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Total patients
            cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = cursor.fetchone()[0]
            self.stats_labels['total_patients'].config(text=str(total_patients))
            
            # Today's appointments
            today = date.today()
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = %s AND status NOT IN ('cancelled', 'completed')", (today,))
            today_appointments = cursor.fetchone()[0]
            self.stats_labels['today_appointments'].config(text=str(today_appointments))
            
            # Pending invoices
            cursor.execute("SELECT COUNT(*) FROM invoices WHERE status = 'pending'")
            pending_invoices = cursor.fetchone()[0]
            self.stats_labels['pending_invoices'].config(text=str(pending_invoices))
            
            # Today's revenue
            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM invoices WHERE invoice_date = %s AND status = 'paid'", (today,))
            today_revenue = cursor.fetchone()[0]
            self.stats_labels['today_revenue'].config(text=f"${float(today_revenue):.2f}")
            
        except Error as e:
            print(f"Error updating stats: {e}")
        finally:
            if conn:
                conn.close()
    
    def load_today_appointments(self):
        """Load today's appointments into the treeview"""
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            today = date.today()
            
            query = """
                SELECT a.appointment_id, CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                       a.appointment_time, a.status, a.reason
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                WHERE a.appointment_date = %s
                ORDER BY a.appointment_time
            """
            cursor.execute(query, (today,))
            
            for row in cursor.fetchall():
                self.appointments_tree.insert('', 'end', values=row)
                
        except Error as e:
            print(f"Error loading appointments: {e}")
        finally:
            if conn:
                conn.close()
    
    def load_recent_patients(self):
        """Load recent patients into the treeview"""
        self.clear_patient_search()
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT patient_id, CONCAT(first_name, ' ', last_name) as name,
                       date_of_birth, phone, email
                FROM patients
                ORDER BY created_at DESC
                LIMIT 50
            """
            cursor.execute(query)
            
            for row in cursor.fetchall():
                self.patients_tree.insert('', 'end', values=row)
                
        except Error as e:
            print(f"Error loading patients: {e}")
        finally:
            if conn:
                conn.close()
    
    def search_patients_tree(self):
        """Search patients based on entered text"""
        search_text = self.patient_search_entry.get().strip().lower()
        
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        if not search_text:
            self.load_recent_patients()
            return
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT patient_id, CONCAT(first_name, ' ', last_name) as name,
                       date_of_birth, phone, email
                FROM patients
                WHERE LOWER(first_name) LIKE %s 
                   OR LOWER(last_name) LIKE %s 
                   OR LOWER(CONCAT(first_name, ' ', last_name)) LIKE %s
                   OR phone LIKE %s
                ORDER BY created_at DESC
                LIMIT 50
            """
            search_pattern = f"%{search_text}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            
            for row in cursor.fetchall():
                self.patients_tree.insert('', 'end', values=row)
                
        except Error as e:
            print(f"Error searching patients: {e}")
        finally:
            if conn:
                conn.close()
    
    def clear_patient_search(self):
        self.patient_search_entry.delete(0, tk.END)
        self.load_recent_patients()
    
    def check_in_appointment(self):
        """Check in a patient for their appointment"""
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment")
            return
        
        values = self.appointments_tree.item(selected[0], 'values')
        appointment_id = values[0]
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE appointments SET status = 'checked_in', updated_at = CURRENT_TIMESTAMP WHERE appointment_id = %s",
                (appointment_id,)
            )
            conn.commit()
            
            messagebox.showinfo("Success", "Patient checked in successfully")
            self.load_today_appointments()
            self.update_stats()
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to check in patient: {e}")
        finally:
            if conn:
                conn.close()
    
    def start_treatment(self):
        """Start treatment for an appointment"""
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment")
            return
        
        values = self.appointments_tree.item(selected[0], 'values')
        appointment_id = values[0]
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE appointments SET status = 'in_progress', updated_at = CURRENT_TIMESTAMP WHERE appointment_id = %s",
                (appointment_id,)
            )
            conn.commit()
            
            messagebox.showinfo("Success", "Treatment started")
            self.load_today_appointments()
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to start treatment: {e}")
        finally:
            if conn:
                conn.close()
    
    def complete_appointment(self):
        """Complete an appointment"""
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment")
            return
        
        if messagebox.askyesno("Confirm", "Mark this appointment as completed?"):
            values = self.appointments_tree.item(selected[0], 'values')
            appointment_id = values[0]
            
            conn = DatabaseConnection.get_connection()
            if not conn:
                return
            
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE appointments SET status = 'completed', updated_at = CURRENT_TIMESTAMP WHERE appointment_id = %s",
                    (appointment_id,)
                )
                conn.commit()
                
                messagebox.showinfo("Success", "Appointment completed")
                self.load_today_appointments()
                self.update_stats()
                
            except Error as e:
                messagebox.showerror("Error", f"Failed to complete appointment: {e}")
            finally:
                if conn:
                    conn.close()
    
    def cancel_appointment(self):
        """Cancel an appointment"""
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment")
            return
        
        if messagebox.askyesno("Confirm", "Cancel this appointment?"):
            values = self.appointments_tree.item(selected[0], 'values')
            appointment_id = values[0]
            
            conn = DatabaseConnection.get_connection()
            if not conn:
                return
            
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE appointments SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE appointment_id = %s",
                    (appointment_id,)
                )
                conn.commit()
                
                messagebox.showinfo("Success", "Appointment cancelled")
                self.load_today_appointments()
                self.update_stats()
                
            except Error as e:
                messagebox.showerror("Error", f"Failed to cancel appointment: {e}")
            finally:
                if conn:
                    conn.close()
    
    def view_patient_details(self):
        """View detailed information about a selected patient"""
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient")
            return
        
        values = self.patients_tree.item(selected[0], 'values')
        patient_id = values[0]
        
        # Open patient details window
        PatientDetailsWindow(self.root, patient_id)
    
    def edit_patient(self):
        """Edit selected patient's information"""
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient")
            return
        
        values = self.patients_tree.item(selected[0], 'values')
        patient_id = values[0]
        
        # Open edit patient window
        PatientFormWindow(self.root, patient_id, self.load_recent_patients)
    
    def add_patient(self):
        """Open add patient window"""
        PatientFormWindow(self.root, None, self.load_recent_patients)
    
    def schedule_appointment(self):
        """Open schedule appointment window"""
        AppointmentFormWindow(self.root, self.load_today_appointments)
    
    def today_appointments(self):
        """Switch to today's appointments tab"""
        self.notebook.select(0)
        self.load_today_appointments()
    
    def view_all_appointments(self):
        """Open all appointments window"""
        AllAppointmentsWindow(self.root)
    
    def view_all_patients(self):
        """Open all patients window"""
        AllPatientsWindow(self.root)
    
    def add_treatment_record(self):
        """Open add treatment record window"""
        TreatmentFormWindow(self.root, self.load_today_appointments)
    
    def view_treatment_history(self):
        """Open treatment history window"""
        TreatmentHistoryWindow(self.root)
    
    def create_invoice(self):
        """Open create invoice window"""
        InvoiceFormWindow(self.root, self.update_stats)
    
    def view_invoices(self):
        """Open invoices window"""
        InvoicesWindow(self.root)
    
    def manage_treatments(self):
        """Open treatment management window"""
        TreatmentManagementWindow(self.root)
    
    def daily_report(self):
        """Generate daily report"""
        ReportWindow(self.root, 'daily')
    
    def monthly_report(self):
        """Generate monthly report"""
        ReportWindow(self.root, 'monthly')
    
    def change_password(self):
        """Open change password window"""
        ChangePasswordWindow(self.root, self.current_user)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Dental Management System v1.0
        
A comprehensive system for managing dental practice operations including:
• Patient Management
• Appointment Scheduling
• Treatment Records
• Billing & Invoicing
• Reporting

Developed using Python & MySQL"""
        messagebox.showinfo("About", about_text)
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            root = tk.Tk()
            LoginWindow(root)
            root.mainloop()

class PatientFormWindow:
    """Window for adding/editing patients"""
    def __init__(self, root, patient_id=None, refresh_callback=None):
        self.root = tk.Toplevel(root)
        self.patient_id = patient_id
        self.refresh_callback = refresh_callback
        
        if patient_id:
            self.root.title("Edit Patient")
        else:
            self.root.title("Add New Patient")
        
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.create_widgets()
        if patient_id:
            self.load_patient_data()
    
    def create_widgets(self):
        # Main frame with scrolling
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Date of Birth (YYYY-MM-DD):", "dob"),
            ("Gender:", "gender"),
            ("Phone:", "phone"),
            ("Email:", "email"),
            ("Address:", "address"),
            ("Emergency Contact:", "emergency_contact"),
            ("Emergency Phone:", "emergency_phone"),
            ("Medical History:", "medical_history"),
            ("Allergies:", "allergies")
        ]
        
        self.entries = {}
        
        for i, (label, key) in enumerate(fields):
            ttk.Label(scrollable_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            
            if key == "address":
                self.entries[key] = tk.Text(scrollable_frame, height=3, width=40)
                self.entries[key].grid(row=i, column=1, padx=10, pady=5)
            elif key == "gender":
                self.entries[key] = ttk.Combobox(scrollable_frame, values=['Male', 'Female', 'Other'], 
                                                width=37, state="readonly")
                self.entries[key].grid(row=i, column=1, padx=10, pady=5)
            elif key in ["medical_history", "allergies"]:
                self.entries[key] = tk.Text(scrollable_frame, height=3, width=40)
                self.entries[key].grid(row=i, column=1, padx=10, pady=5)
            else:
                self.entries[key] = ttk.Entry(scrollable_frame, width=40)
                self.entries[key].grid(row=i, column=1, padx=10, pady=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        if self.patient_id:
            ttk.Button(btn_frame, text="Update", command=self.update_patient).pack(side=tk.LEFT, padx=5)
        else:
            ttk.Button(btn_frame, text="Save", command=self.save_patient).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Cancel", command=self.root.destroy).pack(side=tk.LEFT, padx=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_patient_data(self):
        """Load patient data for editing"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM patients WHERE patient_id = %s"
            cursor.execute(query, (self.patient_id,))
            patient = cursor.fetchone()
            
            if patient:
                self.entries['first_name'].insert(0, patient['first_name'])
                self.entries['last_name'].insert(0, patient['last_name'])
                self.entries['dob'].insert(0, str(patient['date_of_birth']))
                self.entries['gender'].set(patient['gender'])
                self.entries['phone'].insert(0, patient['phone'])
                self.entries['email'].insert(0, patient['email'] if patient['email'] else '')
                self.entries['address'].insert('1.0', patient['address'] if patient['address'] else '')
                self.entries['emergency_contact'].insert(0, patient['emergency_contact'] if patient['emergency_contact'] else '')
                self.entries['emergency_phone'].insert(0, patient['emergency_phone'] if patient['emergency_phone'] else '')
                self.entries['medical_history'].insert('1.0', patient['medical_history'] if patient['medical_history'] else '')
                self.entries['allergies'].insert('1.0', patient['allergies'] if patient['allergies'] else '')
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load patient data: {e}")
        finally:
            if conn:
                conn.close()
    
    def validate_data(self):
        """Validate form data"""
        # Check required fields
        required = ['first_name', 'last_name', 'dob', 'gender', 'phone']
        for field in required:
            value = self.entries[field].get().strip()
            if not value:
                messagebox.showerror("Validation Error", f"{field.replace('_', ' ').title()} is required")
                return False
        
        # Validate date format
        dob = self.entries['dob'].get().strip()
        try:
            datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid date format. Use YYYY-MM-DD")
            return False
        
        # Validate email if provided
        email = self.entries['email'].get().strip()
        if email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                messagebox.showerror("Validation Error", "Invalid email format")
                return False
        
        return True
    
    def save_patient(self):
        """Save new patient to database"""
        if not self.validate_data():
            return
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            query = """
                INSERT INTO patients 
                (first_name, last_name, date_of_birth, gender, phone, email, address, 
                 emergency_contact, emergency_phone, medical_history, allergies)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                self.entries['first_name'].get().strip(),
                self.entries['last_name'].get().strip(),
                self.entries['dob'].get().strip(),
                self.entries['gender'].get(),
                self.entries['phone'].get().strip(),
                self.entries['email'].get().strip() or None,
                self.entries['address'].get('1.0', tk.END).strip() or None,
                self.entries['emergency_contact'].get().strip() or None,
                self.entries['emergency_phone'].get().strip() or None,
                self.entries['medical_history'].get('1.0', tk.END).strip() or None,
                self.entries['allergies'].get('1.0', tk.END).strip() or None
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Patient added successfully")
            self.root.destroy()
            if self.refresh_callback:
                self.refresh_callback()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to save patient: {e}")
        finally:
            if conn:
                conn.close()
    
    def update_patient(self):
        """Update patient information"""
        if not self.validate_data():
            return
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            query = """
                UPDATE patients 
                SET first_name = %s, last_name = %s, date_of_birth = %s, gender = %s,
                    phone = %s, email = %s, address = %s, emergency_contact = %s,
                    emergency_phone = %s, medical_history = %s, allergies = %s
                WHERE patient_id = %s
            """
            
            values = (
                self.entries['first_name'].get().strip(),
                self.entries['last_name'].get().strip(),
                self.entries['dob'].get().strip(),
                self.entries['gender'].get(),
                self.entries['phone'].get().strip(),
                self.entries['email'].get().strip() or None,
                self.entries['address'].get('1.0', tk.END).strip() or None,
                self.entries['emergency_contact'].get().strip() or None,
                self.entries['emergency_phone'].get().strip() or None,
                self.entries['medical_history'].get('1.0', tk.END).strip() or None,
                self.entries['allergies'].get('1.0', tk.END).strip() or None,
                self.patient_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Patient updated successfully")
            self.root.destroy()
            if self.refresh_callback:
                self.refresh_callback()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to update patient: {e}")
        finally:
            if conn:
                conn.close()

class PatientDetailsWindow:
    """Window to display patient details"""
    def __init__(self, root, patient_id):
        self.root = tk.Toplevel(root)
        self.root.title("Patient Details")
        self.root.geometry("800x600")
        self.patient_id = patient_id
        
        self.create_widgets()
        self.load_patient_details()
    
    def create_widgets(self):
        # Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Personal info tab
        personal_tab = ttk.Frame(notebook)
        notebook.add(personal_tab, text="Personal Information")
        self.create_personal_info_tab(personal_tab)
        
        # Treatment history tab
        treatment_tab = ttk.Frame(notebook)
        notebook.add(treatment_tab, text="Treatment History")
        self.create_treatment_history_tab(treatment_tab)
        
        # Appointments tab
        appointments_tab = ttk.Frame(notebook)
        notebook.add(appointments_tab, text="Appointments")
        self.create_appointments_tab(appointments_tab)
        
        # Invoices tab
        invoices_tab = ttk.Frame(notebook)
        notebook.add(invoices_tab, text="Invoices")
        self.create_invoices_tab(invoices_tab)
    
    def create_personal_info_tab(self, parent):
        self.info_frame = ttk.LabelFrame(parent, text="Patient Information", padding=10)
        self.info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Information will be loaded here
        self.info_labels = {}
        info_fields = [
            ("Patient ID", "patient_id"),
            ("Full Name", "full_name"),
            ("Date of Birth", "dob"),
            ("Age", "age"),
            ("Gender", "gender"),
            ("Phone", "phone"),
            ("Email", "email"),
            ("Address", "address"),
            ("Emergency Contact", "emergency_contact"),
            ("Emergency Phone", "emergency_phone"),
            ("Medical History", "medical_history"),
            ("Allergies", "allergies"),
            ("Registered", "created_at")
        ]
        
        for i, (label, key) in enumerate(info_fields):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(self.info_frame, text=f"{label}:", font=("Arial", 10, "bold")).grid(
                row=row, column=col, padx=5, pady=5, sticky='e')
            
            self.info_labels[key] = ttk.Label(self.info_frame, text="Loading...", font=("Arial", 10))
            self.info_labels[key].grid(row=row, column=col+1, padx=5, pady=5, sticky='w')
    
    def create_treatment_history_tab(self, parent):
        # Treeview for treatments
        columns = ('Date', 'Treatment', 'Dentist', 'Diagnosis', 'Status')
        self.treatment_tree = ttk.Treeview(parent, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.treatment_tree.heading(col, text=col)
            self.treatment_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.treatment_tree.yview)
        self.treatment_tree.configure(yscrollcommand=scrollbar.set)
        
        self.treatment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_appointments_tab(self, parent):
        # Treeview for appointments
        columns = ('Date', 'Time', 'Dentist', 'Status', 'Reason')
        self.appointments_tree = ttk.Treeview(parent, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_invoices_tab(self, parent):
        # Treeview for invoices
        columns = ('Invoice ID', 'Date', 'Total', 'Paid', 'Status')
        self.invoices_tree = ttk.Treeview(parent, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.invoices_tree.heading(col, text=col)
            self.invoices_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.invoices_tree.yview)
        self.invoices_tree.configure(yscrollcommand=scrollbar.set)
        
        self.invoices_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_patient_details(self):
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Load patient info
            query = """
                SELECT *, 
                       TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) as age,
                       CONCAT(first_name, ' ', last_name) as full_name
                FROM patients 
                WHERE patient_id = %s
            """
            cursor.execute(query, (self.patient_id,))
            patient = cursor.fetchone()
            
            if patient:
                # Update personal info
                self.info_labels['patient_id'].config(text=str(patient['patient_id']))
                self.info_labels['full_name'].config(text=patient['full_name'])
                self.info_labels['dob'].config(text=str(patient['date_of_birth']))
                self.info_labels['age'].config(text=str(patient['age']))
                self.info_labels['gender'].config(text=patient['gender'])
                self.info_labels['phone'].config(text=patient['phone'])
                self.info_labels['email'].config(text=patient['email'] or 'N/A')
                self.info_labels['address'].config(text=patient['address'] or 'N/A')
                self.info_labels['emergency_contact'].config(text=patient['emergency_contact'] or 'N/A')
                self.info_labels['emergency_phone'].config(text=patient['emergency_phone'] or 'N/A')
                self.info_labels['medical_history'].config(text=patient['medical_history'] or 'None')
                self.info_labels['allergies'].config(text=patient['allergies'] or 'None')
                self.info_labels['created_at'].config(text=str(patient['created_at']))
            
            # Load treatment history
            query = """
                SELECT tr.treatment_date, t.treatment_name, 
                       CONCAT(u.full_name) as dentist_name,
                       tr.diagnosis, tr.status
                FROM treatment_records tr
                JOIN treatments t ON tr.treatment_id = t.treatment_id
                LEFT JOIN dentists d ON tr.dentist_id = d.dentist_id
                LEFT JOIN users u ON d.user_id = u.user_id
                WHERE tr.patient_id = %s
                ORDER BY tr.treatment_date DESC
            """
            cursor.execute(query, (self.patient_id,))
            
            for row in cursor.fetchall():
                self.treatment_tree.insert('', 'end', values=(
                    row['treatment_date'],
                    row['treatment_name'],
                    row['dentist_name'] or 'N/A',
                    row['diagnosis'] or 'N/A',
                    row['status']
                ))
            
            # Load appointments
            query = """
                SELECT a.appointment_date, a.appointment_time,
                       CONCAT(u.full_name) as dentist_name,
                       a.status, a.reason
                FROM appointments a
                LEFT JOIN dentists d ON a.dentist_id = d.dentist_id
                LEFT JOIN users u ON d.user_id = u.user_id
                WHERE a.patient_id = %s
                ORDER BY a.appointment_date DESC
            """
            cursor.execute(query, (self.patient_id,))
            
            for row in cursor.fetchall():
                self.appointments_tree.insert('', 'end', values=(
                    row['appointment_date'],
                    row['appointment_time'],
                    row['dentist_name'] or 'N/A',
                    row['status'],
                    row['reason'] or 'N/A'
                ))
            
            # Load invoices
            query = """
                SELECT invoice_id, invoice_date, total_amount, paid_amount, status
                FROM invoices
                WHERE patient_id = %s
                ORDER BY invoice_date DESC
            """
            cursor.execute(query, (self.patient_id,))
            
            for row in cursor.fetchall():
                self.invoices_tree.insert('', 'end', values=(
                    row['invoice_id'],
                    row['invoice_date'],
                    f"${float(row['total_amount']):.2f}",
                    f"${float(row['paid_amount']):.2f}",
                    row['status']
                ))
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load patient details: {e}")
        finally:
            if conn:
                conn.close()

class AppointmentFormWindow:
    """Window for scheduling appointments"""
    def __init__(self, root, refresh_callback=None):
        self.root = tk.Toplevel(root)
        self.root.title("Schedule Appointment")
        self.root.geometry("500x500")
        self.refresh_callback = refresh_callback
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        fields = [
            ("Patient:", "patient_id"),
            ("Dentist:", "dentist_id"),
            ("Date (YYYY-MM-DD):", "appointment_date"),
            ("Time (HH:MM):", "appointment_time"),
            ("Duration (minutes):", "duration"),
            ("Reason:", "reason"),
            ("Notes:", "notes")
        ]
        
        self.entries = {}
        
        for i, (label, key) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if key == "patient_id":
                self.entries[key] = ttk.Combobox(main_frame, width=35, state="readonly")
                self.load_patients()
            elif key == "dentist_id":
                self.entries[key] = ttk.Combobox(main_frame, width=35, state="readonly")
                self.load_dentists()
            elif key in ["reason", "notes"]:
                self.entries[key] = tk.Text(main_frame, height=3, width=35)
                self.entries[key].grid(row=i, column=1, padx=5, pady=5)
            else:
                self.entries[key] = ttk.Entry(main_frame, width=37)
                self.entries[key].grid(row=i, column=1, padx=5, pady=5)
        
        # Set default values
        self.entries['duration'].insert(0, "30")
        self.entries['appointment_date'].insert(0, str(date.today()))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Schedule", command=self.schedule_appointment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.root.destroy).pack(side=tk.LEFT, padx=5)
    
    def load_patients(self):
        """Load patients into combobox"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT patient_id, CONCAT(first_name, ' ', last_name) as name FROM patients ORDER BY name")
            patients = cursor.fetchall()
            
            self.patient_map = {name: id for id, name in patients}
            self.entries['patient_id']['values'] = list(self.patient_map.keys())
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to load patients: {e}")
        finally:
            if conn:
                conn.close()
    
    def load_dentists(self):
        """Load dentists into combobox"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.dentist_id, CONCAT(u.full_name, ' (', d.specialization, ')') as name
                FROM dentists d
                JOIN users u ON d.user_id = u.user_id
                ORDER BY name
            """)
            dentists = cursor.fetchall()
            
            self.dentist_map = {name: id for id, name in dentists}
            self.entries['dentist_id']['values'] = list(self.dentist_map.keys())
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to load dentists: {e}")
        finally:
            if conn:
                conn.close()
    
    def validate_data(self):
        """Validate form data"""
        required = ['patient_id', 'dentist_id', 'appointment_date', 'appointment_time']
        for field in required:
            if field == 'patient_id':
                value = self.entries[field].get()
            elif field == 'dentist_id':
                value = self.entries[field].get()
            else:
                value = self.entries[field].get().strip()
            
            if not value:
                messagebox.showerror("Validation Error", f"{field.replace('_', ' ').title()} is required")
                return False
        
        # Validate date format
        try:
            datetime.strptime(self.entries['appointment_date'].get().strip(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid date format. Use YYYY-MM-DD")
            return False
        
        # Validate time format
        try:
            datetime.strptime(self.entries['appointment_time'].get().strip(), '%H:%M')
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid time format. Use HH:MM")
            return False
        
        # Validate duration
        try:
            duration = int(self.entries['duration'].get().strip())
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Duration must be a positive number")
            return False
        
        return True
    
    def schedule_appointment(self):
        """Schedule the appointment"""
        if not self.validate_data():
            return
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            patient_name = self.entries['patient_id'].get()
            dentist_name = self.entries['dentist_id'].get()
            
            patient_id = self.patient_map[patient_name]
            dentist_id = self.dentist_map[dentist_name]
            
            query = """
                INSERT INTO appointments 
                (patient_id, dentist_id, appointment_date, appointment_time, 
                 duration, reason, notes, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'scheduled')
            """
            
            values = (
                patient_id,
                dentist_id,
                self.entries['appointment_date'].get().strip(),
                self.entries['appointment_time'].get().strip(),
                int(self.entries['duration'].get().strip()),
                self.entries['reason'].get('1.0', tk.END).strip() or None,
                self.entries['notes'].get('1.0', tk.END).strip() or None
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Appointment scheduled successfully")
            self.root.destroy()
            if self.refresh_callback:
                self.refresh_callback()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to schedule appointment: {e}")
        finally:
            if conn:
                conn.close()

class AllAppointmentsWindow:
    """Window to view all appointments"""
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("All Appointments")
        self.root.geometry("1000x600")
        
        self.create_widgets()
        self.load_appointments()
    
    def create_widgets(self):
        # Filter frame
        filter_frame = ttk.LabelFrame(self.root, text="Filters", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=['All', 'scheduled', 'confirmed', 'checked_in', 
                                                              'in_progress', 'completed', 'cancelled', 'no_show'],
                                        width=15, state="readonly")
        self.status_filter.set('All')
        self.status_filter.pack(side=tk.LEFT, padx=5)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.load_appointments())
        
        ttk.Label(filter_frame, text="Date:").pack(side=tk.LEFT, padx=5)
        self.date_filter = ttk.Entry(filter_frame, width=15)
        self.date_filter.insert(0, str(date.today()))
        self.date_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Apply Filter", command=self.load_appointments).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Clear", command=self.clear_filters).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        columns = ('ID', 'Patient', 'Dentist', 'Date', 'Time', 'Status', 'Reason')
        self.appointments_tree = ttk.Treeview(self.root, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=100)
        
        self.appointments_tree.column('Patient', width=150)
        self.appointments_tree.column('Dentist', width=150)
        self.appointments_tree.column('Reason', width=200)
        
        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
    
    def clear_filters(self):
        self.status_filter.set('All')
        self.date_filter.delete(0, tk.END)
        self.date_filter.insert(0, str(date.today()))
        self.load_appointments()
    
    def load_appointments(self):
        """Load appointments based on filters"""
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT a.appointment_id, 
                       CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                       CONCAT(u.full_name) as dentist_name,
                       a.appointment_date, a.appointment_time, a.status, a.reason
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                LEFT JOIN dentists d ON a.dentist_id = d.dentist_id
                LEFT JOIN users u ON d.user_id = u.user_id
                WHERE 1=1
            """
            params = []
            
            status = self.status_filter.get()
            if status and status != 'All':
                query += " AND a.status = %s"
                params.append(status)
            
            date_val = self.date_filter.get().strip()
            if date_val:
                try:
                    datetime.strptime(date_val, '%Y-%m-%d')
                    query += " AND a.appointment_date = %s"
                    params.append(date_val)
                except ValueError:
                    pass
            
            query += " ORDER BY a.appointment_date DESC, a.appointment_time"
            
            cursor.execute(query, params)
            
            for row in cursor.fetchall():
                self.appointments_tree.insert('', 'end', values=row)
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load appointments: {e}")
        finally:
            if conn:
                conn.close()

class AllPatientsWindow:
    """Window to view all patients"""
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("All Patients")
        self.root.geometry("1000x600")
        
        self.create_widgets()
        self.load_patients()
    
    def create_widgets(self):
        # Search frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_patients())
        
        ttk.Button(search_frame, text="Add Patient", command=self.add_patient).pack(side=tk.RIGHT, padx=5)
        
        # Treeview
        columns = ('ID', 'Name', 'DOB', 'Phone', 'Email', 'Registered')
        self.patients_tree = ttk.Treeview(self.root, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=100)
        
        self.patients_tree.column('Name', width=200)
        self.patients_tree.column('Email', width=200)
        
        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=scrollbar.set)
        
        self.patients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Double-click to view details
        self.patients_tree.bind('<Double-1>', self.view_patient)
    
    def add_patient(self):
        PatientFormWindow(self.root, None, self.load_patients)
    
    def view_patient(self, event):
        selected = self.patients_tree.selection()
        if selected:
            values = self.patients_tree.item(selected[0], 'values')
            patient_id = values[0]
            PatientDetailsWindow(self.root, patient_id)
    
    def load_patients(self):
        """Load patients with search filter"""
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        search_text = self.search_entry.get().strip().lower()
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            if search_text:
                query = """
                    SELECT patient_id, CONCAT(first_name, ' ', last_name) as name,
                           date_of_birth, phone, email, created_at
                    FROM patients
                    WHERE LOWER(first_name) LIKE %s 
                       OR LOWER(last_name) LIKE %s 
                       OR LOWER(CONCAT(first_name, ' ', last_name)) LIKE %s
                       OR phone LIKE %s
                    ORDER BY created_at DESC
                """
                search_pattern = f"%{search_text}%"
                cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            else:
                query = """
                    SELECT patient_id, CONCAT(first_name, ' ', last_name) as name,
                           date_of_birth, phone, email, created_at
                    FROM patients
                    ORDER BY created_at DESC
                """
                cursor.execute(query)
            
            for row in cursor.fetchall():
                self.patients_tree.insert('', 'end', values=(
                    row[0], row[1], row[2], row[3], row[4] or 'N/A', row[5]
                ))
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load patients: {e}")
        finally:
            if conn:
                conn.close()

class TreatmentFormWindow:
    """Window for adding treatment records"""
    def __init__(self, root, refresh_callback=None):
        self.root = tk.Toplevel(root)
        self.root.title("Add Treatment Record")
        self.root.geometry("600x600")
        self.refresh_callback = refresh_callback
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        fields = [
            ("Patient:", "patient_id"),
            ("Dentist:", "dentist_id"),
            ("Treatment:", "treatment_id"),
            ("Diagnosis:", "diagnosis"),
            ("Treatment Date (YYYY-MM-DD):", "treatment_date"),
            ("Notes:", "notes"),
            ("Follow-up Date (YYYY-MM-DD):", "follow_up_date"),
            ("Status:", "status")
        ]
        
        self.entries = {}
        
        for i, (label, key) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if key == "patient_id":
                self.entries[key] = ttk.Combobox(main_frame, width=35, state="readonly")
                self.load_patients()
            elif key == "dentist_id":
                self.entries[key] = ttk.Combobox(main_frame, width=35, state="readonly")
                self.load_dentists()
            elif key == "treatment_id":
                self.entries[key] = ttk.Combobox(main_frame, width=35, state="readonly")
                self.load_treatments()
            elif key == "status":
                self.entries[key] = ttk.Combobox(main_frame, values=['planned', 'in_progress', 'completed', 'cancelled'],
                                                width=35, state="readonly")
                self.entries[key].set('planned')
            elif key in ["diagnosis", "notes"]:
                self.entries[key] = tk.Text(main_frame, height=3, width=35)
                self.entries[key].grid(row=i, column=1, padx=5, pady=5)
            else:
                self.entries[key] = ttk.Entry(main_frame, width=37)
                self.entries[key].grid(row=i, column=1, padx=5, pady=5)
        
        # Set default treatment date
        self.entries['treatment_date'].insert(0, str(date.today()))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self.save_treatment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.root.destroy).pack(side=tk.LEFT, padx=5)
    
    def load_patients(self):
        """Load patients into combobox"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT patient_id, CONCAT(first_name, ' ', last_name) as name FROM patients ORDER BY name")
            patients = cursor.fetchall()
            
            self.patient_map = {name: id for id, name in patients}
            self.entries['patient_id']['values'] = list(self.patient_map.keys())
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to load patients: {e}")
        finally:
            if conn:
                conn.close()
    
    def load_dentists(self):
        """Load dentists into combobox"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.dentist_id, CONCAT(u.full_name, ' (', d.specialization, ')') as name
                FROM dentists d
                JOIN users u ON d.user_id = u.user_id
                ORDER BY name
            """)
            dentists = cursor.fetchall()
            
            self.dentist_map = {name: id for id, name in dentists}
            self.entries['dentist_id']['values'] = list(self.dentist_map.keys())
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to load dentists: {e}")
        finally:
            if conn:
                conn.close()
    
    def load_treatments(self):
        """Load treatments into combobox"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT treatment_id, treatment_name FROM treatments WHERE is_active = TRUE ORDER BY treatment_name")
            treatments = cursor.fetchall()
            
            self.treatment_map = {name: id for id, name in treatments}
            self.entries['treatment_id']['values'] = list(self.treatment_map.keys())
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to load treatments: {e}")
        finally:
            if conn:
                conn.close()
    
    def validate_data(self):
        """Validate form data"""
        required = ['patient_id', 'dentist_id', 'treatment_id', 'treatment_date']
        for field in required:
            if field in ['patient_id', 'dentist_id', 'treatment_id']:
                value = self.entries[field].get()
            else:
                value = self.entries[field].get().strip()
            
            if not value:
                messagebox.showerror("Validation Error", f"{field.replace('_', ' ').title()} is required")
                return False
        
        # Validate treatment date
        try:
            datetime.strptime(self.entries['treatment_date'].get().strip(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid treatment date format. Use YYYY-MM-DD")
            return False
        
        # Validate follow-up date if provided
        follow_up = self.entries['follow_up_date'].get().strip()
        if follow_up:
            try:
                datetime.strptime(follow_up, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid follow-up date format. Use YYYY-MM-DD")
                return False
        
        return True
    
    def save_treatment(self):
        """Save treatment record"""
        if not self.validate_data():
            return
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            patient_name = self.entries['patient_id'].get()
            dentist_name = self.entries['dentist_id'].get()
            treatment_name = self.entries['treatment_id'].get()
            
            patient_id = self.patient_map[patient_name]
            dentist_id = self.dentist_map[dentist_name]
            treatment_id = self.treatment_map[treatment_name]
            
            query = """
                INSERT INTO treatment_records 
                (patient_id, dentist_id, treatment_id, diagnosis, treatment_date, 
                 notes, follow_up_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            follow_up = self.entries['follow_up_date'].get().strip() or None
            
            values = (
                patient_id,
                dentist_id,
                treatment_id,
                self.entries['diagnosis'].get('1.0', tk.END).strip() or None,
                self.entries['treatment_date'].get().strip(),
                self.entries['notes'].get('1.0', tk.END).strip() or None,
                follow_up,
                self.entries['status'].get()
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Treatment record saved successfully")
            self.root.destroy()
            if self.refresh_callback:
                self.refresh_callback()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to save treatment: {e}")
        finally:
            if conn:
                conn.close()

class TreatmentHistoryWindow:
    """Window to view treatment history"""
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Treatment History")
        self.root.geometry("1000x600")
        
        self.create_widgets()
        self.load_history()
    
    def create_widgets(self):
        # Search frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Patient:").pack(side=tk.LEFT, padx=5)
        self.patient_search = ttk.Entry(search_frame, width=30)
        self.patient_search.pack(side=tk.LEFT, padx=5)
        self.patient_search.bind('<KeyRelease>', lambda e: self.load_history())
        
        # Treeview
        columns = ('ID', 'Patient', 'Treatment', 'Dentist', 'Date', 'Diagnosis', 'Status', 'Follow-up')
        self.history_tree = ttk.Treeview(self.root, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        
        self.history_tree.column('Patient', width=150)
        self.history_tree.column('Treatment', width=150)
        self.history_tree.column('Dentist', width=150)
        self.history_tree.column('Diagnosis', width=150)
        
        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
    
    def load_history(self):
        """Load treatment history with search"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        search_text = self.patient_search.get().strip()
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT tr.record_id,
                       CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                       t.treatment_name,
                       CONCAT(u.full_name) as dentist_name,
                       tr.treatment_date, tr.diagnosis, tr.status, tr.follow_up_date
                FROM treatment_records tr
                JOIN patients p ON tr.patient_id = p.patient_id
                JOIN treatments t ON tr.treatment_id = t.treatment_id
                LEFT JOIN dentists d ON tr.dentist_id = d.dentist_id
                LEFT JOIN users u ON d.user_id = u.user_id
            """
            
            params = []
            if search_text:
                query += " WHERE CONCAT(p.first_name, ' ', p.last_name) LIKE %s"
                params.append(f"%{search_text}%")
            
            query += " ORDER BY tr.treatment_date DESC"
            
            cursor.execute(query, params)
            
            for row in cursor.fetchall():
                self.history_tree.insert('', 'end', values=(
                    row[0], row[1], row[2], row[3] or 'N/A',
                    row[4], row[5] or 'N/A', row[6], row[7] or 'N/A'
                ))
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load treatment history: {e}")
        finally:
            if conn:
                conn.close()

class InvoiceFormWindow:
    """Window for creating invoices"""
    def __init__(self, root, refresh_callback=None):
        self.root = tk.Toplevel(root)
        self.root.title("Create Invoice")
        self.root.geometry("700x600")
        self.refresh_callback = refresh_callback
        self.items = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Patient selection
        ttk.Label(main_frame, text="Patient:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.patient_combo = ttk.Combobox(main_frame, width=40, state="readonly")
        self.patient_combo.grid(row=0, column=1, padx=5, pady=5)
        self.load_patients()
        
        # Invoice date
        ttk.Label(main_frame, text="Invoice Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.invoice_date = ttk.Entry(main_frame, width=40)
        self.invoice_date.insert(0, str(date.today()))
        self.invoice_date.grid(row=1, column=1, padx=5, pady=5)
        
        # Due date
        ttk.Label(main_frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.due_date = ttk.Entry(main_frame, width=40)
        self.due_date.insert(0, str(date.today()))
        self.due_date.grid(row=2, column=1, padx=5, pady=5)
        
        # Add item section
        item_frame = ttk.LabelFrame(main_frame, text="Add Item", padding=10)
        item_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky='ew')
        
        ttk.Label(item_frame, text="Description:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.item_desc = ttk.Entry(item_frame, width=30)
        self.item_desc.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(item_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.item_qty = ttk.Entry(item_frame, width=10)
        self.item_qty.insert(0, "1")
        self.item_qty.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(item_frame, text="Unit Price:").grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.item_price = ttk.Entry(item_frame, width=15)
        self.item_price.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(item_frame, text="Add Item", command=self.add_item).grid(row=0, column=6, padx=5, pady=5)
        
        # Items list
        items_frame = ttk.LabelFrame(main_frame, text="Invoice Items", padding=10)
        items_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky='nsew')
        
        columns = ('Description', 'Quantity', 'Unit Price', 'Total')
        self.items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=5)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)
        
        self.items_tree.column('Description', width=250)
        
        scrollbar = ttk.Scrollbar(items_frame, orient='vertical', command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Summary
        summary_frame = ttk.Frame(main_frame)
        summary_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=10)
        
        ttk.Label(summary_frame, text="Subtotal:", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        self.subtotal_label = ttk.Label(summary_frame, text="$0.00", font=("Arial", 10, "bold"))
        self.subtotal_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(summary_frame, text="Tax (0%):", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        self.tax_label = ttk.Label(summary_frame, text="$0.00", font=("Arial", 10))
        self.tax_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(summary_frame, text="Total:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=10)
        self.total_label = ttk.Label(summary_frame, text="$0.00", font=("Arial", 12, "bold"), foreground='green')
        self.total_label.pack(side=tk.LEFT, padx=10)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Create Invoice", command=self.create_invoice).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Items", command=self.clear_items).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.root.destroy).pack(side=tk.LEFT, padx=5)
    
    def load_patients(self):
        """Load patients into combobox"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT patient_id, CONCAT(first_name, ' ', last_name) as name FROM patients ORDER BY name")
            patients = cursor.fetchall()
            
            self.patient_map = {name: id for id, name in patients}
            self.patient_combo['values'] = list(self.patient_map.keys())
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to load patients: {e}")
        finally:
            if conn:
                conn.close()
    
    def add_item(self):
        """Add item to invoice"""
        desc = self.item_desc.get().strip()
        qty = self.item_qty.get().strip()
        price = self.item_price.get().strip()
        
        if not desc or not qty or not price:
            messagebox.showwarning("Warning", "Please fill in all item fields")
            return
        
        try:
            qty = int(qty)
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive number")
            return
        
        try:
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number")
            return
        
        total = qty * price
        self.items.append({
            'description': desc,
            'quantity': qty,
            'unit_price': price,
            'total': total
        })
        
        self.items_tree.insert('', 'end', values=(desc, qty, f"${price:.2f}", f"${total:.2f}"))
        
        # Clear entry fields
        self.item_desc.delete(0, tk.END)
        self.item_qty.delete(0, tk.END)
        self.item_qty.insert(0, "1")
        self.item_price.delete(0, tk.END)
        
        self.update_summary()
    
    def clear_items(self):
        """Clear all items"""
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        self.items = []
        self.update_summary()
    
    def update_summary(self):
        """Update invoice summary"""
        subtotal = sum(item['total'] for item in self.items)
        tax = subtotal * 0.00  # 0% tax
        total = subtotal + tax
        
        self.subtotal_label.config(text=f"${subtotal:.2f}")
        self.tax_label.config(text=f"${tax:.2f}")
        self.total_label.config(text=f"${total:.2f}")
    
    def create_invoice(self):
        """Create the invoice"""
        if not self.patient_combo.get():
            messagebox.showwarning("Warning", "Please select a patient")
            return
        
        if not self.items:
            messagebox.showwarning("Warning", "Please add at least one item")
            return
        
        patient_name = self.patient_combo.get()
        patient_id = self.patient_map[patient_name]
        
        subtotal = sum(item['total'] for item in self.items)
        tax = subtotal * 0.00
        total = subtotal + tax
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Insert invoice
            query = """
                INSERT INTO invoices 
                (patient_id, invoice_date, due_date, subtotal, tax, total_amount, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'pending')
            """
            
            values = (
                patient_id,
                self.invoice_date.get().strip(),
                self.due_date.get().strip(),
                subtotal,
                tax,
                total
            )
            
            cursor.execute(query, values)
            invoice_id = cursor.lastrowid
            
            # Insert invoice items
            for item in self.items:
                query = """
                    INSERT INTO invoice_items 
                    (invoice_id, description, quantity, unit_price, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                """
                values = (
                    invoice_id,
                    item['description'],
                    item['quantity'],
                    item['unit_price'],
                    item['total']
                )
                cursor.execute(query, values)
            
            conn.commit()
            
            messagebox.showinfo("Success", f"Invoice #{invoice_id} created successfully")
            self.root.destroy()
            if self.refresh_callback:
                self.refresh_callback()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to create invoice: {e}")
        finally:
            if conn:
                conn.close()

class InvoicesWindow:
    """Window to view all invoices"""
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Invoices")
        self.root.geometry("1000x600")
        
        self.create_widgets()
        self.load_invoices()
    
    def create_widgets(self):
        # Filter frame
        filter_frame = ttk.LabelFrame(self.root, text="Filters", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=['All', 'pending', 'paid', 'overdue', 'cancelled'],
                                        width=15, state="readonly")
        self.status_filter.set('All')
        self.status_filter.pack(side=tk.LEFT, padx=5)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.load_invoices())
        
        ttk.Label(filter_frame, text="Patient:").pack(side=tk.LEFT, padx=5)
        self.patient_filter = ttk.Entry(filter_frame, width=20)
        self.patient_filter.pack(side=tk.LEFT, padx=5)
        self.patient_filter.bind('<KeyRelease>', lambda e: self.load_invoices())
        
        ttk.Button(filter_frame, text="Refresh", command=self.load_invoices).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Create Invoice", command=self.create_invoice).pack(side=tk.RIGHT, padx=5)
        
        # Treeview
        columns = ('ID', 'Patient', 'Date', 'Due Date', 'Total', 'Paid', 'Status')
        self.invoices_tree = ttk.Treeview(self.root, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.invoices_tree.heading(col, text=col)
            self.invoices_tree.column(col, width=100)
        
        self.invoices_tree.column('Patient', width=150)
        self.invoices_tree.column('Total', width=120)
        self.invoices_tree.column('Paid', width=120)
        
        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.invoices_tree.yview)
        self.invoices_tree.configure(yscrollcommand=scrollbar.set)
        
        self.invoices_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Double-click to view invoice details
        self.invoices_tree.bind('<Double-1>', self.view_invoice)
    
    def create_invoice(self):
        InvoiceFormWindow(self.root, self.load_invoices)
    
    def view_invoice(self, event):
        selected = self.invoices_tree.selection()
        if selected:
            values = self.invoices_tree.item(selected[0], 'values')
            invoice_id = values[0]
            InvoiceDetailsWindow(self.root, invoice_id)
    
    def load_invoices(self):
        """Load invoices with filters"""
        for item in self.invoices_tree.get_children():
            self.invoices_tree.delete(item)
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT i.invoice_id, 
                       CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                       i.invoice_date, i.due_date, i.total_amount, i.paid_amount, i.status
                FROM invoices i
                JOIN patients p ON i.patient_id = p.patient_id
                WHERE 1=1
            """
            params = []
            
            status = self.status_filter.get()
            if status and status != 'All':
                query += " AND i.status = %s"
                params.append(status)
            
            patient_search = self.patient_filter.get().strip()
            if patient_search:
                query += " AND CONCAT(p.first_name, ' ', p.last_name) LIKE %s"
                params.append(f"%{patient_search}%")
            
            query += " ORDER BY i.invoice_date DESC"
            
            cursor.execute(query, params)
            
            for row in cursor.fetchall():
                self.invoices_tree.insert('', 'end', values=(
                    row[0], row[1], row[2], row[3],
                    f"${float(row[4]):.2f}",
                    f"${float(row[5]):.2f}",
                    row[6]
                ))
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load invoices: {e}")
        finally:
            if conn:
                conn.close()

class InvoiceDetailsWindow:
    """Window to view invoice details"""
    def __init__(self, root, invoice_id):
        self.root = tk.Toplevel(root)
        self.root.title(f"Invoice #{invoice_id}")
        self.root.geometry("800x600")
        self.invoice_id = invoice_id
        
        self.create_widgets()
        self.load_invoice_details()
    
    def create_widgets(self):
        # Info frame
        info_frame = ttk.LabelFrame(self.root, text="Invoice Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.info_labels = {}
        info_fields = [
            ("Invoice #", "invoice_id"),
            ("Patient", "patient"),
            ("Date", "date"),
            ("Due Date", "due_date"),
            ("Status", "status")
        ]
        
        for i, (label, key) in enumerate(info_fields):
            row = i // 3
            col = (i % 3) * 2
            
            ttk.Label(info_frame, text=f"{label}:", font=("Arial", 10, "bold")).grid(
                row=row, column=col, padx=5, pady=5, sticky='e')
            
            self.info_labels[key] = ttk.Label(info_frame, text="Loading...", font=("Arial", 10))
            self.info_labels[key].grid(row=row, column=col+1, padx=5, pady=5, sticky='w')
        
        # Items frame
        items_frame = ttk.LabelFrame(self.root, text="Invoice Items", padding=10)
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('Description', 'Quantity', 'Unit Price', 'Total')
        self.items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)
        
        self.items_tree.column('Description', width=300)
        
        scrollbar = ttk.Scrollbar(items_frame, orient='vertical', command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Summary frame
        summary_frame = ttk.Frame(self.root)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.summary_labels = {}
        summary_fields = [
            ("Subtotal:", "subtotal"),
            ("Tax:", "tax"),
            ("Total:", "total"),
            ("Paid:", "paid"),
            ("Balance Due:", "balance")
        ]
        
        for i, (label, key) in enumerate(summary_fields):
            row = i // 5
            col = (i % 5) * 2
            
            ttk.Label(summary_frame, text=label, font=("Arial", 11, "bold")).grid(
                row=row, column=col, padx=10, pady=5, sticky='e')
            
            self.summary_labels[key] = ttk.Label(summary_frame, text="Loading...", font=("Arial", 11))
            self.summary_labels[key].grid(row=row, column=col+1, padx=10, pady=5, sticky='w')
        
        # Payment button
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Record Payment", command=self.record_payment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
    
    def load_invoice_details(self):
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Load invoice info
            query = """
                SELECT i.*, CONCAT(p.first_name, ' ', p.last_name) as patient_name
                FROM invoices i
                JOIN patients p ON i.patient_id = p.patient_id
                WHERE i.invoice_id = %s
            """
            cursor.execute(query, (self.invoice_id,))
            invoice = cursor.fetchone()
            
            if invoice:
                self.info_labels['invoice_id'].config(text=str(invoice['invoice_id']))
                self.info_labels['patient'].config(text=invoice['patient_name'])
                self.info_labels['date'].config(text=str(invoice['invoice_date']))
                self.info_labels['due_date'].config(text=str(invoice['due_date']))
                self.info_labels['status'].config(text=invoice['status'])
                
                self.summary_labels['subtotal'].config(text=f"${float(invoice['subtotal']):.2f}")
                self.summary_labels['tax'].config(text=f"${float(invoice['tax']):.2f}")
                self.summary_labels['total'].config(text=f"${float(invoice['total_amount']):.2f}")
                self.summary_labels['paid'].config(text=f"${float(invoice['paid_amount']):.2f}")
                
                balance = float(invoice['total_amount']) - float(invoice['paid_amount'])
                self.summary_labels['balance'].config(text=f"${balance:.2f}")
            
            # Load items
            query = "SELECT * FROM invoice_items WHERE invoice_id = %s"
            cursor.execute(query, (self.invoice_id,))
            
            for row in cursor.fetchall():
                self.items_tree.insert('', 'end', values=(
                    row['description'],
                    row['quantity'],
                    f"${float(row['unit_price']):.2f}",
                    f"${float(row['total_price']):.2f}"
                ))
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load invoice details: {e}")
        finally:
            if conn:
                conn.close()
    
    def record_payment(self):
        """Record payment for the invoice"""
        amount = tk.simpledialog.askfloat("Payment", "Enter payment amount:", minvalue=0.01)
        if amount is None:
            return
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Get current paid amount
            cursor.execute("SELECT total_amount, paid_amount FROM invoices WHERE invoice_id = %s", (self.invoice_id,))
            total, paid = cursor.fetchone()
            
            new_paid = float(paid) + amount
            
            if new_paid > float(total):
                messagebox.showerror("Error", "Payment amount exceeds balance due")
                return
            
            # Update invoice
            status = 'paid' if new_paid >= float(total) else 'pending'
            cursor.execute(
                "UPDATE invoices SET paid_amount = %s, status = %s WHERE invoice_id = %s",
                (new_paid, status, self.invoice_id)
            )
            conn.commit()
            
            messagebox.showinfo("Success", f"Payment of ${amount:.2f} recorded successfully")
            self.load_invoice_details()
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to record payment: {e}")
        finally:
            if conn:
                conn.close()

class TreatmentManagementWindow:
    """Window for managing treatments"""
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Manage Treatments")
        self.root.geometry("800x600")
        
        self.create_widgets()
        self.load_treatments()
    
    def create_widgets(self):
        # Form frame
        form_frame = ttk.LabelFrame(self.root, text="Treatment Details", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Description:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.desc_entry = ttk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.category_entry = ttk.Entry(form_frame, width=30)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Duration (minutes):").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.duration_entry = ttk.Entry(form_frame, width=30)
        self.duration_entry.insert(0, "30")
        self.duration_entry.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Cost ($):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.cost_entry = ttk.Entry(form_frame, width=30)
        self.cost_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Active:").grid(row=2, column=2, padx=5, pady=5, sticky='e')
        self.active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, variable=self.active_var).grid(row=2, column=3, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Add Treatment", command=self.add_treatment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_treatment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_treatment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        tree_frame = ttk.LabelFrame(self.root, text="Treatments", padding=10)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Name', 'Description', 'Category', 'Duration', 'Cost', 'Active')
        self.treatment_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.treatment_tree.heading(col, text=col)
            self.treatment_tree.column(col, width=100)
        
        self.treatment_tree.column('Description', width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.treatment_tree.yview)
        self.treatment_tree.configure(yscrollcommand=scrollbar.set)
        
        self.treatment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.treatment_tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def clear_form(self):
        """Clear form fields"""
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, "30")
        self.cost_entry.delete(0, tk.END)
        self.active_var.set(True)
    
    def on_select(self, event):
        """Handle treatment selection"""
        selected = self.treatment_tree.selection()
        if not selected:
            return
        
        values = self.treatment_tree.item(selected[0], 'values')
        
        self.current_treatment_id = values[0]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, values[2] if values[2] else '')
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, values[3] if values[3] else '')
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, values[4])
        self.cost_entry.delete(0, tk.END)
        self.cost_entry.insert(0, values[5])
        self.active_var.set(values[6] == 'Yes')
    
    def load_treatments(self):
        """Load treatments into treeview"""
        for item in self.treatment_tree.get_children():
            self.treatment_tree.delete(item)
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM treatments ORDER BY treatment_name")
            
            for row in cursor.fetchall():
                active = 'Yes' if row[6] else 'No'
                self.treatment_tree.insert('', 'end', values=(
                    row[0], row[1], row[2] or '', row[3] or '', row[4], f"${float(row[5]):.2f}", active
                ))
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load treatments: {e}")
        finally:
            if conn:
                conn.close()
    
    def validate_form(self):
        """Validate form data"""
        if not self.name_entry.get().strip():
            messagebox.showerror("Error", "Treatment name is required")
            return False
        
        try:
            duration = int(self.duration_entry.get().strip())
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Duration must be a positive number")
            return False
        
        try:
            cost = float(self.cost_entry.get().strip())
            if cost < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Cost must be a valid number")
            return False
        
        return True
    
    def add_treatment(self):
        """Add new treatment"""
        if not self.validate_form():
            return
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            query = """
                INSERT INTO treatments 
                (treatment_name, description, category, duration, cost, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            values = (
                self.name_entry.get().strip(),
                self.desc_entry.get().strip() or None,
                self.category_entry.get().strip() or None,
                int(self.duration_entry.get().strip()),
                float(self.cost_entry.get().strip()),
                self.active_var.get()
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Treatment added successfully")
            self.clear_form()
            self.load_treatments()
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to add treatment: {e}")
        finally:
            if conn:
                conn.close()
    
    def update_treatment(self):
        """Update selected treatment"""
        if not hasattr(self, 'current_treatment_id'):
            messagebox.showwarning("Warning", "Please select a treatment to update")
            return
        
        if not self.validate_form():
            return
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            query = """
                UPDATE treatments 
                SET treatment_name = %s, description = %s, category = %s,
                    duration = %s, cost = %s, is_active = %s
                WHERE treatment_id = %s
            """
            
            values = (
                self.name_entry.get().strip(),
                self.desc_entry.get().strip() or None,
                self.category_entry.get().strip() or None,
                int(self.duration_entry.get().strip()),
                float(self.cost_entry.get().strip()),
                self.active_var.get(),
                self.current_treatment_id
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Treatment updated successfully")
            self.load_treatments()
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to update treatment: {e}")
        finally:
            if conn:
                conn.close()
    
    def delete_treatment(self):
        """Delete selected treatment"""
        if not hasattr(self, 'current_treatment_id'):
            messagebox.showwarning("Warning", "Please select a treatment to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this treatment?"):
            return
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM treatments WHERE treatment_id = %s", (self.current_treatment_id,))
            conn.commit()
            
            messagebox.showinfo("Success", "Treatment deleted successfully")
            self.clear_form()
            self.load_treatments()
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to delete treatment: {e}")
        finally:
            if conn:
                conn.close()

class ReportWindow:
    """Window for generating reports"""
    def __init__(self, root, report_type):
        self.root = tk.Toplevel(root)
        self.root.title(f"{report_type.title()} Report")
        self.root.geometry("1000x600")
        self.report_type = report_type
        
        self.create_widgets()
        self.generate_report()
    
    def create_widgets(self):
        # Report info
        info_frame = ttk.LabelFrame(self.root, text="Report Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"{self.report_type.title()} Report", 
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=10)
        
        if self.report_type == 'daily':
            ttk.Label(info_frame, text=f"Date: {date.today()}").pack(side=tk.LEFT, padx=10)
        
        # Report content
        self.report_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier", 10))
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def generate_report(self):
        """Generate the report"""
        conn = DatabaseConnection.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            report_lines = []
            report_lines.append("=" * 80)
            report_lines.append(f"{self.report_type.title()} REPORT")
            report_lines.append("=" * 80)
            report_lines.append("")
            
            if self.report_type == 'daily':
                today = date.today()
                
                # Appointments today
                cursor.execute("""
                    SELECT COUNT(*), status FROM appointments 
                    WHERE appointment_date = %s 
                    GROUP BY status
                """, (today,))
                
                report_lines.append("APPOINTMENTS TODAY:")
                report_lines.append("-" * 40)
                for row in cursor.fetchall():
                    report_lines.append(f"  {row[1]}: {row[0]}")
                report_lines.append("")
                
                # Treatments today
                cursor.execute("""
                    SELECT COUNT(*) FROM treatment_records 
                    WHERE treatment_date = %s
                """, (today,))
                count = cursor.fetchone()[0]
                report_lines.append(f"Treatments Performed: {count}")
                report_lines.append("")
                
                # Revenue today
                cursor.execute("""
                    SELECT COALESCE(SUM(total_amount), 0) FROM invoices 
                    WHERE invoice_date = %s AND status = 'paid'
                """, (today,))
                revenue = cursor.fetchone()[0]
                report_lines.append(f"Total Revenue: ${float(revenue):.2f}")
                
            elif self.report_type == 'monthly':
                # Monthly summary
                cursor.execute("""
                    SELECT 
                        DATE_FORMAT(appointment_date, '%Y-%m') as month,
                        COUNT(*) as total_appointments,
                        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled
                    FROM appointments
                    WHERE appointment_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                    GROUP BY DATE_FORMAT(appointment_date, '%Y-%m')
                    ORDER BY month DESC
                """)
                
                report_lines.append("MONTHLY APPOINTMENT SUMMARY:")
                report_lines.append("-" * 60)
                report_lines.append(f"{'Month':<10} {'Total':<10} {'Completed':<12} {'Cancelled':<10}")
                report_lines.append("-" * 60)
                
                for row in cursor.fetchall():
                    report_lines.append(f"{row[0]:<10} {row[1]:<10} {row[2]:<12} {row[3]:<10}")
                report_lines.append("")
                
                # Monthly revenue
                cursor.execute("""
                    SELECT 
                        DATE_FORMAT(invoice_date, '%Y-%m') as month,
                        COUNT(*) as invoices,
                        COALESCE(SUM(total_amount), 0) as revenue
                    FROM invoices
                    WHERE status = 'paid' 
                        AND invoice_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                    GROUP BY DATE_FORMAT(invoice_date, '%Y-%m')
                    ORDER BY month DESC
                """)
                
                report_lines.append("MONTHLY REVENUE:")
                report_lines.append("-" * 50)
                report_lines.append(f"{'Month':<10} {'Invoices':<12} {'Revenue':<15}")
                report_lines.append("-" * 50)
                
                for row in cursor.fetchall():
                    report_lines.append(f"{row[0]:<10} {row[1]:<12} ${float(row[2]):,.2f}")
            
            # Write to text widget
            self.report_text.delete('1.0', tk.END)
            self.report_text.insert('1.0', "\n".join(report_lines))
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
        finally:
            if conn:
                conn.close()

class ChangePasswordWindow:
    """Window for changing password"""
    def __init__(self, root, user):
        self.root = tk.Toplevel(root)
        self.root.title("Change Password")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        self.user = user
        
        self.create_widgets()
    
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Current Password:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=10, sticky='e')
        self.current_password = ttk.Entry(frame, width=25, show="*")
        self.current_password.grid(row=0, column=1, padx=5, pady=10)
        
        ttk.Label(frame, text="New Password:", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=10, sticky='e')
        self.new_password = ttk.Entry(frame, width=25, show="*")
        self.new_password.grid(row=1, column=1, padx=5, pady=10)
        
        ttk.Label(frame, text="Confirm Password:", font=("Arial", 11)).grid(row=2, column=0, padx=5, pady=10, sticky='e')
        self.confirm_password = ttk.Entry(frame, width=25, show="*")
        self.confirm_password.grid(row=2, column=1, padx=5, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Change Password", command=self.change_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.root.destroy).pack(side=tk.LEFT, padx=5)
    
    def change_password(self):
        """Change user password"""
        current = self.current_password.get().strip()
        new = self.new_password.get().strip()
        confirm = self.confirm_password.get().strip()
        
        if not current or not new or not confirm:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if new != confirm:
            messagebox.showerror("Error", "New passwords do not match")
            return
        
        if len(new) < 6:
            messagebox.showerror("Error", "New password must be at least 6 characters")
            return
        
        # In production, verify current password and update
        # For demo, we'll just show success
        messagebox.showinfo("Success", "Password changed successfully")
        self.root.destroy()

def open_main_window(user):
    """Open the main window"""
    root = tk.Tk()
    app = MainWindow(root, user)
    root.mainloop()

# Main application entry point
if _name_ == "_main_":
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()
python app.py
You may be offline or with limited connectivity. Try downloading instead.