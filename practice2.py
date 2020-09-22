print("....game....")
temp=input("猜数字？\n")
guess=int(temp)
if guess==8:#此处冒号的作用是使下一行自动缩进
    print("你猜对了！")
else:
    print("猜错了。")
print("game over")