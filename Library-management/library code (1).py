import pandas as pd
from datetime import datetime
import numpy as np
import time

stock=pd.read_csv(r"C:\Users\HP\Desktop\library mangement\bookstock.csv",index_col='bid',encoding='latin1')
entry=pd.read_csv(r"C:\Users\HP\Desktop\library mangement\entry.csv",index_col='bid',encoding='latin1')
stuinfo=pd.read_csv(r"C:\Users\HP\Desktop\library mangement\stuinfo.csv",index_col='sid',encoding='latin1')
regive=pd.read_csv(r"C:\Users\HP\Desktop\library mangement\regive.csv",index_col='bid',encoding='latin1') 
 
f= "%d/%m/%Y"
ex=False


#VIEW BOOK STOCK with count details
def stockdetails():
    print(stock[['genre','bname']].rename(columns={'genre':'GENRE','bname':'BOOK NAME'}))
    time.sleep(2)
    print('\n') 
    t=int((stock.index[-1])[-2:])
    x=len(entry.index)
    y=len(regive.index) 
    print('TOTAL NUMBER OF BOOKS IN THE LIBRARY :',t)
    print('\n')
    print('Number of books available            :',t-(x-y))
    print('Number of books to be returned       :',x-y)
    print('\n')

#VIEW books GENRE wise
def bookgenre():
    print('\n')
    print('''GENRES AVAILABLE:

Non Fiction - 1
Fiction - 2 
Biographies - 3 
Science Fiction - 4
Subject related - 5''')
    print('\n')
    g=int(input('Enter the genre code to view its books available: '))
    print('\n')
    if g not in range(1,6):
        print('Please enter an appropriate number!')
    else:
        if g==1:
            print(stock[(stock['genre']=='Non Fiction')][['genre','bname']].rename(columns={'bid':'BOOK ID','genre':'GENRE','bname':'BOOK NAME'}))
        elif g==2: 
            print(stock[(stock['genre']=='Fiction')][['genre','bname']].rename(columns={'bid':'BOOK ID','genre':'GENRE','bname':'BOOK NAME'}))
        elif g==3:
            print(stock[(stock['genre']=='Biographies')][['genre','bname']].rename(columns={'bid':'BOOK ID','genre':'GENRE','bname':'BOOK NAME'}))
        elif g==4:
            print(stock[(stock['genre']=='Science Fiction')][['genre','bname']].rename(columns={'bid':'BOOK ID','genre':'GENRE','bname':'BOOK NAME'}))
        else:
            print(stock[(stock['genre']=='Subject Related')][['genre','bname']].rename(columns={'bid':'BOOK ID','genre':'GENRE','bname':'BOOK NAME'}))        
    print('\n') 
 
#VIEW particular book details 
def bdetail():
    cts=1
    while cts==1:
        bookgenre() 
        bid=input('Enter the book ID to view its details: ')
        print('\n')
        if bid in stock.index:
            print('BOOK ID (bid)  : ',bid,'\n',
                  'GENRE          : ',stock.loc[bid,'genre'],'\n',
                  'BOOK NAME      : ',stock.loc[bid,'bname'],'\n',
                  'AUTHOR         : ',stock.loc[bid,'author'],'\n',
                  'PUBLISHED YEAR : ',stock.loc[bid,'pyear'],'\n',
                  'PUBLISHER      : ',stock.loc[bid,'publisher'],'\n',
                  'EDITION        : ',stock.loc[bid,'edition'])
            print('\n')
        else:
            print('The given book ID is not found! (check the entered id)')
        print('\n') 
        cts=int(input('Do you want to continue? (yes=1/no=0): '))
        print('\n')


#CHECK availability of book
def availability():
    cts=1
    while cts==1:
        bookgenre()
        print('\n') 
        bid=input('Enter the book ID (bid) to check its availability:  ')
        print('\n')
        if bid not in stock.index:
            print('BOOK NOT FOUND')
        else:
            if (bid not in entry.index) and (bid not in regive.index):
                print('The book is AVAILABLE in the library...')
            else:
                print('The book is NOT AVAILABLE in the library...')
        print('\n') 
        cts=int(input('Do you want to continue?(yes=1/no=0) :'))
        print('\n')
        

