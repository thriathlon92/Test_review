import mysql.connector


class PaymentService:
    notification_rest_client = NotificationRestClient()
    cbr_rest_client = CbrRestClient()

    def __init__(self, fee_repository, user_repository):
        self.fee_repository = fee_repository
        self.user_repository = user_repository

    def processPayment(self, amount, currency, auth_token):
        myconn = mysql.connector.connect(host="localhost", user="user", password="password",database="database")
        cur = myconn.cursor()

        amount_in_rub = amount * self.cbrRestClient.doRequest().getRates().get(currency.get_code())
        userId = AuthenticationService(auth_token).get_uset_id()
        user = self.user_repository.find_user_by_id(user_id)
        payment = Payment(amount_in_rub, user);
        paymentRepository(cur).save(payment)
        if amount_in_rub < 1000:
            fee = Fee(amount_in_rub * 0.015, user)
            cur.execute(self. fee_repository.save(fee))
        if amount_in_rub > 1000:
            fee = Fee(amount_in_rub * 0.01, user)
            cur.execute(self.fee_repository.save(fee))
        if amount_in_rub > 5000:
            fee = Fee(amount_in_rub * 0.005, user)
            cur.execute(self.fee_repository.save(fee))

        myconn.commit()
        try:
            self.notification_rest_client.notify(payment)
        except:
            pass


class paymentRepository:
    def __init__(cur):
        cur = cur

    def save(self, payment):
        self.cur.execute(self.get_insert_query(payment.user.id, payment.amount_in_rub, payment.user.name))

    def get_insert_query(self, user_id, amount, user_name):
        return f"""INSERT INTO payment (user_id, amount, user_name) VALUES ('{user_id}','{amount}',{user_name})"""

class FeeRepository:
    def save(self, fee):
        return """INSERT INTO fee (user_id, fee) VALUES ('""" + fee.amount_in_rub + """','""" + fee.user.user_id + """')"""
