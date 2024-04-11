import openai
import anthropic
import os
from dotenv import load_dotenv
from openai import OpenAI

class OAI: 

    def __init__(self, model = "gpt-4-0125-preview", systemPrompt="You are a helpful assistant."):

        self.client = OpenAI()
        self.model = model
        self.systemPrompt = {"role": "system", "content": systemPrompt}

        self.tot_tokens_in = 0
        self.tokens_in = 0
        self.tot_tokens_out =0
        self.tokens_out = 0

        load_dotenv()

    def get_chatresponse(self, prompt, temperature = .5, max_tokens = 50):

        response = self.client.chat.completions.create(
            model = self.model,
            max_tokens = max_tokens,
            temperature = temperature,
            messages=[
                self.systemPrompt,
                {"role": "user", "content": prompt},
                ]
            )

        #object accounting
        
        """
        self.tot_tokens_in += response.usage.input_tokens
        self.tokens_in = response.usage.input_tokens
        self.tot_tokens_out += response.usage.output_tokens
        self.tokens_out = response.usage.output_tokens
        """
        
        #Return text, token counts
        return response.choices[0].message.content, response
    
    
    def get_JSON_response(self, prompt, temperature = .5, max_tokens = 50):
        
        response = self.client.chat.completions.create(
            model = self.model,
            response_format={ "type": "json_object" },
            max_tokens = max_tokens,
            temperature = temperature,
            messages=[
                self.systemPrompt,
                {"role": "user", "content": prompt},
                ]
            )
        
        #object accounting
        self.tot_tokens_in += response.usage.input_tokens
        self.tokens_in = response.usage.input_tokens
        self.tot_tokens_out += response.usage.output_tokens
        self.tokens_out = response.usage.output_tokens
        
        #Return text, token counts
        return response.choices[0].message.content, response




class Anthropic:

    def __init__(self, model = "claude-3-opus-20240229", systemPrompt="You are a helpful assistant."):

        load_dotenv()

        self.client = anthropic.Anthropic()
        self.model = model
        self.systemPrompt = systemPrompt
        self.tokens_in = 0
        self.tot_tokens_in=0
        self.tokens_out = 0
        self.tot_tokens_out=0


    def get_chatresponse(self, prompt, temperature = .5, max_tokens = 50):
        
        response = self.client.messages.create(
            model = self.model,
            system=self.systemPrompt,
            max_tokens = 1034,
            temperature = 0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        #object accounting
        self.tot_tokens_in += response.usage.input_tokens
        self.tokens_in = response.usage.input_tokens
        self.tot_tokens_out += response.usage.output_tokens
        self.tokens_out = response.usage.output_tokens
        #Return text, token counts
        return response.content[0].text, response.usage.input_tokens, response.usage.output_tokens
    
