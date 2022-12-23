from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

import datacommons
import datacommons_pandas
import time

import pandas as pd
import matplotlib.pyplot as plt

class Harvester:

    def BLS(self):
        count=0
        series_id=[]
        title=[]
        units=[]
        age=[]
        
        driver = webdriver.Chrome()
        driver.get('https://data.bls.gov/cgi-bin/surveymost?bls')
        stats=driver.find_elements(By.NAME,'series_id')
        for i in stats:
            i.click()
        
        driver.find_element(By.XPATH,'//form//p/input[@type="Submit"]').click()
        ele=driver.find_element(By.XPATH,'//html')
        html=ele.get_attribute('innerHTML')
        table=pd.read_html(html)

        for i in range(len(table)):
            
            if(count<len(table)):
                df=table[count]
                for j in range(len(df.index)):
                    if(j==0):
                        series_id.append(df.iloc[0][1])
                    if(j==2):
                        title.append(df.iloc[2][1])
                    if(j==4):
                        units.append(df.iloc[4][1])
                    if(j==5):
                        age.append(df.iloc[5][1])
            count+=2
        
        count=1
        checker=0
        for i in range(len(table)):
            if(count<len(table)):
                df=table[count]
                
            if(checker<len(series_id)):
                
                df['series_id']=series_id[checker]
                df['title']=title[checker]
                df['units']=units[checker]
                df['source']='https://data.bls.gov/cgi-bin/surveymost?bls'
                df['country']='U.S'
                name=f'{title[checker]}'
                df.to_csv(name+'.csv')

            count+=2
            checker+=1
        cols=table[11].columns
        y=table[11][cols[0]]
        x_axis=cols[1:13]
        values_df=table[11][x_axis] 
        titles=table[11]['title']
        values_df.drop(index=values_df.index[-1],axis=1,inplace=True)

        ax,fig=plt.subplots()
        
        for i in range(len(values_df.index)-1):
            x=values_df.loc[i].values
            print(i)    
            plt.figure(figsize=(10,5))
            plt.plot(y,x,linewidth=2)
            plt.title(titles[0])
            plt.show()

    def BEA(self):
        
        driver = webdriver.Chrome()
        driver.get('https://apps.bea.gov/international/factsheet/factsheet.html#600')
        ele=driver.find_element(By.XPATH,'//html')
        html=ele.get_attribute('innerHTML')
        tb=driver.find_element(By.ID,'udiTable_outward')
        tbl=ele.get_attribute('innerHTML')
        table=pd.read_html(tbl)
        headers=tb=driver.find_elements(By.XPATH,'//div//div/h8')
        for i in range(1,len(table)):
            if(i<len(headers)):
                table[i].to_csv(f'{headers[i].text}.csv')
            else:
                table[i].to_csv(f'BEA{i}.csv')
        
    def DataCommons(self):

        country_id=['geoId/05','country/BIH','geoId/12086','geoId/12086','country/GMB']
        title=["Count_Person_Male", "Count_Person","Count_Death","RetailDrugDistribution_DrugDistribution_Naloxone","Amount_EconomicActivity_ExpenditureActivity_EducationExpenditure_Government_AsFractionOf_Amount_EconomicActivity_GrossDomesticProduction_Nominal"]
        
        series_1=datacommons_pandas.build_time_series("geoId/05", "Count_Person_Male")
        series_2=datacommons_pandas.build_time_series("country/BIH", "Count_Person", measurement_method="BosniaCensus")
        series_3=datacommons_pandas.build_time_series("geoId/12086", "Count_Death", observation_period="P1Y")
        series_4=datacommons_pandas.build_time_series("geoId/12086", "RetailDrugDistribution_DrugDistribution_Naloxone", unit="Grams")
        series_5=datacommons_pandas.build_time_series("country/GMB", "Amount_EconomicActivity_ExpenditureActivity_EducationExpenditure_Government_AsFractionOf_Amount_EconomicActivity_GrossDomesticProduction_Nominal", scaling_factor="100.0000000000")

        
        series_1.plot(title='count_person_male')
        series_2.plot(title='count_person')
        series_3.plot(title='count_death')
        series_4.plot(title='RetailDrugDistribution_DrugDistribution_Naloxone')
        series_5.plot(title='Amount_EconomicActivity_ExpenditureActivity_EducationExpenditure_Government_AsFractionOf_Amount_EconomicActivity_GrossDomesticProduction_Nominal')

        data_list=[series_1,series_2,series_3,series_4,series_5]
        df_list=[]
        counter=0

        for i in data_list:
            df=pd.DataFrame(i,columns=['values'])
            df['source']='DataCommons_Python_Pandas_Endpoint'
            df['country_id']=country_id[counter]
            df['title']=title[counter]
            counter+=1
            df_list.append(df)
        

harvest=Harvester()

harvest.BLS()
#harvest.BEA()
#harvest.DataCommons()