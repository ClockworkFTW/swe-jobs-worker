from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx2txt
import re

from db import session, Job

# Get cleaned resume text
resume = " ".join(str(docx2txt.process("resume.docx")).split())

# Get all jobs
jobs = session.query(Job).all()

# Calculate match similarity between job description and resume
cv = CountVectorizer()

for job in jobs:

    description = re.sub(re.compile('<.*?>'), '', job.description)

    count_matrix = cv.fit_transform([resume, description])
    match_percentage = round(cosine_similarity(count_matrix)[0][1] * 100, 2)

    print(match_percentage)
