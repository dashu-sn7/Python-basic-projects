import pandas as pd
import datetime
import matplotlib.pyplot as plt
format='%d/%m/%Y'

pinfo=pd.read_csv(r'C:\Users\HP\Desktop\blood bank management\pinfo.csv',index_col='cno',encoding='latin1')
donor=pd.read_csv(r'C:\Users\HP\Desktop\blood bank management\donor.csv',index_col='cno',encoding='latin1')
receiver=pd.read_csv(r'C:\Users\HP\Desktop\blood bank management\receiver.csv',index_col='cno',encoding='latin1')
stock=pd.read_csv(r'C:\Users\HP\Desktop\blood bank management\stock.csv',index_col='btype',encoding='latin1')
cno=pinfo.index[-1]


#Personal information function.
def perinfo():
    print('Please fill in your PERSONAL DETAILS to start new...!')
    print('\n')
    no=pinfo.index[-1]+1
    date=datetime.datetime.strptime((input('Todays date(dd/mm/yyyy): ')),format)
    name=input('Name: ').capitalize()
    b=True
    while b==True:
        btype=input('Blood type: ').upper()
        if btype not in list(stock.index):
            print('Please enter an appropriate blood group.')
            continue
        else:
            b=False
    age=int(input('Age: '))
    dob=datetime.datetime.strptime((input('Date of Birth(dd/mm/yyyy): ')),format)
    p=False
    while p==False:
        pno=int(input('Phone number: '))
        if len(str(pno))==10:
            p=True
        else:
            print('please enter an appropriate contact number.')
    email=input('E-MAIL id: ')
    addr=input('Address: ')
    pinfo.loc[no]=[date,name,btype,age,dob,pno,email,addr]
    pinfo.to_csv(r'C:\Users\HP\Desktop\blood bank management\pinfo.csv')
    print('\n')
    print('Your CLIENT NUMBER is ',no)
    print('Please remember this number to resume back with us!!')
    print('\n')

         
def service():
    print('''Servies provided by us:
1. Donate blood
2. Receive blood
3. Blood stock graph
4. Exit''')
    print('\n')
    s=int(input('Enter the service number to continue with our servies: '))
    print('\n')

    
    #donor details
    if s==1:
        print('''Dear client, you have chosen to donate blood!!!
    You are on the way on life saving mission!!!''')
        print('\n')
        cno=int(input('Enter your client number: '))
        if cno not in pinfo.index:
            print('Please fill in your personal details first to continue!!')
            pinfo()
            service()
        dod=datetime.datetime.strptime((input('Date of donating blood(dd/mm/yyyy): ')),format)
        btype=pinfo.loc[cno,'btype']
        print('Your blood group is ',btype)
        units=int(input('Units of blood donated: '))
        stock.loc[btype]+=units
        donor.loc[cno]=[pinfo.loc[cno,'name'],dod,btype,units]
        donor.to_csv(r'C:\Users\HP\Desktop\blood bank management\donor.csv')
        stock.to_csv(r'C:\Users\HP\Desktop\blood bank management\stock.csv')
        print('THANK YOU!! for your active participation in saving lives!!!')
        print('\n')
        service()

    #receiver details
    elif s==2:
        print('''Dear client, you have chosen to receive blood!!!
    May the blood received by you help a life...''')
        print('\n')
        cno=int(input('Enter your client number: '))
        if cno not in pinfo.index:
            print
            perinfo()
            service()
        dor=datetime.datetime.strptime((input('Date of receiving blood(dd/mm/yyyy): ')),format)
        btype=pinfo.loc[cno,'btype']
        print('Your blood group is ',btype)
        sa=stock.loc[btype]
        units=int(input('Units of blood needed: '))
        if units<sa:
            print('Blood group available..!')
            print('Your entry has been counted.. collect the blood units from the counter.')
            sa-=units
        else:
            print('Given blood group not available. Sorry for the inconvenience!')
            service()
        receiver.loc[cno]=[pinfo[cno,'name'],dor,btype,units]
        receiver.to_csv(r'C:\Users\HP\Desktop\blood bank management\receiver.csv')
        stock.to_csv(r'C:\Users\HP\Desktop\blood bank management\stock.csv')
        print('\n')
        service()

        
    #barh of stock
    elif s==3:
        print('The graph of the stock available...!')
        x=stock.index
        y=stock['tunits']
        plt.barh(x,y)
        plt.xlabel('UNITS OF BLOOD AVAILABLE')
        plt.ylabel('TYPES OF BLOOD')
        plt.title('BAR CHART OF BLOOD AVAILABLE')
        plt.show()
        print('\n')
        service()
        
    #exit
    elif s==4:
        print('THANK YOU !!!')
        r=False

    else:
        print('Please enter the appropriate number !')

r=True
if r==True:
    print('''WELCOME TO BLOOD BANK SERVICES!

If you are new to our service,
please FILL in your PERSONAL DETAILS to continue further!!!
or else continue further with ur client number!!''')
    print('\n')
    c=int(input('Are you new to our blood bank?(yes=1/no=2) :'))
    print('\n')
    if c==1:
        perinfo()
        service()
    elif c==2:
        service()
    else:
        print('Please enter the appropraite number to continue!')
