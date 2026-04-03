# ============================================
# MADHESHWARAN'S COMPLETE PROFILE
# This is what the AI knows about you
# ============================================

profile = {
    "personal": {
        "name": "Madheshwaran Maruthamuthu",
        "email": "madheshwaran402@gmail.com",
        "location": "Tamil Nadu, India",
        "status": "Engineering Student",
        "github": "github.com/madheshwaran402-blip",
        "bio": "VLSI Design student and hardware-focused innovator building FPGA-based deterministic systems and neuromorphic-inspired architectures."
    },

    "education": {
        "degree": "B.E. / B.Tech",
        "specialization": "VLSI Design and Technology",
        "year": "2nd Year",
        "location": "Tamil Nadu, India",
        "focus": "Progressing toward core VLSI specialization"
    },

    "skills": {
        "programming": ["Python (Brian2, Nengo)", "MATLAB / Simulink", "Java + DSA", "JavaScript", "Node.js"],
        "hardware": ["Verilog", "SystemVerilog", "FPGA Design", "Digital Design", "FSM / FIFO / Counters", "Event-driven Architecture"],
        "tools": ["MQTT", "Turbotic", "Linux RH104", "Git", "GitHub"]
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
            "description": "ESP32-based shoe with air-bladder sole — Sport Mode and Casual Mode via mobile app. Includes MPU6050, MAX30102 sensors, pump control and battery management.",
            "tech": ["ESP32", "IoT", "Embedded Systems"]
        },
        {
            "name": "Smart Water Tank Automation",
            "status": "Completed",
            "description": "MQTT-based dual-mode control system with live hardware mode and simulation demo mode. Built with Node.js and Turbotic.",
            "tech": ["MQTT", "Node.js", "Turbotic"]
        },
        {
            "name": "Personal AI Assistant",
            "status": "In Progress",
            "description": "AI chatbot that knows everything about Madheshwaran. Built over a 9-month roadmap using React and Ollama.",
            "tech": ["React", "Python", "Ollama", "Flask"]
        }
    ],

    "research": {
        "interests": [
            "Neuromorphic Computing",
            "Spiking Neural Networks (SNN)",
            "Edge AI for Medical Systems",
            "Safety-aware AI Systems",
            "Event-driven Hardware"
        ],
        "goal": "Publish Scopus-indexed research in neuromorphic hardware"
    },

    "goals": {
        "primary": "Core VLSI / Hardware Engineering role",
        "secondary": "Software / Programming role",
        "long_term": [
            "Build neuromorphic hardware systems",
            "Publish Scopus-indexed research",
            "Develop real-world safety-critical systems"
        ]
    },

    "achievements": [
        {
            "title": "IDEATHON 1.0 Winner",
            "organizer": "PSNA College of Engineering and Technology — IT Dept",
            "team": "Determinex",
            "domain": "Industry Innovation & Infrastructure",
            "prize": "Medal + Cash Prize"
        }
    ],

    "startups": [
        {
            "name": "Determinex",
            "focus": "Data integrity and event-driven hardware systems"
        },
        {
            "name": "Safety Watch Platform",
            "focus": "Offline wearable-to-wearable alert system",
            "products": ["Hospital Monitoring Watch", "Elder Safety Watch", "Child Safety Watch", "Couple Safety Watch"]
        }
    ],

    "personality": [
        "Hardware-first mindset",
        "Practical and implementation-focused",
        "Competition-oriented thinking",
        "System-level problem solving",
        "Detail-oriented engineering approach"
    ],

    "currently_learning": [
        "Verilog + SystemVerilog (Advanced)",
        "Java + Data Structures",
        "Linux RH104",
        "FPGA-based Design"
    ]
}


def build_system_prompt():
    p = profile

    projects_text = ""
    for proj in p["projects"]:
        projects_text += f"\n  - {proj['name']} ({proj['status']}): {proj['description']}"
        if "achievement" in proj:
            projects_text += f" | Achievement: {proj['achievement']}"

    achievements_text = ""
    for ach in p["achievements"]:
        achievements_text += f"\n  - {ach['title']} at {ach['organizer']}. Prize: {ach['prize']}"

    startups_text = ""
    for s in p["startups"]:
        startups_text += f"\n  - {s['name']}: {s['focus']}"

    system_prompt = f"""You are the personal AI assistant for Madheshwaran Maruthamuthu, a VLSI Design student and hardware innovator from Tamil Nadu, India.

ROLE: Represent Madheshwaran professionally to recruiters, professors, and collaborators.

STRICT RULES:
1. Answer in maximum 3 sentences unless more detail is specifically requested
2. Always answer in first person — "Madheshwaran has..." or "His project..."
3. Never make up information — only use data provided below
4. Be confident, professional and specific
5. If asked something not in the data, say "That information isn't in my profile yet"
6. For technical questions, show depth and enthusiasm
7. End answers with a relevant follow-up suggestion when appropriate

TONE: Professional, confident, concise. Like a smart portfolio assistant, not a chatbot.

=== PROFILE DATA ===

NAME: {p['personal']['name']}
LOCATION: {p['personal']['location']}
EMAIL: {p['personal']['email']}
GITHUB: {p['personal']['github']}
BIO: {p['personal']['bio']}

EDUCATION:
{p['education']['degree']} in {p['education']['specialization']}, {p['education']['year']} — {p['education']['location']}

HARDWARE & VLSI SKILLS: {', '.join(p['skills']['hardware'])}
PROGRAMMING SKILLS: {', '.join(p['skills']['programming'])}
TOOLS: {', '.join(p['skills']['tools'])}

PROJECTS:{projects_text}

RESEARCH INTERESTS: {', '.join(p['research']['interests'])}
RESEARCH GOAL: {p['research']['goal']}

CAREER GOALS:
Primary: {p['goals']['primary']}
Long-term: {', '.join(p['goals']['long_term'])}

ACHIEVEMENTS:{achievements_text}

STARTUPS:{startups_text}

CURRENTLY LEARNING: {', '.join(p['currently_learning'])}

PERSONALITY: {', '.join(p['personality'])}
"""
    return system_prompt


def build_recruiter_prompt():
    """Special prompt for recruiter mode — more formal"""
    base = build_system_prompt()
    recruiter_addition = """
SPECIAL INSTRUCTION — RECRUITER MODE:
This person is a recruiter evaluating Madheshwaran for a position.
- Be extra professional and highlight achievements prominently
- Mention specific technical skills relevant to hardware/VLSI roles
- Emphasize the patented project and competition win
- Keep answers concise — recruiters are busy
- Always mention GitHub: github.com/madheshwaran402-blip
"""
    return base + recruiter_addition
    return system_prompt