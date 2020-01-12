
# coding: utf-8

# In[12]:
# This program aggregates competitor portfolio data from SEC.GOV, and creates a file with the compiled data calle 'IssuerData.csv'
# This data includes REPO (repurchase agreement) portfolios

import bs4 as bs
import urllib.request
import csv
import time

start_time = time.time()

gs = 'https://www.sec.gov/Archives/edgar/data/822977/000114554918004475/primary_doc.xml'
dreyfus = 'https://www.sec.gov/Archives/edgar/data/759667/000003015818000071/primary_doc.xml'
fidelity = 'https://www.sec.gov/Archives/edgar/data/356173/000035617318000120/primary_doc.xml'
federated = 'https://www.sec.gov/Archives/edgar/data/856517/000125889718001697/primary_doc.xml'
jp = 'https://www.sec.gov/Archives/edgar/data/1217286/000171874518000194/primary_doc.xml'
tempf = 'https://www.sec.gov/Archives/edgar/data/97098/000171773418000132/primary_doc.xml'
ss = 'https://www.sec.gov/Archives/edgar/data/1094885/000114554918004779/primary_doc.xml'
mipmmf = 'https://www.sec.gov/Archives/edgar/data/915092/000114554918004419/primary_doc.xml'

funds = [gs, dreyfus, fidelity, federated, jp, tempf, ss, mipmmf]
portfolios = ['GS', 'Dreyfus', 'Fidelity', 'Federated', 'JPM', 'L-TEMPF', 'SS', 'MIPMMF']
count = 0

issuer_data = open('IssuerData.csv', 'w+')
csvwriter = csv.writer(issuer_data)


for i in range(len(funds)):
    source = urllib.request.urlopen(funds[i]).read()
    soup = bs.BeautifulSoup(source,'xml')

    issuer_head = []

    for security in soup.find_all('scheduleOfPortfolioSecuritiesInfo'):
        issuer = []
        collateral = []

        # Creating Headers
        if count == 0:
            
            headers = ['Portfolio', 'Issuer Name', 'Issuer Title', 'CUSIP', 'Category', 
                       'Collateral', 'WAM', 'WAL', 'MAT Date','Sec Yield', 'Including Value','MV %']  

            for title in headers:
                issuer_head.append(title)

            csvwriter.writerow(issuer_head)
            count+=1


        # add data to headers  

        issuer.append(portfolios[i])

        issuername = security.find('nameOfIssuer').text
        issuer.append(issuername)

        issuertitle = security.find('titleOfIssuer').text
        issuer.append(issuertitle)

        try:
            cusip = security.find('CUSIPMember').text
            issuer.append(cusip)
        except:
            issuer.append("#N/A") 

        category = security.find('investmentCategory').text
        issuer.append(category)

        txt = ""
        for c in security.find_all('collateralIssuers'):
            txt += c.text.strip()

        txt = txt.replace("\n","")
        txt = txt.strip('\n\t')
        txt = txt.replace("\r","")
        
        if txt == '':
            txt = "#N/A"
        
        issuer.append(txt[0:30000])

        wam = security.find('investmentMaturityDateWAM').text
        issuer.append(wam)

        wal = security.find('investmentMaturityDateWAL').text
        issuer.append(wal)

        mat = security.find('finalLegalInvestmentMaturityDate').text
        issuer.append(mat)

        secyield = security.find('yieldOfTheSecurityAsOfReportingDate').text
        issuer.append(float(secyield))

        value = security.find('includingValueOfAnySponsorSupport').text
        issuer.append(float(value))

        mv = security.find('percentageOfMoneyMarketFundNetAssets').text
        issuer.append(float(mv))

        csvwriter.writerow(issuer)
    

issuer_data.close()
print('Complete')
print('Time elapsed:', round(time.time() - start_time, 2), 'seconds')

