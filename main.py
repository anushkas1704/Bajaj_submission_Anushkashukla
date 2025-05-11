import requests

def generate_webhook():
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    payload = {
        "name": "Anushka Shukla",
        "regNo": "0827CS221047", 
        "email": "anushkashukla220116@acropolis.in"
    }

    print("[STEP 1] Sending webhook generation request...")
    response = requests.post(url, json=payload)

    print("[DEBUG] Status code:", response.status_code)
    print("[DEBUG] Response text:", response.text)

    if response.status_code == 200:
        data = response.json()
        print("Webhook and token received.")
        return data['webhook'], data['accessToken']  
    else:
        print("[-] Failed to generate webhook.")
        exit(1)

def submit_solution(webhook_url, access_token, final_query):
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    body = {
        "finalQuery": final_query
    }

    print("[STEP 2] Submitting SQL query...")
    response = requests.post(webhook_url, headers=headers, json=body)

    print("Submission Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code == 200:
        print("Query submitted successfully!")
    else:
        print("Submission failed.")

def main():
    webhook_url, token = generate_webhook()

    final_query = """
    SELECT
        P.AMOUNT AS SALARY,
        E.FIRST_NAME || ' ' || E.LAST_NAME AS NAME,
        CAST((julianday('2025-05-11') - julianday(E.DOB)) / 365.25 AS INT) AS AGE,
        D.DEPARTMENT_NAME
    FROM PAYMENTS P
    JOIN EMPLOYEE E ON P.EMP_ID = E.EMP_ID
    JOIN DEPARTMENT D ON E.DEPARTMENT = D.DEPARTMENT_ID
    WHERE strftime('%d', P.PAYMENT_TIME) != '01'
    ORDER BY P.AMOUNT DESC
    LIMIT 1;
    """.strip()

    submit_solution(webhook_url, token, final_query)

if __name__ == "__main__":
    main()