#BORROW a book
def borrow():
    print('Reading makes you more wiser! You have chosen to borrow a book!')
    print('\n')
    sid=int(input('Enter your Student ID to borrow: '))
    print('\n')
    if sid not in stuinfo.index:
        print('YOU are NOT a MEMBER OF THE LIBRARY!')
        print('\n')
        print('''If you want to register enter 1,
or if you want to restart this service again enter 0''')
        cts=int(input('Enter the number correctly : '))
        print('\n')
        if cts==1:
            studentregister()
            print('\n')
            borrow()
        elif cts==0: borrow()
        else:
            print('Please type the appropriate option.')
            menu()
    bookgenre() 
    print('\n')
    y=True
    while y==True:
        c=input('Enter the Book ID (bid) of the book you want to borrow: ')
        if c not in stock.index:
            print('The given book ID is not valid!(Please recheck)')
        elif c in entry.index: 
            print('The chosen book is already borrowed!')
        else: 
            print('Congratulations! The chosen book ID is available!')
            y=False
            print('\n')
            b=input('Borrowing date(DD/MM/YYYY):  ')
            bdate=datetime.strptime(b, f)
            entry.loc[c]=[sid,bdate,np.nan]
            entry.to_csv(r"C:\Users\HP\Desktop\library mangement\entry.csv")
            print('\n') 
            print('You have successfully borrowed the book!') 
            print('Please make sure that you return the book within four days from the day of borrowing.')
            print('NOTE: If not returned on time, fine of Rs.50 will be charged for each day of delay')
            print('\n') 


# RETURN a book
def returning():
    print('You have opted to return a book...')
    print('\n') 
    sid=int(input('Enter your Student ID to return: '))
    print('\n')
    if sid not in stuinfo.index:
        print('YOU are NOT a MEMBER OF THE LIBRARY!')
        print('\n')
        print('''If you want to register enter 1,
or if you want to restart this service again enter 0''')
        cts=int(input('Enter the number correctly : '))
        print('\n')
        if cts==1:
            studentregister()
            print('\n')
            returning()
        elif cts==0: returning()
        else:
            print('Please type the appropriate option.')
            menu()
    else:
        if sid in list(entry['sid']):
            bid=input('Enter the book ID to return: ')
            if bid not in stock.index:
                print('BOOK NOT FOUND')
            elif bid not in entry.index:
                print('Book not borrowed. Please recheck the Book ID!') 
            elif list(entry.loc[bid,['sid','returned']])==[sid,'yes']:
                print('\n') 
                print('The book has been already returned..!')
            else: 
                r=input('Returning date(DD/MM/YYYY): ')
                rdate=datetime.strptime(r, f) 
                bdate=datetime.strptime(str(entry.loc[bid,'bdate']),'%Y-%m-%d %H:%M:%S')
                d=rdate-bdate
                diff=int(f"{d.days}")
                if diff<=4:
                    fine=0
                    print('\n') 
                    print('You have returned the book on time!')
                    print('You have no fine to pay!')
                else:
                    fine=50*diff
                    print('\n') 
                    print('You have not returned the book on time and therefore fine has been charged!')
                    print('Your due date was delayed by',diff,'days') 
                    print('Fine of Rs.50 has been charged for each in delay.')
                    print('\n')
                    print('The FINE you have to pay is Rs.',fine) 
                    print('Kindly pay the fine in the counter WITHOUT FAIL!')
                    regive.loc[bid]=[sid,rdate,diff,fine]
                    entry['returned'] = entry['returned'].astype(str)
                    entry.loc[bid,'returned']='yes' 
                    regive.to_csv(r"C:\Users\HP\Desktop\library mangement\regive.csv")
                    entry.to_csv(r"C:\Users\HP\Desktop\library mangement\entry.csv")
        else:
            print('You have no book to return...')
    print('\n')


#ADD a new book
def addbook(): 
  print('Fill in the following details carefully to add a book.')
  print('\n') 
  bno=int((stock.index[-1])[-2:])+1
  bid='b'+str(bno)
  print('The book ID is ',bid)
  cts=1
  while cts==1: 
    print('The genres accepted are Non Fiction, Fiction, Biographies, Science Fiction, Subject related')
    genre=input('Genre of the book: ').title()
    if genre not in ['Non Fiction','Fiction','Biographies','Science Fiction','Subject related']:
        print('The typed genre is not available.')
        print('\n')
        cts=int(input('Do you want to retype? (yes=1/no=0) :'))
    else:
        break
  if cts!=1:
      print('\n')
      menu()
  else: 
    bname=input('Book Name: ')
    author=input('Author: ')
    pyear=int(input('Published year: '))
    publisher=input('Publisher: ')
    edition=input('Edition: ') 
    stock.loc[bid]=[genre,bname,author,pyear,publisher,edition]
    stock.to_csv(r"C:\Users\HP\Desktop\library mangement\bookstock.csv")
    print('\n') 
    print('The Book has been added successfully!')


