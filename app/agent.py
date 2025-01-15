from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import time
import os

def analyze_code(files, opMode):
    # Initialize with kwargs instead of positional argument
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    analysis = "\n"

    for file in files:
        analysis += str(file['filename']) + "\n"
        analysis += str(file['Patch File']) + "\n"

    if opMode == 1:
        promptText = f"Here are Github Pull-Request files. Analyze the following code for style, bugs, and best practices: {analysis} List out potential issues with the code, each point no longer than 50 words. Provide a technical analysis of the code as a whole; Providing the fully fixed code is unnecessary."
    elif opMode == 2:
        promptText = f"Here are Github Pull-Request files. Analyze the following code for style, bugs, and best practices: {analysis} Identify any potential issues with the code and create a fully functional  and implementable plan to address them, providing the fixed code at the end; A technical analysis of the code is unnecessary."
    else:
        promptText = f"Here are Github Pull-Request files. Analyze the following code for style, bugs, and best practices: {analysis} List out potential issues with the code, each point no longer than 50 words. Also provide the code to fix the issues if applicable."

    promptResponse = llm.invoke(promptText)
    print(promptResponse.content)
    results = str(promptResponse.content)
    return results