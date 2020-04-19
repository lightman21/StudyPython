
1.删除编译前的主工程build目录,重新git add.待编译完成后观察分析新增文件.
2.扫描主工程build目录,得到一个merge的目录列表.merged_dir_list
3.遍历merged_dir_list根据最近修改时间排序



拉取远端 主工程i18n_5.34.10分支 app/src/main/res/values/strings.xml 文件
git archive i18n_5.34.10 --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile-Android.git app/src/main/res/values/strings.xml | tar -x


拉取远端 主工程master分支/values-en/ strings.xml  文件
git archive --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile-Android.git HEAD:app/src/main/res/values-en/ strings.xml | tar -x


 
 
