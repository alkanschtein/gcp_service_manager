# setup.py

from setuptools import setup, find_packages

setup(
    name="gcp_service_manager",
    version="0.1.0",
    description="A package for managing Firebase, Pub/Sub, and Cloud Storage on GCP.",
    author="Cem ALKAN",
    url="https://github.com/alkanschtein/gcp_service_manager",
    packages=find_packages(),
    install_requires=[
        "google-cloud-storage>=2.18.2",
        "google-cloud-firestore>=2.19.0",
        "google-cloud-pubsub>=2.26.1",
        "opencv-python==4.10.0.84",
        "numpy==2.1.1",
        "pillow==10.4.0"
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
)
