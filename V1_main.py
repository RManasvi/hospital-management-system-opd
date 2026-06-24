#CONNECTIVITY

import mysql.connector

#CREATING DATABASE

'''
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE hospital")

'''
#CREATING TABLES
mydb = mysql.connector.connect(
  host="localhost",
  user="Manasvi",
  password="manasvi",
  database="hospital"
)

mycursor = mydb.cursor()
'''
mycursor.execute("CREATE TABLE doctors (id_doctor INT not null AUTO_INCREMENT PRIMARY KEY, name_doc VARCHAR(255), age_doc integer(5),qualifications VARCHAR(50), department VARCHAR(50), Years_Of_Experience integer(5), charges integer(5))")
ID = "ALTER TABLE doctors AUTO_INCREMENT=1"

mycursor.execute("CREATE TABLE patients (id_patients INT not null AUTO_INCREMENT PRIMARY KEY, DateofVisit date,  name_patients VARCHAR(255), age integer(5),address VARCHAR(255),gender VARCHAR(255),Phone_number VARCHAR(10),blood_group VARCHAR(25),height integer(5),weight integer(5),Blood_Pressure VARCHAR(25),allergy VARCHAR(2) ,allergic_medicine VARCHAR(255),current_prob VARCHAR(255),doctor_id integer(5),foreign key(doctor_id) references doctors(id_doctor))")
ID = "ALTER TABLE patients AUTO_INCREMENT=1"

'''


mycursor.execute("create table if not exists users\
                 (username varchar(30) primary key,\
                  password varchar(30) default'000')")




#USER DEFINED FUNCTIONS
def sign_up():
    print("""

            ============================================
                       Please enter new user details
            ============================================
                                                """)
    u=input("Enter New User Name!!:")
    p=input("Enter password (Combination of Letters, Digits etc.):")
    mycursor.execute("insert into users values('"+u+"','"+p+"')")
    mydb.commit()
    print("""
        ========================================================
                       New user created successfully! 
        ========================================================
                                            """)
def pref():
                  return("""Choose your preference:
                                       1. login as: Admin
                                       2. login as: Patient
                                       3. login as: Doctor
                                       4. Exit
                                
                                                        """)
#============================================================================================================================================
#DOCTOR FUNC
#DELETE DOCTOR RECORD
def delete_rec():
    try:
        mycursor = mydb.cursor()
        id_doctor=int(input("enter the unique ID: "))
        delete="delete from doctors where id_doctor={}".format(id_doctor)
        mycursor.execute(delete)
        mydb.commit()

        if mycursor.rowcount>0:
            print("record deleted successfully")
        else:
            print("Incorrect ID")
    except Exception:
        print("The record can't be deleted as it is linked with patients table")
        
#MODIFY DOCTOR       
def modify_doc():
    mycursor = mydb.cursor()
    print('''enter the field which you want to change:-
            1. charges of doctors
            2. age of doctor 
            3. Years Of Experience of doctor
            4. Name of doctor''')

    print("\n")
    choice_modi=int(input("Enter your choice: "))
    id_doctor=int(input("Enter the doctor id: "))
    
    if choice_modi==1:
                    charges=int(input("Enter the new salary of doctor: "))
                    sql="update doctors set charges=%s where id_doctor=%s"
                    mycursor.execute(sql,(charges,id_doctor))
                    sql="select id_doctor, name_doc , age_doc ,qualifications , department , Years_Of_Experience, charges"
                    mydb.commit()
                    if mycursor.rowcount>0:
                        print("updated record ID: ",id_doctor)
                        print("successfully updated!!")
                    else:
                        print("Incorrect ID")
                    

                        
                        
    elif choice_modi==2:
                   
                    age_doc=int(input("Enter the new the age of doctor: "))
                    l_doc=[]
                    l_doc.append(age_doc)
                    l_doc.append(id_doctor)
                    t=tuple(l_doc)
                    update="UPDATE doctors SET age_doc=%s WHERE   id_doctor=%s"
                    mycursor.execute(update,t)
                    mydb.commit()
                    if mycursor.rowcount>0:
                           print("updated record ID: ",  id_doctor)
                           print("successfully updated!!")
                    else:
                           print("Incorrect ID")

                       
                        
    elif choice_modi==3:
                   Years_Of_Experience=int(input("Enter the Years Of Experienceof doctor: "))
                   sql="update doctors set Years_Of_Experience=%s where id_doctor=%s"
                   mycursor.execute(sql,(Years_Of_Experience,id_doctor))
                   sql="select id_doctor, name_doc , age_doc ,qualifications , department , Years_Of_Experience, charges"
                   mydb.commit()
                   if mycursor.rowcount>0:
                       print("updated record ID: ",id_doctor)
                       print("successfully updated!!")
                   else:
                       print("Incorrect ID")


    elif choice_modi==4:
                   name_doc=input("Enter the name_doc of doctor: ")
                   sql="update doctors set name_doc=%s where id_doctor=%s"
                   mycursor.execute(sql,(name_doc,id_doctor))
                   sql="select id_doctor, name_doc , age_doc ,qualifications , department , Years_Of_Experience, charges"
                   mydb.commit()
                   if mycursor.rowcount>0:
                       print("updated record ID: ",id_doctor)
                       print("successfully updated!!")
                   else:
                       print("Incorrect ID")
                       
