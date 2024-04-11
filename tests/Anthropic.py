import anthropic
from dotenv import load_dotenv

# defaults to os.environ.get("ANTHROPIC_API_KEY")
load_dotenv()

client = anthropic.Anthropic(

)

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1034,
    temperature=0,
    system="I would like you to write 2 jokes in the style of Steven Wright. Only return the output in the form of a JSON data structure, and nothing more",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Make the jokes incredibly funny, make them very sarcastic like Stephen Wright would be, and make them very sardonic."
                }
            ]
        }
    ]
)
print(message.content)