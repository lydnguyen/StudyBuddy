import os
import openai
import yaml
# Read from source/input
input_transcript_path = os.path.abspath(os.path.join(os.getcwd(), 'sources', 'input', 'chapter_8_transcript.txt'))
f = open(input_transcript_path, 'r')
prompt_transcript = f.read()
f.close()

# Authenticate/Authorize to ChatGPT account
config_path = os.path.abspath(os.path.join(os.getcwd(), "configurations.yaml"))
with open(config_path) as f:
    config = yaml.safe_load(f)
    openai.api_key = config['openai_api_key']

# Generate Prompt (standardize to get structured answer
# prompt = f'Return in yaml format 10 multiple choice scenario-type question with 4 possible answers, in which indicates the correct answer, similar to the AWS Certified Solutions Architect Associate SAA-C03 exam. Use the following transcript: \n{prompt_transcript}'
prompt = 'Return in yaml format 2 different multiple choice scenario-type question with 4 possible answers, in which indicates the only one correct answer, content relevant to the AWS Certified Solutions Architect Associate SAA-C03 exam.' \
         'The yaml output should include unique id, question, options and the correct_answer_position.'

response = openai.Completion.create(
    engine='text-davinci-002',
    prompt=prompt,
    temperature=1,
    max_tokens=200
)

output_response = (response['choices'][0]['text'])

test = output_response.replace('---\n- id: ', '')
test = test.replace('\n  q', ':\n  q')

import json

# convert dictionary string to dictionary
res = json.loads(test)

# print result
print(res)