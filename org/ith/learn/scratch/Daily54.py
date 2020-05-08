import collections
import os
import sys
import time
from xml.dom import minidom

from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.scratch.Trans535 import big_dict
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd, XmlStdin, gener_dict_by_path
import re
import difflib
from xml.dom.minidom import parse
import xml.dom.minidom

"""

from xml.dom.minidom import parse
import xml.dom.minidom
 
# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("movies.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("shelf"):
   print "Root element : %s" % collection.getAttribute("shelf")
 
# 在集合中获取所有电影
movies = collection.getElementsByTagName("movie")
 
# 打印每部电影的详细信息
for movie in movies:
   print "*****Movie*****"
   if movie.hasAttribute("title"):
      print "Title: %s" % movie.getAttribute("title")
 
   type = movie.getElementsByTagName('type')[0]
   print "Type: %s" % type.childNodes[0].data
   format = movie.getElementsByTagName('format')[0]
   print "Format: %s" % format.childNodes[0].data
   rating = movie.getElementsByTagName('rating')[0]
   print "Rating: %s" % rating.childNodes[0].data
   description = movie.getElementsByTagName('description')[0]
   print "Description: %s" % description.childNodes[0].data

"""


def main():
    xml_path = '/Users/lightman_mac/.gradle/caches/transforms-1/files-1.1/kmobile-takeout-ui-1.1.60-SNAPSHOT.aar' \
               '/a02af6608f1913eb7acab91f26add209/res/values/values.xml'

    xml_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/incremental/mergeOfficialEnvGrdResources/merged.dir/values/values.xml'

    value_tag_dict = gener_dict_by_path(xml_path)

    # create_xml_doc(value_tag_dict, out_path='/Users/lightman_mac/Desktop/tanghao/values_cn_arr_sort.xml')

    pass


if __name__ == '__main__':
    main()
