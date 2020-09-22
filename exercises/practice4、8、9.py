#while循环

"""
import random #导入random模块
secret=random.randint(1,10)#随机从1到10产生一个随机数
print("....game....")
temp=input("猜数字？\n")
guess=int(temp)
while guess != secret:#while循环
    if guess >secret:
        temp=input("大了，大了，请重新输入：")
    else:
        temp=input("小了，小了，请重新输入：")
    guess = int(temp)#将temp转化为整数？
print("猜对了！")
print("game over")#三对单引号或者双引号进行多行注解
"""

  #if-else

"""
score=int(input("请输入你的分数："))
if 100>score>=90:
    print("A")
else:
    if 90>score>=80:
        print("B")
    else:
        if 80>score>=60:
            print("C")
        else:
            if 60>score>=0:
                print("D")
            else:
                print("输入错误")
"""
 #else if合并为elif
"""
score=int(input("请输入你的分数："))
if 100>score>=90:
    print("A")
elif 90>score>=80:
    print("B")
elif 80>score>=60:
    print("C")
elif 60>score>=0:
    print("D")
else:
    print("输入错误!")
"""
 #关键字assert(断言）,一般来说，我们可以利用assert在程序中置入检查点，当需要确保程序中某个条件一定为真才能让程序正常工作的话，assert关键字就非常有用
 #assert 3>4

#for
a="gdywu"
for i in a:
 print(i,end=" ")