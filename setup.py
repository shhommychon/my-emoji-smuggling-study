from setuptools import setup, find_packages

setup(
    name="emoji_smuggle",
    version="0.1.0",
    author="shhommychon",
    author_email="shhommychon@github.com",
    description="A study on emoji smuggling",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
)