# print("Hello Word"," India")
# print()
# name="Manoj Kumar"
# age=32
# city="Amethi"
# print("Welcome=:",name)
# print("Your age is=:",age);
# print("Your city name is=:",city);
# Print program to sum two numbers 
# num1=input("Please enter first number=");
# num2=input("Please enter second number=");
# sum = int(num1) + int(num2);
# print("Sum of two number is:",sum)

# if(num1 > num2):
#     print(True);
# else:
#     print(False)
# day= 10

# if day == 10:
#     print("hi")
# elif day == 1:
#   print("wrong")    
# else:
#     print('bye')  

# value =11
# for i in range(1,value):
#     print(i*2)
# arr = [2,3,4]
# for i in  arr:
#     print(i)
# str = "Hello"
# for st in str:
#     print(st)
# for i in range(1, 6):
#     if i == 3:
#         continue
#     print(i)
# arr = [34,5,2,3]
# print(len(arr))
# print(len("hello"))
# for i in range(len(arr)):
#     for j in range(len(arr)):
#        if arr[i] < arr[j]:
#            temp = arr[i]
#            arr[i]=arr[j]
#            arr[j]=temp
# print(arr)           

# reveser string 
# str= "Hello"
# rev = ""
# for ch in str:
#     rev = ch+rev
# print(rev)    

# s = "hello"
# rev = "".join(reversed(s))

# print(rev)

# s = "hello"
# i = len(s) - 1
# rev = ""

# while i >= 0:
#     rev += s[i]
#     i -= 1

# print(rev)

# sum two numbers using function
# def sum(a,b):
#     print("sum of two numbers is=",(a+b))

# sum(2,3)
# # return data from function
# def yourName():
#     return "My name is manoj"
# print("What is your name=",yourName())

# class Person:
#   def __init__(self,name,age):
#     self.name=name
#     self.age=age
# p1=Person("Manoj",23)
# print(p1.name,p1.age)

# data = {"name": "mnoj", "age": 24}

# print(data["name"])
# print(data["age"])

# import json

# json_data = '{"name":"shivm","age":24}'

# data = json.loads(json_data)

# print(data["name"])

# js_string = json.dumps(data);
# print(js_string)
# print(type(js_string))
# if type(js_string) == int:
#   print("It is string")
# else:
#   print("Not integer value")

# file read 
# with open("my.txt","r+") as file:
#     data=file.read()
#     print("File saved content is=",data)
#     file.write("\nI am from U.P")
#     file.seek(0)
#     final_data=file.read()
#     print("Final saved content is=",final_data)
# line by line
# with open("my.txt", "r") as file:
#     lines = file.readlines() # read lines
#     print(lines[0])  # reads only first line
    # for line in file:
    #     print(line.strip())