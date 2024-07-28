import json
import boto3

def generate_bedrock_client():
    
    bedrock_client = boto3.client('bedrock-runtime')
    
    kwargs = {
        'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
        'accept': 'application/json',
        'contentType': 'application/json',
    }
    
    return bedrock_client, kwargs
    
def activate_prompt(body):
    system_prompt = f'''
You are You are a helpful worker that helps with reading text files, extracting relevant imformation and arranging it in a given order as JSON format.
The file you receive is a CV of a potential worker in our company and it can be English and/or Hebrew,
Your job is to read the entire file and arrange the data in the following order:

1/ candidate name
2/ job title and total years: usually under "Work Experience", "Work","Experience" and alike, it is important to sum the number of years - 
   for example if it has the following information
   "2004-2007 full stack developer
   # skill information
   2019-2020 senior full stack developer" then your understanding should be "full stack developer, 4 (because she worked 4 years in total as fullstack developer)"
   it is important not to confuse with leading titles, for example "fullstack developer" and "fullstack team leader" is not the same title and it is important not to get confused with 
   titles like "professional experience from courses" because this is NOT professional experience and should not be considered
   
3/ technologies experience the candidate WORKED with only and number of years: usually under same headlines like section 2, but this time you search for relevant technologies used and skills, and number of years.
   for example for the following information
   "2004 -2007 full stack dveloper
   - MySQL, JSON, Angular
   
   "2009-2012 senior full stack developer
   - Github, Jenkins, Angular, Teamwork" then your understanding should be "MySQL,3 JSON,3 Angular,6 (because it showed up in different places) Github,3 Jenkins,3 Teamwork, 3"
   
4/ educational experience and years: usually under titles like "Education", "Studying", "Courses" and alike. here what we care about is what the candidate learned (title) and years
   for example for the following information 
   "2010-2012 (Naya Technologies) Cloud Data Engineer" your understanding should be "Data Engineer Certificate,Naya Technologies, 2",
   
5/ educational technologies experience and years: just like section 3 but for technologies mentioned under section 4 only.

6/ languages the candidate speaks, the level is irrelevant for us
      
It is important to reply in JSON format, in English and the answer only, if the information is in hebrew than translate it to english and then reply

The JSON format should be with the following keys:
"candidateName"
"jobTitleAndTotalYears:[]"
"technologiesWorkedWithAndYears:[]"
"educationalExperienceAndYears:[]"
"educationalTechnologiesAndYears"[]
"languages:[]"

the content you should read\n: {body}

    '''
    
    json_data = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text",
                             "text": system_prompt
            }
            ],
            }
            ],
            }
    

    return json_data  
    
    
def send_to_llm(body, bedrock_client, kwargs) ->str:

    '''
    received the body and send it to the prompt to get the answer, returns the answer as s
    '''

    answer = activate_prompt(body)
    
    kwargs['body'] = json.dumps(answer)
    
    response = bedrock_client.invoke_model(**kwargs)
    
    response_json = json.loads(response.get("body").read())
    output = response_json.get("content", [])
    full_response = ""

    for obj in output:
        full_response += obj["text"]
    
    return full_response