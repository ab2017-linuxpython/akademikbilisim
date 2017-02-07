from setuptools import setup

setup(
    name="gozcu",
    version="0.0.5",
    author="Umut Karcı",
    author_email="master.repeal@gmail.com",
    description="An example project for Akademik Bilişim 2017 Python for Gnu/Linux Systems "
                "course",
    license="MIT",
    keywords="example akademik bilisim",
    packages=['gozcu'],
    requires=["psutil"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': [
            'gozcu = gozcu.__main__:main',
        ]
    }
)
