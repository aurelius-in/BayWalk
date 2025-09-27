import requests, json
def evaluate_opa(opa_url: str, policy_pkg: str, data: dict)->dict:
    r = requests.post(f"{opa_url}/v1/data/{policy_pkg}", json={"input": data})
    r.raise_for_status()
    return r.json()
