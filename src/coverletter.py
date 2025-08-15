from jinja2 import Template

def generate_cover_letter(company, job_title, description):
    with open('../templates/cover_letter_template.j2', 'r') as f:
        template = Template(f.read())
    
    keyword = extract_keywords(description)
    return template.render(
        company=company,
        job_title=job_title,
        keyword=keyword,
        skills="Python, JavaScript, Data Analysis",  # Customize
        industry="technology",  # Customize
        experience="building projects and collaborating in teams"  # Customize
    )

def extract_keywords(description):
    keywords = ['innovation', 'technology', 'research', 'development', 'teamwork']
    for kw in keywords:
        if kw in description.lower():
            return kw
    return 'mission'