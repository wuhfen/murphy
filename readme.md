# readme

## 测试一下先写个readme吧

hello

~~~bash
git status
git add file
git commit -m "comment"
git checkout -b dev
git branch
git rm file
git log
git reflog
git diff file
git reset --hard HEAD^
git remote add origin git@github.com:michaelliao/learngit.git
git clone git@https://murphy.git
git push origin master
git push -u origin master第一次推送master分支的所有内容
~~~

> Git鼓励大量使用分支：
>
> 查看分支：`git branch`
>
> 创建分支：`git branch `
>
> 切换分支：`git checkout `
>
> 创建+切换分支：`git checkout -b `
>
> 合并某分支到当前分支：`git merge `
>
> 删除分支：`git branch -d `

~~~bash
git branch dev
git checkout dev
$ git checkout master
Switched to branch 'master'
git merge dev
$ git add readme.txt 
$ git commit -m "add merge"
[dev 6224937] add merge
 1 file changed, 1 insertion(+)
$ git merge --no-ff -m "merge with no-ff" dev
Merge made by the 'recursive' strategy.
 readme.txt |    1 +
 1 file changed, 1 insertion(+)
~~~



