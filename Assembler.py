# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:33:53 2021

@author: FarisAbu3ram
"""
import numpy as np
import pandas as pd

data = pd.read_excel (r'AppendixA.xlsx')
Mnemonic = pd.DataFrame(data, columns= ['Mnemonic'])
Mnemonic =np.asarray(Mnemonic)
Opcode = pd.DataFrame(data, columns= ['Opcode'])
Opcode = np.asarray(Opcode)


pass1 = np.array([])

def isTheMnemonicIsExist(x):
    exist=np.where(Mnemonic==x)
    if(len(exist[0])==0):
       return False;
    else:
        return True;

    
initialLocator=0;
pcLoc=initialLocator
currentLine=[]
errors = []
symTab=np.array([])
currantSymTab=[]
literals=np.array([])

def isTheLabelIsExist(x):
    exist=np.where(symTab==x)
    if(len(exist[0])==0):
       return False;
    else:
        return True;
def isTheLitralIsExist(x):
    exist=np.where(literals==x)
    if(len(exist[0])==0):
       return False;
    else:
        return True;
           
def star():
    exist=np.where(symTab=='*')
    if(len(exist[0])==0):
       return -1;
    else:
        return exist[0][0];
def toDecimal(x):
    x=str(x)
    value=x[::-1]
    sum=0;
    for i in range(len(value)):
        if(value[i]=='A'):
            sum+=pow(16,i)*10
        elif(value[i]=='B'):
            sum+=pow(16,i)*11
        elif (value[i]=='C'):
            sum+=pow(16,i)*12
        elif (value[i]=='D'):
            sum+=pow(16,i)*13
        elif (value[i]=='E'):
            sum+=pow(16,i)*14
        elif (value[i]=='F'):
            sum+=pow(16,i)*15
        else: 
            sum+=pow(16,i)*int(value[i])

    return sum; 


file = open("test1.asm","r");
for x in file:        
     line=x.split(' ')
     if(x[0]!='.'):
         if(line[1]=='START'):
                 initialLocator=toDecimal(line[2])
                 pcLoc= initialLocator
                 
         if(line[0]!=''):
                 
                 if(isTheLabelIsExist(line[0])):
                     print("Dublicate symbol")
                     exit
                 currantSymTab.append(line[0])
                 currantSymTab.append(hex(pcLoc)[2:].upper())
                 symTab=np.append(symTab,currantSymTab)
                 currantSymTab=[]
                 
                 currentLine.append(hex(pcLoc)[2:].upper())
                 currentLine.append(line[0])
                 currentLine.append(line[1])
                 currentLine.append(line[2])
                 pass1= np.append(pass1,currentLine);
                 currentLine=[]
                 if(isTheMnemonicIsExist(line[1])):
                     pcLoc=pcLoc+3
                     if(line[2][0]=='='):
                         literals=np.append(literals,line[2])
                     
                 elif (line[1]=="WORD"):
                      pcLoc=pcLoc+3
                 elif (line[1]=="RESW"):
                     pcLoc+=(3*int(line[2]))
                 elif (line[1]=="RESB"):
                     pcLoc+=int(line[2])
                 elif (line[1]=="BYTE"):
                  if(line[2][0]=='C'):
                      pcLoc+=len(line[2])-3
                  else:
                      pcLoc+=int((len(line[2])-3)/2)
                 elif(line[1]=='START'):
                       continue  
                 elif(line[1]=='END'):
                       pass1[len(pass1)-4]=''
                       pcLoc=pcLoc+3
                       for j in literals:
                            if(star()==-1):
                                currantSymTab.append('*')
                                currantSymTab.append(hex(pcLoc)[2:].upper())
                                symTab=np.append(symTab,currantSymTab)
                                currantSymTab=[]
                            else:
                                symTab[star()+1]=hex(pcLoc)[2:].upper();
                            currentLine.append(hex(pcLoc)[2:].upper())
                            currentLine.append('*')
                            currentLine.append(j)
                            currentLine.append('')
                            pass1= np.append(pass1,currentLine);
                            currentLine=[]
                            if(j[1]=='C'):
                                pcLoc+=len(j)-4
                            else:
                                pcLoc+=int((len(j)-4)/2)
                       literals=np.array([])  
                 else:
                     print("Invalid operations code",line[1])
                     exit
         else:
             for i in range(len(line)):
                 if(line[i]!=''):
                    if(line[i]=='LTORG'):
                        
                        currentLine.append('')
                        currentLine.append('')
                        currentLine.append("LTORG")
                        currentLine.append('')
                        pass1= np.append(pass1,currentLine);
                        currentLine=[]
                        pcLoc=pcLoc+3
                        
                        for j in literals:
                            if(star()==-1):
                                currantSymTab.append('*')
                                currantSymTab.append(hex(pcLoc)[2:].upper())
                                symTab=np.append(symTab,currantSymTab)
                                currantSymTab=[]
                            else:
                                symTab[star()+1]=hex(pcLoc)[2:].upper();
                            currentLine.append(hex(pcLoc)[2:].upper())
                            currentLine.append('*')
                            currentLine.append(j)
                            currentLine.append('')
                            pass1= np.append(pass1,currentLine);
                            currentLine=[]
                            if(j[1]=='C'):
                                pcLoc+=len(j)-4
                            else:
                                pcLoc+=int((len(j)-4)/2) 
                        literals=np.array([])       
                    else:
                        currentLine.append(hex(pcLoc)[2:].upper())
                        currentLine.append('')
                        currentLine.append(line[i])
                        currentLine.append(line[i+1])
                        pass1= np.append(pass1,currentLine);
                        currentLine=[]
                        if(isTheMnemonicIsExist(line[i])):
                            pcLoc=pcLoc+3
                            if( line[i]!="RSUB" and line[i+1][0]=='='):
                                if(not isTheLitralIsExist(line[i+1])):
                                    literals =np.append(literals,line[i+1])
                                    
                     
                        elif (line[i]=="WORD"):
                            pcLoc=pcLoc+3
                        elif (line[i]=="RESW"):
                            pcLoc+=(3*line[i+1])
                        elif (line[i]=="RESB"):
                            pcLoc+=line[i+1]
                        elif (line[i]=="BYTE"):
                            if(line[i+1][0]=='C'):
                                pcLoc+=len(line[i+1])-3
                            else:
                                pcLoc+=int((len(line[i+1])-3)/2)
                        
                        elif(line[i]=='END'):
                            pass1[len(pass1)-4]=''
                            pcLoc=pcLoc+3
                            for j in literals:
                                if(star()==-1):
                                    currantSymTab.append('*')
                                    currantSymTab.append(hex(pcLoc)[2:].upper())
                                    symTab=np.append(symTab,currantSymTab)
                                    currantSymTab=[]
                                else:
                                    symTab[star()+1]=hex(pcLoc)[2:].upper();
                                currentLine.append(hex(pcLoc)[2:].upper())
                                currentLine.append('*')
                                currentLine.append(j)
                                currentLine.append('')
                                pass1= np.append(pass1,currentLine);
                                currentLine=[]
                                if(j[1]=='C'):
                                    pcLoc+=len(j)-4
                                else:
                                    pcLoc+=(len(j)-4)/2 
                                literals=np.array([])
                        else:
                         print("Invalid operations code")
                         exit  
                    
                    break
                    
        
      
file.close(); 

print("Program's Name is: ",pass1[1] )
print("Program's Length is: ",hex(pcLoc-initialLocator)[2:].upper())  
print(pass1.reshape(-4,4))   
print(symTab.reshape(-2,2))














