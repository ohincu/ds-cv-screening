#############################################
# Load libraries
#############################################

# Get files
import pandas as pd 
# Iterate over each CV file
import os 
# Exclude certain words
from nltk.corpus import stopwords 
# Transform words to tokens
from nltk.tokenize import word_tokenize 
# Extract text from CVs in PDF
import pdfplumber
# Visualize the final evaluation
import plotly.graph_objects as go 

#############################################
# Load skills file and manipulate it
#############################################

def extract_skills(csv_file):
    skills_df = pd.read_csv(csv_file)
    skills_by_area = {}
    for area, skills in skills_df.items():
        area = area.lower()
        skills = [skill.lower() for skill in skills.dropna()]
        # Skip the first column (skill area) so no points are assigned
        if area != 'skill area':
            for skill in skills:
                skills_by_area[skill] = area

    return skills_by_area

skills_by_area = extract_skills('CV_Screening_Skills.csv')

# Preprocess CV text
def preprocess_text(text):
    tokens = word_tokenize(text)
    stopwords_list = set(stopwords.words('english'))
    tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stopwords_list]
    return tokens

#############################################
# Extract text from CVs in PDF
#############################################

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        text = text.replace('\n', ' ').lower()
    return text

def assign_points(pdf_path, points_by_cv, skill_areas):
    pdf_text = extract_text_from_pdf(pdf_path)
    pdf_tokens = preprocess_text(pdf_text)
    points_by_area = {area: 0 for area in skill_areas}
    # Assign points for each skill area mentioned
    for i, token in enumerate(pdf_tokens):
        if token in skills_by_area:
            area = skills_by_area[token]
            points_by_area[area] += 1
    # Update points by CV
    cv_name = os.path.basename(pdf_path)
    points_by_cv[cv_name] = points_by_area

#############################################
# Assign points for each skill area mentioned
#############################################

pdf_folder = 'CVs'
points_by_cv = {}
skill_areas = list(set(skills_by_area.values()))

# Process each PDF in the folder and update points dictionary
for file in os.listdir(pdf_folder):
    if file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, file)
        assign_points(pdf_path, points_by_cv, skill_areas)

data = {area: [] for area in skill_areas}
for cv_name, points in points_by_cv.items():
    for area in skill_areas:
        data[area].append(points[area])


#############################################
# Plot results
#############################################

fig = go.Figure()
for area in skill_areas:
    fig.add_trace(go.Bar(
        y = list(points_by_cv.keys()),
        x = data[area],
        name = area,
        orientation = 'h'
    ))

fig.update_layout(barmode = 'stack', title = 'Skill Points by CV', yaxis_title = 'CV', xaxis_title = 'Points')
fig.show()
