from lutech_erp_next.setup.customer import setup_customer


def after_install():
	setup_customer()


def after_migrate():
	setup_customer()
