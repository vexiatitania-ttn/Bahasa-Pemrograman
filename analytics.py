"""Kelas OOP untuk analisis kesehatan finansial."""

class BaseFinance:
    """Base Class (Parent) - Mendemonstrasikan Inheritance"""
    def __init__(self, user_id):
        self.user_id = user_id

class FinancialAnalyzer(BaseFinance):
    """Child Class - Menginherit BaseFinance"""
    def __init__(self, user_id):
        super().__init__(user_id)

    def evaluate_health(self, income: float, expense: float) -> str:
        """Encapsulation: Menyembunyikan logika perhitungan kesehatan finansial"""
        if income == 0 and expense == 0: return "Netral (Belum ada data)"
        if income == 0 and expense > 0: return "Defisit ⚠️"
        saving_ratio = (income - expense) / income
        if saving_ratio >= 0.2: return "Sangat Baik 🌟"
        elif saving_ratio >= 0.1: return "Baik 👍"
        elif saving_ratio >= 0: return "Cukup 👌"
        else: return "Buruk ⚠️"

    def calculate_savings_ratio(self, income: float, expense: float) -> int:
        """Encapsulation: Menghitung persentase rasio tabungan"""
        return max(0, int(((income - expense) / income * 100)) if income > 0 else 0)
