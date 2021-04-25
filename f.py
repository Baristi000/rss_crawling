import re

def pare(indexs:list):
    for i in range(len(indexs)):
        indexs[i].replace("&","and")
        indexs[i] = re.sub(r"[^a-zA-Z0-9]+"," ",indexs[i])
    return indexs[0]




#pare('Alcohol, Drugs, and Substance Abuse Disorder  \' CDC\'')
print(pare(['Alcohol, Drugs, and Substance Abuse Disorder#@  \' -CDC\'']))