from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in battle_ships/__init__.py
from battle_ships import __version__ as version

setup(
	name="battle_ships",
	version=version,
	description="An online battle ship game with a twist",
	author="Kamal Johnson",
	author_email="kamal@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
