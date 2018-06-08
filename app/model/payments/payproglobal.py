import datetime
import logging
import sys

from psycopg2._psycopg import DatabaseError

from app.exception import BillingError, BillingException, BillingNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class PayProGlobalPayment(object):
    __version__ = 1

    _sid = None
    _payment_id = None
    _order_id = None
    _product_id = None
    _order_status = None
    _order_status_id = None
    _order_referrer_url = None
    _customer_name = None
    _customer_first_name = None
    _customer_last_name = None
    _customer_email = None
    _customer_country_name = None
    _customer_state_name = None
    _ec_product_id = None
    _product_quantity = None
    _order_item_id = None
    _order_item_name = None
    _order_item_type_id = None
    _order_item_type_name = None
    _order_item_sku = None
    _order_currency_code = None
    _order_item_vendor_amount = None
    _order_item_price = None
    _order_item_unit_price = None
    _order_item_total_amount = None
    _order_item_affiliate_amount = None
    _order_item_partners_amount = None
    _order_total_amount = None
    _order_taxes_amount = None
    _order_item_coupon_discount = None
    _order_item_dynamic_discount = None
    _order_item_lead_discount = None
    _order_item_promo_discount = None
    _order_item_volume_discount = None
    _order_item_total_discount = None
    _order_total_amount_shown = None
    _vendor_balance_currency_code = None
    _payment_method_id = None
    _payment_method_name = None
    _customer_id = None
    _customer_country_code_by_ip = None
    _customer_country_name_by_ip = None
    _customer_country_code = None
    _customer_phone = None
    _customer_language_code = None
    _customer_state_code = None
    _customer_city = None
    _customer_street_address = None
    _customer_zipcode = None
    _corporate_purchase = None
    _subscription_id = None
    _paypal_account = None
    _ipn_type_id = None
    _ipn_type_name = None
    _test_mode = None
    _hash = None
    _order_items_count = None
    _regional_price = None
    _invoice_link = None
    _credit_card_bin = None
    _credit_card_last4 = None
    _credit_card_expiration_date = None
    _credit_card_bin_result = None
    _order_total_amount_with_taxes_shown = None
    _is_delayed_payment = None
    _created_date = None

    def __init__(self, sid: int = None, payment_id: int = None, order_id: int = None, product_id: int = None,
                 order_status: str = None, order_status_id: int = None, order_referrer_url: str = None,
                 customer_name: str = None, customer_first_name: str = None, customer_last_name: str = None,
                 customer_email: str = None, customer_country_name: str = None, customer_state_name: str = None,
                 ec_product_id: int = None, product_quantity: int = None, order_item_id: int = None,
                 order_item_name: str = None, order_item_type_id: int = None, order_item_type_name: str = None,
                 order_item_sku: str = None, order_currency_code: str = None, order_item_vendor_amount: int = None,
                 order_item_price: int = None, order_item_unit_price: int = None, order_item_total_amount: int = None,
                 order_item_affiliate_amount: int = None, order_item_partners_amount: int = None,
                 order_total_amount: int = None, order_taxes_amount: int = None, order_item_coupon_discount: int = None,
                 order_item_dynamic_discount: int = None, order_item_lead_discount: int = None,
                 order_item_promo_discount: int = None, order_item_volume_discount: int = None,
                 order_item_total_discount: int = None, order_total_amount_shown: int = None,
                 vendor_balance_currency_code: str = None, payment_method_id: int = None,
                 payment_method_name: str = None, customer_id: int = None, customer_country_code_by_ip: str = None,
                 customer_country_name_by_ip: str = None, customer_country_code: str = None, customer_phone: str = None,
                 customer_language_code: str = None, customer_state_code: str = None, customer_city: str = None,
                 customer_street_address: str = None, customer_zipcode: str = None, corporate_purchase: str = None,
                 subscription_id: int = None, paypal_account: int = None, ipn_type_id: int = None,
                 ipn_type_name: str = None, test_mode: str = None, hash: str = None, order_items_count: str = None,
                 regional_price: int = None, invoice_link: str = None, credit_card_bin: str = None,
                 credit_card_last4: str = None, credit_card_expiration_date: datetime = None,
                 credit_card_bin_result: str = None, order_total_amount_with_taxes_shown: str = None,
                 is_delayed_payment: bool = None, created_date: datetime = None):
        self._sid = sid
        self._payment_id = payment_id
        self._order_id = order_id
        self._product_id = product_id
        self._order_status = order_status
        self._order_status_id = order_status_id
        self._order_referrer_url = order_referrer_url
        self._customer_name = customer_name
        self._customer_first_name = customer_first_name
        self._customer_last_name = customer_last_name
        self._customer_email = customer_email
        self._customer_country_name = customer_country_name
        self._customer_state_name = customer_state_name
        self._ec_product_id = ec_product_id
        self._product_quantity = product_quantity
        self._order_item_id = order_item_id
        self._order_item_name = order_item_name
        self._order_item_type_id = order_item_type_id
        self._order_item_type_name = order_item_type_name
        self._order_item_sku = order_item_sku
        self._order_currency_code = order_currency_code
        self._order_item_vendor_amount = order_item_vendor_amount
        self._order_item_price = order_item_price
        self._order_item_unit_price = order_item_unit_price
        self._order_item_total_amount = order_item_total_amount
        self._order_item_affiliate_amount = order_item_affiliate_amount
        self._order_item_partners_amount = order_item_partners_amount
        self._order_total_amount = order_total_amount
        self._order_taxes_amount = order_taxes_amount
        self._order_item_coupon_discount = order_item_coupon_discount
        self._order_item_dynamic_discount = order_item_dynamic_discount
        self._order_item_lead_discount = order_item_lead_discount
        self._order_item_promo_discount = order_item_promo_discount
        self._order_item_volume_discount = order_item_volume_discount
        self._order_item_total_discount = order_item_total_discount
        self._order_total_amount_shown = order_total_amount_shown
        self._vendor_balance_currency_code = vendor_balance_currency_code
        self._payment_method_id = payment_method_id
        self._payment_method_name = payment_method_name
        self._customer_id = customer_id
        self._customer_country_code_by_ip = customer_country_code_by_ip
        self._customer_country_name_by_ip = customer_country_name_by_ip
        self._customer_country_code = customer_country_code
        self._customer_phone = customer_phone
        self._customer_language_code = customer_language_code
        self._customer_state_code = customer_state_code
        self._customer_city = customer_city
        self._customer_street_address = customer_street_address
        self._customer_zipcode = customer_zipcode
        self._corporate_purchase = corporate_purchase
        self._subscription_id = subscription_id
        self._paypal_account = paypal_account
        self._ipn_type_id = ipn_type_id
        self._ipn_type_name = ipn_type_name
        self._test_mode = test_mode
        self._hash = hash
        self._order_items_count = order_items_count
        self._regional_price = regional_price
        self._invoice_link = invoice_link
        self._credit_card_bin = credit_card_bin
        self._credit_card_last4 = credit_card_last4
        self._credit_card_expiration_date = credit_card_expiration_date
        self._credit_card_bin_result = credit_card_bin_result
        self._order_total_amount_with_taxes_shown = order_total_amount_with_taxes_shown
        self._is_delayed_payment = is_delayed_payment
        self._created_date = created_date

    def to_dict(self):
        return {
            'sid': self._sid,
            'payment_id': self._payment_id,
            'order_id': self._order_id,
            'product_id': self._product_id,
            'order_status': self._order_status,
            'order_status_id': self._order_status_id,
            'order_referrer_url': self._order_referrer_url,
            'customer_name': self._customer_name,
            'customer_first_name': self._customer_first_name,
            'customer_last_name': self._customer_last_name,
            'customer_email': self._customer_email,
            'customer_country_name': self._customer_country_name,
            'customer_state_name': self._customer_state_name,
            'ec_product_id': self._ec_product_id,
            'product_quantity': self._product_quantity,
            'order_item_id': self._order_item_id,
            'order_item_name': self._order_item_name,
            'order_item_type_id': self._order_item_type_id,
            'order_item_type_name': self._order_item_type_name,
            'order_item_sku': self._order_item_sku,
            'order_currency_code': self._order_currency_code,
            'order_item_vendor_amount': self._order_item_vendor_amount,
            'order_item_price': self._order_item_price,
            'order_item_unit_price': self._order_item_unit_price,
            'order_item_total_amount': self._order_item_total_amount,
            'order_item_affiliate_amount': self._order_item_affiliate_amount,
            'order_item_partners_amount': self._order_item_partners_amount,
            'order_total_amount': self._order_total_amount,
            'order_taxes_amount': self._order_taxes_amount,
            'order_item_coupon_discount': self._order_item_coupon_discount,
            'order_item_dynamic_discount': self._order_item_dynamic_discount,
            'order_item_lead_discount': self._order_item_lead_discount,
            'order_item_promo_discount': self._order_item_promo_discount,
            'order_item_volume_discount': self._order_item_volume_discount,
            'order_item_total_discount': self._order_item_total_discount,
            'order_total_amount_shown': self._order_total_amount_shown,
            'vendor_balance_currency_code': self._vendor_balance_currency_code,
            'payment_method_id': self._payment_method_id,
            'payment_method_name': self._payment_method_name,
            'customer_id': self._customer_id,
            'customer_country_code_by_ip': self._customer_country_code_by_ip,
            'customer_country_name_by_ip': self._customer_country_name_by_ip,
            'customer_country_code': self._customer_country_code,
            'customer_phone': self._customer_phone,
            'customer_language_code': self._customer_language_code,
            'customer_state_code': self._customer_state_code,
            'customer_city': self._customer_city,
            'customer_street_address': self._customer_street_address,
            'customer_zipcode': self._customer_zipcode,
            'corporate_purchase': self._corporate_purchase,
            'subscription_id': self._subscription_id,
            'paypal_account': self._paypal_account,
            'ipn_type_id': self._ipn_type_id,
            'ipn_type_name': self._ipn_type_name,
            'test_mode': self._test_mode,
            'hash': self._hash,
            'order_items_count': self._order_items_count,
            'regional_price': self._regional_price,
            'invoice_link': self._invoice_link,
            'credit_card_bin': self._credit_card_bin,
            'credit_card_last4': self._credit_card_last4,
            'credit_card_expiration_date': self._credit_card_expiration_date,
            'credit_card_bin_result': self._credit_card_bin_result,
            'order_total_amount_with_taxes_shown': self._order_total_amount_with_taxes_shown,
            'is_delayed_payment': self._is_delayed_payment,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return {
            'sid': self._sid,
            'payment_id': self._payment_id,
            'order_id': self._order_id,
            'product_id': self._product_id,
            'order_status': self._order_status,
            'order_status_id': self._order_status_id,
            'order_referrer_url': self._order_referrer_url,
            'customer_name': self._customer_name,
            'customer_first_name': self._customer_first_name,
            'customer_last_name': self._customer_last_name,
            'customer_email': self._customer_email,
            'customer_country_name': self._customer_country_name,
            'customer_state_name': self._customer_state_name,
            'ec_product_id': self._ec_product_id,
            'product_quantity': self._product_quantity,
            'order_item_id': self._order_item_id,
            'order_item_name': self._order_item_name,
            'order_item_type_id': self._order_item_type_id,
            'order_item_type_name': self._order_item_type_name,
            'order_item_sku': self._order_item_sku,
            'order_currency_code': self._order_currency_code,
            'order_item_vendor_amount': self._order_item_vendor_amount,
            'order_item_price': self._order_item_price,
            'order_item_unit_price': self._order_item_unit_price,
            'order_item_total_amount': self._order_item_total_amount,
            'order_item_affiliate_amount': self._order_item_affiliate_amount,
            'order_item_partners_amount': self._order_item_partners_amount,
            'order_total_amount': self._order_total_amount,
            'order_taxes_amount': self._order_taxes_amount,
            'order_item_coupon_discount': self._order_item_coupon_discount,
            'order_item_dynamic_discount': self._order_item_dynamic_discount,
            'order_item_lead_discount': self._order_item_lead_discount,
            'order_item_promo_discount': self._order_item_promo_discount,
            'order_item_volume_discount': self._order_item_volume_discount,
            'order_item_total_discount': self._order_item_total_discount,
            'order_total_amount_shown': self._order_total_amount_shown,
            'vendor_balance_currency_code': self._vendor_balance_currency_code,
            'payment_method_id': self._payment_method_id,
            'payment_method_name': self._payment_method_name,
            'customer_id': self._customer_id,
            'customer_country_code_by_ip': self._customer_country_code_by_ip,
            'customer_country_name_by_ip': self._customer_country_name_by_ip,
            'customer_country_code': self._customer_country_code,
            'customer_phone': self._customer_phone,
            'customer_language_code': self._customer_language_code,
            'customer_state_code': self._customer_state_code,
            'customer_city': self._customer_city,
            'customer_street_address': self._customer_street_address,
            'customer_zipcode': self._customer_zipcode,
            'corporate_purchase': self._corporate_purchase,
            'subscription_id': self._subscription_id,
            'paypal_account': self._paypal_account,
            'ipn_type_id': self._ipn_type_id,
            'ipn_type_name': self._ipn_type_name,
            'test_mode': self._test_mode,
            'hash': self._hash,
            'order_items_count': self._order_items_count,
            'regional_price': self._regional_price,
            'invoice_link': self._invoice_link,
            'credit_card_bin': self._credit_card_bin,
            'credit_card_last4': self._credit_card_last4,
            'credit_card_expiration_date': self._credit_card_expiration_date,
            'credit_card_bin_result': self._credit_card_bin_result,
            'order_total_amount_with_taxes_shown': self._order_total_amount_with_taxes_shown,
            'is_delayed_payment': self._is_delayed_payment,
            'created_date': self._created_date,
        }


class PayProGlobalPaymentStored(StoredObject, PayProGlobalPayment):
    __version__ = 1

    def __init__(self, storage_service: StorageService, sid: int = None, payment_id: int = None, order_id: int = None,
                 product_id: int = None, order_status: str = None, order_status_id: int = None,
                 order_referrer_url: str = None, customer_name: str = None, customer_first_name: str = None,
                 customer_last_name: str = None, customer_email: str = None, customer_country_name: str = None,
                 customer_state_name: str = None, ec_product_id: int = None, product_quantity: int = None,
                 order_item_id: int = None, order_item_name: str = None, order_item_type_id: int = None,
                 order_item_type_name: str = None, order_item_sku: str = None, order_currency_code: str = None,
                 order_item_vendor_amount: int = None, order_item_price: int = None, order_item_unit_price: int = None,
                 order_item_total_amount: int = None, order_item_affiliate_amount: int = None,
                 order_item_partners_amount: int = None, order_total_amount: int = None, order_taxes_amount: int = None,
                 order_item_coupon_discount: int = None, order_item_dynamic_discount: int = None,
                 order_item_lead_discount: int = None, order_item_promo_discount: int = None,
                 order_item_volume_discount: int = None, order_item_total_discount: int = None,
                 order_total_amount_shown: int = None, vendor_balance_currency_code: str = None,
                 payment_method_id: int = None, payment_method_name: str = None, customer_id: int = None,
                 customer_country_code_by_ip: str = None, customer_country_name_by_ip: str = None,
                 customer_country_code: str = None, customer_phone: str = None, customer_language_code: str = None,
                 customer_state_code: str = None, customer_city: str = None, customer_street_address: str = None,
                 customer_zipcode: str = None, corporate_purchase: str = None, subscription_id: int = None,
                 paypal_account: int = None, ipn_type_id: int = None, ipn_type_name: str = None, test_mode: str = None,
                 hash: str = None, order_items_count: str = None, regional_price: int = None, invoice_link: str = None,
                 credit_card_bin: str = None, credit_card_last4: str = None,
                 credit_card_expiration_date: datetime = None, credit_card_bin_result: str = None,
                 order_total_amount_with_taxes_shown: str = None, is_delayed_payment: bool = None,
                 created_date: datetime = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        PayProGlobalPayment.__init__(self, sid=sid, payment_id=payment_id, order_id=order_id, product_id=product_id,
                                     order_status=order_status, order_status_id=order_status_id,
                                     order_referrer_url=order_referrer_url, customer_name=customer_name,
                                     customer_first_name=customer_first_name, customer_last_name=customer_last_name,
                                     customer_email=customer_email, customer_country_name=customer_country_name,
                                     customer_state_name=customer_state_name, ec_product_id=ec_product_id,
                                     product_quantity=product_quantity, order_item_id=order_item_id,
                                     order_item_name=order_item_name, order_item_type_id=order_item_type_id,
                                     order_item_type_name=order_item_type_name, order_item_sku=order_item_sku,
                                     order_currency_code=order_currency_code,
                                     order_item_vendor_amount=order_item_vendor_amount,
                                     order_item_price=order_item_price, order_item_unit_price=order_item_unit_price,
                                     order_item_total_amount=order_item_total_amount,
                                     order_item_affiliate_amount=order_item_affiliate_amount,
                                     order_item_partners_amount=order_item_partners_amount,
                                     order_total_amount=order_total_amount, order_taxes_amount=order_taxes_amount,
                                     order_item_coupon_discount=order_item_coupon_discount,
                                     order_item_dynamic_discount=order_item_dynamic_discount,
                                     order_item_lead_discount=order_item_lead_discount,
                                     order_item_promo_discount=order_item_promo_discount,
                                     order_item_volume_discount=order_item_volume_discount,
                                     order_item_total_discount=order_item_total_discount,
                                     order_total_amount_shown=order_total_amount_shown,
                                     vendor_balance_currency_code=vendor_balance_currency_code,
                                     payment_method_id=payment_method_id, payment_method_name=payment_method_name,
                                     customer_id=customer_id, customer_country_code_by_ip=customer_country_code_by_ip,
                                     customer_country_name_by_ip=customer_country_name_by_ip,
                                     customer_country_code=customer_country_code, customer_phone=customer_phone,
                                     customer_language_code=customer_language_code,
                                     customer_state_code=customer_state_code, customer_city=customer_city,
                                     customer_street_address=customer_street_address, customer_zipcode=customer_zipcode,
                                     corporate_purchase=corporate_purchase, subscription_id=subscription_id,
                                     paypal_account=paypal_account, ipn_type_id=ipn_type_id,
                                     ipn_type_name=ipn_type_name, test_mode=test_mode, hash=hash,
                                     order_items_count=order_items_count, regional_price=regional_price,
                                     invoice_link=invoice_link, credit_card_bin=credit_card_bin,
                                     credit_card_last4=credit_card_last4,
                                     credit_card_expiration_date=credit_card_expiration_date,
                                     credit_card_bin_result=credit_card_bin_result,
                                     order_total_amount_with_taxes_shown=order_total_amount_with_taxes_shown,
                                     is_delayed_payment=is_delayed_payment, created_date=created_date, )


class PayProGlobalPaymentDB(PayProGlobalPaymentStored):
    __version__ = 1

    _sid_field = 'sid'
    _payment_id_field = 'payment_id'
    _order_id_field = 'order_id'
    _product_id_field = 'product_id'
    _order_status_field = 'order_status'
    _order_status_id_field = 'order_status_id'
    _order_referrer_url_field = 'order_referrer_url'
    _customer_name_field = 'customer_name'
    _customer_first_name_field = 'customer_first_name'
    _customer_last_name_field = 'customer_last_name'
    _customer_email_field = 'customer_email'
    _customer_country_name_field = 'customer_country_name'
    _customer_state_name_field = 'customer_state_name'
    _ec_product_id_field = 'ec_product_id'
    _product_quantity_field = 'product_quantity'
    _order_item_id_field = 'order_item_id'
    _order_item_name_field = 'order_item_name'
    _order_item_type_id_field = 'order_item_type_id'
    _order_item_type_name_field = 'order_item_type_name'
    _order_item_sku_field = 'order_item_sku'
    _order_currency_code_field = 'order_currency_code'
    _order_item_vendor_amount_field = 'order_item_vendor_amount'
    _order_item_price_field = 'order_item_price'
    _order_item_unit_price_field = 'order_item_unit_price'
    _order_item_total_amount_field = 'order_item_total_amount'
    _order_item_affiliate_amount_field = 'order_item_affiliate_amount'
    _order_item_partners_amount_field = 'order_item_partners_amount'
    _order_total_amount_field = 'order_total_amount'
    _order_taxes_amount_field = 'order_taxes_amount'
    _order_item_coupon_discount_field = 'order_item_coupon_discount'
    _order_item_dynamic_discount_field = 'order_item_dynamic_discount'
    _order_item_lead_discount_field = 'order_item_lead_discount'
    _order_item_promo_discount_field = 'order_item_promo_discount'
    _order_item_volume_discount_field = 'order_item_volume_discount'
    _order_item_total_discount_field = 'order_item_total_discount'
    _order_total_amount_shown_field = 'order_total_amount_shown'
    _vendor_balance_currency_code_field = 'vendor_balance_currency_code'
    _payment_method_id_field = 'payment_method_id'
    _payment_method_name_field = 'payment_method_name'
    _customer_id_field = 'customer_id'
    _customer_country_code_by_ip_field = 'customer_country_code_by_ip'
    _customer_country_name_by_ip_field = 'customer_country_name_by_ip'
    _customer_country_code_field = 'customer_country_code'
    _customer_phone_field = 'customer_phone'
    _customer_language_code_field = 'customer_language_code'
    _customer_state_code_field = 'customer_state_code'
    _customer_city_field = 'customer_city'
    _customer_street_address_field = 'customer_street_address'
    _customer_zipcode_field = 'customer_zipcode'
    _corporate_purchase_field = 'corporate_purchase'
    _subscription_id_field = 'subscription_id'
    _paypal_account_field = 'paypal_account'
    _ipn_type_id_field = 'ipn_type_id'
    _ipn_type_name_field = 'ipn_type_name'
    _test_mode_field = 'test_mode'
    _hash_field = 'hash'
    _order_items_count_field = 'order_items_count'
    _regional_price_field = 'regional_price'
    _invoice_link_field = 'invoice_link'
    _credit_card_bin_field = 'credit_card_bin'
    _credit_card_last4_field = 'credit_card_last4'
    _credit_card_expiration_date_field = 'credit_card_expiration_date'
    _credit_card_bin_result_field = 'credit_card_bin_result'
    _order_total_amount_with_taxes_shown_field = 'order_total_amount_with_taxes_shown'
    _is_delayed_payment_field = 'is_delayed_payment'
    _created_date_field = 'created_date'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def create(self):
        logging.info('PayProGlobalPaymentDB create method')
        insert_sql = '''
                        INSERT INTO public.ppg_payment (
                            id,
                            payment_id,
                            order_id,
                            product_id,
                            order_status,
                            order_status_id,
                            order_referrer_url,
                            customer_name,
                            customer_first_name,
                            customer_last_name,
                            customer_email,
                            customer_country_name,
                            customer_state_name,
                            ec_product_id,
                            product_quantity,
                            order_item_id,
                            order_item_name,
                            order_item_type_id,
                            order_item_type_name,
                            order_item_sku,
                            order_currency_code,
                            order_item_vendor_amount,
                            order_item_price,
                            order_item_unit_price,
                            order_item_total_amount,
                            order_item_affiliate_amount,
                            order_item_partners_amount,
                            order_total_amount,
                            order_taxes_amount,
                            order_item_coupon_discount,
                            order_item_dynamic_discount,
                            order_item_lead_discount,
                            order_item_promo_discount,
                            order_item_volume_discount,
                            order_item_total_discount,
                            order_total_amount_shown,
                            vendor_balance_currency_code,
                            payment_method_id,
                            payment_method_name,
                            customer_id,
                            customer_country_code_by_ip,
                            customer_country_name_by_ip,
                            customer_country_code,
                            customer_phone,
                            customer_language_code,
                            customer_state_code,
                            customer_city,
                            customer_street_address,
                            customer_zipcode,
                            corporate_purchase,
                            subscription_id,
                            paypal_account,
                            ipn_type_id,
                            ipn_type_name,
                            test_mode,
                            hash,
                            order_items_count,
                            regional_price,
                            invoice_link,
                            credit_card_bin,
                            credit_card_last4,
                            credit_card_expiration_date,
                            credit_card_bin_result,
                            order_total_amount_with_taxes_shown,
                            is_delayed_payment,
                            created_date,
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                        ?, ?, ?, ?, ?);
                     '''
        insert_params = (
            self._sid,
            self._payment_id,
            self._order_id,
            self._product_id,
            self._order_status,
            self._order_status_id,
            self._order_referrer_url,
            self._customer_name,
            self._customer_first_name,
            self._customer_last_name,
            self._customer_email,
            self._customer_country_name,
            self._customer_state_name,
            self._ec_product_id,
            self._product_quantity,
            self._order_item_id,
            self._order_item_name,
            self._order_item_type_id,
            self._order_item_type_name,
            self._order_item_sku,
            self._order_currency_code,
            self._order_item_vendor_amount,
            self._order_item_price,
            self._order_item_unit_price,
            self._order_item_total_amount,
            self._order_item_affiliate_amount,
            self._order_item_partners_amount,
            self._order_total_amount,
            self._order_taxes_amount,
            self._order_item_coupon_discount,
            self._order_item_dynamic_discount,
            self._order_item_lead_discount,
            self._order_item_promo_discount,
            self._order_item_volume_discount,
            self._order_item_total_discount,
            self._order_total_amount_shown,
            self._vendor_balance_currency_code,
            self._payment_method_id,
            self._payment_method_name,
            self._customer_id,
            self._customer_country_code_by_ip,
            self._customer_country_name_by_ip,
            self._customer_country_code,
            self._customer_phone,
            self._customer_language_code,
            self._customer_state_code,
            self._customer_city,
            self._customer_street_address,
            self._customer_zipcode,
            self._corporate_purchase,
            self._subscription_id,
            self._paypal_account,
            self._ipn_type_id,
            self._ipn_type_name,
            self._test_mode,
            self._hash,
            self._order_items_count,
            self._regional_price,
            self._invoice_link,
            self._credit_card_bin,
            self._credit_card_last4,
            self._credit_card_expiration_date,
            self._credit_card_bin_result,
            self._order_total_amount_with_taxes_shown,
            self._is_delayed_payment,
            self._created_date,
        )
        logging.debug('Create PayProGlobalPaymentDB SQL : %s' % insert_sql)

        try:
            logging.debug('Call database service')
            self._storage_service.create(sql=insert_sql, data=insert_params)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.PPG_PAYMENT_CREATE_ERROR_DB.message
            error_code = BillingError.PPG_PAYMENT_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PPG_PAYMENT_CREATE_ERROR_DB.description, e.pgcode, e.pgerror)

            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('PayProGlobalPaymentDB created.')

        return self._sid

    def update_by_order_id(self):
        logging.info('PayProGlobalPayment update method')

        update_sql = '''
                    UPDATE 
                      public.ppg_payment 
                    SET
                        id = ?,
                        payment_id = ?,
                        product_id = ?,
                        order_status = ?,
                        order_status_id = ?,
                        order_referrer_url = ?,
                        customer_name = ?,
                        customer_first_name = ?,
                        customer_last_name = ?,
                        customer_email = ?,
                        customer_country_name = ?,
                        customer_state_name = ?,
                        ec_product_id = ?,
                        product_quantity = ?,
                        order_item_id = ?,
                        order_item_name = ?,
                        order_item_type_id = ?,
                        order_item_type_name = ?,
                        order_item_sku = ?,
                        order_currency_code = ?,
                        order_item_vendor_amount = ?,
                        order_item_price = ?,
                        order_item_unit_price = ?,
                        order_item_total_amount = ?,
                        order_item_affiliate_amount = ?,
                        order_item_partners_amount = ?,
                        order_total_amount = ?,
                        order_taxes_amount = ?,
                        order_item_coupon_discount = ?,
                        order_item_dynamic_discount = ?,
                        order_item_lead_discount = ?,
                        order_item_promo_discount = ?,
                        order_item_volume_discount = ?,
                        order_item_total_discount = ?,
                        order_total_amount_shown = ?,
                        vendor_balance_currency_code = ?,
                        payment_method_id = ?,
                        payment_method_name = ?,
                        customer_id = ?,
                        customer_country_code_by_ip = ?,
                        customer_country_name_by_ip = ?,
                        customer_country_code = ?,
                        customer_phone = ?,
                        customer_language_code = ?,
                        customer_state_code = ?,
                        customer_city = ?,
                        customer_street_address = ?,
                        customer_zipcode = ?,
                        corporate_purchase = ?,
                        subscription_id = ?,
                        paypal_account = ?,
                        ipn_type_id = ?,
                        ipn_type_name = ?,
                        test_mode = ?,
                        hash = ?,
                        order_items_count = ?,
                        regional_price = ?,
                        invoice_link = ?,
                        credit_card_bin = ?,
                        credit_card_last4 = ?,
                        credit_card_expiration_date = ?,
                        credit_card_bin_result = ?,
                        order_total_amount_with_taxes_shown = ?,
                        is_delayed_payment = ?,
                        created_date = ?
                    WHERE 
                        order_id = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._sid,
            self._payment_id,
            self._product_id,
            self._order_status,
            self._order_status_id,
            self._order_referrer_url,
            self._customer_name,
            self._customer_first_name,
            self._customer_last_name,
            self._customer_email,
            self._customer_country_name,
            self._customer_state_name,
            self._ec_product_id,
            self._product_quantity,
            self._order_item_id,
            self._order_item_name,
            self._order_item_type_id,
            self._order_item_type_name,
            self._order_item_sku,
            self._order_currency_code,
            self._order_item_vendor_amount,
            self._order_item_price,
            self._order_item_unit_price,
            self._order_item_total_amount,
            self._order_item_affiliate_amount,
            self._order_item_partners_amount,
            self._order_total_amount,
            self._order_taxes_amount,
            self._order_item_coupon_discount,
            self._order_item_dynamic_discount,
            self._order_item_lead_discount,
            self._order_item_promo_discount,
            self._order_item_volume_discount,
            self._order_item_total_discount,
            self._order_total_amount_shown,
            self._vendor_balance_currency_code,
            self._payment_method_id,
            self._payment_method_name,
            self._customer_id,
            self._customer_country_code_by_ip,
            self._customer_country_name_by_ip,
            self._customer_country_code,
            self._customer_phone,
            self._customer_language_code,
            self._customer_state_code,
            self._customer_city,
            self._customer_street_address,
            self._customer_zipcode,
            self._corporate_purchase,
            self._subscription_id,
            self._paypal_account,
            self._ipn_type_id,
            self._ipn_type_name,
            self._test_mode,
            self._hash,
            self._order_items_count,
            self._regional_price,
            self._invoice_link,
            self._credit_card_bin,
            self._credit_card_last4,
            self._credit_card_expiration_date,
            self._credit_card_bin_result,
            self._order_total_amount_with_taxes_shown,
            self._is_delayed_payment,
            self._created_date,
            self._order_id,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('PayProGlobalPayment updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.PPG_PAYMENT_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PPG_PAYMENT_UPDATE_ERROR_DB.description, e.pgcode, e.pgerror)
            error_code = BillingError.PPG_PAYMENT_UPDATE_ERROR_DB.code
            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)

    def find_by_payment_id(self):
        logging.info('PayProGlobalPayment find_by_payment_id method')
        select_sql = '''
                    SELECT 
                          ppgp.id AS sid,
                          ppgp.payment_id AS payment_id,
                          ppgp.order_id AS order_id,
                          ppgp.product_id AS product_id,
                          ppgp.order_status AS order_status,
                          ppgp.order_status_id AS order_status_id,
                          ppgp.order_referrer_url AS order_referrer_url,
                          ppgp.customer_name AS customer_name,
                          ppgp.customer_first_name AS customer_first_name,
                          ppgp.customer_last_name AS customer_last_name,
                          ppgp.customer_email AS customer_email,
                          ppgp.customer_country_name AS customer_country_name,
                          ppgp.customer_state_name AS customer_state_name,
                          ppgp.ec_product_id AS ec_product_id,
                          ppgp.product_quantity AS product_quantity,
                          ppgp.order_item_id AS order_item_id,
                          ppgp.order_item_name AS order_item_name,
                          ppgp.order_item_type_id AS order_item_type_id,
                          ppgp.order_item_type_name AS order_item_type_name,
                          ppgp.order_item_sku AS order_item_sku,
                          ppgp.order_currency_code AS order_currency_code,
                          ppgp.order_item_vendor_amount AS order_item_vendor_amount,
                          ppgp.order_item_price AS order_item_price,
                          ppgp.order_item_unit_price AS order_item_unit_price,
                          ppgp.order_item_total_amount AS order_item_total_amount,
                          ppgp.order_item_affiliate_amount AS order_item_affiliate_amount,
                          ppgp.order_item_partners_amount AS order_item_partners_amount,
                          ppgp.order_total_amount AS order_total_amount,
                          ppgp.order_taxes_amount AS order_taxes_amount,
                          ppgp.order_item_coupon_discount AS order_item_coupon_discount,
                          ppgp.order_item_dynamic_discount AS order_item_dynamic_discount,
                          ppgp.order_item_lead_discount AS order_item_lead_discount,
                          ppgp.order_item_promo_discount AS order_item_promo_discount,
                          ppgp.order_item_volume_discount AS order_item_volume_discount,
                          ppgp.order_item_total_discount AS order_item_total_discount,
                          ppgp.order_total_amount_shown AS order_total_amount_shown,
                          ppgp.vendor_balance_currency_code AS vendor_balance_currency_code,
                          ppgp.payment_method_id AS payment_method_id,
                          ppgp.payment_method_name AS payment_method_name,
                          ppgp.customer_id AS customer_id,
                          ppgp.customer_country_code_by_ip AS customer_country_code_by_ip,
                          ppgp.customer_country_name_by_ip AS customer_country_name_by_ip,
                          ppgp.customer_country_code AS customer_country_code,
                          ppgp.customer_phone AS customer_phone,
                          ppgp.customer_language_code AS customer_language_code,
                          ppgp.customer_state_code AS customer_state_code,
                          ppgp.customer_city AS customer_city,
                          ppgp.customer_street_address AS customer_street_address,
                          ppgp.customer_zipcode AS customer_zipcode,
                          ppgp.corporate_purchase AS corporate_purchase,
                          ppgp.subscription_id AS subscription_id,
                          ppgp.paypal_account AS paypal_account,
                          ppgp.ipn_type_id AS ipn_type_id,
                          ppgp.ipn_type_name AS ipn_type_name,
                          ppgp.test_mode AS test_mode,
                          ppgp.hash AS HASH,
                          ppgp.order_items_count AS order_items_count,
                          ppgp.regional_price AS regional_price,
                          ppgp.invoice_link AS invoice_link,
                          ppgp.credit_card_bin AS credit_card_bin,
                          ppgp.credit_card_last4 AS credit_card_last4,
                          to_json(ppgp.credit_card_expiration_date) AS credit_card_expiration_date,
                          ppgp.credit_card_bin_result AS credit_card_bin_result,
                          ppgp.order_total_amount_with_taxes_shown AS order_total_amount_with_taxes_shown,
                          ppgp.is_delayed_payment AS is_delayed_payment,
                          to_json(ppgp.created_date) AS created_date
                      FROM public.ppg_payment AS ppgp
                      WHERE ppgp.payment_id = ?
        '''

        logging.debug('Select SQL: %s' % select_sql)
        params = (self._payment_id,)

        try:
            logging.debug('Call database service')
            ppg_payment_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR_DB.message
            error_code = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR_DB.description, e.pgcode,
                                    e.pgerror)
            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(ppg_payment_list_db) == 1:
            ppg_payment_db = ppg_payment_list_db[0]
        elif len(ppg_payment_list_db) == 0:
            error_message = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR.message
            error_code = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR.code
            developer_message = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR.description
            raise BillingNotFoundException(error=error_message, error_code=error_code,
                                           developer_message=developer_message)
        else:
            error_message = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % BillingError.PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR.description
            error_code = BillingError.PPG_PAYMENT_FIND_BY_PAYMENTID_ERROR.code
            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__mappayproglobalpaymentdb_to_payproglobalpayment(ppg_payment_db)

    def find_by_order_id(self):
        logging.info('PayProGlobalPayment find_by_order_id method')
        select_sql = '''
                    SELECT 
                          ppgp.id AS sid,
                          ppgp.payment_id AS payment_id,
                          ppgp.order_id AS order_id,
                          ppgp.product_id AS product_id,
                          ppgp.order_status AS order_status,
                          ppgp.order_status_id AS order_status_id,
                          ppgp.order_referrer_url AS order_referrer_url,
                          ppgp.customer_name AS customer_name,
                          ppgp.customer_first_name AS customer_first_name,
                          ppgp.customer_last_name AS customer_last_name,
                          ppgp.customer_email AS customer_email,
                          ppgp.customer_country_name AS customer_country_name,
                          ppgp.customer_state_name AS customer_state_name,
                          ppgp.ec_product_id AS ec_product_id,
                          ppgp.product_quantity AS product_quantity,
                          ppgp.order_item_id AS order_item_id,
                          ppgp.order_item_name AS order_item_name,
                          ppgp.order_item_type_id AS order_item_type_id,
                          ppgp.order_item_type_name AS order_item_type_name,
                          ppgp.order_item_sku AS order_item_sku,
                          ppgp.order_currency_code AS order_currency_code,
                          ppgp.order_item_vendor_amount AS order_item_vendor_amount,
                          ppgp.order_item_price AS order_item_price,
                          ppgp.order_item_unit_price AS order_item_unit_price,
                          ppgp.order_item_total_amount AS order_item_total_amount,
                          ppgp.order_item_affiliate_amount AS order_item_affiliate_amount,
                          ppgp.order_item_partners_amount AS order_item_partners_amount,
                          ppgp.order_total_amount AS order_total_amount,
                          ppgp.order_taxes_amount AS order_taxes_amount,
                          ppgp.order_item_coupon_discount AS order_item_coupon_discount,
                          ppgp.order_item_dynamic_discount AS order_item_dynamic_discount,
                          ppgp.order_item_lead_discount AS order_item_lead_discount,
                          ppgp.order_item_promo_discount AS order_item_promo_discount,
                          ppgp.order_item_volume_discount AS order_item_volume_discount,
                          ppgp.order_item_total_discount AS order_item_total_discount,
                          ppgp.order_total_amount_shown AS order_total_amount_shown,
                          ppgp.vendor_balance_currency_code AS vendor_balance_currency_code,
                          ppgp.payment_method_id AS payment_method_id,
                          ppgp.payment_method_name AS payment_method_name,
                          ppgp.customer_id AS customer_id,
                          ppgp.customer_country_code_by_ip AS customer_country_code_by_ip,
                          ppgp.customer_country_name_by_ip AS customer_country_name_by_ip,
                          ppgp.customer_country_code AS customer_country_code,
                          ppgp.customer_phone AS customer_phone,
                          ppgp.customer_language_code AS customer_language_code,
                          ppgp.customer_state_code AS customer_state_code,
                          ppgp.customer_city AS customer_city,
                          ppgp.customer_street_address AS customer_street_address,
                          ppgp.customer_zipcode AS customer_zipcode,
                          ppgp.corporate_purchase AS corporate_purchase,
                          ppgp.subscription_id AS subscription_id,
                          ppgp.paypal_account AS paypal_account,
                          ppgp.ipn_type_id AS ipn_type_id,
                          ppgp.ipn_type_name AS ipn_type_name,
                          ppgp.test_mode AS test_mode,
                          ppgp.hash AS HASH,
                          ppgp.order_items_count AS order_items_count,
                          ppgp.regional_price AS regional_price,
                          ppgp.invoice_link AS invoice_link,
                          ppgp.credit_card_bin AS credit_card_bin,
                          ppgp.credit_card_last4 AS credit_card_last4,
                          to_json(ppgp.credit_card_expiration_date) AS credit_card_expiration_date,
                          ppgp.credit_card_bin_result AS credit_card_bin_result,
                          ppgp.order_total_amount_with_taxes_shown AS order_total_amount_with_taxes_shown,
                          ppgp.is_delayed_payment AS is_delayed_payment,
                          to_json(ppgp.created_date) AS created_date
                      FROM public.ppg_payment AS ppgp
                      WHERE ppgp.order_id = ?
        '''

        logging.debug('Select SQL: %s' % select_sql)
        params = (self._order_id,)

        try:
            logging.debug('Call database service')
            ppg_payment_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR_DB.message
            error_code = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR_DB.description, e.pgcode, e.pgerror)
            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(ppg_payment_list_db) == 1:
            ppg_payment_db = ppg_payment_list_db[0]
        elif len(ppg_payment_list_db) == 0:
            error_message = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.message
            error_code = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.code
            developer_message = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.description
            raise BillingNotFoundException(error=error_message, error_code=error_code,
                                           developer_message=developer_message)
        else:
            error_message = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.description
            error_code = BillingError.PPG_PAYMENT_FIND_BY_ORDERID_ERROR.code
            raise BillingException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__mappayproglobalpaymentdb_to_payproglobalpayment(ppg_payment_db)

    def __mappayproglobalpaymentdb_to_payproglobalpayment(self, payproglobalpayment_db):
        return PayProGlobalPayment(
            sid=payproglobalpayment_db[self._sid_field],
            payment_id=payproglobalpayment_db[self._payment_id_field],
            order_id=payproglobalpayment_db[self._order_id_field],
            product_id=payproglobalpayment_db[self._product_id_field],
            order_status=payproglobalpayment_db[self._order_status_field],
            order_status_id=payproglobalpayment_db[self._order_status_id_field],
            order_referrer_url=payproglobalpayment_db[self._order_referrer_url_field],
            customer_name=payproglobalpayment_db[self._customer_name_field],
            customer_first_name=payproglobalpayment_db[self._customer_first_name_field],
            customer_last_name=payproglobalpayment_db[self._customer_last_name_field],
            customer_email=payproglobalpayment_db[self._customer_email_field],
            customer_country_name=payproglobalpayment_db[self._customer_country_name_field],
            customer_state_name=payproglobalpayment_db[self._customer_state_name_field],
            ec_product_id=payproglobalpayment_db[self._ec_product_id_field],
            product_quantity=payproglobalpayment_db[self._product_quantity_field],
            order_item_id=payproglobalpayment_db[self._order_item_id_field],
            order_item_name=payproglobalpayment_db[self._order_item_name_field],
            order_item_type_id=payproglobalpayment_db[self._order_item_type_id_field],
            order_item_type_name=payproglobalpayment_db[self._order_item_type_name_field],
            order_item_sku=payproglobalpayment_db[self._order_item_sku_field],
            order_currency_code=payproglobalpayment_db[self._order_currency_code_field],
            order_item_vendor_amount=payproglobalpayment_db[self._order_item_vendor_amount_field],
            order_item_price=payproglobalpayment_db[self._order_item_price_field],
            order_item_unit_price=payproglobalpayment_db[self._order_item_unit_price_field],
            order_item_total_amount=payproglobalpayment_db[self._order_item_total_amount_field],
            order_item_affiliate_amount=payproglobalpayment_db[self._order_item_affiliate_amount_field],
            order_item_partners_amount=payproglobalpayment_db[self._order_item_partners_amount_field],
            order_total_amount=payproglobalpayment_db[self._order_total_amount_field],
            order_taxes_amount=payproglobalpayment_db[self._order_taxes_amount_field],
            order_item_coupon_discount=payproglobalpayment_db[self._order_item_coupon_discount_field],
            order_item_dynamic_discount=payproglobalpayment_db[self._order_item_dynamic_discount_field],
            order_item_lead_discount=payproglobalpayment_db[self._order_item_lead_discount_field],
            order_item_promo_discount=payproglobalpayment_db[self._order_item_promo_discount_field],
            order_item_volume_discount=payproglobalpayment_db[self._order_item_volume_discount_field],
            order_item_total_discount=payproglobalpayment_db[self._order_item_total_discount_field],
            order_total_amount_shown=payproglobalpayment_db[self._order_total_amount_shown_field],
            vendor_balance_currency_code=payproglobalpayment_db[self._vendor_balance_currency_code_field],
            payment_method_id=payproglobalpayment_db[self._payment_method_id_field],
            payment_method_name=payproglobalpayment_db[self._payment_method_name_field],
            customer_id=payproglobalpayment_db[self._customer_id_field],
            customer_country_code_by_ip=payproglobalpayment_db[self._customer_country_code_by_ip_field],
            customer_country_name_by_ip=payproglobalpayment_db[self._customer_country_name_by_ip_field],
            customer_country_code=payproglobalpayment_db[self._customer_country_code_field],
            customer_phone=payproglobalpayment_db[self._customer_phone_field],
            customer_language_code=payproglobalpayment_db[self._customer_language_code_field],
            customer_state_code=payproglobalpayment_db[self._customer_state_code_field],
            customer_city=payproglobalpayment_db[self._customer_city_field],
            customer_street_address=payproglobalpayment_db[self._customer_street_address_field],
            customer_zipcode=payproglobalpayment_db[self._customer_zipcode_field],
            corporate_purchase=payproglobalpayment_db[self._corporate_purchase_field],
            subscription_id=payproglobalpayment_db[self._subscription_id_field],
            paypal_account=payproglobalpayment_db[self._paypal_account_field],
            ipn_type_id=payproglobalpayment_db[self._ipn_type_id_field],
            ipn_type_name=payproglobalpayment_db[self._ipn_type_name_field],
            test_mode=payproglobalpayment_db[self._test_mode_field],
            hash=payproglobalpayment_db[self._hash_field],
            order_items_count=payproglobalpayment_db[self._order_items_count_field],
            regional_price=payproglobalpayment_db[self._regional_price_field],
            invoice_link=payproglobalpayment_db[self._invoice_link_field],
            credit_card_bin=payproglobalpayment_db[self._credit_card_bin_field],
            credit_card_last4=payproglobalpayment_db[self._credit_card_last4_field],
            credit_card_expiration_date=payproglobalpayment_db[self._credit_card_expiration_date_field],
            credit_card_bin_result=payproglobalpayment_db[self._credit_card_bin_result_field],
            order_total_amount_with_taxes_shown=payproglobalpayment_db[self._order_total_amount_with_taxes_shown_field],
            is_delayed_payment=payproglobalpayment_db[self._is_delayed_payment_field],
            created_date=payproglobalpayment_db[self._created_date_field],
        )