#REGISTER as a new library member
def studentregister():
    print('\n')
    print('Please fill in your STUDENT DETAILS to start new...!')
    print('\n')
    if len(stuinfo.index)==0:
        s=0
    else:
        s=int(stuinfo.index[-1])
    sid=s+1 
    name=input('NAME: ')
    cls=int(input('CLASS: '))
    sec=input('SECTION: ')
    p=False
    while p==False:
        pno=int(input('PHONE NUMBER: '))
        if len(str(pno))==10:
            p=True
        else:
            print('Please enter an appropriate contact number.')
    email=input('EMAIL: ') 
    stuinfo.loc[sid]=[name.capitalize(),cls,sec.upper(),pno,email]
    stuinfo.to_csv(r"C:\Users\HP\Desktop\library mangement\stuinfo.csv")
    print('\n')
    print('Your STUDENT ID is ',sid,'\n','Please remember your student id!!')
 


#VIEW all members of library
def members():
    print(stuinfo[['name','class','section']].rename(columns={'name':'NAME','class':'CLASS','section':'SECTION'}))
    print('\n')

    
#VIEW particular member details
def mdetails():
    cts=1
    while cts==1:
        members() 
        sid=int(input('Enter the Student ID to view details: '))
        print('\n')
        if sid in stuinfo.index:
            print('STUDENT ID (sid) : ',sid,'\n',
                  'STUDENT NAME     : ',stuinfo.loc[sid,'name'],'\n',
                  'CLASS            : ',stuinfo.loc[sid,'class'],'\n',
                  'SECTION          : ',stuinfo.loc[sid,'section'],'\n',
                  'PHONE NUMBER     : ',stuinfo.loc[sid,'pno'],'\n',
                  'EMAIL ID         : ',stuinfo.loc[sid,'email'])
            print('\n')
        else:
            print('The given STUDENT ID (sid) is not found! (check the entered id)')
        print('\n') 
        cts=int(input('Do you want to continue? (yes=1/no=0): '))

# MENU
def menu():
    print('\n') 
    print('-'*100)
    print('\n')
    
    print('''THE LIBRARY SERVICES AVAILABLE:

(1)  - VIEW BOOK STOCK with count details
(2)  - VIEW books GENRE wise
(3)  - VIEW particular book details 
(4)  - CHECK availability of book
(5)  - BORROW a book
(6)  - RETURN a book
(7)  - ADD a new book
(8)  - REGISTER as a new library member
(9)  - VIEW all members of library
(10) - VIEW particular member details
(11) - Exit''')
    
    print('\n')
    s=int(input('Enter the service code to proceed: '))
    print('-'*100)
    
    if s not in range(1,13):
        print('Please enter an appropraite service code...!')
        menu()
    else:
        if s in range(1,11):
            if s==1:  stockdetails()
            elif s==2:
                cts=1
                while cts==1:
                    bookgenre() 
                    cts=int(input('Do you want to continue? (yes=1/no=0): '))
                    print('\n')
            elif s==3:  bdetail()
            elif s==4:  availability()
            elif s==5:  borrow()
            elif s==6:  returning()
            elif s==7:  addbook()
            elif s==8:  studentregister()
            elif s==9:  members()
            else: mdetails()
            menu()
            ex=False
        elif s==11:
            ex=True
        else:
            print('PLEASE ENTER THE APPROPRIATE NUMBER !')
            ex=False
            menu()
    return ex
 
 
while ex==False:
    print('-'*100)
    print('\n')
    print('-----WELCOME TO OUR LIBRARY-----')
    print('\n')
    time.sleep(0.5)
    ex=menu()
    
print('-----THANK YOU FOR VISITING OUR LIBRARY-----')
print('*'*100)
time.sleep(10)
    
