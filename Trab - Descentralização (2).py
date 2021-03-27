#Adicionar índices na hora de criar as variáveis
# -*- coding: utf-8 -*-
from gurobipy import *

m = Model ('Decentralização')
depa = ['A','B','C','D','E']
cida = ['LON','BRIS','BRIG']

bene1 = [0,10000,10000,0,15000,20000,0,10000,15000,0,20000,15000,0,5000,15000]
 

depaloc= tuplelist([
        ('A','LON'), 
        ('A','BRIS'),
        ('A','BRIG'),
        ('B','LON') ,
        ('B','BRIS'),
        ('B','BRIG'),
        ('C','LON') ,
        ('C','BRIS'),
        ('C','BRIG'),
        ('D','LON'),
        ('D','BRIS'),
        ('D','BRIG'),
        ('E','LON'),
        ('E','BRIS'),
        ('E','BRIG'),
        ])


bene= {
        ('A','LON'):0, 
        ('A','BRIS'):10000,
        ('A','BRIG'):10000,
        ('B','LON'):0 ,
        ('B','BRIS'):15000,
        ('B','BRIG'):20000,
        ('C','LON') :0,
        ('C','BRIS'):10000,
        ('C','BRIG'):15000,
        ('D','LON'):0,
        ('D','BRIS'):20000,
        ('D','BRIG'):15000,
        ('E','LON'):0,
        ('E','BRIS'):5000,
        ('E','BRIG'):15000,
        }


custos = {('LON','LON'): 10,
          ('LON','BRIG'): 9,
          ('LON','BRIS'):13,
          ('BRIS','BRIS'):5,
          ('BRIS','BRIG'):14,
          ('BRIS','LON'):13,
          ('BRIG','BRIS'):14,
          ('BRIG','BRIG'):5,
          ('BRIG','LON'):9
          }


quantidade = {('A','A'):0,
              ('A','B'):0,
              ('A','C'):1000,
              ('A','D'):1500,
              ('A','E'):0,
              ('B','A'):0,
              ('B','B'):0,
              ('B','C'):1400,
              ('B','D'):1200,
              ('B','E'):0,
              ('C','A'):1000,
              ('C','B'):1400,
              ('C','C'):0,
              ('C','D'):0,
              ('C','E'):2000,
              ('D','A'):1500,
              ('D','B'):1200,
              ('D','C'):0,
              ('D','D'):0,
              ('D','E'):700,
              ('E','A'):0,
              ('E','B'):0,
              ('E','C'):2000,
              ('E','D'):700,
              ('E','E'):0,
        }


          
#DECLARAÇÃO DAS VARIÁVEIS#
var={}
for dep,cit in depaloc:
    var[dep,cit] = m.addVar ( vtype=GRB.BINARY, name=dep+cit)
    m.update()

#DESCOBRE O CUSTO ESPECÍFICO DA RELAÇÃO ENTRE DOIS DEPARTAMENTOS#
custos_total = []
quantidades_total =[]

for v in var:
    for x in var:
        a = v[1],x[1]
        b = v[0],x[0]
        quantidades_total.append(quantidade[b])
        custos_total.append(custos[a])

#ESCREVE A PARTE DOS CUSTOS DA FUNÇÃO OBJETIVO#
FO2 = []
i=0;
for v in m.getVars():
    for x in m.getVars():
        FO2.append(x*v*custos_total[i]*quantidades_total[i])
        i += 1

#ESCREVE A PARTE DOS BENEFÍCIOS DA FUNÇÃO OBJETIVO#
FO1=[]
j=0
for v in m.getVars():
    FO1.append(v*bene1[j])
    j += 1


   
#ESCREVE A FUNÇÃO OBJETIVO COMPLETA#
FO =  - sum(FO2)/2 + sum(FO1)


#ESCREVE A PRIMEIRA RESTRIÇÃO: CADA CIDADE SÓ PODE CONTER NO MÁX 3 DEPARTAMENTOS#
res1=sum(m.getVars()[0:3])

    
res2=sum(m.getVars()[3:6])


res3=sum(m.getVars()[6:9])


res4=sum(m.getVars()[9:12])


res5=sum(m.getVars()[12:15])


#ESCREVE A SEGUNDA RESTRIÇÃO: CADA DEPARTAMENTO SÓ PODE SER ALOCADO EM UM CIDADE#
res6= m.getVars()[0] + m.getVars()[3] + m.getVars()[6] + m.getVars()[9] + m.getVars()[12]


res7= m.getVars()[1] + m.getVars()[4] + m.getVars()[7] + m.getVars()[10] + m.getVars()[13]


res8= m.getVars()[2] + m.getVars()[5] + m.getVars()[8] + m.getVars()[11] + m.getVars()[14]

#DECLARANDO FUNÇÃO OBJETIVO#
m.setObjective(FO, GRB.MAXIMIZE)

#ADICIONANDO RESTRIÇÕES#
m.addConstr(res1 ==1,'SomaA')
m.addConstr(res2 ==1,'SomaB')
m.addConstr(res3 ==1,'SomaC')
m.addConstr(res4 ==1,'SomaD')
m.addConstr(res5 ==1,'SomaE')
m.addConstr(res6<=3,'SomaLON')
m.addConstr(res7<=3,'SomaBRIS')
m.addConstr(res8<=3,'SomaBRIG')

m.optimize()

for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)











