from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
import json


# Define state schema
class AnalysisState(TypedDict):
    files: list
    language_info: dict
    issues: list
    rating: str
    fixes: list
    final_response: str


# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


# Node 1: Identify language and frameworks
def identifyLanguage(state: AnalysisState) -> AnalysisState:
    analysis = "\n".join(
        f"{file['filename']}\n{file['Patch File']}"
        for file in state['files']
    )

    prompt = f"""Analyze these code files and identify:
    1. The primary programming language(s)
    2. Any frameworks or libraries being used
    3. The general purpose of the code

    Code to analyze:
    {analysis}

    Return the response as a JSON object with keys: 'languages', 'frameworks', 'purpose'.
    IMPORTANT: Only return valid JSON. Do not include additional text."""
    print("Gathering First Node response.")
    response = llm.invoke(prompt)
    ans = response.content
    ans = ans.replace('```','',2)
    ans = ans.replace('json','')
    
    print(f"First node: {ans}")
    state['language_info'] = json.loads(ans)
    print("Everything fine here.")
    return state

# Node 2: Rating (Added later as a demonstration for agentic-driven input)
def codeRating(state: AnalysisState):
    analysis = "\n".join(
        f"{file["filename"]}\n{file["Patch File"]}"
        for file in state['files']
    )

    prompt = f"""Given this {state['language_info']['languages']} code using {', '.join(state['language_info']['frameworks'])}:

        {analysis}

        Examine the code, probing it for:
        1. Potential bugs or edge cases
        2. Code style and best practices
        3. Performance bottlenecks
        4. Security Vulnerabilities
        
        If potential shortcomings and/or issues were found with the code, reply: Yes.
        However, if the code is properly written and has no discernible shortcomings and/or issues, then reply: No.
        IMPORTANT: Answer must be a single word: Yes or No.
        """

    response = llm.invoke(prompt)
    ans = response.content
    print(f"Rating Response: {ans}")
    state['rating'] = ans
    return ans

#Node 3: Commendation
def commendCoder(state: AnalysisState) -> AnalysisState:
    analysis = "\n".join(
        f"{file['filename']}\n{file['Patch File']}"
        for file in state['files']
    )
    prompt = f"""Given this {state['language_info']['languages']} code using {', '.join(state['language_info']['frameworks'])}:

    {analysis}
    
    Examine the code and formulate a commendation message praising the lack of shortcomings in the code, relaying the best aspects of the code as a list.
    Each point in the list not being more than 25 words.
    """
    response = llm.invoke(prompt)
    ans = response.content
    state['final_response'] = ans
    return state


# Node 3.1: Identify issues
def identifyIssues(state: AnalysisState) -> AnalysisState:
    analysis = "\n".join(
        f"{file['filename']}\n{file['Patch File']}"
        for file in state['files']
    )
    prompt = f"""Given this {state['language_info']['languages']} code using {', '.join(state['language_info']['frameworks'])}:

    {analysis}

    List all potential issues regarding:
    1. Code style and best practices
    2. Potential bugs or edge cases
    3. Performance considerations
    4. Security concerns
    

    Return the response as a JSON array of issues, each with 'category' and 'description' keys.
    IMPORTANT: Only return valid JSON. Do not include additional text."""
    print("Gathering Issues.")
    response = llm.invoke(prompt)
    ans = response.content
    ans = ans.replace('```','',2)
    ans = ans.replace('json','')
    print(f"Issue Response: {ans}")
    state['issues'] = json.loads(ans)
    print("Node 3.1 all okay.")
    return state


# Node 3: Generate fixes
def generateFixesCode(state: AnalysisState) -> AnalysisState:
    analysis = "\n".join(
        f"{file['filename']}\n{file['Patch File']}"
        for file in state['files']
    )

    issues_text = "\n".join(
        f"- {issue['category']}: {issue['description']}"
        for issue in state['issues']
    )

    prompt = f"""Given this code and its identified issues:

    Code:
    {analysis}

    Issues:
    {issues_text}

    Provide the fully fixed code for the mentioned issues, a short paragraph explaining the solution if necessary.
    Avoid fixation on elaborate descriptions of the solution.
    Return as a JSON array with 'issue_index', 'original_code', and 'fixed_code' keys.
    IMPORTANT: Only return valid JSON. Do not include additional text."""

    response = llm.invoke(prompt)
    ans = response.content
    ans = ans.replace("```","",2)
    ans = ans.replace("json","")
    print(ans)
    state['fixes'] = json.loads(ans)
    
    state['final_response'] = (
                "Issues Found:\n" +
                "\n".join(f"- {issue['category']}: {issue['description']}" for issue in state['issues']) +
                "\n\nCode Fixes:\n" +
                "\n".join(f"Fix {fix['issue_index']}:\n{fix['fixed_code']}" for fix in state['fixes'])
    )
    
    return state

