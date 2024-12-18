import json
import dotenv
import os

import boto3

dotenv.load_dotenv()

access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')


def get_models(client, provider='meta'):
    models = client.list_foundation_models(byProvider='meta')
    ids = []
    for m in models['modelSummaries']:
        id_ = m['modelId']
        ids.append(id_)
        print(id_)

    return ids


main_prompt = """

Extract information from the text in json. Only return json. No additional text
Example:

Hello I am from bharatpur. It very cold here. Its about  9 degree celcuis. 

{
"temperature": 9,
"location": "Bharatpur"
}

Text to extract:

"""


class FoundationModel:
    def __init__(self, client_, main_prompt_=main_prompt, model_name_='us.meta.llama3-2-1b-instruct-v1:0'):
        self.client = client_
        self.base_prompt = main_prompt_
        self.model_name = model_name_

    def get_json_from_text(self, text_):

        prompt = self.base_prompt + text_ + "\n result:"
        return self.call_model(prompt, 0, 0.9, 512)

    def get_fake_letter(self):
        text_ = ("write a fake letter where a person is taking about how they are feeling and it should include "
                 "information about their current place name and temperature. The information about these should come "
                 "naturally in the letter. only generate letter nothing extra.")

        return self.call_model(text_, 0.3, 0.9, 100)

    def call_model(self, text_, temp, top_p, max_):

        try:
            # Send the prompt to the Bedrock model
            payload = {
                "prompt": text_,
                "temperature": temp,
                "top_p": top_p,
                "max_gen_len": max_
            }

            response = self.client.invoke_model(
                modelId=self.model_name,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )
            # Parse and return the response
            result = response['body'].read().decode('utf-8')
            result_json = json.loads(result)
            return result_json["generation"]
        except Exception as e:
            print(f"Error invoking model: {e}")
            return {}


if __name__ == '__main__':
    client = boto3.client('bedrock-runtime',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=access_key, region_name=region)
    fm = FoundationModel(client)
    x = fm.get_json_from_text("Hello I am from china. It very cold here. Its about  30 degree celcuis.")
    print(x)
