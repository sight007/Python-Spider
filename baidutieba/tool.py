__author__ = 'GZH'
import re

class Tool:
      #除去img标签，7位长空格
      removeImg = re.compile('<img.*?>| {7}|')
      #删除超链接标签
      removeAddr = re.compile('<a.*?>|</a>')
      #把换行标签改为 \n
      replaceLine = re.compile('<tr>|<div>|</div>|</p>')
      #将表格制表符<td>替换为 \t
      replaceTD = re.compile('<td>')
      #把段落开头换为 \n加两个
      replacePara = re.compile('<p.*?>')
      #把换行符或者双换行符换为 \n
      replaceBR = re.compile('<br><br>|<br>')
      #将其余标签剔除
      removeExtraTag = re.compile('<.*?>')

      def replace(self, x):
            x = re.sub(self.removeImg, '', x)
            x = re.sub(self.removeAddr, '', x)
            x = re.sub(self.replaceLine, '\n', x)
            x = re.sub(self.replaceTD, '\t', x)
            x = re.sub(self.replacePara, '\n', x)
            x = re.sub(self.replaceBR, '\n', x)
            x = re.sub(self.removeExtraTag, '', x)
            #将前后多余的空格去掉
            return x.strip()
