import boto3
import yaml
import json
import re
import os
from _authentications import Authenticate
# from telegram_bot._authentications import Authenticate
import redshift_connector
import pandas as pd
# pd.set_option('display.max_columns', None)
# pd.set_option('max_colwidth', None)


class ListQuestionaire:
    def __init__(self):
        self.secret = Authenticate().get_secret()
        self.host = self.secret['db_host']
        self.dbname = self.secret['db_dev']
        self.port = int(os.environ.get("DB_PORT", 5439))
        self.username = self.secret['redshift_username']
        self.password = self.secret['redshift_password']
        self.con = redshift_connector.connect(host=self.host
                                              , database=self.dbname
                                              , port=self.port
                                              , user=self.username
                                              , password=self.password
                                              )

        self.bucket = "studybuddy2212"  # TODO: Move this into secret. This storage will be used for writing data into
        self.s3_client = boto3.client('s3')

    def get_all_questions_available(self):
        all_input_files = self.s3_client.list_objects(Bucket=self.bucket)
        all_questions = {}
        unique_id_question = 0
        for i in all_input_files['Contents']:
            if re.match('input_v1/\S+.yaml', i['Key']):
                response = self.s3_client.get_object(Bucket=self.bucket, Key=i['Key'])
                questionaire = yaml.safe_load(response["Body"])
                for key, value in questionaire.items():
                    unique_id_question += 1
                    question = {unique_id_question: value}
                    all_questions.update(question)
        return all_questions

    def fetch_data(self, quizid: int):
        cursor = self.con.cursor()
        cursor.execute('select'
                       '  q.quizid'
                       ', q.questionid'
                       ', q.context as question_content'
                       ', o.optionid'
                       ', o.option_no'
                       ', o.context as option_content'
                       ', o.iscorrect'
                       ' from accp.dim_question q '
                       ' join accp.dim_option o on q.questionid=o.questionid '
                       ' where 1=1'
                       f' and q.quizid = {str(quizid)}')
        result = pd.DataFrame(cursor.fetchall(),
                              columns=['quizid', 'questionid', 'question_content', 'optionid', 'optin_no',
                                       'option_content', 'iscorrect'])
        cursor.close()

        # Reconstruct the fetched result to appropriate json
        questions = {}
        grouped = result.groupby('questionid')
        for questionid, gr in grouped:
            questions[int(questionid)] = {
                'question': result[result['questionid'] == questionid].question_content.dropna().unique()[0]
                , 'options': {}
                , 'correct_optionid': int(result[(result['questionid'] == questionid) & (
                            result['iscorrect'] == True)].optionid.dropna().unique()[0])
            }
            for index, row in gr.iterrows():
                option = {int(row.optionid): row.option_content}
                questions[int(row.questionid)]['options'].update(option)

        return questions


# new_fetch = ListQuestionaire().fetch_data(1)
# # all_questions = ListQuestionaire().get_all_questions_available()[1]
# # print(json.dumps(all_questions, indent=4))
# print(json.dumps(new_fetch, indent=4))

