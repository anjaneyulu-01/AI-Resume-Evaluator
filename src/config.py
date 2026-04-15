# Configuration for Resume ATS Checker
# Customize this file to tailor the app to your needs

SKILLS_TO_DETECT = [
    # Programming Languages
    'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'kotlin',
    'swift', 'typescript', 'r', 'matlab', 'scala', 'perl', 'assembly', 'visual basic',
    
    # Web Frameworks
    'react', 'angular', 'vue', 'svelte', 'next.js', 'nuxt', 'ember',
    'node.js', 'express', 'fastapi', 'django', 'flask', 'spring', 'asp.net',
    
    # Mobile Development
    'react native', 'flutter', 'ios', 'android', 'xamarin', 'cordova',
    
    # Data Science & ML
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
    'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
    'nlp', 'computer vision', 'data analysis', 'data visualization',
    'jupyter', 'anaconda', 'spark', 'hadoop', 'hive',
    
    # Cloud Platforms
    'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
    'linode', 'vultr', 'ibm cloud', 'oracle cloud',
    
    # DevOps & Tools
    'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'bitbucket',
    'git', 'svn', 'terraform', 'ansible', 'puppet', 'chef',
    'elk stack', 'prometheus', 'grafana', 'datadog',
    
    # Databases
    'sql', 'mysql', 'postgresql', 'oracle', 'mongodb', 'redis',
    'elasticsearch', 'cassandra', 'dynamodb', 'firebase', 'mariadb',
    'sqlite', 'nosql', 'graphql', 'cypher',
    
    # Frontend Technologies
    'html', 'css', 'bootstrap', 'tailwind', 'material ui', 'webpack',
    'babel', 'npm', 'yarn', 'sass', 'less',
    
    # APIs & Architecture
    'rest', 'graphql', 'soap', 'microservices', 'serverless', 'lambda',
    'api design', 'socket.io', 'websockets',
    
    # Testing & QA
    'junit', 'pytest', 'mocha', 'jest', 'selenium', 'cypress',
    'testing', 'unit testing', 'integration testing', 'test automation',
    'tdd', 'bdd', 'appium',
    
    # Operating Systems & Networking
    'linux', 'windows', 'macos', 'unix', 'bash', 'powershell',
    'networking', 'tcp/ip', 'dns', 'ssl', 'https', 'ssh',
    
    # Productivity & Office
    'excel', 'powerpoint', 'word', 'sheets', 'docs', 'notion',
    'jira', 'confluence', 'trello', 'asana', 'monday.com',
    
    # Business & Soft Skills
    'agile', 'scrum', 'kanban', 'project management', 'leadership',
    'communication', 'teamwork', 'problem solving', 'critical thinking'
]

EDUCATION_KEYWORDS = [
    'bachelor', 'bachelors',
    'master', 'masters', 'mba', 'msc',
    'phd', 'doctorate', 'doctoral',
    'diploma', 'associate',
    'certification', 'certified',
    'bootcamp', 'course', 'training',
    'engineering', 'science', 'technology',
    'computer science', 'information technology', 'software engineering'
]

CERTIFICATION_KEYWORDS = [
    'aws certified', 'aws solutions architect',
    'azure certified', 'microsoft certified',
    'kubernetes certified', 'cka', 'ckad',
    'certified data scientist', 'gcp certified',
    'scrum master', 'certified scrum',
    'pmp', 'project management professional',
    'cissp', 'cism', 'ceh',
    'comptia', 'network+', 'security+',
    'oracle certified', 'salesforce certified',
    'google analytics', 'google ads'
]

# Scoring Weights (how much each factor contributes)
SCORE_WEIGHTS = {
    'skill_count': 2,              # Points per skill (max 20)
    'education_count': 5,          # Points per education entry (max 15)
    'certification_count': 3,      # Points per certification (max 15)
    'word_count_base': 15,         # Base points for adequate length
    'contact_info': 5,             # Points for email
    'phone_number': 2,             # Points for phone
}

# Score thresholds
SCORE_THRESHOLDS = {
    'excellent': 85,
    'good': 70,
    'average': 50,
    'poor': 0
}

# Recommendations configuration
MIN_WORD_COUNT = 500
MAX_WORD_COUNT = 1500
MIN_SKILLS = 5
MAX_KEYWORDS_TO_SHOW = 10

# UI Configuration
THEME_COLORS = {
    'primary': '#667eea',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8'
}

# Application Settings
APP_TITLE = "Resume ATS Score Checker"
APP_ICON = "📄"
PAGE_LAYOUT = "wide"

# Recommendations
RECOMMENDATIONS_CONFIG = {
    'min_word_count': f"Add more details to your resume. Aim for {MIN_WORD_COUNT}+ words.",
    'no_contact': "Add your email address to make it easy for recruiters to contact you.",
    'no_phone': "Include your phone number for direct contact.",
    'low_skills': f"Include at least {MIN_SKILLS} technical skills relevant to the position.",
    'no_education': "Add your educational background (degrees, institutions, graduation years).",
    'no_certifications': "Add professional certifications and credentials if available.",
    'low_score': "Your resume needs significant improvements. Consider restructuring content.",
    'generic': "Tailor your resume keywords to match the job description."
}
