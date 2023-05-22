# -*- coding: utf-8 -*-

import os
import re
import time
from pathlib import Path
import sys

import pyperclip
from git.cmd import Git
from git import Repo, GitCommandError,InvalidGitRepositoryError


pattern = re.compile(r'(?P<name>[a-zA-Z0-9_]+)\/(?P<version>\d+(\.\d+){2,3})(\@(?P<owner>\w+))?(\/(?P<channel>[a-zA-Z0-9_]+))?')

def GetNewlineType(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        line = f.readline()
        if '\r\n' in line:
            return '\r\n'
        elif '\n' in line:
            return '\n'
        elif '\r' in line:
            print(3)
        return ''

def _GitCmd(cmd):
    git = Git(os.getcwd())
    return git.execute(cmd)

def Diff(path):
    cmd = ["git", "-c", "color.ui=always", "diff", path]
    return(_GitCmd(cmd))


def IsGitRepoRecursively(path):
    try:
        Repo(path)
        return True
    except InvalidGitRepositoryError:
        parent = os.path.normpath(os.path.join(path, os.pardir))
        if parent == path:
            return False
        return IsGitRepoRecursively(parent)

def PrintPackageInfo(package_info):
    print(f'name: {package_info["name"]}')
    print(f'version: {package_info["version"]}')
    print(f'owner: {package_info["owner"]}')
    print(f'channel: {package_info["channel"]}')
    print('=============')


def ParsePackageInfoLine(line):
    result_dict = {}
    result = pattern.search(line)
    if result:
        result_dict = result.groupdict()
    return result_dict

def ParsePackageInfoText(text):
    result_list = []
    results = pattern.finditer(text)
    for result in results:
        result_dict = result.groupdict()
        result_list.append(result_dict)
    return result_list


def FindTargetPackageInfo(curent_package_info , target_package_infos):
    for target_package_info in  target_package_infos:
        if curent_package_info['name'] == target_package_info['name'] and curent_package_info['version'] != target_package_info['version']:
            if curent_package_info['owner'] == target_package_info['owner']:
                return target_package_info
            else:
                print("waring: not same owner!")
    return None


def UpdatePackageInfoLine(line,curent_package_info, target_package_info ):
    updated_line =  line.replace(curent_package_info['version'], target_package_info['version'])
    if curent_package_info['channel']:
        updated_line =  updated_line.replace(curent_package_info['channel'], target_package_info['channel'])
    return updated_line

is_changed = False
def UpdatePackageInfoLines(lines, target_package_infos):
    global is_changed
    for idx, line in enumerate(lines):
        curent_package_info = ParsePackageInfoLine(line)
        if curent_package_info:
            target_package_info =FindTargetPackageInfo(curent_package_info, target_package_infos)
            if target_package_info:
                lines[idx] = UpdatePackageInfoLine(line,curent_package_info, target_package_info)
                is_changed=True
       

    return lines


test_target_text='''asio/1.25.0
hello/2.3.4@world/stable
good/1.0.1@boy/snapshot

1.修复一些已知问题
2.优化性能
'''

def GetTargetText():
    #return test_target_text
    return pyperclip.paste()


c = 0
def PrintStar():
    star_count = 20
    global c
    c = c % star_count
    tips = "请复制包含conan包文本到剪贴板"
    dots = tips +" " + ("." * (c+1))
    dots = dots.ljust(star_count + 20, ' ')
    print(dots, end="", flush=True)
    print("\r", end="")
    c+=1


file_list = ['conanfile.py','conanfile.txt']
conanfile = ''
def EnvCheck():
    # 检测是否有conan文件
    global conanfile
    for file_name in file_list:
        if os.path.exists(file_name):
            conanfile = file_name
            break
    if not conanfile :
        print(f"未找到文件:{file_list}") 





def main():
    EnvCheck()

    target_package_infos = []
    while True:
        target_text = GetTargetText()
        target_package_infos = ParsePackageInfoText(target_text)
        if target_package_infos:
            break
        else:
            PrintStar()
            time.sleep(0.3)
        
    print("\033[K")


    print(f'输入字符串:\n{target_text}')

    with open(conanfile, "r") as inf:
        input_lines = inf.readlines()
        updated_lines = UpdatePackageInfoLines(input_lines,  target_package_infos)

        if is_changed:
            #写回原文件，替换文本
            with open(conanfile, 'w', newline=GetNewlineType(conanfile)) as outf:
                outf.writelines(updated_lines)

            # 检测是否是git项目，若是则打印修改项
            if IsGitRepoRecursively(os.getcwd()):
                diff = Diff(conanfile)
                print(f'修改项:\n{diff}')
        else:
            print("无修改")

   




if __name__ == "__main__":
    EnvCheck()
    Main()

