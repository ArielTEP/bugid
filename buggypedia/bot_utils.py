import requests
import json

# Y2lzY29zcGFyazovL3VzL1dFQkhPT0svMDcyOTBiYjktNThkNC00OGFmLWFjNzYtMTQ0MWYzMjM5N2Rj

bearer = "YzZkZWEyYjUtMmE5NS00ZTYzLWFjZjYtZDA2ZThkNTNlZTEzOTY5OGM2OGEtNzli_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
headers = { 'Content-Type':'application/json', 'Accept' : 'application/json' ,'Authorization' : 'Bearer ' + bearer}

def send_spark_get(url):
    '''
    Retrieve contents of the messsge that triggered the bot.
    '''
    response = requests.get(url, headers=headers)
    return response.json()

def send_spark_post(url, data):
    '''
    Respond to the user who entered the bot command.
    '''
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_bug_note(bug_id):
    '''
    Example URL:
    http://cdetsweb-prd.cisco.com/findsimple/findcr_simple?field=Submitted-on,Identifier,Status,Headline&query=[Identifier]=%27CSCug59348%27
    url = "http://cdetsweb-prd.cisco.com/cdets/cli/ViewNote.html?identifier={bug_id}&title={note_name}".format(bug_id=bug_id, note_name=note_name)
   '''
    url = 'http://72.163.43.97/findsimple/findcr_simple?field=Product,Status-desc,Headline&query=[Identifier]=%27{bug_id}%27'.format(bug_id=bug_id)
    response = requests.get(url).text
    # print(response)
    return response.split()