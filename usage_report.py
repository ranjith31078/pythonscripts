#!/usr/bin/env python

# This script prepares a report on customer's environment usage and mails them to CSMs
# ------------------------------------------------------------------------------------
# Author: Ranjith Karunakaran

import sys, subprocess, smtplib, logging as log, os

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

MAX_MAIL_LINES = 50


def run_command(*args, **kwargs):
    """Run shell command and capture output"""
    log.info('Running: ' + (' '.join(str(s) for s in args)))
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    proc.wait()
    if proc.returncode != 0:
        log.error('Error running command, exiting script')
        sys.exit(0)
    return out


def send_mail(send_from, send_to, subject, text, server, files=None):
    log.info('Sending mail to %s with %d attachment(s) and subject: %s: ' \
             % (send_to, len(files) if files else 0, subject))
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    for f in files or []:
        with open(os.path.join(os.getcwd(), f), 'rb') as fil:
            part = MIMEApplication(fil.read(), Name=os.path.basename(f))
            part['Content-Disposition'] = "attachment; filename='%s'" % os.path.basename(f)
            msg.attach(part)
    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
    log.info('Mail sent.')


def get_db_list(conf):
    db_list = run_command('sqlcmd', '-h', '-1', "-s,", '-w', '700', '-W', \
                          '-Q', 'SET NOCOUNT ON select name from sysdatabases where dbid > 4', \
                          '-H', 'localhost', '-U', conf['DB_SERVER_LOGIN'], '-P', conf['DB_SERVER_PASSWORD']).split(
        "\n")
    db_client_map = eval(conf['DB_CLIENT_NAME_MAP'])
    db_list = [(db_name.strip(), db_client_map[db_name.strip()]) for db_name in db_list if db_name.strip() != '']
    db_list.sort(key=lambda db_pair: db_pair[1])
    log.info("DB list: " + str(db_list))
    return db_list


def run_query(conf, db_name, db, retain_header=False):
    log.info('Started running query in DB ''%s''..' % db)
    lines = run_command('sqlcmd', '-i', SCRIPT_NAME + '.sql', '-H', \
                        conf['DB_SERVER_HOST'], '-U', conf['DB_SERVER_LOGIN'], '-d', db, '-P', \
                        conf['DB_SERVER_PASSWORD'], "-s,", '-w', '700', '-W').strip().split("\n")
    out_content = db_name + ',' + lines[2]
    if retain_header:
        out_content = 'Client,' + lines[0] + out_content
    with open(SCRIPT_NAME + '.csv', "a") as csv:
        csv.write(out_content + "\n")
    log.info('Completed query execution.')


def script_init():
    global SCRIPT_NAME
    SCRIPT_NAME = sys.argv[0].split('.')[0]
    log.basicConfig(filename=SCRIPT_NAME + '.log', level=log.INFO)
    try:
        os.remove(os.path.join(os.getcwd(), SCRIPT_NAME + '.csv'))
    except OSError:
        pass
    return dict(line.strip().split('=') for line in open(SCRIPT_NAME + '.properties') \
                if not line.startswith('#') and not line.strip() == '')


def prepate_and_send_mail(conf):
    mail_content = ""
    for ln in range(1, MAX_MAIL_LINES + 1):
        if not 'MAIL_LINE' + str(ln) in conf:
            break
        mail_content += conf['MAIL_LINE' + str(ln)] + "\n"
    send_mail(conf['MAIL_FROM'], [conf['MAIL_TO']], conf['MAIL_SUBJECT'], \
              mail_content, conf['SMTP_HOST'], [SCRIPT_NAME + '.csv'])


def main():
    conf = script_init()
    for idx, (db, db_name) in enumerate(get_db_list(conf)):
        run_query(conf, db_name, db, idx == 0)
    prepate_and_send_mail(conf)


if __name__ == '__main__':
    main()
