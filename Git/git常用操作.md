# git常用命令操作

## 1. git常用命令操作

### 1.1. git常用命令

- git init: 初始化一个本地仓库
- git add: 添加文件到暂存区
  - git add .: 添加所有文件到暂存区
  - git add -A: 添加所有文件到暂存区
  - git add -u: 添加已经被跟踪的文件到暂存区
- git commit: 提交文件到本地仓库
  - git commit -m "message": 提交文件到本地仓库并添加提交信息
  - git commit --amend: 修改上一次提交的信息
  - git commit -a: 跳过add步骤，直接提交到本地仓库
- git status: 查看文件状态
- git diff: 查看文件修改内容

### 1.2. git分支操作

- git branch: 查看分支
- git checkout: 切换分支
- git merge: 合并分支
- git branch -d: 删除分支

### 1.3. git远程操作

- git remote add origin: 添加远程仓库
- git push: 推送到远程仓库
  - git push -u origin master: 推送到远程仓库并关联本地仓库
  - git push origin --delete branchName: 删除远程分支
  - git push origin :branchName: 删除远程分支
  - git push origin --all: 推送所有分支
  - git push origin --tags: 推送所有标签
  - git push origin master: 推送master分支
- git pull: 从远程仓库拉取
- git clone: 克隆远程仓库

### 1.4. git标签操作

- git tag: 查看标签
- git tag -a: 创建标签
- git tag -d: 删除标签
- git push origin --tags: 推送标签到远程仓库

