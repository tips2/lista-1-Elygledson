from pickle import TRUE
import re


class Rules:
    def __init__(self,antencedent,consequent,flag):
        self.antecedent = antencedent
        self.consequent = consequent
        self.activatedRule = flag
        
    @staticmethod
    def formattingExpress(list):
       try:
          while True:
           list.remove('')
       except ValueError:
            pass
       return list


class Forward_chaining:
    facts = []
    rules = []
    conflicts = []
    def __init__(self, file_name):
        self.fileName = file_name

    def setRules(self):
        print('Conhecendo a base de conhecimento...')
        with open(self.fileName) as file: 
            rules = file.readlines()
            for r in rules:
                predicate = r.split('->')
                predicate[0]= Rules.formattingExpress(re.split(r'\&|\s',predicate[0]))
                predicate[1] = Rules.formattingExpress(re.split(r'\&|\s',predicate[1]))
                new_rule = Rules(predicate[0],predicate[1],False)
                self.rules.append(new_rule)
        info = input('Digite os fatos:\n').upper().split(' ')
        self.facts = info.copy()

    def displayRules(self):
        for i,r in enumerate(self.rules):
            print(f' regra {i}: {r.antecedent} -> {r.consequent}')

    def executeChaining(self):
        for i , r in enumerate(self.rules):
            count = 0
            for j in range(len(r.antecedent)):
                if r.antecedent[j] in self.facts:
                    count+=1
            
            if count == len(r.antecedent) and r.activatedRule != TRUE:
                print(f'r{i + 1}: adicionada na lista de conflitos e consequente adicionado {r.consequent}')
                self.conflicts.append(i + 1)
                self.facts.append(r.consequent[0])
                r.activatedRule = TRUE
                print('Memória de trabalho: ',self.facts)
                print('Regras ativadas',self.conflicts)
                self.executeChaining()
            



window = Forward_chaining('Forward_chaining/baseToForward.txt')
print('Encadeamento para frente')
window.setRules()
window.displayRules()
print('Exibindo processo de busca:')
window.executeChaining()