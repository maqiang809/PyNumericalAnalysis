#字符串
str="""eer
err
eer
er
yy
yy"""#跨越多行的字符串使用三重引号字符串
print(str)
str="let's go!"
print(str)
str='let\’s go!'#反斜杠对‘进行转义
print(str)
str="C:\sdd\dff\ggg"
print(str)
str='C:\\sdd\\dff\\ggg'  #反斜杠对自身转义
print(str)
str=r'C:\sdd\dff\ggg' #利用原始字符串r进行转义，但是不能对最后的反斜杠进行转义
print(str)