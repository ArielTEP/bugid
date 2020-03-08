import os
import markdown
from flask import Flask
from flask import request
from flask_restful import Resource, Api
from .bot_utils import send_spark_get
from .bot_utils import send_spark_post
from .bot_utils import get_bug_note


app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    # Open the readme.md file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r' ) as markdown_file:
        # Read the contents of the file
        content = markdown_file.read()
        # Convert to HTML
        return markdown.markdown(content)

class BugQuery(Resource):

    def __init__(self):
        result = send_spark_get('https://api.ciscospark.com/v1/people/me')
        self.bot_name = result.get('displayName','')
        self.bot_email = 'buggypedia@webex.bot'

    def get(self):
        return {'data' : 'Empty', 'description' : 'This method is not implemented yet!'}

    def post(self):
        webhook = request.get_json(silent=True)
        print(webhook['resource'])
        if webhook['resource'] != 'messages': return -1
        print("Message received from: " + webhook['data']['personEmail'])
        print("Webhook data id: " + webhook['data']['id'])
        result = send_spark_get('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
        msg = None
        if webhook['data']['personEmail'] != self.bot_email:
            in_message = result.get('text', '')
            in_message = in_message.replace(self.bot_name,'').strip()
            print(" Message: " + in_message)
            if in_message.startswith('CSC') and len(in_message)==10:
                attr_list = get_bug_note(in_message)
                product = attr_list[0]
                status = attr_list[1]
                headline = attr_list[2]
                # print(headline)
                for i in range(3,len(attr_list)):
                    headline += ' '
                    headline += attr_list[i]
                msg = '#### ' + headline + '\n' + 'Status: ' + status + ', Product: ' + product + '<br/>' + 'https://scripts.cisco.com/app/quicker_cdets/?bug=' + in_message
                msg += '<br/>'
                # msg += 'CCO: ' + 'https://bst.cloudapps.cisco.com/bugsearch/bug/' + in_message
            else:
                msg = "Double-check bug id and try again"
            result = send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "markdown": msg})
        return "ok"

api.add_resource(BugQuery, '/bugquery')

'''
# Attributes that never have spaces in them
 60     # ez_attrs = ["Status","Severity","Project","Product","DE-manager","Doc-manager","Engineer","Submitter","BTK-security-complete",
 61 #                 "Is-customer-visible","BadCodeFlag","Priority","Regression-submitter","Identifier","Component","RNE-Type","Submitter-id","Code-reviewer"]
 62     
 63     
'''

