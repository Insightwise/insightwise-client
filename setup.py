from setuptools import setup, find_packages

setup(
    name="insightwise-client",
    version="0.0.1",
    packages=find_packages(include=["client", "client.*"]),
    install_requires=[
        "requests==2.32.3",
        "warrant-lite==1.0.4",
        "boto3==1.37.35",
        "pydantic==2.11.3",
        "pyhumps==3.8.0",
        "python-jose[cryptography]",
    ],
    author="InsightWise",
    author_email="support@insightwise.ai",
    description="InsightWise Client SDK",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    include_package_data=False,
)
