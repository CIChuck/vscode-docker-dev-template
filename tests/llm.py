import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

class OAI: 

    def __init__(self, systemPrompt="You are a helpful assistant."):

        super.__init__()
        self.client = OpenAI()
        self.systemPrompt = {"role": "system", "content": systemPrompt}

        load_dotenv()

    def get_chatresponse(self, prompt, temperature = .5, max_tokens = 50,model = "gpt-4-0125-preview"):

        response = self.client.chat.completions.create(
            model = model,
            max_tokens = max_tokens,
            temperature = temperature,
            messages=[
                self.systemPrompt,
                {"role": "user", "content": prompt},
                ]
            )

        return response.choices[0].message.content
    
    
    def get_JSON_response(self, prompt, temperature = .5, max_tokens = 50,model = "gpt-4-0125-preview"):
        
        response = self.client.chat.completions.create(
            model = model,
            response_format={ "type": "json_object" },
            max_tokens = max_tokens,
            temperature = temperature,
            messages=[
                self.systemPrompt,
                {"role": "user", "content": prompt},
                ]
            )
        return response.choices[0].message.content

#oai = OAI()   
#response= oai.get_chatresponse(prompt="What is life?", temperature=0)
#print(response)






