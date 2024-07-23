
import requests
from bs4 import BeautifulSoup
import boto3

s3_client = boto3.client('s3')
bucket_name = 'genaya-backend'
sub_dir = 'raw_files/'

urls = {
# תנאי זכאות
'page1':'https://www.btl.gov.il/benefits/Disability/Pages/%d7%94%d7%96%d7%9b%d7%90%d7%99%d7%9d%20%d7%9c%d7%a7%d7%a6%d7%91%d7%aa%20%d7%a0%d7%9b%d7%95%d7%aa%20%d7%97%d7%95%d7%93%d7%a9%d7%99%d7%aa.aspx',
# לעבוד ולקבל קצבת נכות
'page2':'https://www.btl.gov.il/benefits/Disability/Pages/laavod.aspx',
# קביעת אחוז הנכות הרפואית
'page3':'https://www.btl.gov.il/benefits/Disability/Pages/%d7%a7%d7%91%d7%99%d7%a2%d7%aa%20%d7%90%d7%97%d7%95%d7%96%20%d7%94%d7%a0%d7%9b%d7%95%d7%aa%20%d7%94%d7%a8%d7%a4%d7%95%d7%90%d7%99%d7%aa.aspx',
# בדיקה מחדש של אחוזי נכות רפואיים או דרגת אי כושר
'page4':'https://www.btl.gov.il/benefits/Disability/Pages/%d7%91%d7%a7%d7%a9%d7%94%20%d7%9c%d7%a7%d7%91%d7%99%d7%a2%d7%94%20%d7%9e%d7%97%d7%93%d7%a9%20%d7%a9%d7%9c%20%d7%90%d7%97%d7%95%d7%96%20%d7%94%d7%a0%d7%9b%d7%95%d7%aa%20%d7%94%d7%a8%d7%a4%d7%95%d7%90%d7%99%d7%aa.aspx',
# קביעת דרגת אי–הכושר להשתכר או לתפקד במשק בית
'page5':'https://www.btl.gov.il/benefits/Disability/Pages/%d7%a7%d7%91%d7%99%d7%a2%d7%aa%20%d7%93%d7%a8%d7%92%d7%aa%20%d7%90%d7%99%e2%80%93%d7%94%d7%9b%d7%95%d7%a9%d7%a8%20%d7%9c%d7%94%d7%a9%d7%aa%d7%9b%d7%a8%20%d7%90%d7%95%20%d7%9c%d7%aa%d7%a4%d7%a7%d7%93%20%d7%91%d7%9e%d7%a9%d7%a7%20%d7%91%d7%99%d7%aa.aspx',
# סכום הקצבה
'page6':'https://www.btl.gov.il/benefits/Disability/Pages/%d7%a9%d7%99%d7%a2%d7%95%d7%a8%d7%99%20%d7%94%d7%a7%d7%a6%d7%91%d7%94.aspx',
# בדיקה על ידי ועדה רפואית
'page7':'https://www.btl.gov.il/benefits/Disability/Pages/%d7%91%d7%93%d7%99%d7%a7%d7%94%20%d7%a2%d7%9c%20%d7%99%d7%93%d7%99%20%d7%95%d7%a2%d7%93%d7%94%20%d7%a8%d7%a4%d7%95%d7%90%d7%99%d7%aa.aspx',
# מסלול מהיר לבעלי מוגבלויות קשות
'page8':'https://www.btl.gov.il/benefits/Disability/Pages/MaslulYarok.aspx',
# תהליך טיפול בתביעה
'page9':'https://www.btl.gov.il/benefits/Disability/Pages/tipulBetvia.aspx',
# תשלום הקצבה
'page10':'https://www.btl.gov.il/benefits/Disability/Pages/%d7%aa%d7%a9%d7%9c%d7%95%d7%9d%20%d7%94%d7%a7%d7%a6%d7%91%d7%94.aspx'
}


def scrape_and_save(key, url, output_folder):

    response = requests.get(url)  
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.title.string
    div_content = soup.find('div', class_='opener-txt')
    div_text = div_content.get_text(strip=True)
    
    file_data = f"title:{title}\n\
                  content:\n{div_text}\n\
                  url:\n{url}"
    
    key = sub_dir + f"{key}.txt"

    s3_client.put_object(Bucket=bucket_name,
                         Key=key,
                         Body=file_data
                        )
    
    print(f"Sucessfully scraped and saved {key} into {bucket_name}")

def lambda_handler(event, context):
    
    for page_num,url in urls.items():
        try:
            scrape_and_save(page_num, url, bucket_name)
        except Exception as e:
            print(f"Issue with file {page_num}: {e}")
    
    
    return {    
        'statusCode': 200,
        'body': 'Completed.'
    }
    
