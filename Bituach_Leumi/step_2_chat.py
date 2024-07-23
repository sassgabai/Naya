import json
import boto3
from get_subject import llm_result
from llm_result import get_answer


def lambda_handler(event, context):
    
    question = 'מה מחיר החמוציות בשוק?'
    
    get_subject = llm_result(question)
    
    error_answer = f'''
   לצערי לא הצלחתי להבין את השאלה ולכן לא הצלחתי לקשר לנושא המתאים,
המטרה שלי היא לעזור לכם לקבל תשובות עבור השאלות שלכם בנושא "נכות כללית" 

 מבקש לחדד את השאלה לאחד הנושאים הבאים:
 תנאי זכאות
 לעבוד ולקבל קצבת נכות       
קביעת אחוז הנכות הרפואית       
בדיקה מחדש של אחוזי נכות רפואיים או דרגת אי כושר
קביעת דרגת אי–הכושר להשתכר או לתפקד במשק בית
סכום הקצבה
בדיקה על ידי ועדה רפואית
מסלול מהיר לבעלי מוגבלויות קשות
תהליך הטיפול בתביעה
תשלום הקצבה
    '''
    
    answer = error_answer if get_answer(question, get_subject) == 'NoSuchKey' else get_answer(question, get_subject)
    
    print('response {}'.format(answer))
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(answer)
    }
