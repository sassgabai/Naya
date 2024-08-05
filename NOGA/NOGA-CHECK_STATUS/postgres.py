import json
import psycopg2

def get_status(secret, body):
    try:
        connection = psycopg2.connect(
            dbname= 'testpoc',
            user= secret['username'],
            password= secret['password'],
            host= 'noga-poc-1-instance-1.cocluqwjpuyf.us-east-1.rds.amazonaws.com',
            port= 5432
        )
        
        cursor = connection.cursor()
        
        
        #select
        cursor.execute(
            f'''
                select request_id, user_id, timestamp, status
                from requests_table
                where request_id = {body['request_id']}
            '''
            )
        
        connection.commit()
        
        answer = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if isinstance(answer,tuple):
            answer_dict = {
                'request_id': answer[0],
                'user_id': answer[1],
                'timestamp': answer[2].isoformat().split('.')[0].replace('T',' ') if answer[2] else None,
                'status': answer[3]
            }
            
            return json.dumps(answer_dict)
            
        else:
            return {}
        
    except Exception as e:
        raise e
        return '', ''
    
    
