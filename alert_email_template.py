from pyscope import GSConnection
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def convert(seconds):
    days = seconds // (24 * 3600)
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d Days, %d Hours, %02d Minutes, %02d Seconds" % (days, hour, minutes, seconds)


GRADESCOPE_USERNAME = ""
GRADESCOPE_PASSWORD = ""
FROM_ADDR = ""
PASSWORD = ""
TO_ADDR = ""
SMTP_SERVER = ""
SMTP_PORT = 1337

conn = GSConnection()
conn.login(GRADESCOPE_USERNAME, GRADESCOPE_PASSWORD)
conn.get_account()
dues = conn.account.get_dues('Fall 2020')

submitted = {}
no_submission = {}

for cid in dues.keys():
    submitted[cid] = []
    no_submission[cid] = []
    # print(conn.account.student_courses[cid].shortname)
    for due_dict in dues[cid]:
        if due_dict['status'] == "No Submission":
            no_submission[cid].append({'name': due_dict['name'], 'timeleft': due_dict['due_ts'] - due_dict['current_ts']})
        else:
            submitted[cid].append({'name': due_dict['name'], 'timeleft': due_dict['due_ts'] - due_dict['current_ts']})

content = ""
for cid in no_submission:
    if len(no_submission[cid]):
        content += conn.account.student_courses[cid].shortname
        content += ":\n"
        for assignment in no_submission[cid]:
            if assignment['timeleft'] < 0:
                continue
            content += ("\tName: " + assignment['name'])
            content += ("\tTimeleft: " + convert(assignment['timeleft']) + "\n")
        content += "\n"

msg = MIMEText(content, 'plain', 'utf-8')
msg['From'] = _format_addr('Angry me <{}>'.format(FROM_ADDR))
msg['To'] = _format_addr('Lazy you <{}>'.format(TO_ADDR))
msg['Subject'] = Header('Notice the dues!', 'utf-8').encode()

server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
# server.set_debuglevel(1)
server.login(FROM_ADDR, PASSWORD)
server.sendmail(FROM_ADDR, [TO_ADDR], msg.as_string())
server.quit()
