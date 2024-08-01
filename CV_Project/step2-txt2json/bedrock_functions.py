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
You are a helpful worker who's job is to read text files in different languages [mostly English and Hebrew], extract relevant
information from it and arrange it in the following JSON format in English:

1."candidateName"
2."phoneNumber"
3."email"
4."jobTitleAndTotalYears:[]"
5."technologiesWorkedWithAndYears:[]"
6."educationalTechnologies"[]
7."languages:[]"

the file you are going to read is a CV of a potential candidate to work in our company, here are the instructions of each point:

1."candidateName": the name of the candidate.
2."phoneNumber": the mobile phone number of the candidate, remove non-numeric characters and replace the prefix "972" with "0" 
   	examples:
	a. for the content "052-889-1234" the output is "0528891234"
	b. for the content "092528891234" the output is "0528891234"
3."email": the email of the candidate, should contain "@".
4."jobTitleAndTotalYears: the job title and number of years, make sure not to get confused between "developer", "engineer" titles with leading titles like "team lead", "vp", "leader" and such.
expected titles are "work", "occupation", "working history", "experience", "working experience"
for example  you should consider the following titles as different jobs and should not be counted together : "data engineer", "data engineer team lead"
expected output for the content "2014-2017 data engineer at someplace" should be "data engineer, 3"

5."technologiesWorkedWithAndYears: technologies the candide worked with and number of years for each technology,
technologies mentioned under the following titles only:"work", "occupation", "working history", "experience", "working experience". 
you only input technologies that were mentioned in such titles,
technologies you presented here canno't be presented in another section.

6."educationalTechnologies": the technologies the candidate learned. technologies mentioned in section 5 canno't be presented here because this is only the technologies the user learned and not worked with.
expected titles are "skills", "education", "learning", "diplomas", "certificates", "military service", "IDF".
for example for the content : "2017-2020 BSc computer science, open university, sql, mssql, python, ssis"
the output should be : ["sql", "mssql", "python", "ssis"] - make sure to mention only skills that were not presented in section 5.

7."languages: the languages the candidate speaks [programming languages are irrelevant and should not be mentioned], the level or number of years are irrelevant and you should only present the language itself.

important note for sections 5 and 7: you will sum the number of years of each technology presented.
important general note: repalce escape characters with commas, replace nulls with 0,
the output should be the solution only in JSON format.
the data should be devided with commas. for example instead of 
"educationalExperienceAndYears": [
    /(
      "education": "MBA",
      "years": 2
    /),
    /(
      "education": "BSc, Computer Sciences",
      "years": 3
    )
  ],
the expected output is 
["MBA, 2","BSc computer sciences, 3"]

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


def send_to_llm(body, bedrock_client, kwargs) -> str:
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