#INSERT DOCTOR    
def new_doctor():
    try:
          lst = []
          no_of_rcd =int(input("enter the number of records: "))
          if no_of_rcd<=0:
              print("enter valid number")
          else:
              for i in range(0,no_of_rcd):
                    name_doc=input("enter the name: ")
                    age_doc=int(input("enter the age"))
                    qualifications=str(input("enter the qualifications: "))
                    department=str(input("enter the department: "))
                    Years_Of_Experience =int(input("enter the years of experience: "))
                    charges=int(input("enter the doctor fee"))
                    lst.append(name_doc) 
                    lst.append(age_doc)
                    lst.append(qualifications)
                    lst.append(department)
                    lst.append(Years_Of_Experience)
                    lst.append(charges)
                    tup1=tuple(lst) 
                    print(tup1) 
                    mycursor=mydb.cursor()
                    insert_doc="insert into doctors(name_doc,age_doc,qualifications,department,Years_Of_Experience,charges) values('{}','{}','{}','{}','{}','{}')". format(name_doc, age_doc,qualifications,department, Years_Of_Experience , charges)
                    mycursor.execute(insert_doc)
                    a= mydb.commit()
                    print("Record created successfully!!")
              return a
    except Exception:
        print("enter valid value")

       
#PRINT THE LIST OF DOCTORS
def show_doctor_lst():
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM hospital.doctors")
            myresult = mycursor.fetchall()
            for x in myresult:
                  print(x)
            return x
              
#SEARCH DOCTOR
def search_doc():
              ID=int(input("enter the unique id: "))
              ID_tupl=(ID,)
              search_data= 'select * from doctors where id_doctor =%s'
              mycursor = mydb.cursor()
              my_cursor=mycursor.execute(search_data,ID_tupl)
              record = mycursor.fetchone()
              print(record)
#====================================================================================================================================
#PATIENT FUNC
#DELETE PATIENT RECORD
def del_rec():
    mycursor = mydb.cursor()
    id_patients=int(input("enter the unique id: "))
    del_patient="DELETE FROM hospital.patients WHERE id_patients= {}".format(id_patients)
    mycursor.execute(del_patient)
    mydb.commit()
    if mycursor.rowcount>0:
        print("record deleted successfully")
    else:
        print("Incorrect ID")
        

