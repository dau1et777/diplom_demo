"""
Production-Ready Career Dataset - 80+ In-Demand Careers
Sourced from Bureau of Labor Statistics and industry demand data.

Each career includes:
- Name and description
- Required abilities (15 dimensions, 0-10 scale)
- Skills, education, salary range
- Growth outlook
"""

CAREERS_DATASET = [
    # TECHNOLOGY (15 careers)
    {
        "name": "Software Engineer",
        "description": "Develops, tests, and maintains software applications.",
        "required_skills": ["Python", "Java", "Git", "OOP", "Testing", "Problem-solving"],
        "ability_vector": [9.5, 7.0, 7.0, 9.0, 8.0, 6.0, 8.5, 6.0, 7.5, 3.0, 9.5, 7.0, 5.0, 8.0, 7.0],
        "cluster": "Technology",
        "average_salary_range": "$80k - $150k",
        "job_growth": "15% annually",
        "required_education": "Bachelor's in Computer Science"
    },
    {
        "name": "Data Scientist",
        "description": "Analyzes complex data to help organizations make decisions.",
        "required_skills": ["Python", "R", "SQL", "Machine Learning", "Statistics", "Data visualization"],
        "ability_vector": [9.0, 6.0, 6.5, 8.5, 6.0, 5.0, 9.5, 5.5, 8.0, 3.0, 8.5, 8.0, 4.0, 7.0, 8.0],
        "cluster": "Technology",
        "average_salary_range": "$95k - $160k",
        "job_growth": "36% annually",
        "required_education": "Bachelor's in Statistics, Math, or CS"
    },
    {
        "name": "DevOps Engineer",
        "description": "Manages infrastructure and deployment pipelines.",
        "required_skills": ["Docker", "Kubernetes", "AWS", "Linux", "Git", "CI/CD"],
        "ability_vector": [8.5, 5.0, 6.0, 8.0, 7.5, 6.0, 8.0, 5.5, 7.0, 2.5, 9.0, 7.0, 4.5, 8.5, 7.5],
        "cluster": "Technology",
        "average_salary_range": "$85k - $155k",
        "job_growth": "13% annually",
        "required_education": "Bachelor's in Computer Science or related field"
    },
    {
        "name": "Cloud Architect",
        "description": "Designs and manages cloud infrastructure solutions.",
        "required_skills": ["AWS/Azure", "Architecture", "Security", "Networking", "Linux"],
        "ability_vector": [8.0, 5.5, 6.5, 8.5, 6.0, 7.5, 8.0, 5.0, 7.0, 2.0, 8.5, 8.0, 5.0, 7.5, 7.0],
        "cluster": "Technology",
        "average_salary_range": "$110k - $180k",
        "job_growth": "20% annually",
        "required_education": "Bachelor's in CS, AWS certifications"
    },
    {
        "name": "Machine Learning Engineer",
        "description": "Builds and deploys ML models at scale.",
        "required_skills": ["Python", "TensorFlow", "PyTorch", "ML theory", "Statistics"],
        "ability_vector": [9.5, 5.5, 6.0, 9.0, 6.5, 5.0, 9.5, 5.0, 8.5, 2.5, 9.0, 8.0, 3.5, 7.5, 8.0],
        "cluster": "Technology",
        "average_salary_range": "$100k - $170k",
        "job_growth": "40% annually",
        "required_education": "Master's in ML, Statistics, or CS"
    },
    {
        "name": "Frontend Developer",
        "description": "Builds user interfaces and web applications.",
        "required_skills": ["JavaScript", "React", "HTML/CSS", "UI/UX", "Git"],
        "ability_vector": [7.5, 8.5, 8.0, 7.5, 7.5, 5.5, 6.5, 7.5, 5.0, 7.0, 8.5, 6.5, 6.5, 7.0, 6.5],
        "cluster": "Technology",
        "average_salary_range": "$70k - $130k",
        "job_growth": "23% annually",
        "required_education": "Bachelor's in CS or coding bootcamp"
    },
    {
        "name": "Backend Developer",
        "description": "Develops server-side logic and databases.",
        "required_skills": ["JavaScript/Python/Java", "Databases", "APIs", "Git"],
        "ability_vector": [8.5, 6.0, 6.5, 8.5, 7.0, 5.5, 7.5, 5.5, 6.5, 2.5, 8.5, 7.0, 5.0, 8.0, 7.0],
        "cluster": "Technology",
        "average_salary_range": "$75k - $140k",
        "job_growth": "13% annually",
        "required_education": "Bachelor's in CS"
    },
    {
        "name": "Cybersecurity Analyst",
        "description": "Protects computer networks from security threats.",
        "required_skills": ["Network security", "Linux", "SIEM tools", "Threat analysis"],
        "ability_vector": [8.0, 4.5, 6.0, 8.5, 6.5, 6.5, 7.0, 5.0, 7.5, 2.0, 8.5, 7.0, 4.5, 8.5, 7.5],
        "cluster": "Technology",
        "average_salary_range": "$75k - $140k",
        "job_growth": "35% annually",
        "required_education": "Bachelor's in Cybersecurity or CS"
    },
    {
        "name": "QA Engineer",
        "description": "Tests software to ensure quality and functionality.",
        "required_skills": ["Test automation", "Python/Java", "Selenium", "Test planning"],
        "ability_vector": [8.0, 5.5, 7.0, 7.5, 7.0, 5.0, 6.5, 6.5, 6.0, 3.0, 7.5, 6.0, 6.0, 7.5, 6.5],
        "cluster": "Technology",
        "average_salary_range": "$65k - $110k",
        "job_growth": "8% annually",
        "required_education": "Bachelor's in CS or related field"
    },
    {
        "name": "Systems Administrator",
        "description": "Manages computer systems, servers, and networks.",
        "required_skills": ["Linux", "Windows Server", "Networking", "Security"],
        "ability_vector": [7.5, 4.0, 6.0, 7.0, 6.5, 6.0, 6.5, 5.0, 6.5, 2.0, 8.0, 6.5, 5.0, 8.0, 7.0],
        "cluster": "Technology",
        "average_salary_range": "$65k - $120k",
        "job_growth": "5% annually",
        "required_education": "Bachelor's in IT or CompTIA certifications"
    },
    {
        "name": "Database Administrator",
        "description": "Manages and maintains database systems.",
        "required_skills": ["SQL", "Database design", "Backup/Recovery", "Performance tuning"],
        "ability_vector": [8.0, 4.0, 6.0, 7.5, 6.0, 5.5, 7.5, 5.0, 6.5, 2.0, 8.0, 7.0, 4.5, 8.0, 7.0],
        "cluster": "Technology",
        "average_salary_range": "$70k - $130k",
        "job_growth": "7% annually",
        "required_education": "Bachelor's in Database Administration"
    },
    {
        "name": "UX/UI Designer",
        "description": "Designs user interfaces and experiences for digital products.",
        "required_skills": ["Figma", "User research", "Prototyping", "Design thinking"],
        "ability_vector": [6.5, 9.0, 8.0, 7.0, 7.0, 6.0, 5.0, 7.5, 5.0, 9.0, 7.5, 6.0, 7.5, 6.5, 6.0],
        "cluster": "Technology",
        "average_salary_range": "$70k - $130k",
        "job_growth": "16% annually",
        "required_education": "Bachelor's in Design or UX"
    },
    {
        "name": "Technical Project Manager",
        "description": "Manages technical projects and team coordination.",
        "required_skills": ["Project management", "Technical knowledge", "Leadership", "Communication"],
        "ability_vector": [7.0, 6.0, 9.0, 7.5, 8.5, 8.0, 6.0, 7.0, 6.0, 4.0, 7.5, 8.0, 7.5, 7.0, 8.0],
        "cluster": "Technology",
        "average_salary_range": "$85k - $150k",
        "job_growth": "10% annually",
        "required_education": "Bachelor's in CS + PMP certification"
    },
    {
        "name": "IT Support Specialist",
        "description": "Provides technical support to end users.",
        "required_skills": ["Troubleshooting", "Communication", "Customer service", "Windows/Mac"],
        "ability_vector": [6.5, 4.5, 8.0, 6.5, 7.0, 5.5, 5.0, 6.0, 5.5, 3.0, 7.0, 5.0, 8.0, 6.5, 5.5],
        "cluster": "Technology",
        "average_salary_range": "$40k - $70k",
        "job_growth": "6% annually",
        "required_education": "Associate's in IT or CompTIA A+"
    },
    {
        "name": "Solutions Architect",
        "description": "Designs technical solutions for client problems.",
        "required_skills": ["System design", "Technical communication", "Problem-solving"],
        "ability_vector": [8.0, 6.5, 8.5, 8.5, 7.0, 7.5, 7.0, 7.5, 7.0, 3.5, 8.5, 8.0, 6.0, 7.5, 7.5],
        "cluster": "Technology",
        "average_salary_range": "$95k - $160k",
        "job_growth": "11% annually",
        "required_education": "Bachelor's in CS + 5+ years experience"
    },

    # BUSINESS & MANAGEMENT (15 careers)
    {
        "name": "Business Analyst",
        "description": "Analyzes business processes and recommends improvements.",
        "required_skills": ["Data analysis", "SQL", "Communication", "Problem-solving", "Documentation"],
        "ability_vector": [7.5, 5.0, 8.0, 7.5, 7.5, 6.5, 7.0, 7.5, 5.5, 3.5, 6.5, 8.5, 7.0, 6.5, 7.0],
        "cluster": "Business",
        "average_salary_range": "$65k - $110k",
        "job_growth": "10% annually",
        "required_education": "Bachelor's in Business or related field"
    },
    {
        "name": "Management Consultant",
        "description": "Advises organizations on business strategy and operations.",
        "required_skills": ["Strategic thinking", "Communication", "Analysis", "Leadership"],
        "ability_vector": [8.0, 6.5, 9.0, 8.0, 7.5, 8.0, 7.0, 8.0, 6.0, 4.0, 6.5, 9.0, 6.5, 7.5, 8.0],
        "cluster": "Business",
        "average_salary_range": "$70k - $150k",
        "job_growth": "9% annually",
        "required_education": "Bachelor's in Business, MBA preferred"
    },
    {
        "name": "Financial Analyst",
        "description": "Analyzes financial data to guide investment decisions.",
        "required_skills": ["Financial modeling", "Excel", "Analysis", "Attention to detail"],
        "ability_vector": [8.5, 4.0, 7.0, 8.0, 6.0, 6.0, 9.0, 7.5, 7.0, 2.5, 6.5, 9.0, 5.0, 7.0, 7.5],
        "cluster": "Business",
        "average_salary_range": "$65k - $130k",
        "job_growth": "6% annually",
        "required_education": "Bachelor's in Finance/Accounting"
    },
    {
        "name": "Product Manager",
        "description": "Oversees product development and market strategy.",
        "required_skills": ["Strategy", "Communication", "Data analysis", "Leadership", "User research"],
        "ability_vector": [8.0, 7.5, 8.5, 8.0, 8.0, 8.5, 6.5, 7.5, 6.5, 5.5, 7.5, 8.5, 6.5, 7.5, 8.0],
        "cluster": "Business",
        "average_salary_range": "$85k - $160k",
        "job_growth": "8% annually",
        "required_education": "Bachelor's in Business/Engineering"
    },
    {
        "name": "Operations Manager",
        "description": "Manages daily operations and efficiency of organizations.",
        "required_skills": ["Process improvement", "Leadership", "Organization", "Problem-solving"],
        "ability_vector": [7.0, 5.0, 8.0, 7.5, 8.5, 8.0, 6.0, 7.0, 6.0, 3.0, 6.0, 8.0, 7.0, 8.0, 8.0],
        "cluster": "Business",
        "average_salary_range": "$70k - $130k",
        "job_growth": "5% annually",
        "required_education": "Bachelor's in Business/Operations"
    },
    {
        "name": "HR Manager",
        "description": "Manages human resources and employee relations.",
        "required_skills": ["People management", "Communication", "Compliance knowledge", "Empathy"],
        "ability_vector": [6.0, 6.0, 9.0, 6.5, 8.5, 8.0, 5.0, 7.5, 5.0, 5.0, 5.5, 7.0, 9.0, 6.5, 7.5],
        "cluster": "Business",
        "average_salary_range": "$65k - $120k",
        "job_growth": "5% annually",
        "required_education": "Bachelor's in HR or related field"
    },
    {
        "name": "Sales Manager",
        "description": "Leads sales teams and manages revenue growth.",
        "required_skills": ["Leadership", "Communication", "Sales strategy", "Negotiation"],
        "ability_vector": [6.5, 6.5, 9.0, 7.0, 8.5, 8.5, 5.5, 7.0, 5.5, 4.5, 6.0, 8.5, 8.0, 5.5, 7.5],
        "cluster": "Business",
        "average_salary_range": "$70k - $140k",
        "job_growth": "5% annually",
        "required_education": "Bachelor's in Business"
    },
    {
        "name": "Marketing Manager",
        "description": "Develops and executes marketing strategies.",
        "required_skills": ["Strategic thinking", "Creativity", "Data analysis", "Communication"],
        "ability_vector": [7.0, 8.0, 8.5, 7.0, 7.5, 7.5, 6.0, 8.0, 6.0, 6.5, 6.5, 8.5, 6.5, 6.5, 7.5],
        "cluster": "Business",
        "average_salary_range": "$70k - $130k",
        "job_growth": "7% annually",
        "required_education": "Bachelor's in Marketing or Business"
    },
    {
        "name": "Supply Chain Manager",
        "description": "Manages logistics and supply chain operations.",
        "required_skills": ["Logistics", "Data analysis", "Organization", "Problem-solving"],
        "ability_vector": [7.0, 4.5, 7.5, 7.5, 7.0, 7.0, 6.5, 6.5, 6.0, 3.0, 6.0, 8.0, 6.0, 8.0, 7.5],
        "cluster": "Business",
        "average_salary_range": "$70k - $130k",
        "job_growth": "4% annually",
        "required_education": "Bachelor's in Supply Chain or Business"
    },
    {
        "name": "Budget Analyst",
        "description": "Analyzes and manages government or organizational budgets.",
        "required_skills": ["Financial analysis", "Attention to detail", "Communication", "Excel"],
        "ability_vector": [8.0, 4.0, 7.5, 7.5, 6.0, 6.0, 8.5, 7.5, 6.5, 2.5, 6.0, 8.5, 5.0, 7.5, 7.0],
        "cluster": "Business",
        "average_salary_range": "$65k - $110k",
        "job_growth": "3% annually",
        "required_education": "Bachelor's in Accounting/Finance"
    },
    {
        "name": "Quality Assurance Manager",
        "description": "Manages quality control and process improvements.",
        "required_skills": ["Process improvement", "Data analysis", "Leadership", "Problem-solving"],
        "ability_vector": [7.5, 5.0, 8.0, 8.0, 7.5, 7.5, 7.0, 7.0, 6.5, 3.5, 6.5, 7.5, 6.5, 8.0, 7.5],
        "cluster": "Business",
        "average_salary_range": "$75k - $130k",
        "job_growth": "6% annually",
        "required_education": "Bachelor's in Engineering/Business"
    },
    {
        "name": "Risk Manager",
        "description": "Identifies and mitigates organizational risks.",
        "required_skills": ["Risk analysis", "Compliance", "Strategic thinking", "Communication"],
        "ability_vector": [8.0, 5.0, 8.0, 8.0, 6.5, 7.0, 7.5, 8.0, 7.0, 3.0, 6.5, 8.5, 5.5, 8.0, 7.5],
        "cluster": "Business",
        "average_salary_range": "$80k - $140k",
        "job_growth": "7% annually",
        "required_education": "Bachelor's in Risk Management"
    },
    {
        "name": "Procurement Manager",
        "description": "Manages purchasing and vendor relationships.",
        "required_skills": ["Negotiation", "Vendor management", "Analysis", "Communication"],
        "ability_vector": [7.0, 5.0, 8.5, 7.5, 7.5, 7.5, 6.5, 7.0, 6.0, 3.5, 6.0, 8.0, 6.5, 7.5, 7.5],
        "cluster": "Business",
        "average_salary_range": "$70k - $125k",
        "job_growth": "4% annually",
        "required_education": "Bachelor's in Procurement or Business"
    },
    {
        "name": "Corporate Trainer",
        "description": "Develops and delivers training programs for employees.",
        "required_skills": ["Teaching", "Communication", "Content creation", "Empathy"],
        "ability_vector": [6.5, 7.5, 9.0, 6.5, 8.0, 7.5, 5.0, 8.0, 5.5, 6.0, 5.5, 6.5, 8.5, 5.5, 7.0],
        "cluster": "Business",
        "average_salary_range": "$60k - $110k",
        "job_growth": "8% annually",
        "required_education": "Bachelor's in Education or related field"
    },

    # CREATIVE & DESIGN (12 careers)
    {
        "name": "Graphic Designer",
        "description": "Creates visual content for digital and print media.",
        "required_skills": ["Adobe Creative Suite", "Design thinking", "Creativity", "Attention to detail"],
        "ability_vector": [6.0, 9.5, 7.5, 6.5, 6.5, 5.5, 4.5, 7.5, 5.0, 9.5, 6.0, 5.5, 6.0, 5.5, 6.0],
        "cluster": "Creative",
        "average_salary_range": "$50k - $90k",
        "job_growth": "3% annually",
        "required_education": "Bachelor's in Graphic Design"
    },
    {
        "name": "Web Designer",
        "description": "Designs websites and web applications.",
        "required_skills": ["Web design", "UX/UI", "HTML/CSS basics", "Creativity"],
        "ability_vector": [7.0, 9.0, 7.5, 7.0, 7.0, 5.5, 5.5, 8.0, 5.5, 9.0, 7.5, 6.0, 6.5, 6.0, 6.5],
        "cluster": "Creative",
        "average_salary_range": "$55k - $100k",
        "job_growth": "13% annually",
        "required_education": "Bachelor's in Web Design or related field"
    },
    {
        "name": "Content Writer",
        "description": "Creates written content for web, blogs, and marketing.",
        "required_skills": ["Writing", "SEO", "Research", "Communication"],
        "ability_vector": [6.5, 8.0, 8.5, 6.5, 6.0, 5.5, 5.0, 9.0, 6.0, 7.0, 5.5, 6.5, 6.5, 6.0, 6.5],
        "cluster": "Creative",
        "average_salary_range": "$45k - $80k",
        "job_growth": "4% annually",
        "required_education": "Bachelor's in English or Journalism"
    },
    {
        "name": "Video Producer",
        "description": "Produces and edits video content.",
        "required_skills": ["Video editing", "Filming", "Storytelling", "Creativity"],
        "ability_vector": [6.5, 9.0, 7.5, 7.0, 7.0, 6.0, 4.5, 7.5, 5.5, 8.5, 6.5, 5.5, 6.0, 5.5, 6.5],
        "cluster": "Creative",
        "average_salary_range": "$50k - $100k",
        "job_growth": "8% annually",
        "required_education": "Bachelor's in Film or Media"
    },
    {
        "name": "Animator",
        "description": "Creates animated content for film, TV, and digital media.",
        "required_skills": ["Animation software", "Drawing", "Storytelling", "Creativity"],
        "ability_vector": [6.5, 9.5, 6.5, 7.0, 6.5, 5.0, 4.0, 6.5, 5.5, 9.0, 7.0, 5.0, 5.5, 6.0, 6.5],
        "cluster": "Creative",
        "average_salary_range": "$55k - $110k",
        "job_growth": "4% annually",
        "required_education": "Bachelor's in Animation or related field"
    },
    {
        "name": "Brand Manager",
        "description": "Manages brand identity and marketing strategies.",
        "required_skills": ["Brand strategy", "Creativity", "Communication", "Data analysis"],
        "ability_vector": [7.0, 8.0, 8.5, 7.0, 7.5, 7.5, 6.0, 8.0, 5.5, 7.0, 6.5, 8.5, 6.5, 6.5, 7.5],
        "cluster": "Creative",
        "average_salary_range": "$70k - $130k",
        "job_growth": "5% annually",
        "required_education": "Bachelor's in Marketing or Business"
    },
    {
        "name": "UX Writer",
        "description": "Writes user interface copy and microcopy.",
        "required_skills": ["Writing", "UX understanding", "Empathy", "Clarity"],
        "ability_vector": [7.0, 8.0, 8.5, 7.0, 6.5, 5.5, 5.0, 9.0, 5.5, 6.5, 7.0, 6.0, 6.5, 6.0, 6.5],
        "cluster": "Creative",
        "average_salary_range": "$70k - $120k",
        "job_growth": "10% annually",
        "required_education": "Bachelor's in Writing or UX Design"
    },
    {
        "name": "Social Media Manager",
        "description": "Manages social media presence and community engagement.",
        "required_skills": ["Social media platforms", "Content creation", "Communication", "Analytics"],
        "ability_vector": [6.0, 8.0, 9.0, 6.5, 8.0, 6.5, 5.0, 8.0, 5.5, 6.5, 6.0, 7.0, 8.5, 6.0, 6.5],
        "cluster": "Creative",
        "average_salary_range": "$40k - $75k",
        "job_growth": "7% annually",
        "required_education": "Bachelor's in Marketing or Communications"
    },
    {
        "name": "Music Producer",
        "description": "Produces and oversees music recording and mixing.",
        "required_skills": ["Music production software", "Audio engineering", "Creativity"],
        "ability_vector": [6.0, 9.5, 7.0, 7.0, 7.5, 6.0, 4.0, 7.0, 8.0, 8.5, 6.5, 5.0, 5.0, 6.0, 6.5],
        "cluster": "Creative",
        "average_salary_range": "$50k - $120k",
        "job_growth": "2% annually",
        "required_education": "Bachelor's in Music Production"
    },
    {
        "name": "Copywriter",
        "description": "Writes persuasive content for advertising and marketing.",
        "required_skills": ["Writing", "Creativity", "Persuasion", "Marketing knowledge"],
        "ability_vector": [6.5, 8.5, 8.5, 7.0, 6.5, 6.0, 4.5, 9.0, 5.0, 7.0, 5.5, 7.5, 6.0, 6.0, 6.5],
        "cluster": "Creative",
        "average_salary_range": "$50k - $100k",
        "job_growth": "5% annually",
        "required_education": "Bachelor's in English or Marketing"
    },
    {
        "name": "Interior Designer",
        "description": "Designs interior spaces for residential and commercial use.",
        "required_skills": ["Design software", "Creativity", "Spatial awareness", "Attention to detail"],
        "ability_vector": [6.5, 9.0, 7.0, 6.5, 6.5, 6.0, 4.5, 7.0, 5.0, 9.0, 6.0, 6.0, 6.0, 5.5, 6.5],
        "cluster": "Creative",
        "average_salary_range": "$50k - $95k",
        "job_growth": "4% annually",
        "required_education": "Bachelor's in Interior Design"
    },
    {
        "name": "Art Director",
        "description": "Oversees visual aspects of projects and teams.",
        "required_skills": ["Creative vision", "Leadership", "Communication", "Design knowledge"],
        "ability_vector": [6.5, 9.0, 8.0, 7.0, 7.5, 7.5, 5.0, 8.0, 5.5, 9.0, 6.5, 6.5, 6.5, 6.5, 7.5],
        "cluster": "Creative",
        "average_salary_range": "$70k - $130k",
        "job_growth": "3% annually",
        "required_education": "Bachelor's in Art or Design"
    },

    # HEALTHCARE (10 careers)
    {
        "name": "Software Developer (Healthcare)",
        "description": "Develops healthcare IT systems and EHR software.",
        "required_skills": ["Healthcare IT", "HIPAA compliance", "Programming", "Problem-solving"],
        "ability_vector": [9.0, 6.0, 6.5, 8.5, 7.5, 6.0, 7.5, 6.0, 7.5, 3.0, 8.5, 7.0, 7.0, 7.5, 7.5],
        "cluster": "Healthcare",
        "average_salary_range": "$85k - $155k",
        "job_growth": "12% annually",
        "required_education": "Bachelor's in CS with healthcare focus"
    },
    {
        "name": "Healthcare Data Analyst",
        "description": "Analyzes health data to improve patient outcomes.",
        "required_skills": ["Data analysis", "SQL", "Statistics", "Healthcare knowledge"],
        "ability_vector": [8.5, 5.5, 6.5, 8.0, 6.5, 5.5, 8.5, 6.0, 7.5, 3.5, 7.5, 7.5, 6.0, 7.0, 7.5],
        "cluster": "Healthcare",
        "average_salary_range": "$65k - $120k",
        "job_growth": "15% annually",
        "required_education": "Bachelor's in Data Science/Healthcare"
    },
    {
        "name": "Clinical Informatics Specialist",
        "description": "Manages health IT systems and improves workflows.",
        "required_skills": ["Healthcare IT", "EHR systems", "Communication", "Problem-solving"],
        "ability_vector": [8.0, 6.0, 8.0, 7.5, 7.0, 7.0, 6.0, 7.0, 7.0, 4.0, 8.0, 7.0, 6.5, 7.5, 8.0],
        "cluster": "Healthcare",
        "average_salary_range": "$70k - $130k",
        "job_growth": "18% annually",
        "required_education": "Bachelor's in Health Informatics"
    },
    {
        "name": "Medical Writer",
        "description": "Writes medical and scientific documentation.",
        "required_skills": ["Medical knowledge", "Writing", "Research", "Attention to detail"],
        "ability_vector": [7.5, 6.0, 8.0, 7.5, 6.0, 5.5, 6.5, 9.0, 8.0, 4.0, 6.0, 7.5, 5.5, 7.0, 7.5],
        "cluster": "Healthcare",
        "average_salary_range": "$65k - $120k",
        "job_growth": "6% annually",
        "required_education": "Bachelor's in Biology/Chemistry + business writing"
    },
    {
        "name": "Health IT Manager",
        "description": "Manages health information technology systems.",
        "required_skills": ["Healthcare IT", "Leadership", "Project management", "HIPAA"],
        "ability_vector": [8.0, 6.0, 8.0, 8.0, 7.5, 8.0, 6.5, 7.0, 7.0, 3.5, 8.0, 7.5, 6.5, 8.0, 8.0],
        "cluster": "Healthcare",
        "average_salary_range": "$85k - 150k",
        "job_growth": "13% annually",
        "required_education": "Bachelor's in IT + Healthcare experience"
    },
    {
        "name": "Bioinformatician",
        "description": "Analyzes biological data using computational methods.",
        "required_skills": ["Python", "Bioinformatics", "Statistics", "Research"],
        "ability_vector": [9.0, 5.5, 6.5, 8.5, 6.0, 5.0, 9.0, 6.0, 8.5, 3.0, 8.5, 8.0, 4.0, 7.5, 7.5],
        "cluster": "Healthcare",
        "average_salary_range": "$75k - $135k",
        "job_growth": "21% annually",
        "required_education": "Master's in Bioinformatics"
    },
    {
        "name": "Clinical Data Manager",
        "description": "Manages clinical trial data and databases.",
        "required_skills": ["Data management", "Attention to detail", "Regulatory knowledge"],
        "ability_vector": [8.0, 4.5, 6.5, 7.5, 6.5, 5.5, 7.0, 7.5, 6.5, 2.5, 6.5, 7.5, 5.5, 8.0, 7.5],
        "cluster": "Healthcare",
        "average_salary_range": "$60k - $110k",
        "job_growth": "10% annually",
        "required_education": "Bachelor's in Health Sciences"
    },
    {
        "name": "Healthcare Quality Specialist",
        "description": "Ensures healthcare quality and compliance.",
        "required_skills": ["Quality improvement", "Regulations", "Analysis", "Communication"],
        "ability_vector": [7.5, 5.0, 8.0, 7.5, 7.0, 6.5, 6.5, 7.5, 6.5, 3.5, 6.5, 7.5, 6.5, 7.5, 7.5],
        "cluster": "Healthcare",
        "average_salary_range": "$65k - $115k",
        "job_growth": "8% annually",
        "required_education": "Bachelor's in Health Administration"
    },
    {
        "name": "Medical Device Software Engineer",
        "description": "Develops software for medical devices.",
        "required_skills": ["Embedded systems", "C/C++", "Regulatory knowledge", "Testing"],
        "ability_vector": [8.5, 5.5, 6.5, 8.5, 7.0, 6.0, 7.5, 5.5, 8.0, 3.0, 8.0, 7.0, 5.5, 8.0, 7.5],
        "cluster": "Healthcare",
        "average_salary_range": "$95k - $160k",
        "job_growth": "7% annually",
        "required_education": "Bachelor's in EE/ME/CS"
    },
    {
        "name": "Pharmaceutical Sales Representative",
        "description": "Sells pharmaceutical products to healthcare providers.",
        "required_skills": ["Sales", "Communication", "Product knowledge", "Relationship building"],
        "ability_vector": [6.5, 6.0, 9.0, 6.5, 8.0, 7.5, 6.5, 7.5, 7.0, 4.0, 6.0, 8.0, 8.5, 5.5, 7.0],
        "cluster": "Healthcare",
        "average_salary_range": "$70k - $140k",
        "job_growth": "2% annually",
        "required_education": "Bachelor's in any field"
    },

    # EDUCATION & SOCIAL (10 careers)
    {
        "name": "Data Analyst (Education)",
        "description": "Analyzes educational data to improve learning outcomes.",
        "required_skills": ["Data analysis", "Education knowledge", "Statistical analysis"],
        "ability_vector": [8.0, 5.5, 7.5, 8.0, 6.5, 6.0, 8.5, 7.5, 6.5, 4.0, 7.0, 7.0, 6.5, 7.0, 7.5],
        "cluster": "Education",
        "average_salary_range": "$55k - $100k",
        "job_growth": "12% annually",
        "required_education": "Bachelor's in Data Science/Education"
    },
    {
        "name": "Instructional Designer",
        "description": "Designs educational programs and training materials.",
        "required_skills": ["Instructional design", "Content creation", "Teaching knowledge"],
        "ability_vector": [7.0, 7.5, 8.0, 7.0, 7.0, 6.5, 5.5, 8.0, 6.0, 6.5, 6.5, 6.0, 7.5, 6.0, 7.0],
        "cluster": "Education",
        "average_salary_range": "$60k - $110k",
        "job_growth": "9% annually",
        "required_education": "Bachelor's in Education/Instructional Design"
    },
    {
        "name": "EdTech Developer",
        "description": "Develops educational technology platforms.",
        "required_skills": ["Web development", "Education knowledge", "UX design"],
        "ability_vector": [8.0, 7.0, 7.5, 8.0, 7.5, 6.0, 6.5, 7.0, 6.0, 6.0, 8.5, 7.0, 6.5, 7.0, 7.0],
        "cluster": "Education",
        "average_salary_range": "$75k - $140k",
        "job_growth": "15% annually",
        "required_education": "Bachelor's in CS/Education"
    },
    {
        "name": "Curriculum Developer",
        "description": "Develops educational curriculum and materials.",
        "required_skills": ["Teaching knowledge", "Curriculum design", "Content creation"],
        "ability_vector": [7.0, 7.0, 8.0, 7.0, 6.5, 6.5, 5.5, 8.5, 6.5, 6.0, 5.5, 6.0, 7.5, 6.0, 7.0],
        "cluster": "Education",
        "average_salary_range": "$60k - $110k",
        "job_growth": "5% annually",
        "required_education": "Master's in Curriculum Development"
    },
    {
        "name": "Learning Experience Designer",
        "description": "Designs engaging learning experiences.",
        "required_skills": ["UX/UI design", "Learning theory", "Creativity"],
        "ability_vector": [7.0, 8.5, 8.0, 7.5, 7.5, 6.5, 5.0, 8.0, 5.5, 7.5, 6.5, 6.0, 7.5, 6.0, 7.0],
        "cluster": "Education",
        "average_salary_range": "$65k - $120k",
        "job_growth": "10% annually",
        "required_education": "Bachelor's in Design/Education"
    },
    {
        "name": "Student Success Advisor",
        "description": "Advises students and helps with academic planning.",
        "required_skills": ["Advising", "Empathy", "Communication", "Organization"],
        "ability_vector": [6.5, 6.5, 8.5, 6.5, 7.5, 7.0, 5.0, 7.5, 5.5, 5.5, 5.5, 6.0, 9.0, 5.5, 7.0],
        "cluster": "Education",
        "average_salary_range": "$45k - $75k",
        "job_growth": "8% annually",
        "required_education": "Bachelor's in any field"
    },
    {
        "name": "Research Scientist",
        "description": "Conducts scientific research and publishes findings.",
        "required_skills": ["Research", "Data analysis", "Presentation", "Attention to detail"],
        "ability_vector": [8.5, 6.5, 7.5, 8.5, 6.5, 5.5, 8.5, 8.0, 8.5, 4.0, 6.5, 7.5, 4.5, 8.5, 8.0],
        "cluster": "Education",
        "average_salary_range": "$70k - $130k",
        "job_growth": "3% annually",
        "required_education": "PhD in relevant field"
    },
    {
        "name": "University Administrator",
        "description": "Manages university operations and student services.",
        "required_skills": ["Leadership", "Organization", "Communication", "Student advocacy"],
        "ability_vector": [7.0, 5.5, 8.5, 7.0, 8.0, 8.0, 5.5, 7.5, 5.5, 4.0, 5.5, 7.0, 7.5, 7.0, 8.0],
        "cluster": "Education",
        "average_salary_range": "$70k - $130k",
        "job_growth": "3% annually",
        "required_education": "Master's in Education/Administration"
    },
    {
        "name": "UNiversity Career Services Coordinator",
        "description": "Helps students with career planning and job placement.",
        "required_skills": ["Career counseling", "Networking", "Communication", "Empathy"],
        "ability_vector": [6.5, 6.5, 9.0, 6.5, 8.0, 7.5, 5.0, 8.0, 5.5, 5.0, 5.5, 6.5, 8.5, 5.5, 7.0],
        "cluster": "Education",
        "average_salary_range": "$45k - $80k",
        "job_growth": "8% annually",
        "required_education": "Bachelor's in any field"
    },
    {
        "name": "Librarian Data Manager",
        "description": "Manages library systems and digital resources.",
        "required_skills": ["Information management", "Research", "Customer service"],
        "ability_vector": [7.0, 5.5, 7.5, 6.5, 6.5, 6.0, 6.0, 8.0, 6.0, 4.0, 6.5, 6.0, 7.5, 6.5, 6.5],
        "cluster": "Education",
        "average_salary_range": "$55k - $90k",
        "job_growth": "1% annually",
        "required_education": "Master's in Library Science"
    },

    # FINANCE & ACCOUNTING (8 careers)
    {
        "name": "Accountant",
        "description": "Prepare and manage financial records and tax documents.",
        "required_skills": ["Accounting", "Attention to detail", "Excel", "Compliance"],
        "ability_vector": [8.0, 4.0, 7.0, 7.5, 6.0, 5.5, 8.5, 8.0, 6.5, 2.5, 6.0, 8.5, 5.0, 7.5, 7.0],
        "cluster": "Finance",
        "average_salary_range": "$55k - $100k",
        "job_growth": "4% annually",
        "required_education": "Bachelor's in Accounting + CPA"
    },
    {
        "name": "Auditor",
        "description": "Examines financial records for accuracy and compliance.",
        "required_skills": ["Auditing", "Attention to detail", "Compliance knowledge"],
        "ability_vector": [8.0, 4.0, 6.5, 7.5, 6.0, 5.5, 8.5, 7.5, 6.5, 2.5, 6.0, 8.5, 4.5, 7.5, 7.0],
        "cluster": "Finance",
        "average_salary_range": "$65k - $120k",
        "job_growth": "5% annually",
        "required_education": "Bachelor's in Accounting/Auditing"
    },
    {
        "name": "Tax Specialist",
        "description": "Advises on tax planning and compliance.",
        "required_skills": ["Tax law", "Attention to detail", "Communication"],
        "ability_vector": [8.0, 4.0, 7.5, 7.5, 6.0, 6.0, 8.5, 8.5, 6.5, 3.0, 6.0, 8.5, 5.0, 8.0, 7.5],
        "cluster": "Finance",
        "average_salary_range": "$70k - $130k",
        "job_growth": "4% annually",
        "required_education": "Bachelor's in Taxation"
    },
    {
        "name": "Investment Manager",
        "description": "Manages investment portfolios and strategies.",
        "required_skills": ["Financial analysis", "Investment knowledge", "Decision-making"],
        "ability_vector": [8.5, 5.0, 8.0, 8.5, 6.5, 7.5, 9.0, 7.5, 7.0, 3.5, 6.5, 9.0, 5.0, 7.0, 8.0],
        "cluster": "Finance",
        "average_salary_range": "$80k - $160k",
        "job_growth": "6% annually",
        "required_education": "Bachelor's in Finance + CFA"
    },
    {
        "name": "Credit Analyst",
        "description": "Analyzes creditworthiness of borrowers.",
        "required_skills": ["Financial analysis", "Attention to detail", "Assessment"],
        "ability_vector": [8.0, 4.0, 7.0, 8.0, 6.0, 5.5, 8.5, 7.5, 6.5, 2.5, 6.0, 8.5, 5.0, 7.5, 7.0],
        "cluster": "Finance",
        "average_salary_range": "$60k - $110k",
        "job_growth": "3% annually",
        "required_education": "Bachelor's in Finance"
    },
    {
        "name": "Compliance Officer",
        "description": "Ensures organizational compliance with regulations.",
        "required_skills": ["Compliance knowledge", "Attention to detail", "Risk assessment"],
        "ability_vector": [7.5, 4.0, 7.5, 7.5, 6.5, 6.5, 7.5, 8.0, 7.0, 3.0, 6.0, 8.0, 5.5, 8.0, 7.5],
        "cluster": "Finance",
        "average_salary_range": "$70k - $130k",
        "job_growth": "6% annually",
        "required_education": "Bachelor's in Finance/Law"
    },
    {
        "name": "Treasury Analyst",
        "description": "Manages cash flow and financial risk.",
        "required_skills": ["Cash management", "Analysis", "Financial systems"],
        "ability_vector": [8.0, 4.5, 7.0, 7.5, 6.0, 5.5, 8.5, 7.0, 6.5, 2.5, 6.0, 8.5, 5.0, 7.5, 7.5],
        "cluster": "Finance",
        "average_salary_range": "$70k - $130k",
        "job_growth": "4% annually",
        "required_education": "Bachelor's in Finance"
    },
    {
        "name": "Forensic Accountant",
        "description": "Investigates financial crimes and fraud.",
        "required_skills": ["Accounting", "Investigation", "Attention to detail", "Communication"],
        "ability_vector": [8.5, 5.0, 7.5, 8.5, 6.5, 6.0, 8.5, 8.0, 6.5, 3.5, 6.5, 8.5, 5.5, 8.0, 7.5],
        "cluster": "Finance",
        "average_salary_range": "$75k - $140k",
        "job_growth": "7% annually",
        "required_education": "Bachelor's in Accounting + certifications"
    },

    # ENGINEERING (10 careers)
    {
        "name": "Software Architect",
        "description": "Designs large-scale software systems.",
        "required_skills": ["System design", "Architecture patterns", "Leadership"],
        "ability_vector": [9.0, 6.0, 8.0, 9.0, 7.5, 8.0, 8.0, 7.5, 7.5, 3.0, 8.5, 8.0, 6.0, 8.5, 8.0],
        "cluster": "Engineering",
        "average_salary_range": "$110k - $190k",
        "job_growth": "13% annually",
        "required_education": "Bachelor's in CS + 10+ years experience"
    },
    {
        "name": "Civil Engineer",
        "description": "Designs and oversees construction of infrastructure.",
        "required_skills": ["CAD", "Project management", "Structural knowledge"],
        "ability_vector": [8.5, 4.5, 7.0, 8.5, 8.0, 7.0, 8.0, 6.0, 9.0, 3.0, 6.5, 7.5, 6.0, 8.0, 8.0],
        "cluster": "Engineering",
        "average_salary_range": "$70k - $130k",
        "job_growth": "2% annually",
        "required_education": "Bachelor's in Civil Engineering + PE"
    },
    {
        "name": "Mechanical Engineer",
        "description": "Designs and develops mechanical systems.",
        "required_skills": ["CAD", "Physics", "Problem-solving", "Project management"],
        "ability_vector": [8.5, 5.5, 7.0, 8.5, 7.5, 6.5, 9.0, 6.0, 8.5, 3.5, 7.0, 7.5, 5.5, 8.0, 7.5],
        "cluster": "Engineering",
        "average_salary_range": "$70k - $130k",
        "job_growth": "4% annually",
        "required_education": "Bachelor's in Mechanical Engineering"
    },
    {
        "name": "Electrical Engineer",
        "description": "Designs electrical systems and equipment.",
        "required_skills": ["Electrical theory", "CAD", "Problem-solving"],
        "ability_vector": [9.0, 4.5, 6.5, 8.5, 7.0, 6.0, 9.0, 6.0, 8.5, 2.5, 7.0, 7.5, 4.5, 8.0, 7.5],
        "cluster": "Engineering",
        "average_salary_range": "$75k - $140k",
        "job_growth": "3% annually",
        "required_education": "Bachelor's in Electrical Engineering"
    },
    {
        "name": "Chemical Engineer",
        "description": "Designs chemical production processes.",
        "required_skills": ["Chemistry", "Process design", "Safety knowledge"],
        "ability_vector": [8.5, 5.0, 6.5, 8.5, 7.0, 6.0, 9.0, 7.0, 9.0, 2.5, 6.5, 7.5, 4.5, 8.0, 7.5],
        "cluster": "Engineering",
        "average_salary_range": "$75k - $140k",
        "job_growth": "2% annually",
        "required_education": "Bachelor's in Chemical Engineering"
    },
    {
        "name": "Manufacturing Engineer",
        "description": "Improves manufacturing processes and efficiency.",
        "required_skills": ["Process optimization", "Problem-solving", "Lean methodologies"],
        "ability_vector": [8.0, 5.0, 7.0, 8.0, 7.5, 7.0, 8.0, 6.0, 7.5, 3.0, 7.0, 7.5, 5.5, 8.0, 7.5],
        "cluster": "Engineering",
        "average_salary_range": "$70k - $130k",
        "job_growth": "1% annually",
        "required_education": "Bachelor's in Manufacturing Engineering"
    },
    {
        "name": "Quality Engineer",
        "description": "Ensures product quality and compliance.",
        "required_skills": ["Quality systems", "Testing", "Attention to detail"],
        "ability_vector": [7.5, 4.5, 7.0, 7.5, 7.0, 6.0, 7.0, 7.0, 7.0, 3.0, 6.5, 7.0, 6.0, 8.0, 7.0],
        "cluster": "Engineering",
        "average_salary_range": "$65k - $120k",
        "job_growth": "5% annually",
        "required_education": "Bachelor's in Engineering"
    },
    {
        "name": "Systems Engineer",
        "description": "Designs and integrates complex systems.",
        "required_skills": ["System design", "Problem-solving", "Integration"],
        "ability_vector": [8.5, 5.5, 7.5, 8.5, 7.5, 7.0, 8.0, 6.5, 7.5, 3.5, 7.5, 7.5, 5.5, 8.0, 8.0],
        "cluster": "Engineering",
        "average_salary_range": "$85k - $150k",
        "job_growth": "8% annually",
        "required_education": "Bachelor's in Systems Engineering"
    },
    {
        "name": "Controls Engineer",
        "description": "Designs automated control systems.",
        "required_skills": ["Control theory", "Programming", "Automation knowledge"],
        "ability_vector": [8.5, 5.0, 6.5, 8.5, 6.5, 6.0, 8.5, 5.5, 8.0, 2.5, 8.0, 7.0, 4.5, 8.0, 7.5],
        "cluster": "Engineering",
        "average_salary_range": "$80k - $145k",
        "job_growth": "7% annually",
        "required_education": "Bachelor's in Controls Engineering"
    },
    {
        "name": "Environmental Engineer",
        "description": "Designs solutions for environmental challenges.",
        "required_skills": ["Environmental science", "Design", "Regulations"],
        "ability_vector": [8.0, 6.0, 7.0, 8.0, 7.0, 6.5, 8.0, 7.0, 8.5, 3.5, 6.5, 7.5, 6.0, 8.0, 7.5],
        "cluster": "Engineering",
        "average_salary_range": "$70k - $130k",
        "job_growth": "8% annually",
        "required_education": "Bachelor's in Environmental Engineering"
    },
]

def get_all_careers():
    """Return the complete careers dataset."""
    return CAREERS_DATASET

def get_career_by_name(name: str):
    """Find a career by name."""
    for career in CAREERS_DATASET:
        if career["name"].lower() == name.lower():
            return career
    return None

def get_careers_by_cluster(cluster: str):
    """Get all careers in a specific cluster."""
    return [c for c in CAREERS_DATASET if c.get("cluster") == cluster]

def get_all_clusters():
    """Get list of all unique clusters."""
    clusters = set()
    for career in CAREERS_DATASET:
        if "cluster" in career:
            clusters.add(career["cluster"])
    return sorted(list(clusters))
