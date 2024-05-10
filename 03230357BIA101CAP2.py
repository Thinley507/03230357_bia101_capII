# Constants
tax_rates = {
    (0, 300000): 0,
    (300001, 400000): 0.1,
    (400001, 650000): 0.15,
    (650001, 1000000): 0.20,
    (1000001, 1500000): 0.25,
    (1500001, float('inf')): 0.30
}

bonus_rates= {
    (0, 300000): 30000,
    (300001, 400000): 40000,
    (400001, 650000): 65000,
    (650001, 1000000): 100000,
    (1000001, 1500000): 150000,
    (1500001, float('inf')): 150000
}

class Deductions:
    def __init__(self, life_insurance: int, house_loan_interest: int, house_rent: int):
        self.life_insurance = life_insurance
        self.house_loan_interest = house_loan_interest
        self.house_rent = house_rent

    def get_total_deductions(self) -> int:
        return self.life_insurance + self.house_loan_interest + self.house_rent

class EmployeeFamily:
    def __init__(self, is_married: bool, is_single: bool, is_divorce: bool, children: int):
        self.is_married = is_married
        self.is_single = is_single
        self.is_divorce = is_divorce
        self.children = children

    def get_child_education_allowance(self) -> int:
        if self.is_married or self.is_single:
            return 350000 * self.children
        else:
            return 0

class EmployeeBonus:
    def __init__(self, employee_income: int):
        self.employee_income = employee_income

    def get_bonus_amount(self) -> int:
        for min_income, max_income in bonus_rates:
            if min_income <= self.employee_income <= max_income:
                return bonus_rates[(min_income, max_income)]

class EmployeeIncome:
    def __init__(self, employee_income: int, life_insurance: int, child_education_allowance: int, rent_allowance: int, medical_allowance: int, other_allowance: int, spouse_income: int, house_loan_interest: int, house_rent: int, deductions: Deductions):
        self.employee_income = employee_income
        self.life_insurance = life_insurance
        self.child_education_allowance = child_education_allowance
        self.rent_allowance = rent_allowance
        self.medical_allowance = medical_allowance
        self.other_allowance = other_allowance
        self.spouse_income = spouse_income
        self.house_loan_interest = house_loan_interest
        self.house_rent = house_rent
        self.deductions = deductions
        
    def calculate_pit(self) -> int:
        taxable_income = self.employee_income + self.spouse_income - self.life_insurance - self.child_education_allowance - self.rent_allowance - self.medical_allowance - self.other_allowance - self.deductions.get_total_deductions()

        for min_income, max_income in tax_rates:
            if min_income <= taxable_income <= max_income:
                tax_rate = tax_rates[(min_income, max_income)]
                break

        pit = taxable_income * tax_rate
        if pit >= 1000000:
            surcharge = pit * 0.10
            pit += surcharge

        return pit

# Input and calculation
employee_name = input("Enter your name: ")
status = input("What is your marital status?(single, married or divorce): ")
children = int(input("How many of your children are enrolled in school?: "))
occupation = input("Enter your occupation: ")
income = int(input("Enter your annual income: "))
life_insurance = int(input("Enter your insurance amount: "))
bonus = int(input("Enter your bonus amount: "))
rent_allowance = int(input("Enter your rent allowance: "))
medical_allowance = int(input("Enter your medical allowance: "))
other_allowance = int(input("Enter your other allowance: "))
spouse_income = int(input("Enter your spouse's annual income: "))
house_loan_interest = int(input("Enter your house loan interest: "))
house_rent = int(input("Enter your house rent: "))

# Create objects and calculate PIT
family = EmployeeFamily(status == "married", status == "single", status == "divorce", children)
child_education_allowance = family.get_child_education_allowance()

bonus_obj = EmployeeBonus(income)
bonus_amount = bonus_obj.get_bonus_amount()

deductions = Deductions(life_insurance, house_loan_interest, house_rent)

income_obj = EmployeeIncome(income, life_insurance, child_education_allowance, rent_allowance, medical_allowance, other_allowance, spouse_income, house_loan_interest, house_rent, deductions)
pit = income_obj.calculate_pit()

print(f"{employee_name}'s Personal Income Tax (PIT) is: {pit:.2f}")