#SEARCH PATIENTS
def search_patient():
   p=1
   for i in range (p):
        print(''' search patients by
                1. unique id
                2. date
                ''')
        response=int(input("enter your choice: "))
        if response==1:
              id_patients=int(input("enter the unique id: "))
              ID_tup1=(id_patients,)
              search_data_P= 'select * from patients where id_patients=%s'
              mycursor = mydb.cursor()
              my_cursor=mycursor.execute(search_data_P,ID_tup1)
              rec = mycursor.fetchone()
              if mycursor.rowcount>0:
                       print(rec)
              else:
                       print("Incorrect Input")
                       p=2
                       break
        elif response==2:
             DateOfVisit=input("enter the date(YYYY-MM-DD): ")
             D_tup1=(DateOfVisit,)
             search_data_P= 'select * from patients where DateOfVisit=%s'
             mycursor = mydb.cursor()
             my_cursor=mycursor.execute(search_data_P,D_tup1)
             rec = mycursor.fetchall()
             print("the following patients visited on", DateOfVisit)
             print("*************************************")
             for i in rec:
                   print("\n")
                   print(i)
             if mycursor.rowcount>0:
                       print("************************************")
             else:
                       print("Incorrect Input")
                       p=2
                       break
            
        else:
             print("invalid response")
             response1=input("Do you wish to continue? (y/n)")
             response2=response1.lower()
             if response2=='n':
                   p=2
                   break
                  
        
    
                  
 #INSERT PATIENT      
def new_patient():
        lst = []
        no_of_rcd =int(input("enter the number of records: "))
        for i in range(0,no_of_rcd):
            DateofVisit=input("enter Date of Visit (YYYY-MM-DD)")
            name_patients=input("enter the Patient's name: ")
            age=int(input("enter the age: "))
            address=str(input("enter the address: "))
            gender=str(input("enter your gender: "))

            mycursor = mydb.cursor()
            print('\n')
            print("================================================================================")
            print("SELECT THE DOCTOR YOU WANT APPOINMENT WITH")
            print("THE LIST OF DOCTORS ARE:- ")
            mycursor=mydb.cursor()
            mycursor.execute("SELECT id_doctor,name_doc,qualifications ,department,charges FROM hospital.doctors")
            myresult = mycursor.fetchall()
            for rcd in myresult:
              print(rcd)
            print("================================================================================")
            print('\n')


            
            doctor_id =int(input("enter the doctor id: "))
            Phone_Number = input("Please enter a 10 digit mobile number: ")
            if len(Phone_Number) > 10 or len(Phone_Number) < 10:
                print("Number is not valid")
                
            else:
                Blood_Group=str(input("enter your blood group: "))
                height=float(input("enter your height(in CM): "))
                weight=float(input("enter your weight(in KG): "))
                Blood_Pressure=str(input("enter your BP: "))
                current_prob=input("enter your problem you are going through: ")
                allergy=input("are you allergic to any medicine Y/N: ")
                if allergy=='Y' or allergy=='y' :
                    allergic_medicine=input("Name the medicine: ")
                    lst.append(DateofVisit)
                    lst.append(name_patients) 
                    lst.append(age)
                    lst.append(address)
                    lst.append(gender)
                    lst.append(Phone_Number)
                    lst.append(Blood_Group)
                    lst.append(height)
                    lst.append(weight)
                    lst.append(Blood_Pressure)
                    lst.append(allergy)
                    lst.append(allergic_medicine)
                    lst.append(current_prob)
                    lst.append(doctor_id)
                    tup=tuple(lst) 
                    print(tup) 
                    mycursor=mydb.cursor()
                    insert_p="insert into patients(DateofVisit, name_patients, age,address,gender,Phone_Number,Blood_Group,height,weight,Blood_Pressure,allergy,allergic_medicine,current_prob,doctor_id) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". format(DateofVisit,name_patients, age,address,gender,Phone_Number,Blood_Group,height,weight,Blood_Pressure,allergy,allergic_medicine,current_prob,doctor_id)
                    mycursor.execute(insert_p)
                    mydb.commit()
                    print("Record created successfully!!")
                    
                else:
                    lst.append(DateofVisit)
                    lst.append(name_patients) 
                    lst.append(age)
                    lst.append(address)
                    lst.append(gender)
                    lst.append(doctor_id)
                    lst.append(Phone_Number)
                    lst.append(Blood_Group)
                    lst.append(height)
                    lst.append(weight)
                    lst.append(Blood_Pressure)
                    lst.append(allergy)
                    lst.append(current_prob)
                    lst.append(doctor_id)
                    tup=tuple(lst) 
                    print(tup) 
                    mycursor=mydb.cursor()
                    insert_p="insert into patients(DateofVisit,name_patients, age,address,gender,Phone_Number,Blood_Group,height,weight,Blood_Pressure,allergy,current_prob,doctor_id) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". format(DateofVisit,name_patients, age,address,gender,Phone_Number,Blood_Group,height,weight,Blood_Pressure,allergy,current_prob,doctor_id)
                    mycursor.execute(insert_p)
                    mydb.commit()
                    print("Record created successfully!!")



