import requests

BASE = "http://127.0.0.1:5000/"

#reponse = requests.get(BASE + "recommend/startups/1")
#print(reponse.json())

fullDescription = 'Y Combinator is a startup accelerator that invests in a large number of startups twice a year. It created a new model for funding early-stage startups. Twice a year, the company invests a small amount of money ($150k) in a large number of startups. The startup accelerator works intensively with the companies for three months, to get them into the best possible shape and refine their pitch to investors. Each cycle culminates in Demo Day when the startups present their companies to a carefully selected, invite-only audience.'
name='Y Combinator'
fundingType='Accelerator'
location='Mountain View, California, United States'
description='Y Combinator is a startup accelerator that invests in a wide range of startups twice a year.'

reponse2 = requests.put(BASE + "recommend/startups/1", {'name': name, 'fundingType': fundingType, 'location': location, 'description': description, 'fullDescription': fullDescription})
print(reponse2.json())

reponse = requests.get(BASE + "recommend/startups/1")
print(reponse.json())