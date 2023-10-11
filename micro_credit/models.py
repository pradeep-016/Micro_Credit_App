from django.db import models

class LoanApplication(models.Model):
    # Define the fields for your LoanApplication model
    genders_type = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=255)
    dependents = models.IntegerField()
    education_status = models.CharField(max_length=255)
    self_employment = models.CharField(max_length=255)
    applicantIncome = models.FloatField()
    coapplicantIncome = models.FloatField()
    loan_amnt = models.FloatField()
    term_d = models.IntegerField()
    credit_history = models.IntegerField()
    property_area = models.CharField(max_length=255)

    def __str__(self):
        return f"Loan Application {self.id}"
