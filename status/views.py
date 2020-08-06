from django.shortcuts import render
import json
import requests
from django.views.generic import View

class HomeView(View):
    def get(self,request,*args,**kwargs):
        combined=[]
        state = [] 
        conf = [] 
        delconf = [] 
        act = [] 
        delact = [] 
        rec = [] 
        delrec = [] 
        dth = [] 
        deldth = [] 
        cfr = [] 
        rr = []
        rdr = []
        testtemp=[]
        test=[]
        req1=requests.get('https://api.covid19india.org/state_test_data.json')
        z=json.loads(req1.text)

        request1 = requests.get('https://api.covid19india.org/data.json')
        y = json.loads(request1.text)
        for i in range(38):
            act.append(int(y['statewise'][i]['active']))
            state.append(y['statewise'][i]['state'])
            conf.append(int(y['statewise'][i]['confirmed']))
            rec.append(int(y['statewise'][i]['recovered']))
            dth.append(int(y['statewise'][i]['deaths']))
            delconf.append(int(y['statewise'][i]['deltaconfirmed']))
            deldth.append(int(y['statewise'][i]['deltadeaths']))
            delrec.append(int(y['statewise'][i]['deltarecovered']))
            delact.append(delconf[i]-deldth[i]-delrec[i])
            try:
                cfr.append(round(100*dth[i]/conf[i], 2))
            except:
                cfr.append(float('0.0'))
            try:
                if rec[i]==0 and conf[i]!=0:
                    rr.append('No Recoveries Yet')
                else:
                    rr.append(round(100*rec[i]/conf[i],2))
            except:
                rr.append('No cases confirmed')
            try:
                rdr.append(round(rec[i]/dth[i], 2))
            except:
                rdr.append('No deaths occured')
        for states in state:
            for i in range(0,len(z['states_tested_data'])):
                if z['states_tested_data'][i]['state']==states:
                    testtemp.append(z['states_tested_data'][i]['totaltested'])
            if(len(testtemp)!=0):
                test.append(testtemp[-1])
            else:
                test.append('0')
        sum_=0
        for i in range(0,len(test)):
            test[i]=int(test[i])
            sum_+=test[i]
        test[0]=sum_
        state[0] = 'INDIA'
        for i in range(38):
            join=[] 
            join.extend([state[i],conf[i],delconf[i],act[i],delact[i],rec[i],delrec[i],dth[i],deldth[i],cfr[i],rr[i],test[i]])
            combined.append(join)
        combined=sorted(combined,key=lambda x: x[1],reverse=True)
        comb = []
        for i in range(38):
            data = zip([combined[i][0]],[combined[i][1]],[combined[i][2]],[combined[i][3]],[combined[i][4]],[combined[i][5]],[combined[i][6]],[combined[i][7]],[combined[i][8]],[combined[i][9]],[combined[i][10]],[combined[i][11]])
            comb.append(data)
        
        context = {
            'combined':comb
        }
        return render(request,'index.html',context)

def about(request):
    return render(request,'about.html')
