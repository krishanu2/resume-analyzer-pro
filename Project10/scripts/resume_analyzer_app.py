import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
import json
import os
from datetime import datetime

# Mock functions for demo - replace with your actual implementations
def extract_text_from_pdf(file_path):
    """Mock function - replace with your actual PDF extraction"""
    time.sleep(0.5)  # Simulate processing time
    return f"Sample resume text extracted from {os.path.basename(file_path)}"

def get_ats_score(resume_text, job_description):
    """Mock function - replace with your actual ATS scoring"""
    time.sleep(2)  # Simulate AI processing
    # Simple mock scoring based on common keywords
    common_keywords = ['python', 'data', 'analysis', 'sql', 'machine learning', 'experience']
    jd_lower = job_description.lower()
    resume_lower = resume_text.lower()
    
    matches = sum(1 for keyword in common_keywords if keyword in jd_lower and keyword in resume_lower)
    base_score = min(85, 40 + (matches * 8))
    
    return base_score + (len(resume_text) // 100)  # Bonus for content length

def analyze_resume(resume_text):
    """Mock function - replace with your actual resume analysis"""
    time.sleep(1.5)  # Simulate processing
    return {
        "basic_info": {
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+1-234-567-8900"
        },
        "structure": {
            "contact_info": "✅ Complete contact information found",
            "summary": "✅ Professional summary present",
            "experience": "✅ Work experience well-structured",
            "education": "❌ Education section needs improvement",
            "skills": "✅ Technical skills clearly listed"
        },
        "grammar": [
            "Consider using action verbs in bullet points",
            "Some sentences could be more concise",
            "Check for consistent formatting"
        ]
    }

class AnimatedButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.original_bg = kwargs.get('bg', '#1a1a1a')
        self.hover_bg = self.lighten_color(self.original_bg)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        
    def lighten_color(self, color):
        """Simple color lightening for hover effect"""
        color_map = {
            '#1a1a1a': '#2a2a2a',
            '#00ff87': '#33ff99',
            '#ff6b6b': '#ff8888',
            '#333333': '#444444'
        }
        return color_map.get(color, '#2a2a2a')
    
    def on_enter(self, event):
        self.config(bg=self.hover_bg)
        
    def on_leave(self, event):
        self.config(bg=self.original_bg)
        
    def on_click(self, event):
        self.config(bg=self.original_bg)
        
    def on_release(self, event):
        self.config(bg=self.hover_bg)

class LoadingSpinner:
    def __init__(self, parent, size=40):
        self.parent = parent
        self.size = size
        self.canvas = tk.Canvas(parent, width=size, height=size, bg='#1a1a1a', highlightthickness=0)
        self.angle = 0
        self.running = False
        
    def start(self):
        self.running = True
        self.canvas.pack(pady=10)
        self.animate()
        
    def stop(self):
        self.running = False
        self.canvas.pack_forget()
        
    def animate(self):
        if not self.running:
            return
            
        self.canvas.delete("all")
        center = self.size // 2
        radius = center - 5
        
        # Draw spinning arc
        self.canvas.create_arc(5, 5, self.size-5, self.size-5, 
                              start=self.angle, extent=60, 
                              outline='#00ff87', width=3, style='arc')
        
        self.angle = (self.angle + 10) % 360
        self.parent.after(50, self.animate)

class GradientFrame(tk.Frame):
    def __init__(self, parent, color1="#1a1a1a", color2="#2a2a2a", **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        
class ModernCard(tk.Frame):
    def __init__(self, parent, title, accent_color="#00ff87", **kwargs):
        super().__init__(parent, bg="#1a1a1a", relief="flat", bd=0, **kwargs)
        
        # Create shadow effect
        shadow = tk.Frame(self, bg="#0a0a0a", height=2)
        shadow.pack(fill="x", side="bottom")
        
        # Accent line with glow effect
        accent_line = tk.Frame(self, bg=accent_color, height=3)
        accent_line.pack(fill="x")
        
        # Title section
        title_frame = tk.Frame(self, bg="#1a1a1a", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=title, font=("Inter", 14, "bold"), 
                              bg="#1a1a1a", fg="white")
        title_label.pack(pady=20)
        
        # Content area
        self.content = tk.Frame(self, bg="#1a1a1a")
        self.content.pack(fill="both", expand=True, padx=25, pady=20)

class ResumeAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✨ Resume Analyzer Pro - AI Powered")
        self.geometry("1500x1000")
        self.configure(bg="#0a0a0a")
        self.resizable(True, True)
        
        # Configure styles
        self.configure_styles()
        
        # Job roles data
        self.job_roles = [
            "Data Analyst", "Data Scientist", "Software Engineer", "Frontend Developer",
            "Backend Developer", "Full Stack Developer", "DevOps Engineer", "Machine Learning Engineer",
            "AI Engineer", "Business Analyst", "Product Manager", "Project Manager",
            "UX/UI Designer", "Digital Marketing Specialist", "Sales Manager", "HR Manager",
            "Financial Analyst", "Marketing Manager", "Operations Manager", "Quality Assurance Engineer",
            "Database Administrator", "System Administrator", "Cloud Engineer", "Security Engineer",
            "Mobile App Developer", "Game Developer", "Technical Writer", "Consultant",
            "Research Scientist", "Business Intelligence Analyst"
        ]
        
        self.create_header()
        self.create_main_layout()
        self.create_status_bar()
        
        self.current_page = None
        self.show_page("home")
        
        # Add fade-in animation
        self.animate_startup()
    
    def configure_styles(self):
        # Configure ttk styles for modern look
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure combobox style
        style.configure('Modern.TCombobox', 
                       fieldbackground='#2a2a2a',
                       background='#2a2a2a',
                       foreground='white',
                       arrowcolor='#00ff87',
                       borderwidth=0,
                       relief='flat')
        
        # Configure progressbar style
        style.configure('Modern.Horizontal.TProgressbar',
                       background='#00ff87',
                       troughcolor='#2a2a2a',
                       borderwidth=0,
                       lightcolor='#00ff87',
                       darkcolor='#00ff87')
    
    def animate_startup(self):
        """Fade-in animation for startup"""
        self.attributes('-alpha', 0)
        self.fade_in()
    
    def fade_in(self):
        alpha = self.attributes('-alpha')
        if alpha < 1:
            self.attributes('-alpha', alpha + 0.05)
            self.after(20, self.fade_in)
    
    def create_header(self):
        header = tk.Frame(self, bg="#0a0a0a", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Logo section with glow effect
        logo_frame = tk.Frame(header, bg="#0a0a0a")
        logo_frame.pack(side="left", padx=40, pady=25)
        
        # Animated logo
        logo_canvas = tk.Canvas(logo_frame, width=40, height=40, bg="#0a0a0a", highlightthickness=0)
        logo_canvas.pack(side="left")
        logo_canvas.create_oval(5, 5, 35, 35, fill="#00ff87", outline="#33ff99", width=2)
        logo_canvas.create_text(20, 20, text="⚡", font=("Arial", 16), fill="#0a0a0a")
        
        title_label = tk.Label(logo_frame, text="Resume Analyzer Pro", 
                              font=("Inter", 20, "bold"), bg="#0a0a0a", fg="white")
        title_label.pack(side="left", padx=15)
        
        # Version badge
        version_badge = tk.Label(logo_frame, text="v2.0", font=("Inter", 8), 
                                bg="#333333", fg="#00ff87", padx=8, pady=2)
        version_badge.pack(side="left", padx=10)
        
        # Navigation with modern design
        nav_frame = tk.Frame(header, bg="#0a0a0a")
        nav_frame.pack(side="right", padx=40, pady=25)
        
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Home", "home", "#4a90e2"),
            ("📊 ATS Score", "ats", "#00ff87"),
            ("🔍 Analyzer", "analyzer", "#ff6b6b")
        ]
        
        for i, (text, page, color) in enumerate(nav_items):
            btn = AnimatedButton(nav_frame, text=text, font=("Inter", 12, "bold"),
                               bg="#1a1a1a", fg="white", bd=0, padx=30, pady=12,
                               cursor="hand2", command=lambda p=page: self.show_page(p))
            btn.pack(side="left", padx=8)
            self.nav_buttons[page] = btn
    
    def create_main_layout(self):
        self.main_container = tk.Frame(self, bg="#0a0a0a")
        self.main_container.pack(fill="both", expand=True)
        
        self.pages = {}
        self.pages["home"] = ModernHomePage(self.main_container, self)
        self.pages["ats"] = ModernATSPage(self.main_container, self, self.job_roles)
        self.pages["analyzer"] = ModernAnalyzerPage(self.main_container, self)
        
        for page in self.pages.values():
            page.pack(fill="both", expand=True)
    
    def create_status_bar(self):
        status_bar = tk.Frame(self, bg="#111111", height=35)
        status_bar.pack(fill="x")
        status_bar.pack_propagate(False)
        
        # Status info
        status_left = tk.Frame(status_bar, bg="#111111")
        status_left.pack(side="left", padx=20, pady=8)
        
        self.status_label = tk.Label(status_left, text="Ready", font=("Inter", 9), 
                                    bg="#111111", fg="#00ff87")
        self.status_label.pack(side="left")
        
        # Right side info
        status_right = tk.Frame(status_bar, bg="#111111")
        status_right.pack(side="right", padx=20, pady=8)
        
        tk.Label(status_right, text=f"© 2025 Resume Analyzer Pro | {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                font=("Inter", 8), bg="#111111", fg="#666").pack()
    
    def show_page(self, page_name):
        if self.current_page:
            self.pages[self.current_page].pack_forget()
        
        self.pages[page_name].pack(fill="both", expand=True)
        self.current_page = page_name
        
        # Update nav buttons with smooth transitions
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.config(bg="#00ff87", fg="#0a0a0a")
            else:
                btn.config(bg="#1a1a1a", fg="white")
        
        self.status_label.config(text=f"Viewing {page_name.title()} Page")

class ModernHomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0a0a0a")
        self.controller = controller
        
        # Hero section with particles effect
        hero_frame = tk.Frame(self, bg="#0a0a0a", height=300)
        hero_frame.pack(fill="x", pady=50)
        
        # Main title with glow
        title_frame = tk.Frame(hero_frame, bg="#0a0a0a")
        title_frame.pack(expand=True)
        
        main_title = tk.Label(title_frame, text="🚀 AI-Powered Resume Analysis", 
                             font=("Inter", 36, "bold"), bg="#0a0a0a", fg="white")
        main_title.pack(pady=10)
        
        subtitle = tk.Label(title_frame, text="Transform your career with cutting-edge AI technology", 
                           font=("Inter", 16), bg="#0a0a0a", fg="#888")
        subtitle.pack(pady=5)
        
        # Animated stats
        stats_container = tk.Frame(self, bg="#0a0a0a")
        stats_container.pack(fill="x", pady=40)
        
        stats_frame = tk.Frame(stats_container, bg="#0a0a0a")
        stats_frame.pack()
        
        stats_data = [
            ("50K+", "Resumes Analyzed", "#00ff87"),
            ("98%", "Success Rate", "#4a90e2"),
            ("100+", "Industries Covered", "#ff6b6b")
        ]
        
        for stat, desc, color in stats_data:
            stat_card = tk.Frame(stats_frame, bg="#1a1a1a", width=250, height=120)
            stat_card.pack(side="left", padx=20)
            stat_card.pack_propagate(False)
            
            # Accent line
            tk.Frame(stat_card, bg=color, height=3).pack(fill="x")
            
            # Content
            content = tk.Frame(stat_card, bg="#1a1a1a")
            content.pack(expand=True, fill="both", pady=20)
            
            tk.Label(content, text=stat, font=("Inter", 24, "bold"), 
                    bg="#1a1a1a", fg=color).pack()
            tk.Label(content, text=desc, font=("Inter", 11), 
                    bg="#1a1a1a", fg="#ccc").pack(pady=5)
        
        # Feature cards with hover effects
        features_frame = tk.Frame(self, bg="#0a0a0a")
        features_frame.pack(fill="both", expand=True, padx=60, pady=40)
        
        # Left feature card
        ats_card = self.create_feature_card(
            "📊 ATS Score Analysis",
            "Advanced AI matching against 30+ job roles with real-time compatibility scoring and detailed feedback",
            "#00ff87",
            lambda: controller.show_page("ats")
        )
        ats_card.pack(side="left", fill="both", expand=True, padx=20)
        
        # Right feature card
        analyzer_card = self.create_feature_card(
            "🔍 Deep Resume Analysis",
            "Comprehensive structure analysis with grammar checking, formatting insights, and actionable recommendations",
            "#ff6b6b",
            lambda: controller.show_page("analyzer")
        )
        analyzer_card.pack(side="right", fill="both", expand=True, padx=20)
    
    def create_feature_card(self, title, description, accent_color, command):
        card = tk.Frame(self, bg="#1a1a1a", cursor="hand2")
        card.bind("<Button-1>", lambda e: command())
        
        # Glow effect
        glow = tk.Frame(card, bg=accent_color, height=4)
        glow.pack(fill="x")
        
        # Content
        content = tk.Frame(card, bg="#1a1a1a")
        content.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Icon and title
        header = tk.Frame(content, bg="#1a1a1a")
        header.pack(fill="x", pady=20)
        
        tk.Label(header, text=title, font=("Inter", 20, "bold"),
                bg="#1a1a1a", fg="white").pack()
        
        # Description
        tk.Label(content, text=description, font=("Inter", 13), 
                bg="#1a1a1a", fg="#ccc", wraplength=300, justify="left").pack(pady=20)
        
        # Action button
        action_btn = AnimatedButton(content, text="Launch Analysis →", 
                                   font=("Inter", 13, "bold"),
                                   bg=accent_color, fg="white", bd=0, 
                                   pady=15, cursor="hand2", command=command)
        action_btn.pack(pady=30, fill="x")
        
        return card

class ModernATSPage(tk.Frame):
    def __init__(self, parent, controller, job_roles):
        super().__init__(parent, bg="#0a0a0a")
        self.controller = controller
        self.job_roles = job_roles
        self.resume_text = ""
        self.is_analyzing = False
        
        # Scrollable container
        self.create_scrollable_layout()
        
        # Header
        self.create_header()
        
        # Main content
        self.create_job_role_section()
        self.create_upload_section()
        self.create_job_description_section()
        self.create_analysis_section()
        
        # Loading spinner
        self.spinner = LoadingSpinner(self.scroll_frame)
    
    def create_scrollable_layout(self):
        # Create canvas and scrollbar
        canvas = tk.Canvas(self, bg="#0a0a0a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#0a0a0a")
        
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def create_header(self):
        header = tk.Frame(self.scroll_frame, bg="#0a0a0a", height=120)
        header.pack(fill="x", pady=30)
        
        # Gradient background simulation
        gradient = tk.Frame(header, bg="#1a1a1a", height=80)
        gradient.pack(fill="x", padx=40)
        
        title_frame = tk.Frame(gradient, bg="#1a1a1a")
        title_frame.pack(expand=True, pady=20)
        
        tk.Label(title_frame, text="📊 ATS Compatibility Analyzer", 
                font=("Inter", 28, "bold"), bg="#1a1a1a", fg="white").pack()
        tk.Label(title_frame, text="Advanced AI-powered resume optimization with real-time scoring", 
                font=("Inter", 14), bg="#1a1a1a", fg="#00ff87").pack(pady=8)
    
    def create_job_role_section(self):
        card = ModernCard(self.scroll_frame, "🎯 Target Job Role Selection", "#4a90e2")
        card.pack(fill="x", padx=40, pady=20)
        
        # Instructions
        tk.Label(card.content, text="Select the job role you're targeting for optimized ATS scoring:", 
                font=("Inter", 12), bg="#1a1a1a", fg="#ccc").pack(anchor="w", pady=10)
        
        # Role selection with search
        selection_frame = tk.Frame(card.content, bg="#1a1a1a")
        selection_frame.pack(fill="x", pady=10)
        
        self.role_var = tk.StringVar(value=self.job_roles[0])
        role_dropdown = ttk.Combobox(selection_frame, textvariable=self.role_var, 
                                   values=self.job_roles, state="readonly",
                                   font=("Inter", 12), width=50, style='Modern.TCombobox')
        role_dropdown.pack(side="left")
        
        # Role info
        info_label = tk.Label(selection_frame, text="💡 Choose the role that best matches your target position", 
                             font=("Inter", 10), bg="#1a1a1a", fg="#888")
        info_label.pack(side="left", padx=20)
    
    def create_upload_section(self):
        card = ModernCard(self.scroll_frame, "📄 Resume Upload", "#00ff87")
        card.pack(fill="x", padx=40, pady=20)
        
        # Upload area
        upload_area = tk.Frame(card.content, bg="#2a2a2a", relief="flat", bd=1)
        upload_area.pack(fill="x", pady=15)
        
        # Drag and drop simulation
        drop_zone = tk.Frame(upload_area, bg="#2a2a2a", height=120)
        drop_zone.pack(fill="x", padx=20, pady=20)
        drop_zone.pack_propagate(False)
        
        # Upload button and status
        upload_controls = tk.Frame(drop_zone, bg="#2a2a2a")
        upload_controls.pack(expand=True)
        
        self.upload_btn = AnimatedButton(upload_controls, text="📁 Choose Resume (PDF)", 
                                        font=("Inter", 14, "bold"), bg="#00ff87", fg="#0a0a0a",
                                        bd=0, pady=15, cursor="hand2", command=self.upload_resume)
        self.upload_btn.pack(pady=10)
        
        self.file_status = tk.Label(upload_controls, text="📋 No file selected", 
                                   font=("Inter", 12), bg="#2a2a2a", fg="#888")
        self.file_status.pack(pady=5)
        
        # File requirements
        requirements = tk.Frame(card.content, bg="#1a1a1a")
        requirements.pack(fill="x", pady=10)
        
        tk.Label(requirements, text="✅ Accepted formats: PDF | ✅ Max size: 10MB | ✅ Text-based PDFs only", 
                font=("Inter", 10), bg="#1a1a1a", fg="#666").pack()
    
    def create_job_description_section(self):
        card = ModernCard(self.scroll_frame, "📝 Job Description", "#ff9800")
        card.pack(fill="x", padx=40, pady=20)
        
        # Instructions
        instruction_frame = tk.Frame(card.content, bg="#1a1a1a")
        instruction_frame.pack(fill="x", pady=10)
        
        tk.Label(instruction_frame, text="Paste the complete job description below for accurate ATS matching:", 
                font=("Inter", 12), bg="#1a1a1a", fg="#ccc").pack(anchor="w")
        
        # Text area with modern styling
        text_container = tk.Frame(card.content, bg="#2a2a2a", relief="flat", bd=1)
        text_container.pack(fill="both", expand=True, pady=15)
        
        # Scrollable text widget
        text_frame = tk.Frame(text_container, bg="#2a2a2a")
        text_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.jd_text = tk.Text(text_frame, height=12, font=("Inter", 11), 
                              bg="#2a2a2a", fg="white", insertbackground="#00ff87", 
                              bd=0, selectbackground="#00ff87", selectforeground="#0a0a0a",
                              wrap="word", relief="flat")
        
        # Scrollbar for text
        jd_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.jd_text.yview)
        self.jd_text.configure(yscrollcommand=jd_scrollbar.set)
        
        self.jd_text.pack(side="left", fill="both", expand=True)
        jd_scrollbar.pack(side="right", fill="y")
        
        # Placeholder text
        placeholder = "Enter job description here...\n\nExample:\nWe are looking for a skilled Data Analyst to join our team...\n\nRequired Skills:\n• Python, SQL, Excel\n• Data visualization\n• Statistical analysis\n\nResponsibilities:\n• Analyze large datasets\n• Create reports and dashboards\n• Collaborate with stakeholders"
        self.jd_text.insert("1.0", placeholder)
        self.jd_text.bind("<FocusIn>", self.clear_placeholder)
        
        # Character counter
        self.char_counter = tk.Label(card.content, text="0 characters", 
                                    font=("Inter", 9), bg="#1a1a1a", fg="#666")
        self.char_counter.pack(anchor="e", pady=5)
        
        self.jd_text.bind("<KeyRelease>", self.update_char_counter)
    
    def create_analysis_section(self):
        card = ModernCard(self.scroll_frame, "🚀 AI Analysis Center", "#ff6b6b")
        card.pack(fill="x", padx=40, pady=20)
        
        # Analysis controls
        controls_frame = tk.Frame(card.content, bg="#1a1a1a")
        controls_frame.pack(fill="x", pady=20)
        
        # Analyze button
        self.analyze_btn = AnimatedButton(controls_frame, text="🔍 Analyze Resume", 
                                         font=("Inter", 16, "bold"),
                                         bg="#ff6b6b", fg="white", bd=0, 
                                         pady=18, cursor="hand2", 
                                         command=self.analyze_resume_threaded)
        self.analyze_btn.pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(controls_frame, variable=self.progress_var, 
                                           maximum=100, length=400, 
                                           style='Modern.Horizontal.TProgressbar')
        
        # Results display
        self.results_frame = tk.Frame(card.content, bg="#1a1a1a")
        self.results_frame.pack(fill="x", pady=20)
        
        self.results_label = tk.Label(self.results_frame, 
                                     text="📋 Configure settings above and click 'Analyze Resume' to begin", 
                                     font=("Inter", 13), bg="#1a1a1a", fg="#888")
        self.results_label.pack(pady=20)
    
    def clear_placeholder(self, event):
        if self.jd_text.get("1.0", "end-1c").startswith("Enter job description here..."):
            self.jd_text.delete("1.0", tk.END)
    
    def update_char_counter(self, event):
        content = self.jd_text.get("1.0", "end-1c")
        if not content.startswith("Enter job description here..."):
            char_count = len(content)
            self.char_counter.config(text=f"{char_count} characters")
    
    def upload_resume(self):
        file_path = filedialog.askopenfilename(
            title="Select Resume PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.controller.status_label.config(text="Extracting text from PDF...")
                self.update()
                
                self.resume_text = extract_text_from_pdf(file_path)
                
                if not self.resume_text.strip():
                    raise ValueError("PDF appears to be empty or scanned. Please upload a text-based PDF.")
                
                filename = os.path.basename(file_path)
                self.file_status.config(text=f"✅ {filename} ({len(self.resume_text)} characters)", fg="#00ff87")
                self.upload_btn.config(text="✅ Resume Loaded", bg="#33ff99")
                
                self.controller.status_label.config(text="Resume uploaded successfully")
                
            except Exception as e:
                self.file_status.config(text=f"❌ Error: {str(e)}", fg="#ff6b6b")
                messagebox.showerror("Upload Error", f"Could not process PDF:\n{str(e)}")
                self.controller.status_label.config(text="Upload failed")
                
    def analyze_resume_threaded(self):
        """Thread-safe analysis to prevent UI freezing"""
        if self.is_analyzing:
            return
            
        # Validation
        if not self.resume_text.strip():
            messagebox.showwarning("No Resume", "Please upload a resume first.")
            return
            
        job_desc = self.jd_text.get("1.0", "end-1c").strip()
        if not job_desc or job_desc.startswith("Enter job description here..."):
            messagebox.showwarning("No Job Description", "Please enter a job description.")
            return
        
        # Start analysis in thread
        self.is_analyzing = True
        self.analyze_btn.config(text="🔄 Analyzing...", state="disabled", bg="#666")
        self.progress_bar.pack(pady=10)
        self.spinner.start()
        
        analysis_thread = threading.Thread(target=self.perform_analysis, daemon=True)
        analysis_thread.start()
    
    def perform_analysis(self):
        """Perform the actual analysis"""
        try:
            # Update progress
            self.progress_var.set(20)
            self.controller.status_label.config(text="Analyzing resume structure...")
            
            job_desc = self.jd_text.get("1.0", "end-1c").strip()
            selected_role = self.role_var.get()
            
            # Get ATS score
            self.progress_var.set(60)
            self.controller.status_label.config(text="Calculating ATS compatibility...")
            
            ats_score = get_ats_score(self.resume_text, job_desc)
            
            self.progress_var.set(100)
            self.controller.status_label.config(text="Analysis complete!")
            
            # Schedule UI update on main thread
            self.after(100, lambda: self.display_results(ats_score, selected_role))
            
        except Exception as e:
            self.after(100, lambda: self.handle_analysis_error(str(e)))
    
    def display_results(self, ats_score, selected_role):
        """Display analysis results with modern styling"""
        self.spinner.stop()
        self.progress_bar.pack_forget()
        self.is_analyzing = False
        self.analyze_btn.config(text="🔍 Analyze Resume", state="normal", bg="#ff6b6b")
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Score display with gradient and animations
        score_container = tk.Frame(self.results_frame, bg="#1a1a1a")
        score_container.pack(fill="x", pady=20)
        
        # Main score card
        score_card = tk.Frame(score_container, bg="#2a2a2a", relief="flat", bd=0)
        score_card.pack(fill="x", pady=10)
        
        # Score header with glow effect
        score_header = tk.Frame(score_card, bg="#00ff87", height=4)
        score_header.pack(fill="x")
        
        # Score content
        score_content = tk.Frame(score_card, bg="#2a2a2a")
        score_content.pack(fill="x", padx=30, pady=25)
        
        # Large score display
        score_display = tk.Frame(score_content, bg="#2a2a2a")
        score_display.pack()
        
        # Determine score color and message
        if ats_score >= 80:
            score_color = "#00ff87"
            score_emoji = "🎉"
            score_message = "Excellent Match!"
        elif ats_score >= 60:
            score_color = "#ffa500"
            score_emoji = "👍"
            score_message = "Good Match"
        else:
            score_color = "#ff6b6b"
            score_emoji = "⚠️"
            score_message = "Needs Improvement"
        
        # Animated score circle (simulated)
        score_circle = tk.Frame(score_display, bg=score_color, width=120, height=120)
        score_circle.pack(pady=10)
        score_circle.pack_propagate(False)
        
        # Score text inside circle
        tk.Label(score_circle, text=f"{ats_score}%", font=("Inter", 28, "bold"), 
                bg=score_color, fg="white").pack(expand=True)
        
        # Score message
        tk.Label(score_display, text=f"{score_emoji} {score_message}", 
                font=("Inter", 18, "bold"), bg="#2a2a2a", fg=score_color).pack(pady=10)
        
        # Role match info
        tk.Label(score_display, text=f"Match for: {selected_role}", 
                font=("Inter", 12), bg="#2a2a2a", fg="#ccc").pack(pady=5)
        
        # Detailed breakdown
        breakdown_frame = tk.Frame(self.results_frame, bg="#1a1a1a")
        breakdown_frame.pack(fill="x", pady=20)
        
        # Recommendations section
        recommendations = self.generate_recommendations(ats_score, selected_role)
        
        rec_card = tk.Frame(breakdown_frame, bg="#1a1a1a", relief="flat", bd=1)
        rec_card.pack(fill="x", pady=10)
        
        # Recommendations header
        rec_header = tk.Frame(rec_card, bg="#4a90e2", height=3)
        rec_header.pack(fill="x")
        
        rec_title = tk.Label(rec_card, text="💡 Recommendations", 
                           font=("Inter", 16, "bold"), bg="#1a1a1a", fg="white")
        rec_title.pack(pady=15)
        
        # Recommendations list
        rec_content = tk.Frame(rec_card, bg="#1a1a1a")
        rec_content.pack(fill="x", padx=30, pady=15)
        
        for i, rec in enumerate(recommendations, 1):
            rec_item = tk.Frame(rec_content, bg="#2a2a2a")
            rec_item.pack(fill="x", pady=5, padx=10)
            
            tk.Label(rec_item, text=f"{i}. {rec}", font=("Inter", 11), 
                    bg="#2a2a2a", fg="#ccc", wraplength=600, justify="left").pack(
                    anchor="w", padx=15, pady=10)
        
        # Action buttons
        action_frame = tk.Frame(self.results_frame, bg="#1a1a1a")
        action_frame.pack(fill="x", pady=20)
        
        # Export button
        export_btn = AnimatedButton(action_frame, text="📥 Export Report", 
                                  font=("Inter", 12, "bold"), bg="#4a90e2", fg="white",
                                  bd=0, pady=12, cursor="hand2", 
                                  command=lambda: self.export_report(ats_score, selected_role))
        export_btn.pack(side="left", padx=10)
        
        # Re-analyze button
        reanalyze_btn = AnimatedButton(action_frame, text="🔄 Re-analyze", 
                                     font=("Inter", 12, "bold"), bg="#ff9800", fg="white",
                                     bd=0, pady=12, cursor="hand2",
                                     command=self.analyze_resume_threaded)
        reanalyze_btn.pack(side="left", padx=10)
        
        # Animate results appearance
        self.animate_results_appearance()
    
    def generate_recommendations(self, score, role):
        """Generate personalized recommendations based on score and role"""
        recommendations = []
        
        if score < 60:
            recommendations.extend([
                "Include more relevant keywords from the job description",
                "Quantify your achievements with specific numbers and metrics",
                "Ensure your resume format is ATS-friendly (avoid tables, images, unusual fonts)"
            ])
        
        if score < 80:
            recommendations.extend([
                "Tailor your professional summary to match the job requirements",
                "Add relevant skills that appear in the job posting",
                "Use action verbs to start bullet points in your experience section"
            ])
        
        # Role-specific recommendations
        role_recommendations = {
            "Data Analyst": [
                "Highlight experience with SQL, Python, Excel, and data visualization tools",
                "Mention specific datasets you've worked with and insights you've generated",
                "Include any statistical analysis or machine learning projects"
            ],
            "Software Engineer": [
                "Emphasize programming languages and frameworks relevant to the role",
                "Include links to your GitHub profile or portfolio projects",
                "Mention experience with version control (Git) and development methodologies"
            ],
            "Project Manager": [
                "Highlight leadership experience and team management skills",
                "Include certifications like PMP, Agile, or Scrum Master",
                "Mention specific project outcomes and budget management experience"
            ]
        }
        
        if role in role_recommendations:
            recommendations.extend(role_recommendations[role][:2])
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def export_report(self, score, role):
        """Export analysis report to file"""
        try:
            from datetime import datetime
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Analysis Report"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("=" * 50 + "\n")
                    f.write("RESUME ANALYSIS REPORT\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Target Role: {role}\n")
                    f.write(f"ATS Score: {score}%\n\n")
                    
                    f.write("RECOMMENDATIONS:\n")
                    f.write("-" * 20 + "\n")
                    recommendations = self.generate_recommendations(score, role)
                    for i, rec in enumerate(recommendations, 1):
                        f.write(f"{i}. {rec}\n")
                    
                    f.write("\n" + "=" * 50 + "\n")
                    f.write("Generated by Resume Analyzer Pro v2.0\n")
                
                messagebox.showinfo("Export Success", f"Report saved to:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not save report:\n{str(e)}")
    
    def animate_results_appearance(self):
        """Animate the appearance of results"""
        # Simple fade-in effect simulation
        self.results_frame.update_idletasks()
        
    def handle_analysis_error(self, error_message):
        """Handle analysis errors gracefully"""
        self.spinner.stop()
        self.progress_bar.pack_forget()
        self.is_analyzing = False
        self.analyze_btn.config(text="🔍 Analyze Resume", state="normal", bg="#ff6b6b")
        
        # Clear results and show error
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        error_card = tk.Frame(self.results_frame, bg="#ff6b6b")
        error_card.pack(fill="x", pady=20)
        
        tk.Label(error_card, text="❌ Analysis Error", 
                font=("Inter", 16, "bold"), bg="#ff6b6b", fg="white").pack(pady=10)
        
        tk.Label(error_card, text=error_message, 
                font=("Inter", 12), bg="#ff6b6b", fg="white", 
                wraplength=600).pack(pady=10)
        
        messagebox.showerror("Analysis Error", f"Could not analyze resume:\n{error_message}")

class ModernAnalyzerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0a0a0a")
        self.controller = controller
        self.resume_text = ""
        self.is_analyzing = False
        
        # Create scrollable layout
        self.create_scrollable_layout()
        
        # Header
        self.create_header()
        
        # Upload section
        self.create_upload_section()
        
        # Analysis section
        self.create_analysis_section()
        
        # Loading spinner
        self.spinner = LoadingSpinner(self.scroll_frame)
    
    def create_scrollable_layout(self):
        """Create scrollable layout similar to ATS page"""
        canvas = tk.Canvas(self, bg="#0a0a0a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#0a0a0a")
        
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def create_header(self):
        """Create modern header with animations"""
        header = tk.Frame(self.scroll_frame, bg="#0a0a0a", height=120)
        header.pack(fill="x", pady=30)
        
        gradient = tk.Frame(header, bg="#1a1a1a", height=80)
        gradient.pack(fill="x", padx=40)
        
        title_frame = tk.Frame(gradient, bg="#1a1a1a")
        title_frame.pack(expand=True, pady=20)
        
        tk.Label(title_frame, text="🔍 Deep Resume Analysis", 
                font=("Inter", 28, "bold"), bg="#1a1a1a", fg="white").pack()
        tk.Label(title_frame, text="Comprehensive structure analysis with AI-powered insights", 
                font=("Inter", 14), bg="#1a1a1a", fg="#ff6b6b").pack(pady=8)
    
    def create_upload_section(self):
        """Create upload section with drag-and-drop styling"""
        card = ModernCard(self.scroll_frame, "📄 Resume Upload", "#ff6b6b")
        card.pack(fill="x", padx=40, pady=20)
        
        # Upload area with modern styling
        upload_area = tk.Frame(card.content, bg="#2a2a2a", relief="flat", bd=1)
        upload_area.pack(fill="x", pady=15)
        
        # Enhanced drag-and-drop zone
        drop_zone = tk.Frame(upload_area, bg="#2a2a2a", height=150)
        drop_zone.pack(fill="x", padx=20, pady=20)
        drop_zone.pack_propagate(False)
        
        # Upload controls with better styling
        upload_controls = tk.Frame(drop_zone, bg="#2a2a2a")
        upload_controls.pack(expand=True)
        
        # Upload icon
        tk.Label(upload_controls, text="📁", font=("Arial", 30), 
                bg="#2a2a2a", fg="#ff6b6b").pack(pady=5)
        
        self.upload_btn = AnimatedButton(upload_controls, text="Choose Resume (PDF)", 
                                        font=("Inter", 14, "bold"), bg="#ff6b6b", fg="white",
                                        bd=0, pady=15, cursor="hand2", command=self.upload_resume)
        self.upload_btn.pack(pady=10)
        
        tk.Label(upload_controls, text="or drag and drop your file here", 
                font=("Inter", 11), bg="#2a2a2a", fg="#888").pack(pady=5)
        
        self.file_status = tk.Label(upload_controls, text="No file selected", 
                                   font=("Inter", 12), bg="#2a2a2a", fg="#888")
        self.file_status.pack(pady=10)
        
        # File info
        info_frame = tk.Frame(card.content, bg="#1a1a1a")
        info_frame.pack(fill="x", pady=10)
        
        tk.Label(info_frame, text="✅ Supported: PDF files | ✅ Max size: 10MB | ✅ Text-based PDFs recommended", 
                font=("Inter", 10), bg="#1a1a1a", fg="#666").pack()
    
    def create_analysis_section(self):
        """Create analysis section with modern controls"""
        card = ModernCard(self.scroll_frame, "🚀 Analysis Center", "#4a90e2")
        card.pack(fill="x", padx=40, pady=20)
        
        # Analysis controls
        controls_frame = tk.Frame(card.content, bg="#1a1a1a")
        controls_frame.pack(fill="x", pady=20)
        
        # Analyze button with enhanced styling
        self.analyze_btn = AnimatedButton(controls_frame, text="🔍 Analyze Resume Structure", 
                                         font=("Inter", 16, "bold"),
                                         bg="#4a90e2", fg="white", bd=0, 
                                         pady=18, cursor="hand2", 
                                         command=self.analyze_resume_threaded)
        self.analyze_btn.pack(pady=15)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(controls_frame, variable=self.progress_var, 
                                           maximum=100, length=400, 
                                           style='Modern.Horizontal.TProgressbar')
        
        # Results display
        self.results_frame = tk.Frame(card.content, bg="#1a1a1a")
        self.results_frame.pack(fill="x", pady=20)
        
        self.results_label = tk.Label(self.results_frame, 
                                     text="📋 Upload a resume and click 'Analyze' to begin comprehensive analysis", 
                                     font=("Inter", 13), bg="#1a1a1a", fg="#888")
        self.results_label.pack(pady=30)
    
    def upload_resume(self):
        """Upload resume with better error handling"""
        file_path = filedialog.askopenfilename(
            title="Select Resume PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.controller.status_label.config(text="Extracting text from PDF...")
                self.update()
                
                self.resume_text = extract_text_from_pdf(file_path)
                
                if not self.resume_text.strip():
                    raise ValueError("PDF appears to be empty or scanned image-based. Please upload a text-based PDF.")
                
                filename = os.path.basename(file_path)
                self.file_status.config(text=f"✅ {filename} loaded ({len(self.resume_text)} characters)", 
                                       fg="#00ff87")
                self.upload_btn.config(text="✅ Resume Loaded", bg="#33ff99")
                
                self.controller.status_label.config(text="Resume uploaded successfully")
                
            except Exception as e:
                self.file_status.config(text=f"❌ Error: {str(e)}", fg="#ff6b6b")
                messagebox.showerror("Upload Error", f"Could not process PDF:\n{str(e)}")
                self.controller.status_label.config(text="Upload failed")
    
    def analyze_resume_threaded(self):
        """Thread-safe analysis"""
        if self.is_analyzing:
            return
            
        if not self.resume_text.strip():
            messagebox.showwarning("No Resume", "Please upload a resume first.")
            return
        
        # Start analysis
        self.is_analyzing = True
        self.analyze_btn.config(text="🔄 Analyzing...", state="disabled", bg="#666")
        self.progress_bar.pack(pady=10)
        self.spinner.start()
        
        analysis_thread = threading.Thread(target=self.perform_analysis, daemon=True)
        analysis_thread.start()
    
    def perform_analysis(self):
        """Perform deep resume analysis"""
        try:
            self.progress_var.set(25)
            self.controller.status_label.config(text="Analyzing resume structure...")
            
            # Analyze resume
            analysis_result = analyze_resume(self.resume_text)
            
            self.progress_var.set(100)
            self.controller.status_label.config(text="Analysis complete!")
            
            # Display results
            self.after(100, lambda: self.display_analysis_results(analysis_result))
            
        except Exception as e:
            self.after(100, lambda: self.handle_analysis_error(str(e)))
    
    def display_analysis_results(self, analysis):
        """Display comprehensive analysis results"""
        self.spinner.stop()
        self.progress_bar.pack_forget()
        self.is_analyzing = False
        self.analyze_btn.config(text="🔍 Analyze Resume Structure", state="normal", bg="#4a90e2")
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Analysis results with modern cards
        self.create_basic_info_card(analysis.get('basic_info', {}))
        self.create_structure_analysis_card(analysis.get('structure', {}))
        self.create_grammar_suggestions_card(analysis.get('grammar', []))
        self.create_action_buttons()
    
    def create_basic_info_card(self, basic_info):
        """Create basic info display card"""
        card = tk.Frame(self.results_frame, bg="#2a2a2a")
        card.pack(fill="x", pady=10)
        
        # Header
        header = tk.Frame(card, bg="#00ff87", height=3)
        header.pack(fill="x")
        
        tk.Label(card, text="👤 Basic Information", 
                font=("Inter", 16, "bold"), bg="#2a2a2a", fg="white").pack(pady=15)
        
        # Info content
        info_frame = tk.Frame(card, bg="#2a2a2a")
        info_frame.pack(fill="x", padx=30, pady=15)
        
        for key, value in basic_info.items():
            info_row = tk.Frame(info_frame, bg="#2a2a2a")
            info_row.pack(fill="x", pady=5)
            
            tk.Label(info_row, text=f"{key.replace('_', ' ').title()}:", 
                    font=("Inter", 12, "bold"), bg="#2a2a2a", fg="#ccc").pack(side="left")
            tk.Label(info_row, text=value, 
                    font=("Inter", 12), bg="#2a2a2a", fg="white").pack(side="left", padx=10)
    
    def create_structure_analysis_card(self, structure):
        """Create structure analysis card"""
        card = tk.Frame(self.results_frame, bg="#2a2a2a")
        card.pack(fill="x", pady=10)
        
        # Header
        header = tk.Frame(card, bg="#4a90e2", height=3)
        header.pack(fill="x")
        
        tk.Label(card, text="📋 Structure Analysis", 
                font=("Inter", 16, "bold"), bg="#2a2a2a", fg="white").pack(pady=15)
        
        # Structure content
        structure_frame = tk.Frame(card, bg="#2a2a2a")
        structure_frame.pack(fill="x", padx=30, pady=15)
        
        for section, status in structure.items():
            status_row = tk.Frame(structure_frame, bg="#2a2a2a")
            status_row.pack(fill="x", pady=8)
            
            tk.Label(status_row, text=f"{section.replace('_', ' ').title()}:", 
                    font=("Inter", 12, "bold"), bg="#2a2a2a", fg="#ccc").pack(side="left")
            tk.Label(status_row, text=status, 
                    font=("Inter", 12), bg="#2a2a2a", fg="white").pack(side="left", padx=15)
    
    def create_grammar_suggestions_card(self, grammar_suggestions):
        """Create grammar suggestions card"""
        card = tk.Frame(self.results_frame, bg="#2a2a2a")
        card.pack(fill="x", pady=10)
        
        # Header
        header = tk.Frame(card, bg="#ff9800", height=3)
        header.pack(fill="x")
        
        tk.Label(card, text="📝 Grammar & Style Suggestions", 
                font=("Inter", 16, "bold"), bg="#2a2a2a", fg="white").pack(pady=15)
        
        # Suggestions content
        suggestions_frame = tk.Frame(card, bg="#2a2a2a")
        suggestions_frame.pack(fill="x", padx=30, pady=15)
        
        for i, suggestion in enumerate(grammar_suggestions, 1):
            suggestion_row = tk.Frame(suggestions_frame, bg="#333333")
            suggestion_row.pack(fill="x", pady=5, padx=5)
            
            tk.Label(suggestion_row, text=f"{i}. {suggestion}", 
                    font=("Inter", 11), bg="#333333", fg="#ccc", 
                    wraplength=600, justify="left").pack(anchor="w", padx=15, pady=10)
    
    def create_action_buttons(self):
        """Create action buttons for export and re-analysis"""
        action_frame = tk.Frame(self.results_frame, bg="#1a1a1a")
        action_frame.pack(fill="x", pady=20)
        
        # Export button
        export_btn = AnimatedButton(action_frame, text="📥 Export Analysis", 
                                  font=("Inter", 12, "bold"), bg="#4a90e2", fg="white",
                                  bd=0, pady=12, cursor="hand2", 
                                  command=self.export_analysis)
        export_btn.pack(side="left", padx=10)
        
        # Re-analyze button
        reanalyze_btn = AnimatedButton(action_frame, text="🔄 Re-analyze", 
                                     font=("Inter", 12, "bold"), bg="#ff9800", fg="white",
                                     bd=0, pady=12, cursor="hand2",
                                     command=self.analyze_resume_threaded)
        reanalyze_btn.pack(side="left", padx=10)
    
    def export_analysis(self):
        """Export analysis results to file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Analysis Report"
            )
            
            if file_path:
                # Create comprehensive report
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("=" * 60 + "\n")
                    f.write("COMPREHENSIVE RESUME ANALYSIS REPORT\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    # Add analysis content here
                    f.write("ANALYSIS COMPLETE\n")
                    f.write("See application for detailed results.\n\n")
                    
                    f.write("=" * 60 + "\n")
                    f.write("Generated by Resume Analyzer Pro v2.0\n")
                
                messagebox.showinfo("Export Success", f"Analysis report saved to:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not save report:\n{str(e)}")
    
    def handle_analysis_error(self, error_message):
        """Handle analysis errors gracefully"""
        self.spinner.stop()
        self.progress_bar.pack_forget()
        self.is_analyzing = False
        self.analyze_btn.config(text="🔍 Analyze Resume Structure", state="normal", bg="#4a90e2")
        
        # Show error message
        messagebox.showerror("Analysis Error", f"Could not analyze resume:\n{error_message}")
        self.controller.status_label.config(text="Analysis failed")

if __name__ == "__main__":
    app = ResumeAnalyzerApp()
    app.mainloop()