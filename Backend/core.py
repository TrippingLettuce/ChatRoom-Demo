# DONT FORGET TO SETUP YOUR API KEY!
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
from langchain.chains.router import MultiPromptChain
import warnings

# To ignore a specific warning type
warnings.filterwarnings("ignore", category=UserWarning)

# Your API key here
openai_api_key = "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"

# General Router Chain Method
# ------------------------------------------------------------------------------------------------------------------------------------------------------------- #
def get_bot_response(user_message):
    # Define a senario
    non_lesson_template = '''You are an university professor who teaches university students. If the question that student asks is not
    relate to the statistics, you should reply with short reply (less than 900 characters long).\n{input}'''

    lesson_template = '''You are a world expert Statistics professor who explains statistic topics
    to university students. You can assume anyone you answer has a beginner level understanding of Statistics  (less than 900 characters long). 
    Here is the question\n{input}'''

    # ADD YOUR OWN TEMPLATES !
    empty_template = '{input}'

    # Router Prompt
    prompt_infos = [
        {'name':'empty',
        'description':'Replies to general questions',
        'prompt_template':empty_template},

        {'name':'General Statistics',
        'description': 'Answer general Statistics questions',
        'prompt_template':lesson_template},

        {'name':'General Chat',
        'description': 'Answers general conversation questions',
        'prompt_template':non_lesson_template},
    ]

    try:
        llm = ChatOpenAI(openai_api_key=openai_api_key)
        destination_chains = {}
        for p_info in prompt_infos:
            name = p_info['name']
            prompt_template = p_info['prompt_template']
            prompt = ChatPromptTemplate.from_template(template=prompt_template)
            chain = LLMChain(llm=llm, prompt=prompt)
            destination_chains[name] = chain

        default_prompt = ChatPromptTemplate.from_template("{input}")
        default_chain = LLMChain(llm=llm,prompt=default_prompt)

        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        destinations_str = "\n".join(destinations)

        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
            destinations=destinations_str
        )
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )        

        router_chain = LLMRouterChain.from_llm(llm, router_prompt)
        chain = MultiPromptChain(router_chain=router_chain, 
                                destination_chains=destination_chains, 
                                default_chain=default_chain, 
                                # verbose=True              # set verbose=True for debugging.
                                )

        response = chain.run(user_message)

        return response
    
    except Exception as e:
        print(f"Error in generating response: {e}")
        return "I'm having trouble understanding that right now."
    

# ------------------------------------------------------------------------------------------------------------------------------------------------------------- #