#PRINT THE LIST OF PATIENTS
def show_patients_lst():
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM hospital.patients")
        result = mycursor.fetchall()
        for i in result:
          print(i)

          
#MODIFY PATIENT
def modify_patients():
   try:
          mycursor=mydb.cursor()
          print('''enter the field which you want to change:-
            1. age of patient
            2. name of patient
            3. Problem
            4. Date of Appoinment
            ''')
          

          print("\n")
          choice_Patient=int(input("Enter your choice: "))
          if choice_Patient>0 and choice_Patient<5:
           
                      id_patients=int(input('enter patient id : '))
                      if choice_Patient==1:
                                age=int(input("enter the age:"))
                                mycursor.execute("UPDATE patients SET age={} WHERE id_patients='{}'".format(age,id_patients))
                                mydb.commit()
                                if mycursor.rowcount>0:
                                       print("updated record ID: ",id_patients)
                                       print("successfully updated!!")
                                else:
                                       print("Incorrect ID")
                    
                      elif choice_Patient==2:                  
                                 name_patients=input('Enter the new name:  ')
                                 l=[]
                                 l.append(name_patients)
                                 l.append(id_patients)
                                 tpl=tuple(l)
                                 update_name="UPDATE patients SET name_patients=%s WHERE id_patients=%s"
                                 mycursor.execute(update_name,tpl)
                                 mydb.commit()
                                 if mycursor.rowcount>0:
                                        print("successfully updated!!")
                                 else:
                                       print("Incorrect ID")

                      elif choice_Patient==3:
                          current_prob=input('Enter the new problem:  ')
                          sql="update patients SET current_prob=%s WHERE id_patients=%s"
                          mycursor.execute(sql,(current_prob,id_patients))
                          sql="select * from patients"
                          mydb.commit()
                          if mycursor.rowcount>0:
                              print("updated record ID: ",id_patients)
                              print("successfully updated!!")
                          else:
                              print("Incorrect ID")
                              
                      elif choice_Patient==4:
                          DateOfVisit=input('Enter the new date(YYYY-MM-DD):  ')
                          sql="update patients SET DateOfVisit=%s WHERE id_patients=%s"
                          mycursor.execute(sql,(DateOfVisit,id_patients))
                          sql="select * from patients"
                          mydb.commit()
                          if mycursor.rowcount>0:
                              print("updated record ID: ",id_patients)
                              print("successfully updated!!")
                          else:
                              print("Incorrect ID")
          else:
                print("invalid number")

                              
   except Exception:
         print("invalid input")
         
   
#RECEIPT       
def Receipt():
      try:         
               id_patients=int(input("enter the unique id: "))
               query="SELECT patients.id_patients,patients.DateofVisit,patients.name_patients, patients.address,patients.gender,patients.current_prob,doctors.id_doctor,doctors.name_doc,doctors.charges FROM patients, doctors WHERE doctor_id = id_doctor"
               mycursor.execute(query)
               rows=mycursor.fetchall()
               for x in rows:
                     if x[0]==id_patients:
                           print("================================================================================")
                           print("                                                     YOUR APPOINMENT RECEIPT ")
                           print("\n")
                           print("Patient ID:    ", x[0])
                           print("DateofVisit:   ",x[1])
                           print("Patient Name:   ", x[2])
                           print("Address:   ",x[3])
                           print("Gender:   ", x[4])
                           print("Problem:   ",x[5])
                           print("Doctor id:   ", x[6])
                           print("Doctor Name:   ",x[7])
                           print("Doctor Charges:   ",x[8])
                           print("Your appoinment has been confirmed!!!!")
                           print("================================================================================")
                           break
               else:
                     print("Please enter the valid ID")
      
      except Exception:
            print("Please enter the valid ID")
