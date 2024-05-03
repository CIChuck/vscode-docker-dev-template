
import openai
import anthropic
import numpy as np
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import AzureOpenAI
import google.generativeai as genai



from abc import ABC, abstractmethod

class LLM(ABC):

    def __init__(self, model, client, systemPrompt) -> None:
        self.model = model
        self.client = client
        self.systemPrompt = systemPrompt

        self.tot_tokens_in = 0
        self.tokens_in = 0

        self.tot_tokens_out =0
        self.tokens_out = 0

        self.response = ""

        self.formattedSystemPrompt = {"role": "system", "content": systemPrompt}

        # clss requires key/endpoints etc
        load_dotenv()
    
    def get_client(self):
        return self.client

    def get_model(self):
        return self.model
    
    def get_full_response(self):
        return self.response

    def change_model(self, mod_name):
        self.model = mod_name

    @abstractmethod
    def __accounting__(self, response):
        pass

    @abstractmethod
    def get_chatresponse(self, prompt, temperature = .5, max_tokens = 50):
        pass

    @abstractmethod
    def get_JSON_response(self, prompt, temperature = .5, max_tokens = 50):
        pass

class OAI(LLM): 
    @classmethod
    def list_models(self): 
        a = openai 
        oai_models = []
        for model in a.models.list():
            oai_models.append(model.id)

        return oai_models


    def __init__(self, model = "gpt-4-0125-preview", systemPrompt="You are a helpful assistant."):
        
        super().__init__(model=model, client=OpenAI(), systemPrompt=systemPrompt)
       
    def __accounting__(self, response):
        self.tot_tokens_in += response.usage.prompt_tokens
        self.tokens_in = response.usage.prompt_tokens
        self.tot_tokens_out += response.usage.completion_tokens
        self.tokens_out = response.usage.completion_tokens

    def get_client(self):
        return self.client
    
    def get_model(self):
        return self.model
    
    def get_full_response(self):
        return self.response

    def change_model(self, mod_name):
        self.model = mod_name

    # should be genericized for supporting kwargs
    def get_chatresponse(self, prompt, temperature = .5, max_tokens = 50):

        #print(self.systemPrompt, self.model)
        
        try:
            self.response = self.client.chat.completions.create(
                model = self.model,
                max_tokens = max_tokens,
                temperature = temperature,
                messages=[
                    self.formattedSystemPrompt,
                    {"role": "user", "content": prompt}
                    ],
                stream=False
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
    
    #likely valid only for OpenAI advanced models
    def get_JSON_response(self, prompt, temperature = .5, max_tokens = 50):
        
        #adjust prompt to insure JSON output - required by the API
        suffix = " You output all responses in JSON format and nothing else."
        msg = prompt + suffix

        #adjust system prompt
        content = self.formattedSystemPrompt["content"] + suffix
        newsysprompt = {"role": "system", "content": content}

        print(newsysprompt)

        try:
            self.response = self.client.chat.completions.create(
                model = self.model,
                response_format={"type": "json_object"},
                max_tokens = max_tokens,
                temperature = temperature,
                stream=False,
                messages=[
                    newsysprompt,
                    {"role": "user", "content": msg}
                    ],
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

class AzureOAI(OAI):

    def __init__(self, model = "cigpt4", systemPrompt="You are a helpful assistant."):

        load_dotenv()
        client = AzureOpenAI(
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
                api_key=os.getenv("AZURE_OPENAI_KEY"),  
                api_version=os.getenv("AZURE_API_VERSION")
            )
        super().__init__(model=model, systemPrompt=systemPrompt)
        self.client = client

class Databricks(OAI):

    def __init__(self, model = "databricks-dbrx-instruct", 
                        systemPrompt="You are a helpful assistant."):

        load_dotenv()
    
        #DATABRICKS_TOKEN = os.environ.get('DATABRICKS_TOKEN')
        client = OpenAI(
            api_key=os.environ.get('DATABRICKS_TOKEN'),
            base_url=os.environ.get('DATABRICKS_ENDPOINT')
        )
        super().__init__(model=model, systemPrompt=systemPrompt)
        self.client = client
        
class LLmStudio(OAI):

    def __init__(self, model=None, systemPrompt="You are a helpful assistant."):

        load_dotenv()
        #print(os.environ.get('LLMSTUDIO_ENDPOINT'),os.environ.get('LLMSTUDIO_API_KEY'))
        
        client = OpenAI(
                    base_url=os.environ.get('LLMSTUDIO_ENDPOINT'),
                    api_key=os.environ.get('LLMSTUDIO_API_KEY')
                )

        super().__init__(model=model, systemPrompt=systemPrompt)

        self.client = client
                     
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
    
class Google(LLM):

    def __init__(self, model = "gemini-pro", systemPrompt="You are a helpful assistant."):
        
        load_dotenv()
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)

        super().__init__(model=model, client=genai.GenerativeModel(model), systemPrompt=systemPrompt)
        self.client = genai.GenerativeModel(model)

    def __accounting__(self, response):
        pass
        """
        self.tot_tokens_in += response.usage.prompt_tokens
        self.tokens_in = response.usage.prompt_tokens
        self.tot_tokens_out += response.usage.completion_tokens
        self.tokens_out = response.usage.completion_tokens
        """

    def get_chatresponse(self, prompt, temperature = .5, max_tokens = 50):
        
        generation_config = {
            "temperature": temperature,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": max_tokens
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_HIGH_AND_ABOVE"
            }
        ]
        
        """self.client = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
        """

        prompt_parts = [
        prompt,
        ]

        self.response = self.client.generate_content(prompt_parts)
        return self.response.text
    
    def get_JSON_response(self, prompt, temperature=0.5, max_tokens=50):
        pass