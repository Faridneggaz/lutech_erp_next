from lutech_erp_next.setup.customer import setup_customer
from lutech_erp_next.setup.module_profile import setup_module_profile


def after_install():
	setup_customer()
	setup_module_profile()


def after_migrate():
	setup_customer()
	setup_module_profile()