#==============================================================================================================
#DOCTOR APPOINMENT
def doc_appoinment():
      try:
            n=1
            while n==1:
                    print(''' search patients by
                  1. List all the appoinments
                  2. List appoinments for particular date
                  ''')
                    response=int(input("enter your choice: "))
                    if response==1 or response ==2:
                                doctor_id=int(input("enter the unique id of doctor: "))

                                if response==1:
                                                  ID_tup1=(doctor_id,)
                                                  search_data_P= 'select  DateofVisit,name_patients,age,weight ,Blood_Pressure, current_prob from patients where doctor_id=%s order by  DateofVisit'
                                                  mycursor = mydb.cursor()
                                                  my_cursor=mycursor.execute(search_data_P,ID_tup1)
                                                  rec = mycursor.fetchall()
                                                  print("DateofVisit| name of patients | age |  weight | Blood Pressure | current problem  |  ")
                                                  print("*************************************************************************")                                      
                                                  for x in rec:
                                                               print("\n")
                                                               print( x[0],'|', end=" ")
                                                               print(x[1],'|',end=" ")
                                                               print(x[2],'|', end=" ")
                                                               print(x[3],'|',end=" ")
                                                               print(x[4],'|', end=" ")
                                                               print( x[5],'|',end=" ")
                                                             
                                                  print("\n*************************************************************************")            
                                                  print("\n")
                                                  response1=input("Do you wish to continue?(y/n) ")
                                                  response2=response1.lower()
                                                  if response2=='n':
                                                           n=2
                                                           break
                                                      
                                elif response==2:
                                      DateofVisit=input("Enter the date(YYY-MM-DD): ")
                                      ID_tup1=(doctor_id,DateofVisit)
                                      search_data_P= 'select name_patients,age,weight ,Blood_Pressure, current_prob from patients where doctor_id=%s and DateofVisit=%s '
                                      print(" name of patients | age |  weight | Blood Pressure | current problem  |")
                                      print("*************************************************************************")      
                                      mycursor = mydb.cursor()
                                      my_cursor=mycursor.execute(search_data_P,ID_tup1)
                                      rec = mycursor.fetchall()
                                      
                                      for x in rec:
                                                               print("\n")
                                                               print( x[0],'|', end=" ")
                                                               print(x[1],'|',end=" ")
                                                               print(x[2],'|', end=" ")
                                                               print(x[3],'|',end=" ")
                                                               print(x[4],'|', end=" ")
                                                             
                                      print("\n*************************************************************************")           
                                      response1=input("Do you wish to continue?(y/n) ")
                                      response2=response1.lower()
                                      if response2=='n':
                                                           n=2
                                                           break
                    else:
                          print("Enter valid number")

                               
                                                          
      except Exception:
            print("please enter valid input")
            

        






