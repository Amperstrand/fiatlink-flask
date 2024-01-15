from typing import List, Dict

class PaymentOption:
    def __init__(self, option: str, id: int, fee_rate: float, min_amount: int, max_amount: int):
        self.option = option
        self.id = id
        self.fee_rate = fee_rate
        self.min_amount = min_amount
        self.max_amount = max_amount
    def to_dict(self) -> dict:
        """Converts the PaymentOption instance to a dictionary."""
        return {
            "id": self.id,
            "option": self.option,
            "fee_rate": self.fee_rate,
            "min_amount": self.min_amount,
            "max_amount": self.max_amount
        }

class Currency:
    def __init__(self, currency_id: int, currency_code: str, payment_options: List[PaymentOption]):
        self.currency_id = currency_id
        self.currency_code = currency_code
        self.payment_options = payment_options
    def to_dict(self) -> dict:
        return {
            "currency_code": self.currency_code,
            "currency_id": self.currency_id,
            "payment_options": [option.to_dict() for option in self.payment_options]
        }

class CurrencyManager:
    def __init__(self):
        self.currencies = {
            "eur": Currency(1, "EUR", [
                PaymentOption(option="SEPA", id=1, fee_rate=0.005, min_amount=1, max_amount=100000),
                PaymentOption(option="SEPA Instant", id=2, fee_rate=0.01, min_amount=1, max_amount=100000),
                PaymentOption(option="Credit card", id=3, fee_rate=0.05, min_amount=25, max_amount=100000)
            ]),
            "chf": Currency(2, "CHF", [
                PaymentOption(option="Bank transfer", id=5, fee_rate=0.01, min_amount=10, max_amount=100000),
                PaymentOption(option="Credit card", id=6, fee_rate=0.05, min_amount=10, max_amount=100000)
            ])
        }

    def __call__(self, currency_code=None):
        if currency_code:
            # Return the specified currency if it exists
            return {currency_code: self.currencies[currency_code].to_dict()} if currency_code in self.currencies else None
        else:
            # Return all currencies
            return {code: currency.to_dict() for code, currency in self.currencies.items()}

    def __getitem__(self, key):
        return self.currencies[key].to_dict() if key in self.currencies else None

    def get_payment_option(self, currency_code, payment_option_id):
        if currency_code in self.currencies:
            for option in self.currencies[currency_code].payment_options:
                if option.id == payment_option_id:
                    return option
                    #return option.to_dict()
        return None

class PaymentInfo:
    # Hardcoded payment options
    _payment_options = {
        1: {
            "payment_details": {
                "provider_iban": "provider_iban string",
                "provider_name": "provider_name string",
                "provider_address": "provider_address string",
                "provider_bank": "provider_bank string",
                "provider_country": "provider_country string",
                "provider_bic": "provider_bic string"
            }
        },
        2: {
            "payment_url": "url_for_sepa instant eur"
        },
        3: {
            "payment_url": "url_to_pay_with_credit_card"
        },
        4: {
            "payment_url": "url_for_sepa instant chf"
        },
        5: {
            "payment_url": "payment_url for bank transfer payment info string",
            "payment_details": {
                "provider_accountnumber": "provider_accountnumber string",
                "provider_name": "provider_name string",
                "provider_address": "provider_address string",
                "provider_bank": "provider_bank string",
                "provider_country": "provider_country string",
                "provider_bic": "provider_bic string"
            },
        6: {
            "payment_url": "chf credit card"
        }
        }
    }

    def __init__(self, payment_option_id, payment_url=None, payment_details=None):
        self.payment_option_id = payment_option_id
        self.payment_url = payment_url
        self.payment_details = payment_details or {}

    def __repr__(self):
        return f"PaymentInfo(payment_option_id={self.payment_option_id}, payment_url={self.payment_url}, payment_details={self.payment_details})"

#    def __str__(self):
#        return (f"PaymentInfo(payment_option_id={self.payment_option_id}, "
#                f"payment_url={self.payment_url}, "
#                f"payment_details={self.payment_details})")
#

    def to_dict(self):
        #return {k: v for k, v in self.__dict__.items() if v}
        attributes = ['payment_option_id', 'payment_url', 'payment_details']
        return {attr: getattr(self, attr) for attr in attributes if getattr(self, attr)}

    @classmethod
    def get_payment_info(cls, payment_option_id):
        option = cls._payment_options.get(payment_option_id, {})
        return cls(payment_option_id, option.get("payment_url"), option.get("payment_details"))

# Example usage
#credit_card_payment_info = PaymentInfo.get_payment_info(3)
#print(credit_card_payment_info)

#bank_transfer_payment_info = PaymentInfo.get_payment_info(5)
#print(bank_transfer_payment_info)

#currencies = CurrencyManager()
#all_currencies = currencies()  # Get all currencies
#eur_currency = currencies('eur')  # Get only EUR currency
#chf_currency = currencies('chf')  # Get only EUR currency
#
#logging.info(all_currencies)
#logging.info(eur_currency)
#logging.info(chf_currency)
