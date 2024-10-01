# Extract the questions, the multiple answers, and most voted answers from file:///C:/Users/lanyd/OneDrive/Documents/Python%20Projects/StudyBuddy/sources/AWS%20Certified%20Solutions%20Architect%20-%20Associate%20SAA-C03%20Exam%20%E2%80%93%20Free%20Exam%20Q&As,%20Page%201%20_%20ExamTopics.html
from bs4 import BeautifulSoup
import os
import json
import re
import pandas as pd


html_doc = os.path.join(os.getcwd(), 'sources', 'html_questions.html')

with open(html_doc, encoding='utf8', mode='r') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

questionaire = soup.find_all("div", class_="card-body question-body")
dict_qa = {}
question_id = 0
aws_services = {
    'Amazon API': []
    , 'Amazon AppFlow': []
    , 'Amazon Athena': []
    , 'Amazon Aurora': []
    , 'Amazon Cloud': []
    , 'Amazon CloudFront': []
    , 'Amazon CloudWatch': []
    , 'Amazon Cognito': []
    , 'Amazon Comprehend': []
    , 'Amazon Connect': []
    , 'Amazon Detective': []
    , 'Amazon DLM': []
    , 'Amazon DocumentDB': []
    , 'Amazon DynamoD': []
    , 'Amazon DynamoDB': []
    , 'Amazon DynamoDProvision': []
    , 'Amazon DynamoDUse': []
    , 'Amazon EBS': []
    , 'Amazon EC2-backed': []
    , 'Amazon EC2': []
    , 'Amazon ECR': []
    , 'Amazon ECS': []
    , 'Amazon EFS': []
    , 'Amazon EKS': []
    , 'Amazon Elastic': []
    , 'Amazon ElastiCache': []
    , 'Amazon Elasticsearch': []
    , 'Amazon EMR': []
    , 'Amazon EventBridge': []
    , 'Amazon FSx': []
    , 'Amazon GuardDuty': []
    , 'Amazon Inspector': []
    , 'Amazon Kinesis': []
    , 'Amazon Lex': []
    , 'Amazon Lightsail': []
    , 'Amazon Linux': []
    , 'Amazon Machine': []
    , 'Amazon Macie': []
    , 'Amazon MQ': []
    , 'Amazon MSK': []
    , 'Amazon OpenSearch': []
    , 'Amazon Pinpoint': []
    , 'Amazon Polly': []
    , 'Amazon QuickSight': []
    , 'Amazon RDS': []
    , 'Amazon Redshift': []
    , 'Amazon Rekognition': []
    , 'Amazon Resource': []
    , 'Amazon Route 53': []
    , 'Amazon S3': []
    , 'Amazon SageMaker': []
    , 'Amazon SES': []
    , 'Amazon SNS': []
    , 'Amazon SOS': []
    , 'Amazon SQS': []
    , 'Amazon Textract': []
    , 'Amazon Transcribe': []
    , 'Amazon Translate': []
    , 'Amazon VPC': []
    , 'Amazon WorkMail': []
    , 'AWS Amplify': []
    , 'AWS API': []
    , 'AWS App': []
    , 'AWS App2Container': []
    , 'AWS AppConfig': []
    , 'AWS Application': []
    , 'AWS AppSync': []
    , 'AWS Audit': []
    , 'AWS Auto': []
    , 'AWS Backup': []
    , 'AWS Batch': []
    , 'AWS Billing': []
    , 'AWS Budgets': []
    , 'AWS Certificate': []
    , 'AWS CLI': []
    , 'AWS Client': []
    , 'AWS Cloud': []
    , 'AWS CloudFormation': []
    , 'AWS CloudTrail': []
    , 'AWS Config': []
    , 'AWS Control': []
    , 'AWS Cost': []
    , 'AWS Data': []
    , 'AWS DataSync': []
    , 'AWS Direct': []
    , 'AWS Directory': []
    , 'AWS DMS': []
    , 'AWS Elastic': []
    , 'AWS Fargate': []
    , 'AWS Firewall': []
    , 'AWS Global': []
    , 'AWS Glue': []
    , 'AWS IAM': []
    , 'AWS KMS': []
    , 'AWS Lake': []
    , 'AWS Lambda': []
    , 'AWS Load': []
    , 'AWS Marketplace': []
    , 'AWS Network': []
    , 'AWS Organizations': []
    , 'AWS ParallelCluster': []
    , 'AWS PrivateLink': []
    , 'AWS RAM': []
    , 'AWS Resource': []
    , 'AWS Schema': []
    , 'AWS SCT': []
    , 'AWS SDK': []
    , 'AWS Secrets': []
    , 'AWS Security': []
    , 'AWS Shield': []
    , 'AWS Single': []
    , 'AWS Site-to-Site': []
    , 'AWS Snow': []
    , 'AWS Snowball': []
    , 'AWS Snowcone': []
    , 'AWS SSO': []
    , 'AWS Step': []
    , 'AWS Storage': []
    , 'AWS STS': []
    , 'AWS Systems': []
    , 'AWS Transfer': []
    , 'AWS Transit': []
    , 'AWS Trusted': []
    , 'AWS VPN': []
    , 'AWS WAF': []
    , 'AWS X-Ray': []
}

