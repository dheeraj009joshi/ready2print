import datetime
import time
from ONELOGIN import onLogin





def get_leads_data_multiprocessing():
    f=open(f'all_leads_all_in_one_{datetime.date.today()}.csv','r')
    import json
    all_urls=[]
    for i in f.readlines():
        i=i.replace("'",'"')
        try:
            json_object = json.loads(i)
            print(json_object['Url'])
            all_urls.append(json_object['Url'])
        except:
            pass
    print(len(all_urls))
    instance=onLogin()
    instance.multiprocess_leads_data(all_urls)
    print("process of data collection is completed")
    time.sleep(5)
    instance.combine_csv_files('output_files',f'All_Leads{datetime.date.today()}.csv')
    
    
def get_leads_data_single_run():
    obj=onLogin()
    obj.login_to_oneLogin()
    obj.open_eleads_oneLogin()
    all_urls=obj.get_all_leads_urls()['urls']
    obj.get_lead_details(all_urls,'output_files/All_Leads{datetime.date.today()}.csv',)
    
    

