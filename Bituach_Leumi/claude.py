import boto3
import json


def claude_system_prompt(question):
    '''
    The general prompt explaining the llm where to look for the answer and how to answer it
    '''

    prompt_english = f'''
            You are a loyal helper who gets a question in Hebrew, and answers in English
            The questions that you are going to be asked are about "General Disability" (In hebrew: נכות כללית), and there are 10 subjects where each has a page
            where after each one I am giving a little brief to help you understand the topis:
            1.page1: Ineligibility - Age and Residency, Low Income from Employment, Medical Disability, Degree of Incapacity, Special Track for Housewives

            2.page2: Work and receive a disability pension - Working and Receiving a Disability Allowance, An Employee Wanting to Start Receiving an Allowance, 
            Receiving an Allowance and Wanting to Start Working, How Much Can You Earn While Still Receiving an Allowance, 
            Additions to the Allowance and Accompanying Benefits, Assistance in Job Search and Vocational Rehabilitation, Cessation of Work

            3.page3: Determining the percentage of medical disability - 
            Determining the Degree of Incapacity to Earn or Function in a Household, Determining the Degree of Incapacity to Earn, 
            Determining the Degree of Incapacity to Function in a Household, Determining a Temporary Degree of Incapacity, Less Than 50% Incapacity Does Not Qualify for an Allowance

            4.page4: Re-examination of medical disability percentages or degree of incapacity - 
            What is a Re-Examination?, When Can You Request a Re-Examination?, Re-Examination of Medical Disability Percentage Only, Submitting a Request for Re-Examination,
            When Will the National Insurance Institute Request a Re-Examination?

            5.page5: Determining the degree of incapacity to get paid or function in a household - 
            Determining the Degree of Incapacity to Earn or Function in a Household for the Hearing Impaired,
            Determining the Degree of Incapacity to Earn, Determining the Degree of Incapacity to Function in a Household, Determining a Temporary Degree of Incapacity,
            Less Than 50% Incapacity Does Not Qualify for an Allowance

            6.page6: Allowance amount - 
            Disability Allowance Amounts (Effective 01.01.2024), Full Disability Allowance Amount,
            Partial Disability Allowance Amounts by Degree, Addition for Children, Addition for Spouse, Earning Income is Beneficial,
            Impact of Non-Employment Income on Allowance Amount, Important Note About Child Support Payments

            7.page7: Examination by a Medical Committee - 
            Importance of Seeking Advice Before Medical Committees, What is a Medical Committee?, How Does a Medical Committee Proceed?,
            Defining Medical Issues, Consent to Be Examined by the Committee, Physical Examination, Summarizing the Discussion and Determining the Medical Disability Percentage,
            Referral for Additional Tests, Important Things to Know, Arriving on Time with Proper Identification, Understanding Wait Times,
            Bringing Relevant Medical Documentation, Arranging for a Translator or Companion if Needed, Apology for Potential Delays

            8.page8: A fast track for those with severe disabilities

            9.page9: The claim handling process - 
            Stage 1 - Claims Officer at Branch Examines the Claim, Stage 2 - National Insurance Institute Physician Examines the Claim,
            Stage 3 - Examination by the Medical Committee, The Medical Committee Physician's Role,
            Stage 4 - Decision on the Claim, Actions Taken by Claims Officer After Medical Committee, Notification of Decision and Right to Appeal

            10.page10: Payment of allowance - 
            To Whom is the Allowance Paid?, Start Date of Eligibility for Allowance, Payment of Allowance from the 31st Day of Disability Determination,
            Double Allowance Payment from the 31st Day, Date of Allowance Payment, Potential Changes to Payment Dates Due to Holidays

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


def claude_answer(question, txt_body, txt_url):
    '''
    Gets the relevant page and respond to the user question according to the body given
    '''

    prompt = f'''
        You are a loyal helper that receives context in Hebrew, a question and answers back based on the context and history conversation.

        You should read only what is marked under "context" and reply the question given you accordingly,
        In case you are not sure the answer is correct (maybe because the subject is not accurate) then mentioned in your answer that you are not entirely sure about the answer
        I want your answer to be user friendly - use relevant emojis like smiley faces, hearts and others you see fit.
        If the client says that he got hurt / is ill/ can't work or move alot start with feeling sorry for them and wishing well, but use lowest amout of characters possible.
        After giving your answer you should write the following in a new line:
          "  למידע נוסף ניתן לעיין בכתובת:" {txt_url}
          and a heart at the end

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
                             "text": prompt
                             }
                            ],
            }
        ],
    }

    return json_data


def claude_unhandled_prompt(question):
    '''
    The answer incase the llm did not understand which page is the answer
    '''

    response_subjects = [
        'תנאי זכאות'
        , 'לעבוד ולקבל קצבת נכות'
        , 'קביעת אחוז הנכות הרפואית'
        , 'בדיקה מחדש של אחוזי נכות רפואיים או דרגת אי כושר'
        , 'קביעת דרגת אי–הכושר להשתכר או לתפקד במשק בית'
        , 'סכום הקצבה'
        , 'בדיקה על ידי ועדה רפואית'
        , 'מסלול מהיר לבעלי מוגבלויות קשות'
        , 'תהליך הטיפול בתביעה'
        , 'תשלום הקצבה'
    ]

    prompt = f'''
        You are a 25 year old girl with years of experience in Customer Support, you are very pleasant, friendly and have much desire to help, who uses alot of emojis in her answers.
        You are going to receive a question and you need to decide if it is a greeting or more than that, possible question types:
        1/greeting questions: "Hello", "How you doing?", "Hello how are you?"
        In such cases you reply back answers like "I'm fine thank you?", "How can I help?"

        2/questions like "What is your job?", "How does it work" and alike,
        in such cases you can explain who you are and what is your job.

        3/The user can ask questions like "What subjects are you helping with", "Subjects?" and alike,
        you can explain the following subjects: {[subject for subject in response_subjects]},

        4/If the question given is more than that and you don't know what to answer - then you need 
        to ONLY explain that you are a Bituach Leumi bot designated helping with questions, and that you did not understand the question given
        regarding General Disability (in hebrew: נכות כללית), that you would really like to help but you need the client to adjust the question

        in case you decided the scenario is option 4 - also mention the following line in a new line with a heart at the end:
        "ניתן לעיין גם בצורה עצמאית באתר ביטוח לאומי: https://www.btl.gov.il/benefits/Disability/Pages/default.aspx

        You reply according to the language the question is - and do not mention that you are explaining in a different language,
        your name and that you are a customer support.

        In case question doesn't have a question mark at the end, respond as if there was

        QUESTION : {question}

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


def claude_summarize(question, history_list, get_system_prompt):
    '''
    summarize the latest conversation + the present question for the llm to decide on the relevant page
    '''

    prompt = f'''
        1/ this is the general explanation on where you get your answer and how you respond to the user : {get_system_prompt}
        2/ Please summarize the following Q&A text which represents your previous conversation with this user: {history_list}
        3/ This is the current user question : {question}
        4/ Based on steps 1,2 and 3 - give me an answer to the question you've given in step 3 in a format presented in step 1 which is ONLY the page -


        Examples with good answers:
        a. previous conversation you decided the answer is "page6"
           the current user question is "Can you elaborate", "I did not understand", "Summarize even more", "Elaborate on step 1" , "Please explain 1"
           or even something specific the requires page6
           then your answer is "page6"


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