curriculum =\
    {
        'IAM & AWS CLI': ['IAM', 'CLI', 'policies', 'roles', 'control tower', 'Directory']
        , 'EC2': ['EC2', 'private', 'public', 'elastic', 'ENI', 'EBS', 'AMI', 'EFS']
        , 'High Availablity & Scalability': ['ELB', 'ASG', 'NLB', 'GWLB', 'sticky sessions', 'cross zone load balancing', 'SSL', 'connection draining', 'scaling policy']
        , 'RDS + Aurora + ElastiCache': ['RDS', 'Aurora', 'ElastiCache']
        , 'Route 53': ['DNS', 'Route 53', 'TTL', 'CNAME', 'ALIAS', 'Route policy']
        , 'S3': ['S3', 'Glacier']
        , 'CloudFront & AWS Global Accelerator': ['Cloudfront', 'Global Accelerator']
        , 'AWS Storage Extras': ['Snow', 'FSx', 'Storage Gateway', 'Transfer Family', 'DataSync']
        , 'Decoupling applications': ['SQS', 'SNS', 'Kinesis', 'ActiveMQ', 'MQ', 'queues']
        , 'Containers on AWS': ['ECS', 'Fargate', 'ECR', 'EKS', 'AWS App Runner']
        , 'Serverless Solutions': ['Lambda', 'DynamoDB', 'Step Functions', 'Amazon Cognito']
        , 'Databases in AWS': ['RDS', 'Aurora', 'ElastiCache', 'DynamoDB', 'S3', 'DocumentDB', 'Neptune', 'Keyspaces', 'QLDB', 'Timestream']
        , 'Data & Analytics': ['Athena', 'Redshift', 'OpenSearch', 'EMR', 'QuickSight', 'Glue', 'Kinesis', 'MSK', 'Big Data']
        , 'Machine Learning': ['Rekognition', 'Transcribe', 'Polly', 'Translate', 'Lex', 'Connect', 'Comprehend', 'Sagemaker', 'Forecast', 'Kendra', 'Personalize', 'Textract']
        , 'AWS Monitor & Audit': ['Monitoring', 'CloudWatch', 'EventBridge', 'CloudTrail', 'Config']
        , 'AWS Security & Encryption': ['Security', 'Encryption', 'KMS', 'Encrypt', 'SSM', 'Secret Manager', 'Certificate', 'ACM', 'WAF', 'Shield', 'Firewall', 'DDoS protection', 'GuardDuty', 'Inspector', 'Macie']
        , 'Networking VPC': ['CIDR', 'Private', 'Public', 'VPC', 'Subnet', 'Internet Gateways', 'Route tables', 'Bastion Hosts', 'NAT', 'NACL', 'VPN', ' Site to site', 'Gateway', 'Direct Connect', 'Transit', 'IPv6', 'Egress', 'Network']
        , 'Disaster Recovery & Migration': ['Disaster', 'Migration', 'DMS', 'MGN', 'VMware']
        , 'Other AWS services': ['CloudFormation', 'SES', 'Pinpoint', 'SSM', 'Session Manager', 'Cost Explorer', 'Cost Anomaly Detection', 'AWS BAtch', 'Appflow', 'Amplify']
    }

