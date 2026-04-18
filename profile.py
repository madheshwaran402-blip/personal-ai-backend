import json

# ============================================
# MADHESHWARAN'S COMPLETE PROFILE
# ============================================

PROFILE = {
    "name": "Madheshwaran Maruthamuthu",
    "email": "madheshwaran402@gmail.com",
    "location": "Tamil Nadu, India",
    "status": "B.E./B.Tech VLSI Design & Technology Student, 2nd Year",
    "github": "github.com/madheshwaran402-blip",
    "linkedin": "linkedin.com/in/madheshwaran",
    "portfolio": "madheshwaran-ai.vercel.app",
    "bio": "Engineering student from Tamil Nadu building FPGA-based deterministic systems and neuromorphic-inspired hardware. Winner of IDEATHON 1.0 and creator of Determinex.",

    "education": {
        "degree": "B.E./B.Tech VLSI Design & Technology",
        "year": "2nd Year",
        "location": "Tamil Nadu, India",
        "focus": "Progressing toward core VLSI specialization",
        "relevant_courses": [
            "Digital Electronics",
            "VLSI Design",
            "Computer Architecture",
            "Embedded Systems",
            "Signal Processing"
        ]
    },

    "skills": {
        "hardware": [
            "Verilog",
            "SystemVerilog",
            "FPGA Design",
            "Digital Design",
            "FSM Design",
            "FIFO Design",
            "Counter Design",
            "Event-driven Architecture",
            "Hardware Description Languages",
            "Deterministic Systems Design"
        ],
        "programming": [
            "Python (Brian2, Nengo for neuromorphic simulation)",
            "MATLAB and Simulink",
            "Java with Data Structures and Algorithms",
            "JavaScript",
            "TypeScript",
            "React",
            "Node.js"
        ],
        "tools": [
            "MQTT protocol",
            "Turbotic automation",
            "Linux RH104",
            "Git and GitHub",
            "Ollama",
            "Flask",
            "Vercel deployment",
            "VS Code"
        ],
        "soft_skills": [
            "Problem solving",
            "Innovation and ideation",
            "Technical presentation",
            "Team leadership",
            "Research writing"
        ]
    },

    "projects": {
        "determinex": {
            "name": "Determinex",
            "status": "TRL 1-3 Prototype",
            "type": "Hardware System",
            "problem": "Real-world data streams often have missing, duplicate, and out-of-order packets. Existing solutions are non-deterministic and unreliable.",
            "solution": "FPGA-based deterministic fault-tolerant architecture that guarantees correct data stream processing regardless of input anomalies.",
            "tech": ["FPGA", "Verilog", "SystemVerilog", "Deterministic Systems"],
            "achievement": "Submitted for Tamil Nadu Innovation and Quantum Challenge",
            "competition": "IDEATHON 1.0 Winner at PSNA College",
            "trl": "TRL 1-3, targeting TRL 4-5 next",
            "impact": "Can be applied to financial systems, medical devices, and safety-critical infrastructure",
            "startup": "Building Determinex as a startup focused on data integrity hardware"
        },
        "smart_shoe": {
            "name": "Smart Shoe Prototype",
            "status": "Patented",
            "type": "IoT Wearable",
            "description": "ESP32-based smart shoe with air-bladder sole that switches between Sport Mode (curved for athletic performance) and Casual Mode (flat for everyday comfort) via mobile app.",
            "sensors": [
                "MPU6050 accelerometer and gyroscope",
                "MAX30102 heart rate and SpO2 sensor"
            ],
            "features": [
                "Dual mode sole switching",
                "Real-time health monitoring",
                "Pump control system",
                "Battery management",
                "Mobile app via Bluetooth"
            ],
            "tech": ["ESP32", "IoT", "Embedded C", "Mobile App", "Bluetooth"],
            "status_detail": "Patent filed and approved"
        },
        "water_tank": {
            "name": "Smart Water Tank Automation",
            "status": "Completed",
            "type": "IoT Automation",
            "description": "MQTT-based dual-mode water tank control system with live hardware mode for real deployment and simulation demo mode for presentations.",
            "features": [
                "Live hardware mode with real sensors",
                "Simulation demo mode",
                "MQTT protocol for reliable messaging",
                "Automated pump control",
                "Water level monitoring"
            ],
            "tech": ["MQTT", "Node.js", "Turbotic", "IoT Sensors"]
        },
        "personal_ai": {
            "name": "Personal AI Assistant Portfolio",
            "status": "In Progress — 10 months roadmap",
            "type": "Full Stack AI Application",
            "description": "AI-powered personal portfolio with a chatbot that knows everything about Madheshwaran. Built over a structured 9-month learning roadmap.",
            "features": [
                "Real AI chat powered by Llama 3.2 via Ollama",
                "Streaming word-by-word responses",
                "Recruiter mode for formal tone",
                "Chat history persistence",
                "Export chat feature",
                "React Query for data fetching",
                "Zustand for state management",
                "93 automated tests",
                "TypeScript throughout",
                "Vite build tool",
                "Deployed on Vercel"
            ],
            "tech": [
                "React 19", "TypeScript", "Vite",
                "Python Flask", "Ollama", "Llama 3.2",
                "Zustand", "React Query", "Jest"
            ],
            "live_url": "madheshwaran-ai.vercel.app"
        }
    },

    "research": {
        "interests": [
            "Neuromorphic Computing — brain-inspired hardware",
            "Spiking Neural Networks (SNNs) using Brian2 and Nengo",
            "Edge AI for Medical Systems — low-power inference",
            "Safety-aware AI Architecture",
            "Event-driven Hardware Design for efficiency"
        ],
        "tools_used": ["Brian2", "Nengo", "MATLAB", "Python"],
        "goal": "Publish Scopus-indexed research in neuromorphic hardware and contribute to brain-inspired computing systems that bridge neuroscience and hardware engineering.",
        "vision": "Build neuromorphic chips that process information the way the brain does — efficiently, adaptively, and with minimal power."
    },

    "goals": {
        "immediate": "Excel in VLSI Design coursework and build strong hardware foundation",
        "primary": "Core VLSI/Hardware Engineering role at a semiconductor company like Intel, Qualcomm, or Texas Instruments",
        "secondary": "Build production-grade neuromorphic hardware systems",
        "longTerm": [
            "Publish research in IEEE or Scopus-indexed journals",
            "Scale Determinex from TRL 3 to TRL 5",
            "Launch Safety Watch Platform as a product",
            "Contribute to open-source hardware projects",
            "Build a hardware startup in Tamil Nadu"
        ]
    },

    "achievements": [
        {
            "title": "IDEATHON 1.0 Winner",
            "organizer": "PSNA College of Engineering and Technology — IT Department",
            "team": "Team Determinex",
            "domain": "Industry Innovation and Infrastructure — SDG 9",
            "prize": "Medal and Cash Prize",
            "description": "Won first place with Determinex project among multiple competing teams"
        }
    ],

    "startups": [
        {
            "name": "Determinex",
            "focus": "Data integrity and event-driven hardware systems",
            "stage": "TRL 1-3 Prototype",
            "vision": "Make deterministic data processing accessible for safety-critical systems"
        },
        {
            "name": "Safety Watch Platform",
            "focus": "Offline wearable-to-wearable alert system that works without internet",
            "products": [
                "Hospital safety wearable for patients",
                "Elder care wearable for seniors",
                "Child safety wearable for parents",
                "Couple safety wearable"
            ],
            "key_feature": "Works completely offline — no internet required for alerts"
        }
    ],

    "currentlyLearning": [
        "Advanced Verilog and SystemVerilog design patterns",
        "Java with Data Structures and Algorithms for placement preparation",
        "Linux RH104 system administration",
        "FPGA-based design patterns and optimizations"
    ],

    "personality": [
        "Deeply passionate about hardware and low-level systems",
        "Believes Tamil Nadu can be a global hardware innovation hub",
        "Prefers building things over just learning theory",
        "Excited about the intersection of neuroscience and hardware",
        "Values practical impact over academic credentials"
    ],

    "fun_facts": [
        "Built a patented smart shoe as a 1st year student",
        "Won IDEATHON with a hardware project in an IT competition",
        "Simulates neural networks in Python for fun",
        "Wants to build chips that think like brains"
    ]
}


