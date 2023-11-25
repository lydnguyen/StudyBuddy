import boto3
import yaml
import json
import re
import os
from _authentications import Authenticate
import redshift_connector


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

    def fetch_data(self):
        cursor = self.con.cursor()
        cursor.execute('select * from accp.dim_participant;')
        result = cursor.fetchall()
        cursor.close()
        return result


# all_questions = ListQuestionaire().fetch_data()
# print(all_questions)
# all_questions = ListQuestionaire().get_all_questions_available()
# print(json.dumps(all_questions, indent=4))