def find_aws_services(text):
    regex = r'(?:Amazon|AWS)\s\b[\w-]+\b'
    # Use regex to find abbreviations, which are in uppercase and can include parentheses
    abbreviations = re.findall(regex, text)
    # Clean up parentheses around some abbreviations
    return [abbr.strip('()') for abbr in abbreviations]


def find_voted_correct_answer(html):
    voted_element = html.find('div', class_='voted-answers-tally d-none')
    if voted_element.find('script') is None:
        element_correct_answer = html.find('span', class_='correct-answer').text
    else:
        list_voted_element = json.loads(voted_element.find('script').text)
        element_correct_answer = [i['voted_answers'] for i in list_voted_element if i['is_most_voted'] == True]

    if len(element_correct_answer) > 0:
        correct_answer = element_correct_answer[0].lower()
    else:
        correct_answer = None
    return correct_answer


for element in questionaire:
    question_id += 1
    question_element = element.find('p', class_='card-text').text.strip()
    abbreviations = find_aws_services(question_element)
    for abbr in abbreviations:
        if abbr in aws_services.keys():
            aws_services[abbr] += [question_id] if question_id not in aws_services[abbr] else []
    element_correct_answer = find_voted_correct_answer(element)
    answers_element = element.find_all('li', class_='multi-choice-item')
    dict_a = {}
    for i in answers_element:
        choice_letter = (i.find('span', class_='multi-choice-letter')['data-choice-letter'])
        answer = (i.get_text(strip=True).replace(choice_letter + '.', '').split('Most Voted')[0])
        dict_a[choice_letter] = answer
        # Use regex to find abbreviations, which are in uppercase and can include parentheses
        abbreviations = find_aws_services(answer)
        for abbr in abbreviations:
            if abbr in aws_services.keys():
                aws_services[abbr] += [question_id] if question_id not in aws_services[abbr] else []

    dict_qa[question_id] = {
        'question': question_element
        , 'correct_answer': element_correct_answer
        , 'choices': dict_a
    }

# Defining the questions that were not mentioned in the aws_service dictionary
service = []
for key, value in aws_services.items():
    service += value
general_aws_questions = []
for i in range(584):
    if i not in service:
        general_aws_questions.append(i)
general_aws_questions.pop(0)
aws_services['Other AWS services'] = general_aws_questions

# Constructing the right csv format output
df_qa_1 = pd.DataFrame.from_dict(data=dict_qa, orient='index').reset_index().rename(columns={'index':'qid'})
df_qa_1=df_qa_1[['qid', 'question', 'correct_answer']]
df_qa_choices={}
for key,value in dict_qa.items():
    df_qa_choices[key] = value['choices']

df_qa_choices_processed = pd.DataFrame.from_dict(data=df_qa_choices, orient='index').reset_index().rename(columns={'index':'qid'})
#
# #Checking content of the choices options
# df_qa_choices_processed.E.isnull()
# df_qa_choices_processed.loc[df_qa_choices_processed.F.isnull() == False]

#
result = pd.merge(right=df_qa_1, left=df_qa_choices_processed, on='qid')
result.rename(columns={
    'A': 'a'
    , 'B': 'b'
    , 'C': 'c'
    , 'D': 'd'
    , 'E': 'e'
    , 'F': 'f'
    , 'question': 'q'
    , 'correct_answer': 'ans'
}, inplace=True)
result['marks'] = 1
result['test_id'] = 0
result = result[[
    'test_id'
    , 'qid'
    , 'q'
    , 'a'
    , 'b'
    , 'c'
    , 'd'
    , 'e'
    , 'f'
    , 'ans'
    , 'marks'
]]
# result.to_csv('Questions_aws.csv', index=False)

test_id = 0
for key, value in aws_services.items():
    test_id += 1
    path = os.path.join(os.getcwd(), 'sources', 'AWS - SAA-C03', key + '.csv')
    # if not os.path.exists(path):
    #     os.makedirs(path)
    selections = [i-1 for i in value]
    q = result.iloc[selections]
    q['test_id'] = test_id
    q.to_csv(path, index=False)

