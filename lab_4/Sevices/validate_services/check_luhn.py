from .check_base import Checker

class LuhnCheck(Checker):
    """
    Service for checking the input card number using the Luna algorithm
    """

    def check(self, card_number: str) -> bool:
        """
        Running the algorithm

        Args:
            card_number (str): Tcard number being verified
        Returns:
            is valide value (bool)
        """
        card_number = card_number.replace(" ", "")
        if not card_number.isdigit():
            return False
        sum = 0
        is_second = False
        for i in range(len(card_number) - 1, -1, -1):
            digit = int(card_number[i])
            if is_second:
                digit *= 2
                if digit > 9:
                    digit -= 9
            sum += digit
            is_second = not is_second
        return (10 - sum % 10) % 10 == int(card_number[-1])