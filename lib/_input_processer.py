import os
import openai
import yaml
# Read from source/input

# Authenticate/Authorize to ChatGPT account
config_path = os.path.abspath(os.path.join(os.getcwd(), "configurations.yaml"))
with open(config_path) as f:
    config = yaml.safe_load(f)
    openai.api_key = config['openai_api_key']

# Generate Prompt (standardize to get structured answer
prompt = 'Create 1 multiple choice scenario-type questions (with answer) ' \
         'similar to the AWS Certified Solutions Architect Associate SAA-C03 exam.'

response = openai.Completion.create(
    engine='text-davinci-002',
    prompt=prompt,
    temperature=1,
    max_tokens=200
)

print(response['choices'][0]['text'])


print(response.choices[0].text)
#
