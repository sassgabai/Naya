import boto3
import json

def system_prompt(question):
    
    prompt_english= f'''
            You are a loyal helper who gets a question in Hebrew, and answers in English
            The questions that you are going to be asked are about "General Disability" (In hebrew: נכות כללית), and there are 10 subjects where each has a page:
            1.page1: Ineligibility
            2.page2: Work and receive a disability pension
            3.page3: Determining the percentage of medical disability
            4.page4: Re-examination of medical disability percentages or degree of incapacity
            5.page5: Determining the degree of incapacity to get paid or function in a household
            6.page6: Allowance amount
            7.page7: Examination by a Medical Committee
            8.page8: A fast track for those with severe disabilities
            9.page9: The claim handling process
            10.page10: Payment of allowance
            
            Everytime a question is asked, you need to figure out which subject it's related to and your answer should only be that page,
            for example : user question - "What are the ineligibilities?"
                          your answer - "page1"
            
            another example: user question - "What is the fast track for severe disabilities?"
                             your answer - "page8"
            
            in case you don't know which subject is it related to, please reply "NoSuchKey"
                             
            question: {question}
            
            '''
            
    json_data = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text",
                             "text": prompt_english
            }
            ],
            }
            ],
            }
    

    return json_data


def llm_result(question, bedrock_client, kwargs):

    prompt_body = system_prompt(question)
    
    kwargs['body'] = json.dumps(prompt_body)
    
    response = bedrock_client.invoke_model(**kwargs)
    
    response_json = json.loads(response.get("body").read())
    output = response_json.get("content", [])
    full_response = ""

    for obj in output:
        full_response += obj["text"]
    
    print(f" ***** {full_response}")
    
        
    return full_response