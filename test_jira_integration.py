import requests as req
import getpass
from lxml import etree

JIRA_USER = ''
JIRA_BASE_URL = ""
JIRA_PROJ_KEY = ''

jira_pass = getpass.getpass("Jira password: ")
# jira_pass = ""

PSS_BASE_URL = ""
PSS_USER = ''
PSS_PASS = ''
PSS_PROJ_UUID = ''

PSS_NS = {"ns":"http://integration.rest.v1"} # xml namespace

def get_pss_sprints():
    sprint_ids = []
    pss_url = "%s/rest/projectservice/v1/project/%s/children"
    xml = etree.fromstring(req.get(pss_url %  (PSS_BASE_URL, PSS_PROJ_UUID), auth=(PSS_USER, PSS_PASS)).content)

    jira_id_xpath = "ns:project//ns:customField[ns:name='Jira Id']/ns:value"
    for pss_sprint in xml.findall(jira_id_xpath, PSS_NS):
        sprint_ids.append(int(float(pss_sprint.text)))

    print("Got %s sprint ids from PSS" % len(sprint_ids))

    return (sprint_ids, xml)


def get_jira_issues(sprint_ids):
    start_at = 0
    total_issues = None
    all_issues = []
    while(True):
        url = """%s/rest/api/2/search?startAt=%s&jql= project=%s
                 AND issuetype in (Bug, Story)
                 AND (sprint in (%s) OR
                     (resolution = Unresolved AND
                      (Sprint = EMPTY OR
                       Sprint NOT IN (openSprints(),futureSprints()))))""" % \
                (JIRA_BASE_URL, start_at, JIRA_PROJ_KEY,
                    ", ".join(str(id) for id in sprint_ids))

        issues = req.get(url, auth=(JIRA_USER, jira_pass)).json()
        all_issues.extend(issues['issues'])
        if (total_issues is None):
            total_issues = int(issues['total'])
        if start_at > total_issues:
            break
        start_at += 50
        print("Got %s of %s total records" % (start_at, total_issues), end="\r", flush=True)

    print("Got all %s issues" % len(all_issues))
    return all_issues

def get_all_data():
    sprint_ids, pss_sprints_xml = get_pss_sprints()
    jira_issues = get_jira_issues(sprint_ids)
    return jira_issues, pss_sprints_xml

def compare_data(jira_issues, pss_sprints_xml):
    pass

def main():
    jira_issues, pss_sprints_xml = get_all_data()
    compare_data(jira_issues, pss_sprints_xml)

if __name__ == '__main__':
    main()
