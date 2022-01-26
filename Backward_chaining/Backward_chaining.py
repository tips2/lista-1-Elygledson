import re
from pickle import FALSE, TRUE


class Rules:
    def __init__(self,antecedent,consequent):
        self.antecedent = antecedent
        self.consequent = consequent
  
    @staticmethod
    def formattingExpress(list):
       try:
          while True:
           list.remove('')
       except ValueError:
            pass
       return list


class Bacward_chaining:
    facts = []
    rules = []
    conflicts = []
    def __init__(self, file_name,initial_data):
        self.fileName = file_name
        self.goal = initial_data
        
        
    def getIndex(self,item):
        for i,r in enumerate(self.rules):
            if item == r.consequent[0]:
                return i
        return -1
    
    def setRules(self):
        print('Conhecendo a base de conhecimento...')
        with open(self.fileName) as file: 
            rules = file.readlines()
            for r in rules:
                predicate = r.split('->')
                antecedent = Rules.formattingExpress(re.split(r'\&|\s',predicate[0]))
                consequent = Rules.formattingExpress(re.split(r'\&|\s',predicate[1]))
                new_rule = Rules([antecedent],[consequent])
                idx = self.getIndex(new_rule.consequent[0])
                if idx != -1:
                    self.rules[idx].antecedent.extend(new_rule.antecedent)
                else:
                    self.rules.append(new_rule) 
            self.facts = input('Digite os fatos:\n').upper().split(' ')
             
  
    def displayRules(self):
        for i,r in enumerate(self.rules):
            print(f' regra {i}: {r.antecedent} -> {r.consequent}')
      
    # Remove as regras falsas
    def getknowledge(self,idx):
        antecedent = self.rules[idx].antecedent.copy()
        for i,rules in enumerate(self.rules[idx].antecedent):
            for rule in rules:
                isValid = self.getIndex([rule])
                if isValid == -1 and rule not in self.facts:
                    removed = antecedent.pop(i)
                    print(f'regra removida {removed}')
        
        self.rules[idx].antecedent = antecedent
        

    def dfs(self,idx):
        notActivated = [idx]
        self.conflicts.append(self.rules[idx].consequent[0])
        while notActivated:
            notActivated.sort()
            active = notActivated.pop(0)
            self.getknowledge(active)
            if len(self.rules[active].antecedent) == 0:
                print('O objetivo é falso')
                break
            rule = self.rules[active].antecedent.pop(0)
            print(f'regras ativadas {active}')
            print(f'Memória de trabalho {rule}')
            for r in rule:
                if r not in self.conflicts:
                     num = self.getIndex([r])
                     self.conflicts.append([r])
                     if num != -1:
                        notActivated.append(num)
              
    
    def derivedRules(self):
        print(self.conflicts)



run = input('Digite o objetivo da operação:\n').upper()
window = Bacward_chaining('Backward_chaining/baseToBackward.txt',run)
window.setRules()
window.displayRules()
window.dfs(window.getIndex([run]))
window.derivedRules()


