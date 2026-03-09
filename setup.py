from setuptools import setup, find_packages

setup(
    name='openclaw-skills',
    version='0.1.0',
    description='智能Agent游戏引擎，支持龙虾战争的进化与战斗',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.2.0',
        'Flask-CORS>=3.0.0',
        'SQLAlchemy>=2.0.0',
        'requests>=2.28.0',
        'numpy>=1.24.0',
    ],
    python_requires='>=3.8',
)
