def build_jira_epics_stories(project: dict, coverage: dict, edge: dict)->dict:
    # Produce JSON for Jira import. DoR/DoD, AC, risks
    return {"epics":[{"key":"BAY-1","summary":"BayWalk Pilot"}], "stories":[{"summary":"Place cameras"}]}
