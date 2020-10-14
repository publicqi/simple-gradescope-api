from pyscope import GSConnection
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import time, threading

GRADESCOPE_USERNAME = ""
GRADESCOPE_PASSWORD = ""
FROM_ADDR = ""
PASSWORD = ""
TO_ADDR = ""
SMTP_SERVER = ""
SMTP_PORT = 1337

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

def send_email(near_due=False):
    submitted = {}
    no_submission = {}
    each_timeleft = []

    for cid in dues.keys():
        submitted[cid] = []
        no_submission[cid] = []
        # print(conn.account.student_courses[cid].shortname)
        for due_dict in dues[cid]:
            if due_dict['status'] == "No Submission" and due_dict['due_ts'] - due_dict['current_ts'] > 0:
                no_submission[cid].append({'name': due_dict['name'], 'timeleft': due_dict['due_ts'] - due_dict['current_ts']})
                each_timeleft.append(due_dict['due_ts'] - due_dict['current_ts'])
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

    each_timeleft = sorted(each_timeleft)

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('Angry me <{}>'.format(FROM_ADDR))
    msg['To'] = _format_addr('Lazy you <{}>'.format(TO_ADDR))
    if near_due and each_timeleft[0] < 12 * 3600:
        msg['Subject'] = Header('12 HRS ALARM! Notice the dues!', 'utf-8').encode()
    else:
        msg['Subject'] = Header('Notice the dues!', 'utf-8').encode()

    # If this is called by update_when_some_due_has_12_hrs_left()
    # , it may not be near due. Sleep until 12 hrs left
    if near_due and each_timeleft[0] > 12 * 3600:
        return each_timeleft[0] - 12 * 3600

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.login(FROM_ADDR, PASSWORD)
    server.sendmail(FROM_ADDR, [TO_ADDR], msg.as_string())
    server.quit()
    if len(each_timeleft) > 1:  # if there's a second due, sleep until that due has 12 hrs left
        return each_timeleft[1] - 12 * 3600
    return 4 * 3600  # else sleep 4 hrs


conn = GSConnection()
conn.login(GRADESCOPE_USERNAME, GRADESCOPE_PASSWORD)
conn.get_account()
dues = None  # conn.account.get_dues('Fall 2020')
lock = threading.Lock()

def update_dues_per_12_hrs():
    global dues
    while True:
        print("update_dues_per_12_hrs()")
        lock.acquire()
        print("update_dues_per_12_hrs()\tlock acquired")
        dues = conn.account.get_dues('Fall 2020')
        print("update_dues_per_12_hrs()\tdues updated")
        send_email()
        print("update_dues_per_12_hrs()\temail sent")
        print("update_dues_per_12_hrs()\tsleep(12 * 3600)")
        lock.release()
        time.sleep(60 * 60 * 12)

def update_when_some_due_has_12_hrs_left():
    global dues
    while True:
        print("update_when_some_due_has_12_hrs_left()")
        lock.acquire()
        print("update_when_some_due_has_12_hrs_left()\tlock acquired")
        dues = conn.account.get_dues('Fall 2020')
        print("update_when_some_due_has_12_hrs_left()\tdues updated")
        try:
            closest_due = send_email(True)
            print("update_when_some_due_has_12_hrs_left()\temail sent")
            print("update_dues_per_12_hrs()\tsleep(%d)" % closest_due)
            lock.release()
            time.sleep(closest_due)
        except ValueError:
            exit()


t1 = threading.Thread(target=update_dues_per_12_hrs, name='update_dues_per_12_hrs')
t2 = threading.Thread(target=update_when_some_due_has_12_hrs_left, name='update_when_some_due_has_12_hrs_left')

t1.start()
t2.start()
