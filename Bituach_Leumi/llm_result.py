import boto3
import json

def user_prompt(question, txt_body, txt_url):
    user_prompt = f'''
        You are a loyal helper that receives context in Hebrew, a question and answers back based on the context.
        You should read only what is marked under "content" and reply the question given you accordingly.
        If your answer consists of few bulletpoints please have a new line each time
        After giving your answer you should write the following in a new line:
          "  למידע נוסף ניתן לעיין בכתובת:" {txt_url}
          
          
        the context:\n {txt_body}
        
        the question:\n {question}
          
          
    '''
    
    json_data = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 5000,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text",
                             "text": user_prompt
            }
            ],
            }
            ],
            }
    
    return json_data
    
def unhandled_prompt():
    
        response_subjects = [
            'תנאי זכאות'
            ,'לעבוד ולקבל קצבת נכות'
            ,'קביעת אחוז הנכות הרפואית'
            ,'בדיקה מחדש של אחוזי נכות רפואיים או דרגת אי כושר'
            ,'קביעת דרגת אי–הכושר להשתכר או לתפקד במשק בית'
            ,'סכום הקצבה'
            ,'בדיקה על ידי ועדה רפואית'
            ,'מסלול מהיר לבעלי מוגבלויות קשות'
            ,'תהליך הטיפול בתביעה'
            ,'תשלום הקצבה'
        ]
    
        prompt = f'''
            This is where you failed in getting the right subject for the user's question,
            as a loyal helper that you are we need to summarize a failure reply for the user in Hebrew.
            
            This can happen because The question was not understandable.
            
            In this case, please explain that you did not understand the question, 
            explain that you are a Bituach Leumi bot designated helping with questions,
            Do not say that you are explaining in Hebrew.
            regarding General Disability, tell the customer to briefly adjust the question
            to one of the following topics where after each topic you go to a new line with a bulletpoint: 
            {[subject for subject in response_subjects]}
            
            Finally, mention the following line in a new line:
            "ניתן לעיין גם בצורה עצמאית באתר ביטוח לאומי: https://www.btl.gov.il/benefits/Disability/Pages/default.aspx"
            
            It is important to be precise and on point.
        '''
    
    
        json_data = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 5000,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text",
                             "text": prompt
            }
            ],
            }
            ],
            }
    
        return json_data
    



def get_answer(question, page_number, bedrock_client, kwargs):
    
    s3_client = boto3.client('s3')
    
    bucket = 'genaya-backend'
    sub_dir = 'raw_files/'
    try:
        txt_file = s3_client.get_object(Bucket= bucket, Key= f"{sub_dir}{page_number}.txt")
        
    except Exception as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return 'NoSuchKey'
    
    txt_data = txt_file['Body'].read().decode('utf-8')
    
    txt_body = txt_data.split('content:')[1].split('url:')[0]
    
    txt_url = txt_data.split('url:')[1]
    
    body = user_prompt(question, txt_body, txt_url)
    
    kwargs['body'] = json.dumps(body)
    
    response = bedrock_client.invoke_model(**kwargs)
    
    response_json = json.loads(response.get("body").read())
    output = response_json.get("content", [])
    full_response = ""

    for obj in output:
        full_response += obj["text"]
        
    return full_response
    
    
def get_default_answer(bedrock_client, kwargs):
    
    body = unhandled_prompt()
    
    kwargs['body'] = json.dumps(body)
    
    response = bedrock_client.invoke_model(**kwargs)
    
    response_json = json.loads(response.get("body").read())
    output = response_json.get("content", [])
    full_response = ""

    for obj in output:
        full_response += obj["text"]
        
    return full_response