def generateFixesBoth(state: AnalysisState) -> AnalysisState:
    analysis = "\n".join(
        f"{file['filename']}\n{file['Patch File']}"
        for file in state['files']
    )

    issues_text = "\n".join(
        f"- {issue['category']}: {issue['description']}"
        for issue in state['issues']
    )

    prompt = f"""Given this code and its identified issues:

    Code:
    {analysis}

    Issues:
    {issues_text}

    Provide implementable code fixes for each issue alongside short descriptions of the approach used to solve said issue.
    Return as a JSON array with 'issue_index', 'approach', and 'fixed_code' keys.
    IMPORTANT: Only return valid JSON. Do not include additional text."""

    response = llm.invoke(prompt)
    ans = response.content
    ans = ans.replace("```","",2)
    ans = ans.replace("json","")
    print(ans)
    state['fixes'] = json.loads(ans)
    
    state['final_response'] = (
                "Issues Found:\n" +
                "\n".join(f"- {issue['category']}: {issue['description']}" for issue in state['issues']) +
                "\n\nCode Fixes:\n" +
                "\n".join(f"Fix {fix['issue_index']}:\n{fix['approach']}:\n{fix['fixed_code']}" for fix in state['fixes'])
    )
    
    return state


def generateFixesDesc(state: AnalysisState) -> AnalysisState:
    analysis = "\n".join(
        f"{file['filename']}\n{file['Patch File']}"
        for file in state['files']
    )

    issues_text = "\n".join(
        f"- {issue['category']}: {issue['description']}"
        for issue in state['issues']
    )

    prompt = f"""Given this code and its identified issues:

    Code:
    {analysis}

    Issues:
    {issues_text}

    Provide detailed descriptions of the solution used to solve each issue as a series of structured steps, integrating inline code if necessary.
    Providing the fully fixed code at the end is unnecessary.
    Return as a JSON array with 'issue_index', 'solution' keys.
    IMPORTANT: Only return valid JSON. Do not include additional text."""

    response = llm.invoke(prompt)
    ans = response.content
    ans = ans.replace("```","",2)
    ans = ans.replace("json","")
    print(ans)
    state['fixes'] = json.loads(ans)
    
    state['final_response'] = (
                "Issues Found:\n" +
                "\n".join(f"- {issue['category']}: {issue['description']}" for issue in state['issues']) +
                "\n\nPotential Fixes:\n" +
                "\n".join(f"Fix {fix['issue_index']}:\n{fix['solution']}" for fix in state['fixes'])
    )
    
    return state


def analyze_code(files: list, op_mode: int) -> str:
    if op_mode != 1 or op_mode != 2:
        op_mode = 0

    # Create workflow
    workflow = StateGraph(AnalysisState)

    # Add nodes
    workflow.add_node("identifyLanguage", identifyLanguage)
    workflow.add_node("identifyIssues", identifyIssues)

    # Set entry point
    workflow.set_entry_point("identifyLanguage")
    workflow.add_node("commendCoder", commendCoder)
    workflow.set_finish_point("commendCoder")


    workflow.add_conditional_edges(
        "identifyLanguage",
        codeRating,
        {
            "Yes":"identifyIssues",
            "No":"commendCoder"
        }
    )


    workflow.add_node("generateFixesDesc", generateFixesDesc)
    workflow.set_finish_point("generateFixesDesc")
    workflow.add_node("generateFixesCode", generateFixesCode)
    workflow.set_finish_point("generateFixesCode")
    workflow.add_node("generateFixesBoth", generateFixesBoth)
    workflow.set_finish_point("generateFixesBoth")

    workflow.add_conditional_edges(
         "identifyIssues",
         lambda x: op_mode,
         {
             0: "generateFixesBoth",
             1: "generateFixesCode",
             2: "generateFixesDesc"
         })

    # Compile workflow
    app = workflow.compile()

    # Run analysis
    result = app.invoke({
        "files": files,
        "language_info": {},
        "issues": [],
        "fixes": [],
        "final_response": ""
    })
    print("Finale Done. Response sent.")
    return result['final_response']