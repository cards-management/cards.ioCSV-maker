import imaplib, email
import csv

#logs into email and opens inbox
email_user = ""
email_pass = "" 
imap_url = "outlook.office365.com"

mail = imaplib.IMAP4_SSL(imap_url)
mail.login(email_user,email_pass)
mail.select("INBOX")

#finds all emails
result, data = mail.uid("search",None,"ALL")
inbox_item_list = data[0].split()

#variables to store processed email results
prompts = [["label", "prompt"]]
answers = [["label", "response"]]

#analises each email
for item in inbox_item_list:

    #extracts email content
    result2, email_data = mail.uid("fetch",item,"(RFC822)")
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)

    em_to = email_message["To"]
    em_from = email_message["From"]
    em_subject = email_message["Subject"]

    print("Reading email from " + em_from)
    # Get plaintext version of email
    em_text = ""
    for payload in email_message.walk():
        if payload.get_content_type().lower() == 'text/plain':
            charset = payload.get_content_charset()
            em_text = payload.get_payload(decode=True).decode(encoding=charset, errors="ignore")

    if em_text == "":
        print("Nothing found in email from " + em_from)


    parts = em_text.split("\r\n")
    parts = filter(None, parts) # Removes empty parts
    
    if "prompt" in em_subject.lower() or "question" in em_subject.lower() or "prompts" in em_subject.lower() or "questions" in em_subject.lower():    
        for proms in parts:
            prompts+=[["", proms]]
        print(prompts)

    elif "answer" in em_subject.lower() or "answers" in em_subject.lower():
        for anses in parts:
            answers +=[["", anses]]
        print(answers)

#replaces commas with a similar symbol to stop CSV formatting issues
for i in range(len(answers)):
    answers[i][1] = answers[i][1].replace(",","¸")
for i in range(len(prompts)):
    prompts[i][1] = prompts[i][1].replace(",","¸")

#exports as csvs
with open("promptcards.csv","w",newline='') as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(prompts)
with open("awnsercards.csv","w",newline='') as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(answers)


# Log out of mail
mail.close()
mail.logout()

