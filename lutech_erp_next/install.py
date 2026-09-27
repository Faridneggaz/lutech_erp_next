from lutech_erp_next.setup.customer import setup_customer
from lutech_erp_next.setup.desk import setup_desk_visibility


def after_install():
	setup_customer()
	setup_desk_visibility()


def after_migrate():
	setup_customer()
	setup_desk_visibility()
