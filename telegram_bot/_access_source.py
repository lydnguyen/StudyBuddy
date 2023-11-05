import boto3
import yaml
# import json
import re


class ListQuestionaire:
    def __init__(self):
        self.bucket = "studybuddy2212"
        self.s3_client = boto3.client('s3')

    def get_all_questions_available(self):
        all_input_files = self.s3_client.list_objects(Bucket=self.bucket)
        all_questions = {}
        unique_id_question = 0
        for i in all_input_files['Contents']:
            if re.match('input_v1/\S+.yaml', i['Key']):
            # if re.match('input/\S+.yaml', i['Key']):
                response = self.s3_client.get_object(Bucket=self.bucket, Key=i['Key'])
                questionaire = yaml.safe_load(response["Body"])
                for key, value in questionaire.items():
                    unique_id_question += 1
                    question = {unique_id_question: value}
                    all_questions.update(question)
        return all_questions

# all_questions = ListQuestionaire().get_all_questions_available()
# print(json.dumps(all_questions, indent=4))

