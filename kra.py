class Payroll:
    gross_salary = 0
    nssf_var = 0
    taxable_pay=0
    paye = 0
    nhif = 0
    deductions = 0
    net_salary = 0

    def __init__(self,basic, benefits):
         self.gross_salary = basic+benefits
         self.nssf()
         self.taxable_pay()
         self.paye()
         self.nhif()
         self.deductions()
         self.net_salary()

    def nssf(self):
        if self.gross_salary> 0 and self.gross_salary <= 17999:
         self.nssf_var = 0.06*self.gross_salary
        else:
         self.nssf_var = 1080

    def taxable_pay(self):
         self.taxable_pay = self.gross_salary-self.nssf_var
         
    
    def paye(self):
        paye = 0
        if self.taxable_pay <= 24000:
         self.paye = self.taxable_pay*0.1

        elif self.taxable_pay >= 24001 and self.taxable_pay < 32333:
         self.paye = ((self.taxable_pay-2400)*0.25)+2400

        else:
         self.paye = (self.taxable_pay-(24000+8332))*0.3+2400+2083
        

    def nhif(self):
      if self.taxable_pay < 6000:
       self.nhif = 150
       
      elif self.taxable_pay >= 6000 and self.taxable_pay <8000:
       self.nhif = 300
       
      elif self.taxable_pay >= 8000 and self.taxable_pay < 12000:
       self.nhif = 400

      elif self.taxable_pay >= 12000 and self.taxable_pay < 15000:
       self.nhif = 500

      elif self.taxable_pay >= 15000 and self.taxable_pay < 20000:
       self.nhif = 600

      elif self.taxable_pay >= 20000 and self.taxable_pay < 25000:
       self.nhif = 750

      elif self.taxable_pay >= 25000 and self.taxable_pay < 30000:
       self.nhif = 850

      elif self.taxable_pay >= 30000 and self.taxable_pay < 35000:
       self.nhif = 900

      elif self.taxable_pay >= 35000 and self.taxable_pay < 40000:
       self.nhif = 950

      elif self.taxable_pay >= 40000 and self.taxable_pay < 45000:
       self.nhif = 1000
    
      elif self.taxable_pay >= 45000 and self.taxable_pay < 50000:
       self.nhif = 1100
       
      elif self.taxable_pay >= 50000 and self.taxable_pay < 60000:
       self.nhif = 1200

      elif self.taxable_pay >= 60000 and self.taxable_pay < 70000:
       self.nhif = 1300
 
      elif self.taxable_pay >= 70000 and self.taxable_pay < 80000:
       self.nhif = 1400

      elif self.taxable_pay >= 80000 and self.taxable_pay < 90000:
       self.nhif = 1500

      elif self.taxable_pay >= 90000 and self.taxable_pay < 100000:
       self.nhif = 1600

      else:
        self.nhif = 1700
        

    def deductions(self):
      self.deductions=self.paye+self.nhif
      
    def net_salary(self):
     self.net_salary=self.taxable_pay-self.deductions



   