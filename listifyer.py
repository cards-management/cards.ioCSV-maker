import imaplib, email
from bs4 import BeautifulSoup
import csv

#logs into email and opens inbox
user = "@outlook.com"
password = ""
imap_url = "outlook.office365.com"
mail = imaplib.IMAP4_SSL(imap_url)
mail.login(user,password)
mail.select("INBOX")

#finds all emails
result, data = mail.uid("search",None,"ALL")
inbox_item_list = data[0].split()

#stores processed email results
test_array = [["label", "response"]]
awnsers = [["label", "response"]]
prompts = [["label", "prompt"]]

#analises each email
for item in inbox_item_list:
    print("==============next email=================")
    #extracts email content
    result2, email_data = mail.uid("fetch",item,"(RFC822)")
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)
    to_ = email_message["To"]
    from_ = email_message["From"]
    subject_ = email_message["Subject"]
    for part in email_message.walk():
        pass
    content_type = part.get_content_type()
    print(subject_)
    print(content_type)

    #determines email use
    if subject_ == "Test":
        html_ = part.get_payload()
        soup = BeautifulSoup(html_, "html.parser")
        text = soup.get_text()
        #print(text)
        testcards = text.split("#")
        del testcards[-1]
        #print(testcards)

        for testees in testcards:
            #print(testcards[testcards.index(testees)])
            test_array +=[["", testcards[testcards.index(testees)]]]
        #print(test_array)
        print("valid")
        
    elif subject_ == "prompts" or subject_ == "prompt":
        html_ = part.get_payload()
        soup = BeautifulSoup(html_, "html.parser")
        text = soup.get_text()
        procards = text.split("#")
        del procards[-1]
        #print(cards)
        
        for proms in procards:
            prompts+=[["", procards[procards.index(proms)]]]

        print("added as:")
        print(prompts)
        print("valid")

    elif subject_ == "answer" or subject_ == "answers":
        html_ = part.get_payload()
        soup = BeautifulSoup(html_, "html.parser")
        text = soup.get_text()
        anscards = text.split("#")
        del anscards[-1]
        #print(anscards)

        for anses in anscards:
            awnsers +=[["", anscards[anscards.index(anses)]]]
        print("added as:")
        print(awnsers)
        print("valid")

#tells results
print("\n<<<<<<<<<<<<<<outputing as>>>>>>>>>>>>>>>")
print("\n<<test>>")
print(test_array)
print("\n<<prompts>>")
print(prompts)
print("\n<<awnsers>>")
print(awnsers)

#exports as csvs
with open("testcards.csv","w",newline='') as csvfile:
    writer=csv.writer(csvfile)
    [writer.writerow(r)for r in test_array]
with open("promptcards.csv","w",newline='') as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(prompts)
with open("awnsercards.csv","w",newline='') as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(awnsers)

#checks test csv accuracy
testcards = list(csv.reader(open("testcards.csv")))
print("\n<<<Test csv finally saved as:>>>")
print(testcards)