#====================================================================================================================================
def login():
      try:
            print("""
                ==========================================================
                                     HOSPITAL MANAGEMENT SYSTEM (OPD)
                ===========================================================
                                                    """)
            print(pref())
            choice=int(input('Enter your choice'))
            if choice==4 or choice>4 or choice<=0:
                                 print("Thank you!  Have nice Day!")
            else:
                                                  
                        un=input("Username:")
                        ps=input("Password:")
                        pid=0
                        mycursor.execute("select password from users where username='"+un+"'")
                        rec=mycursor.fetchall()
                        if mycursor.rowcount>0:
                                                for i in rec:
                                                    a=list(i)
                                                    if a[0]==str(ps):
                                                          q=1
                                                          while q==1:
                                                                #Menu for Administrative Tasks
                                                                print("\n")
                                                                n=1
                                                                while q==1:
                                                                      print('\nConnection Successful!!!!')
                                                                      #ADMIN
                                                                      if choice==1:
                                                                            print("Enter your preference")
                                                                            print('\n')
                                                                            print("1. Doctors details \n2. Patient details")
                                                                            print('\n')
                                                                            ans=int(input('enter the option number'))
                                                                            if ans== 1:
                                                                                  while q==1:
                                                                                                  print('\n')
                                                                                                  print("Choose one of the following")
                                                                                                  print('''
                                                                                                    1. Add new doctor in the list
                                                                                                    2. Show details of all doctors
                                                                                                    3. Edit the details
                                                                                                    4. Delete a list
                                                                                                    5. search
                                                                                                    ''')
                                                                                                  a=int(input('enter the option number'))
                                                                                                  if a== 1:
                                                                                                        new_doctor()
                                                                                                  elif a==2:
                                                                                                        show_doctor_lst()
                                                                                                  elif a==3:
                                                                                                        modify_doc()
                                                                                                  elif a==4:
                                                                                                        delete_rec()
                                                                                                  elif a==5:
                                                                                                        search_doc()
                                                                                                  else:
                                                                                                      print("enter the valid number")
                                                                                                  z=1    
                                                                                                  for i in range(z):   
                                                                                                        print("Do your wish to continue?")
                                                                                                        response=input("enter your response.(y/n)")
                                                                                                        if response=='n':
                                                                                                              q=2
                                                                                                              print("thank you")
                                                                                                              break
                                                                                              
                                                                            elif ans==2:
                                                                                  while True:
                                                                                                  print('\n')
                                                                                                  print("Choose one of the following")
                                                                                                  print('''
                                                                                            1. Add new patient in the list
                                                                                            2. Show details of all patient
                                                                                            3. Edit the details
                                                                                            4. Delete a list
                                                                                            5. search
                                                                                            ''')
                                                                                                  a1=int(input('enter the option number'))
                                                                                                  if a1== 1:
                                                                                                      print("\n")
                                                                                                      new_patient()
                                                                                                  elif a1==2:
                                                                                                      print("\n")
                                                                                                      show_patients_lst()
                                                                                                  elif a1==3:
                                                                                                      print("\n") 
                                                                                                      modify_patients()
                                                                                                  elif a1==4:
                                                                                                      print("\n")
                                                                                                      del_rec()
                                                                                                  elif a1==5:
                                                                                                      print("\n")  
                                                                                                      search_patient()
                                                                                                  else:
                                                                                                      print("enter the valid number")
                                                                                                  print("Do your wish to continue?")
                                                                                                  response=input("enter your response.(y/n)")
                                                                                                  if response=='n':
                                                                                                              q=2
                                                                                                              print("thank you")
                                                                                                              break           
                                                                            
                                                                      elif choice==2:
                                                                                  while q==1:
                                                                                      print("""
                                                                                            1. Fix an appoinment
                                                                                            2. Edit your account infomation
                                                                                            3. Cancel your appoinment
                                                                                            4. Show receipt""")
                                                                                      c=int(input("enter your choice: "))
                                                                                      if c==1:
                                                                                          print("\n")  
                                                                                          new_patient()
                                                                                      elif c==2:
                                                                                          print("\n")
                                                                                          modify_patients()
                                                                                      elif c==3:
                                                                                          print("\n") 
                                                                                          del_rec()
                                                                                      elif c==4:
                                                                                          print("\n")  
                                                                                          Receipt()
                                                                                      else:
                                                                                             print("please enter the valid number")
                                                                                      
                                                                                      response=input("enter your response.(y/n)")
                                                                                      if response=='n':
                                                                                                              q=2
                                                                                                              print("thank you")
                                                                                                              break   
                                                                                      else:
                                                                                            print("enter valid number")
                                                                                             
                                                                      elif choice==3:
                                                                                      print("\n")
                                                                                      doc_appoinment()
                                                                                      q=2
                                                                                      print("thank you")
                                                                                      break         
                                                                                      
                        else:
                              print("INCORRECT ID/PASSWORD")
                                                   
                                                                                                                                                

                                          
      except Exception:
            print("invalid")


#===========================================================================================================================================
#MAIN MENU
def main():
      try:
            print("""
                      ==========================================================
                                            HOSPITAL MANAGEMENT SYSTEM (OPD)
                      ===========================================================
                                                          """)
            while True:
                  print("""Choose your preference:
                     1. sign up (New user)
                     2. login (Existing user)
                     3. Exit""")
                  ch=int(input("enter your choice: "))
                  if ch==1:
                        sign_up()
                        
                  elif ch==2:
                        login()
                  elif ch==3:
                        print("Thank You")
                  break
      except Exception:
            print("enter valid input")

if __name__=="__main__":
    main()

            
