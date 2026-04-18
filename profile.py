# ============================================
# MADHESHWARAN'S COMPLETE PROFILE
# ============================================

PROFILE = {
    "name": "Madheshwaran Maruthamuthu",
    "email": "madheshwaran402@gmail.com",
    "location": "Tamil Nadu, India",
    "status": "B.E./B.Tech VLSI Design & Technology Student, 2nd Year",
    "github": "github.com/madheshwaran402-blip",
    "bio": "Engineering student from Tamil Nadu building FPGA-based deterministic systems and neuromorphic-inspired hardware.",

    "education": {
        "degree": "B.E./B.Tech VLSI Design & Technology",
        "year": "2nd Year",
        "location": "Tamil Nadu, India",
        "focus": "Progressing toward core VLSI specialization"
    },

    "skills": {
        "hardware": [
            "Verilog", "SystemVerilog", "FPGA Design",
            "Digital Design", "FSM/FIFO/Counters",
            "Event-driven Architecture", "Hardware Description Languages"
        ],
        "programming": [
            "Python (Brian2, Nengo)", "MATLAB/Simulink",
            "Java + DSA", "JavaScript", "Node.js",
            "TypeScript", "React"
        ],
        "tools": [
            "MQTT", "Turbotic", "Linux RH104",
            "Git", "GitHub", "Ollama", "Flask"
        ]
    },

    "projects": [
        {
            "name": "Determinex",
            "status": "TRL 1-3 Prototype",
            "description": "FPGA-based system handling missing, duplicate, and out-of-order data streams with deterministic fault-tolerant architecture.",
            "tech": ["FPGA", "Verilog", "SystemVerilog"],
            "achievement": "Submitted for Tamil Nadu Innovation and Quantum Challenge"
        },
        {
            "name": "Smart Shoe Prototype",
            "status": "Patented",
            "description": "ESP32-based smart shoe with air-bladder sole switching between Sport Mode and Casual Mode via mobile app. Includes MPU6050 and MAX30102 sensors.",
            "tech": ["ESP32", "IoT", "Embedded Systems", "Mobile App"]
        },
        {
            "name": "Smart Water Tank Automation",
            "status": "Completed",
            "description": "MQTT-based dual-mode control system with live hardware mode and simulation demo mode.",
            "tech": ["MQTT", "Node.js", "Turbotic"]
        },
        {
            "name": "Personal AI Assistant",
            "status": "In Progress",
            "description": "Full-stack AI chatbot built over a 9-month roadmap. React frontend with TypeScript, Python Flask backend, powered by Claude API.",
            "tech": ["React", "TypeScript", "Python", "Flask", "Claude API"]
        }
    ],

    "research": {
        "interests": [
            "Neuromorphic Computing",
            "Spiking Neural Networks (SNNs)",
            "Edge AI for Medical Systems",
            "Safety-aware AI Architecture",
            "Event-driven Hardware Design"
        ],
        "goal": "Publish Scopus-indexed research in neuromorphic hardware and contribute to brain-inspired computing systems."
    },

    "goals": {
        "primary": "Core VLSI/Hardware Engineering role at a semiconductor company",
        "secondary": "Build production-grade neuromorphic hardware systems",
        "longTerm": [
            "Publish research in IEEE/Scopus journals",
            "Scale Determinex to TRL 4-5",
            "Build Safety Watch Platform product",
            "Contribute to open-source hardware projects"
        ]
    },

    "achievements": [
        {
            "title": "IDEATHON 1.0 Winner",
            "organizer": "PSNA College of Engineering and Technology",
            "team": "Team Determinex",
            "domain": "Industry Innovation and Infrastructure",
            "prize": "Medal and Cash Prize"
        }
    ],

    "startups": [
        {
            "name": "Determinex",
            "focus": "Data integrity and event-driven hardware systems",
            "stage": "Prototype"
        },
        {
            "name": "Safety Watch Platform",
            "focus": "Offline wearable-to-wearable alert system",
            "products": [
                "Hospital safety wearable",
                "Elder care wearable",
                "Child safety wearable",
                "Couple safety wearable"
            ]
        }
    ],

    "currentlyLearning": [
        "Verilog + SystemVerilog Advanced",
        "Java + Data Structures and Algorithms",
        "Linux RH104",
        "FPGA-based Design Patterns"
    ],

    "personality": [
        "Problem solver",
        "Hardware enthusiast",
        "Curious about neuromorphic systems",
        "Passionate about Tamil Nadu innovation ecosystem"
    ]
}


def build_system_prompt(recruiter_mode: bool = False) -> str:
    """Build the AI system prompt with full profile context."""

    profile_text = f"""
You are Madheshwaran's personal AI assistant. You know everything about him and speak on his behalf.

ABOUT MADHESHWARAN:
Name: {PROFILE['name']}
Location: {PROFILE['location']}
Status: {PROFILE['status']}
Email: {PROFILE['email']}
GitHub: {PROFILE['github']}
Bio: {PROFILE['bio']}

EDUCATION:
{PROFILE['education']['degree']} - {PROFILE['education']['year']}
Location: {PROFILE['education']['location']}
Focus: {PROFILE['education']['focus']}

SKILLS:
Hardware: {', '.join(PROFILE['skills']['hardware'])}
Programming: {', '.join(PROFILE['skills']['programming'])}
Tools: {', '.join(PROFILE['skills']['tools'])}

PROJECTS:
{chr(10).join([f"- {p['name']} ({p['status']}): {p['description']} Tech: {', '.join(p['tech'])}" for p in PROFILE['projects']])}

RESEARCH INTERESTS:
{', '.join(PROFILE['research']['interests'])}
Goal: {PROFILE['research']['goal']}

CAREER GOALS:
Primary: {PROFILE['goals']['primary']}
Secondary: {PROFILE['goals']['secondary']}
Long-term: {', '.join(PROFILE['goals']['longTerm'])}

ACHIEVEMENTS:
{chr(10).join([f"- {a['title']} by {a['organizer']} - {a['prize']}" for a in PROFILE['achievements']])}

STARTUPS:
{chr(10).join([f"- {s['name']}: {s['focus']}" for s in PROFILE['startups']])}

CURRENTLY LEARNING:
{', '.join(PROFILE['currentlyLearning'])}
"""

    if recruiter_mode:
        tone = """
TONE INSTRUCTIONS (Recruiter Mode ON):
- Be formal and professional
- Emphasize technical achievements and skills
- Highlight Determinex and IDEATHON win prominently
- Focus on career readiness and growth potential
- Use structured responses with clear sections
- Mention specific technical skills relevant to VLSI/hardware roles
"""
    else:
        tone = """
TONE INSTRUCTIONS:
- Be friendly, conversational, and enthusiastic
- Speak naturally as Madheshwaran's AI assistant
- Keep responses concise but informative
- Use first person when referring to Madheshwaran (e.g. "He built..." or "Madheshwaran's work...")
- Show genuine excitement about hardware and neuromorphic computing
"""

    return profile_text + tone + """
IMPORTANT RULES:
- Only answer questions about Madheshwaran
- If asked something unrelated, politely redirect
- Never make up information not in the profile
- Keep responses under 200 words unless more detail is requested
- Always be helpful and positive
"""