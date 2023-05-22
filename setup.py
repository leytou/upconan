#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='upconan',
    version="1.0.4",
    description="一个更新conanfile的便捷工具",
    long_description="""从剪贴板复制conan包信息，更新当前路径下的conanfile.py或conanfile.txt文件中对应的conan包版本""",
    long_description_content_type='text/x-rst',
    keywords='python conan',
    author='leytou',
    author_email='hi_litao@163.com',
    url='https://github.com/leytou/upconan',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=['GitPython','pyperclip'],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    entry_points={'console_scripts': [
        'upconan = src.upconan:main',
    ]},
)
