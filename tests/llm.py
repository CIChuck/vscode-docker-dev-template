import openai
import anthropic
import numpy as np
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

        self.response = ""

        load_dotenv()

    def __accounting__(self, response):
        self.tot_tokens_in += response.usage.prompt_tokens
        self.tokens_in = response.usage.prompt_tokens
        self.tot_tokens_out += response.usage.completion_tokens
        self.tokens_out = response.usage.completion_tokens

    def get_client(self):
        return self.client
    
    def list_models(self): 
        a = openai 
        oai_models = []
        for model in a.models.list():
            oai_models.append(model.id)

        return oai_models
    
    def get_model(self):
        return self.model
    
    def get_full_response(self):
        return self.response

    def change_model(self, mod_name):
        self.model = mod_name

    def get_chatresponse(self, prompt, temperature = .5, max_tokens = 50):

        try:
            self.response = self.client.chat.completions.create(
                model = self.model,
                max_tokens = max_tokens,
                temperature = temperature,
                messages=[
                    self.systemPrompt,
                    {"role": "user", "content": prompt}
                    ]
            )
        except openai.error.Timeout as e:
            #Handle timeout error, e.g. retry or log
            print(f"OpenAI API request timed out: {e}")
            pass
        except openai.error.APIError as e:
            #Handle API error, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            pass
        except openai.error.APIConnectionError as e:
            #Handle connection error, e.g. check network or log
            print(f"OpenAI API request failed to connect: {e}")
            pass
        except openai.error.InvalidRequestError as e:
            #Handle invalid request error, e.g. validate parameters or log
            print(f"OpenAI API request was invalid: {e}")
            pass
        except openai.error.AuthenticationError as e:
            #Handle authentication error, e.g. check credentials or log
            print(f"OpenAI API request was not authorized: {e}")
            pass
        except openai.error.PermissionError as e:
            #Handle permission error, e.g. check scope or log
            print(f"OpenAI API request was not permitted: {e}")
            pass
        except openai.error.RateLimitError as e:
            #Handle rate limit error, e.g. wait or log
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass


        #object accounting
        self.__accounting__(self.response)
    
        #Return text, token counts
        return self.response.choices[0].message.content
    
    
    def get_JSON_response(self, prompt, temperature = .5, max_tokens = 50):
        
        suffix = " Return content in json format. "

        try:
            self.response = self.client.chat.completions.create(
                model = self.model,
                response_format={ "type": "json_object" },
                max_tokens = max_tokens,
                temperature = temperature,
                messages=[
                    self.systemPrompt,
                    {"role": "user", "content": prompt + suffix}
                    ]
            )
            
        except openai.error.Timeout as e:
            #Handle timeout error, e.g. retry or log
            print(f"OpenAI API request timed out: {e}")
            pass
        except openai.error.APIError as e:
            #Handle API error, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            pass
        except openai.error.APIConnectionError as e:
            #Handle connection error, e.g. check network or log
            print(f"OpenAI API request failed to connect: {e}")
            pass
        except openai.error.InvalidRequestError as e:
            #Handle invalid request error, e.g. validate parameters or log
            print(f"OpenAI API request was invalid: {e}")
            pass
        except openai.error.AuthenticationError as e:
            #Handle authentication error, e.g. check credentials or log
            print(f"OpenAI API request was not authorized: {e}")
            pass
        except openai.error.PermissionError as e:
            #Handle permission error, e.g. check scope or log
            print(f"OpenAI API request was not permitted: {e}")
            pass
        except openai.error.RateLimitError as e:
            #Handle rate limit error, e.g. wait or log
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass

        
        #object accounting
        self.__accounting__(self.response)
        
        #Return text, full response
        return self.response.choices[0].message.content




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

    def __accounting__(self, response):
    #object accounting
        self.tot_tokens_in += response.usage.input_tokens
        self.tokens_in = response.usage.input_tokens
        self.tot_tokens_out += response.usage.output_tokens
        self.tokens_out = response.usage.output_tokens

    def get_client(self):
        return self.client
    
    def get_model(self):
        return self.model

    def change_model(self, mod_name):
        self.model = mod_name

    def get_chatresponse(self, prompt, temperature = .5, max_tokens = 50):
        
        try:

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

        except anthropic.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except anthropic.RateLimitError as e:
            print("Rate Limited. A 429 status code was received; we should back off a bit.")
        except anthropic.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
        
        self.__accounting__(response)
        #Return text, token counts
        return response.content[0].text, response.usage.input_tokens, response.usage.output_tokens
    
