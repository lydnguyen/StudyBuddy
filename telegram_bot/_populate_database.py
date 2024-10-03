from _access_source import UpdateData
import yaml
import os
import random



file = os.path.join(os.getcwd(), 'data', 'aws.yaml')

with open(file,'r') as f:
    curriculum = yaml.full_load(f)

subsql = []
for topic, level in curriculum.items():
    quiztopic = topic
    for key, value in level.items():
        quizid = str(random.randint(0,10000))
        quizdifficulty = '2' #for now just a placeholder, todo: might consider delete this column or replace with other column
        quizlevel = key

        query = "(%s, '%s', %s, '%s')" % (quizid, quiztopic, quizdifficulty, quizlevel)
        subsql.append(query)

sql = ','.join(subsql)

updater = UpdateData()
updater.insert_into_dim_quiz_multiple_tb(rows=sql)
