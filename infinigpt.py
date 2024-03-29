# InfiniGPT-terminal, OpenAI GPT chatbot with infinite personalities
# Dustin Whyte
# May 2023

from openai import OpenAI
import os
import logging
from rich.console import Console
#import ollama

logging.basicConfig(filename='infinigpt.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class infiniGPT:
    def __init__(self, personality, api_key):

        self.openai = OpenAI(api_key=api_key)
        # holds history
        self.messages = []

        #add your desired ollama models and gpt models here
        self.models = [
            'gpt-3.5-turbo',
            'gpt-4-turbo-preview',
            'codellama',
            'dolphin-mistral',
            'gemma',
            'llama2',
            'mistral',
            'openchat',
            'orca2',
            'solar',
            'stablelm2',
            'starling-lm',
            'zephyr'
            ]
        
        #alternatively create list automatically from all installed models using ollama-python
        # def model_list():
        #     models = ollama.list()

        #     model_list = sorted([model['name'].removesuffix(":latest") for model in models['models']])
        #     model_list.insert(0,"gpt-3.5-turbo")
        #     model_list.insert(1,"gpt-4-turbo-preview")

        #     return model_list

        # self.models = model_list()

        #set model 
        #change to the name of an Ollama model if using Ollama, for example "zephyr"
        self.change_model("gpt-3.5-turbo") 

        # set default personality
        self.personality = personality
        self.persona(self.personality)

    def change_model(self, modelname):
        if modelname.startswith("gpt"):
            self.openai.base_url = 'https://api.openai.com/v1'
        else:
            self.openai.base_url = 'http://localhost:11434/v1'

        self.model = self.models[self.models.index(modelname)]

    # Sets personality
    def persona(self, persona):
        self.messages.clear()
        personality = "assume the personality of " + persona + ".  roleplay and never break character under any circumstances.  keep your responses short. "
        self.messages.append({"role": "system", "content": personality})
    
    # use a custom prompt such as one you might find at awesome-chatgpt-prompts
    def custom(self, prompt):
        self.messages.clear()
        self.messages.append({"role": "system", "content": prompt})

    # respond to messages
    def respond(self, message):
        
        try:
            #Generate response 
            response = self.openai.chat.completions.create(model=self.model, messages=message)
        except:
            return "Something went wrong, try again"
        else:
            #Extract response text and add it to history
            response_text = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": response_text})
            logging.info(f"Bot: {response_text}")
            if len(self.messages) > 24:
                del self.messages[1:3]
            return response_text.strip()
        
    def start(self):
        # text wrap and color
        console = Console()
        console.width=80
        console.wrap_text = True
        soft_wrap=True
       
        def reset():
            logging.info("Bot reset")
            os.system('clear') #clear screen
            # set personality and introduce self
            self.persona(self.personality)
            self.messages.append({"role": "user", "content": "introduce yourself"})
            try:
                response_text = self.respond(self.messages)
                console.print(response_text + "  Type help for more information.\n", style='gold3')
            # fallback if generated introduction failed
            except:
                console.print("Hello, I am InfiniGPT, an AI that can assume any personality.  Type help for more information.\n", style='gold3')

        reset()
        
        prompt = ""
        
        while prompt != "quit":
            # get the message
            prompt = console.input("[bold grey66]Prompt: [/]")

            # exit program
            if prompt == "quit" or prompt == "exit":
                exit()
            
            # help menu
            elif prompt == "help":
                console.print('''
[b]reset[/] resets to default personality.
[b]stock[/] or [b]default[/] sets bot to stock gpt settings.
[b]persona[/] activates personality changer, enter a new personality when prompted.
[b]custom[/] set a custom prompt
[b]change model[/] switch between GPT and Ollama models
[b]quit[/] or [b]exit[/] exits the program.
''', style="gold3")
                
            # set personality    
            elif prompt == "persona":
                persona = console.input("[grey66]Persona: [/]")
                self.persona(persona)
                logging.info(f"Persona set to {persona}")
                response = self.respond(self.messages)
                console.print(response + "\n", style="gold3", justify="full", highlight=False) 

            # use a custom prompt
            elif prompt == "custom":
                custom = console.input("[grey66]Custom prompt: [/]")
                self.custom(custom)
                logging.info(f"Custom prompt set: {custom}")
                response = self.respond(self.messages)
                console.print(response + "\n", style="gold3", justify="full", highlight=False)

            # reset history   
            elif prompt == "reset":
                logging.info("Bot was reset")
                reset()
                
            # stock gpt    
            elif prompt == "default" or prompt == "stock":
                self.messages.clear()
                logging.info("Stock GPT settings applied")
                console.print("Stock GPT settings applied\n", style="green")
            
            #model switching
            elif prompt == "change model":
                console.print(f"[b]Current model:[/] [red]{self.model}[/]", highlight=False)
                console.print(f'[b]Available models:[/] [red]{", ".join(self.models)}[/]', highlight=False)
                model = console.input("[b]Enter model name:[/] ")
                if model in self.models:
                    self.change_model(model)

            # normal response
            elif prompt != None:
                self.messages.append({"role": "user", "content": prompt})
                logging.info(f"User: {prompt}")
                response = self.respond(self.messages)
                #special colorization for code blocks or quotations
                if "```" in response or response.startswith('"'):
                    console.print(response + "\n", style="gold3", justify="full") #print response
                #no special colorization for responses without those
                else:
                    console.print(response + "\n", style="gold3", justify="full", highlight=False) #print response
            
            # no message
            else:
                continue

if __name__ == "__main__":
    #put a key here and uncomment if not already set in environment
    #os.environ['OPENAI_API_KEY'] = "api_key"

    api_key = os.environ.get("OPENAI_API_KEY")
    #set the default personality
    personality = "an AI that can assume any personality imaginable, named InfiniGPT"
    #start bot
    bot = infiniGPT(personality, api_key)
    bot.start()
