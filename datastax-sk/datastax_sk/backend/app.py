from typing import Union, Optional
from fastapi import FastAPI, UploadFile, File
import semantic_kernel as sk
import pandas as pd
import json
import re
from semantic_kernel.connectors.ai.open_ai import (
    OpenAITextEmbedding,
    OpenAIChatCompletion,
)
from semantic_kernel.orchestration.context_variables import ContextVariables





# Initialize Semantic Kernel
kernel = sk.Kernel()
api_key, org_id = sk.openai_settings_from_dot_env()
# Add connectors (AI Services)
kernel.add_chat_service(
        "chat_completion", 
        OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id)
    )
kernel.add_text_embedding_generation_service("ada", OpenAITextEmbedding("text-embedding-ada-002", api_key, org_id))
# Add connectors (Memory Stores) (Temporarily VOLATILE)
kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
kernel.import_skill(sk.core_skills.TextMemorySkill())
# Define plugins
plugins_directory = "plugins"
#Extract Plugins
# Dealing with initial dataframe pre-processing
extract_plugin = kernel.import_semantic_skill_from_directory(plugins_directory, "Extract")
generateQuestions = extract_plugin['generateQuestions']
analyzeDataframe = extract_plugin['analyzeDataframe']
#Transform
# Dealing with task specific dataframe transformations
transform_plugin = kernel.import_semantic_skill_from_directory(plugins_directory, "Transform")
dfReframer = transform_plugin['dfReframer']
simpleCodeGen = transform_plugin['simpleCodeGen']
#Interpret
# Dealing with prompt interpretation
interpret_plugin = kernel.import_semantic_skill_from_directory(plugins_directory, "Interpret")
decipherPrompt = interpret_plugin['decipherPrompt']

app = FastAPI()


@app.get("/")
def read_root():
    return {"Welcome to DataStax API" : "Please use /docs to see the API documentation"}


# FILE UPLOAD
# Definition: API that handles the file upload
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    #Store file in temp folder
    with open(f"temp/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
    #Return success message
    return {"Uploaded": file.filename}



# INTERPRET API
# Definition: API that handles the interpretation of the prompt and the dataframe
@app.get("/interpretPrompt/")
def interpret_prompt(prompt: str, dataframe: str):
    response = decipherPrompt(variables=ContextVariables(content=prompt, variables={'dataframe':dataframe})).result
    response = re.search(r'\[STARTMODPROMPT\]\n\"(.*)\"\n\[ENDMODPROMPT\]', response).group(1)
    print("Response: ", response)
    return response



# EXTRACT API
# Definition: The initial API that takes the dataframe and process it to generate the questions

# Analyzes the dataframe.
@app.get("/analyzeDataframe/")
def analyze_dataframe(dataframe: str):
    print("Prompt: ", dataframe )
    #Call analyze dataframe function with prompt dataframe
    result_str = analyzeDataframe(variables=ContextVariables(content=dataframe)).result
    print("Response: ", result_str)
    #Write result to analysisDF.txt
    with open('temp/analysisDF.txt', 'w') as f:
        f.write(result_str)
    return result_str


# Returns the json object that we get from generateQuestions function. This accepts a string as parameter and returns a json object
@app.get("/generateQuestions/")
def generate_questions(dataframe: str):
    # Convert prompt string to a dataframe
    print("Prompt: ", dataframe)
    # Call generateQuestions function with prompt dataframe
    result_str = generateQuestions(variables=ContextVariables(content=dataframe)).result
    print("Response: ", result_str)
    # Convert result string to a json object
    result_json = json.loads(result_str)
    #Get only the key values from the json object
    questions = list(result_json.keys())
    print(questions)
    #TEMPORARY MEMORY WILL FIX WITH INTEGRATING DATABASES
    #Write the result_json to dfquestions.json
    with open('temp/dfquestions.json', 'w') as f:
        json.dump(result_json, f)

    # Return the json object
    return questions

#Return the Question Query Pair
@app.get("/initQuestionQueryPair/")
def init_question_query_pair():
    #Read the dfquestions.json file
    with open('temp/dfquestions.json') as f:
        data = json.load(f)
    #Return the json object
    return data



# TRANSFORM API
# Definition: API that handles code generation and transforming the dataframes
@app.get("/simpleCodeGeneration/")
def simple_code_generation(dataframe: str, prompt: str, code: str):
    #Check temp folder if analysis df exists
    response = simpleCodeGen(variables=ContextVariables(content=prompt, variables={'dataframe':dataframe, 'code':code})).result
    #Return the json object
    return json.loads(response)


