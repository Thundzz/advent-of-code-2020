def parse_input(filename):
    with open(filename) as file:
        return [int(l.strip()) for l in file.readlines()]
    
def find_expenses_firststar(expenses):
    expensesSet = set(expenses)
    for expense in expenses:
        other = 2020 - expense
        if other in expensesSet:
            return expense * other

def find_expenses_sndstar(expenses):
    expensesSet = set(expenses)
    for fstExpense in expenses:
        for sndExpense in expenses:
            rest = 2020 - fstExpense - sndExpense
            if rest in expensesSet:
                return fstExpense * sndExpense * rest

def main():
    inputs = parse_input("input.txt")
    s = find_expenses_firststar(inputs)
    print(s)
    s = find_expenses_sndstar(inputs)
    print(s)

if __name__ == '__main__':
    main()