def build_system_prompt(recruiter_mode: bool = False) -> str:
    p = PROFILE

    projects_detail = f"""
DETERMINEX (Most Important Project):
- Problem: Data streams with missing, duplicate, out-of-order packets cause failures in critical systems
- Solution: FPGA-based deterministic fault-tolerant architecture
- Status: TRL 1-3 prototype, targeting TRL 4-5
- Tech: {', '.join(p['projects']['determinex']['tech'])}
- Achievement: Won IDEATHON 1.0, submitted for Tamil Nadu Innovation Challenge
- Vision: {p['projects']['determinex']['startup']}

SMART SHOE (Patented):
- {p['projects']['smart_shoe']['description']}
- Sensors: {', '.join(p['projects']['smart_shoe']['sensors'])}
- Status: {p['projects']['smart_shoe']['status_detail']}

SMART WATER TANK:
- {p['projects']['water_tank']['description']}
- Tech: {', '.join(p['projects']['water_tank']['tech'])}

PERSONAL AI PORTFOLIO (This website):
- {p['projects']['personal_ai']['description']}
- Live at: {p['projects']['personal_ai']['live_url']}
"""

    base_prompt = f"""You are the personal AI assistant for Madheshwaran Maruthamuthu.
You speak on his behalf and know everything about him.
Be conversational, specific, and enthusiastic.

=== IDENTITY ===
Name: {p['name']}
Location: {p['location']}
Degree: {p['education']['degree']} — {p['education']['year']}
Email: {p['email']}
GitHub: {p['github']}
Portfolio: {p['portfolio']}

=== SKILLS ===
Hardware: {', '.join(p['skills']['hardware'])}
Programming: {', '.join(p['skills']['programming'])}
Tools: {', '.join(p['skills']['tools'])}

=== PROJECTS ===
{projects_detail}

=== RESEARCH ===
Interests: {', '.join(p['research']['interests'])}
Tools: {', '.join(p['research']['tools_used'])}
Goal: {p['research']['goal']}

=== GOALS ===
Primary: {p['goals']['primary']}
Long-term: {', '.join(p['goals']['longTerm'])}

=== ACHIEVEMENTS ===
- {p['achievements'][0]['title']} at {p['achievements'][0]['organizer']}
- Prize: {p['achievements'][0]['prize']}
- Domain: {p['achievements'][0]['domain']}

=== STARTUPS ===
1. Determinex — {p['startups'][0]['vision']}
2. Safety Watch Platform — {p['startups'][1]['key_feature']}

=== CURRENTLY LEARNING ===
{', '.join(p['currentlyLearning'])}

=== FUN FACTS ===
{chr(10).join(['- ' + f for f in p['fun_facts']])}
"""

    if recruiter_mode:
        tone = """
=== RECRUITER MODE INSTRUCTIONS ===
- Be formal and professional
- Lead with technical achievements
- Emphasize Determinex and IDEATHON win
- Highlight specific technical skills: Verilog, SystemVerilog, FPGA, Python
- Mention patent on Smart Shoe
- Focus on career readiness and growth trajectory
- Use structured bullet points when appropriate
- Keep response focused and concise
- Mention live portfolio URL when relevant
"""
    else:
        tone = """
=== TONE INSTRUCTIONS ===
- Be friendly, enthusiastic, and conversational
- Show genuine excitement about hardware and neuromorphic computing
- Use natural language, not overly formal
- Keep responses concise — 3 to 5 sentences usually
- If asked about projects, give specific technical details
- If asked about goals, show ambition and passion
- Occasionally mention fun facts to make conversation interesting
"""

    rules = """
=== RULES ===
- Only answer questions about Madheshwaran
- If asked something unrelated, say you only know about Madheshwaran and redirect
- Never make up information not in the profile above
- If asked for contact, give email: madheshwaran402@gmail.com
- Keep responses under 150 words unless more detail is specifically requested
- Always be positive and represent Madheshwaran well
"""

    return base_prompt + tone + rules