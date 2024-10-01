from _access_source import UpdateData
import yaml
import os
import json


file = os.path.join(os.getcwd(), 'data', 'aws.yaml')

with open(file,'r') as f:
    curriculum = yaml.full_load(f)


for key, value in curriculum.items():
    INSERT INTO accp.dim_quiz_multiple(QuizID, Quiztopic, Quizdifficulty, Quizlevel) VALUES
    (1, 'English', 1, 'beginners'),
    (2, 'English', 2, 'intermediate'),
    (3, 'Math', 2, 'intermediate'),
    (4, 'Math', 3, 'advanced'),
    (5, 'AWS Certified Solutions Architect Associate', 1, 'Availablity & Scalability')
    ;