# from typing import List
#if you are beginner for every aspect of this code comment the rest of the sections you are not working on to avoid confusion 
# and focus on the one you are working on this prevent unecessary errors and also helps you to understand the code better.
# def get_full_name(first_name, last_name):
#     full_name =  first_name.title() + " " + last_name.title()
#     return full_name


# print(get_full_name("Alex","Ametepey"))

#TRYING WIHT TYPE HINT: This makes the work easier by helping the autocomplete provide more suggestions with what we are doing.
# def get_full_name2(firstname2: str, last_name2: str):
#     full_name2 = firstname2.title() + " " + last_name2.title()
#     return full_name2

# print(get_full_name2("John","Pinto"))

#USING IT FOR DATA TYPES   HAVING CHALLENGES WITH THIS CODE WILL COME BACK TO IT 
# def process_items(items: list[str]):
#     for item in items:
#         return item.title()

# print(process_items(["waakye", "fish", "egg stew","rice"]))

# def process_items(prices: dict[str,float]):
#     for item_name, item_price in prices.items():
#         print(item_name)
#         print(item_price)

# print(process_items({"food" : 27.5, "rent": 14000

# }))

#Using the Union 
# def process_item(item: int | str):
#     return item.title()

# print(process_item("halidu"))


# def say_hi(name: str | None):
#     if name is not None:
#         return(f"Hey i am {name}")
#     else:
#         return("hello world")
       
# message = say_hi("alidu")
# print(message.title())

# def say_hello(name: str):
#     print(f"hello, my name is {name}.How are you doing?")
#     return name.title()


#hint/ Annotations on Classes 
class Person:
    def __init__(self, name: str):
        self.name = name


