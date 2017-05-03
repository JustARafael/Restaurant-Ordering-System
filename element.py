import pandas
import numpy
from collections import Counter
from tkinter import messagebox

import shop

def get_balance(uid):
    users_database = pandas.read_csv("data/users.csv")
    users_balance_database = users_database["balance"].values
    users_uid_database = users_database["uid"].values
    i=0
    for e in users_uid_database:
        if e == uid:
            return users_balance_database[i]
        i+=1

def get_order_list():
    order_database = pandas.read_csv("data/order.csv")
    order_statues = order_database["status"].values
    order_number = order_database["ddid"].values
    temp_orderlist = []
    i=0
    for x in order_statues:
        if x == -1:
            temp_orderlist.append(order_number[i])
        i+=1
    return temp_orderlist

def get_pending_registrations():
    users_database = pandas.read_csv("data/users.csv")
    users_approved_database = users_database["approved"].values
    users_username_database = users_database["username"].values
    temp_list = []
    i=0
    for s in users_approved_database:
        if s == 0:
            temp_list.append(users_username_database[i])
        i+=1
    return temp_list

def get_pending_complaints():
    complaints_database = pandas.read_csv("data/complaints.csv")
    complaints_approval_database = complaints_database["approval"].values
    complaints_cnid_database = complaints_database["cnid"].values
    temp_list = []
    i=0
    for c in complaints_approval_database:
        if c == 0:
            temp_list.append(complaints_cnid_database[i])
        i+=1
    return temp_list

def get_pending_compliments():
    compliments_database = pandas.read_csv("data/compliments.csv")
    compliments_approval_database = compliments_database["approval"].values
    compliments_cpid_database = compliments_database["cpid"].values
    temp_list = []
    i=0
    for c in compliments_approval_database:
        if c == 0:
            temp_list.append(compliments_cpid_database[i])
        i+=1
    return temp_list

def get_comment_content(id,num):
    if num == 1:
        compliments_database = pandas.read_csv("data/compliments.csv")
        comment_database = compliments_database["comment"].values
        cpid_database = compliments_database["cpid"].values
        i=0
        for c in cpid_database:
            if c == int(id):
                return comment_database[i]
            i+=1
    else:
        complaints_database = pandas.read_csv("data/complaints.csv")
        comment_database = complaints_database["comment"].values
        cnid_database = complaints_database["cnid"].values
        i=0
        for c in cnid_database:
            if c == int(id):
                return comment_database[i]
            i+=1

def get_comment(t, num):
    if t == 1:
        compliments_database = pandas.read_csv("data/compliments.csv")
        compliments_database = compliments_database.loc[compliments_database["approval"] == num]
        return compliments_database["cpid"].values
    else:
        complaints_database = pandas.read_csv("data/complaints.csv")
        complaints_database = complaints_database.loc[complaints_database["approval"] == num]
        return complaints_database["cnid"].values

def get_users(num):
    if num == 0:
        approved_database = pandas.read_csv("data/users.csv")
        return approved_database["username"].values
    else:
        approved_database = pandas.read_csv("data/users.csv")
        approved_database = approved_database.loc[approved_database["approved"] == num]
        return approved_database["username"].values

def get_menu_list():
    did_database = pandas.read_csv("data/dish.csv")
    return (list(reversed(did_database.sort_values("time")["did"].values)))

def get_image_list():
    path_database = pandas.read_csv("data/dish.csv")
    return (list(reversed(path_database.sort_values("time")["path"].values)))

def get_name_list():
    name_database = pandas.read_csv("data/dish.csv")
    return (list(reversed(name_database.sort_values("time")["dish"].values)))

def get_price_list():
    price_database = pandas.read_csv("data/dish.csv")
    return (list(reversed(price_database.sort_values("time")["price"].values)))

def get_top_listing(uid):
    delivery_database = pandas.read_csv("data/order.csv")
    delivery_database = delivery_database.loc[delivery_database["uid"] == uid]
    delivery_database = delivery_database.loc[delivery_database["status"] == 1]
    did_list = []
    for e in delivery_database["order"].values:
        did_list+=e.split(",")
    did_list = [int(x) for x in did_list]
    count = Counter(did_list)
    did_list = sorted(sorted(did_list), key=count.get, reverse=True)
    set_did_list = []
    for e in did_list:
        if len(set_did_list) == 0:
            set_did_list.append(e)
        else:
            if set_did_list[-1] != e:
                set_did_list.append(e)
    return set_did_list

def menu_check(num):
    uid_database = pandas.read_csv("data/menu.csv")
    uid_database = uid_database.loc[uid_database["uid"] == num]["uid"].values
    if len(uid_database) == 1:
        return True
    else:
        return False

def get_chef_employee():
    chef_database = pandas.read_csv("data/users.csv")
    chef_database = chef_database.loc[(chef_database["level"]==4) & (chef_database["approved"] == 1)]["uid"]
    return chef_database

def get_deliver_employee():
    deliver_database = pandas.read_csv("data/users.csv")
    deliver_database = deliver_database.loc[(deliver_database["level"]==3) & (deliver_database["approved"] == 1)]["uid"]
    return deliver_database

def profile(uid):
    profile_database = pandas.read_csv("data/users.csv")
    username = str(profile_database.loc[profile_database["uid"]==uid]["username"].values[0])
    balance = str(int([profile_database.loc[profile_database["uid"]==uid]["balance"].values][0]))
    email = str(profile_database.loc[profile_database["uid"]==uid]["email"].values[0])
    warning = str(profile_database.loc[profile_database["uid"]==uid]["warning"].values[0])
    return [username,balance,email,warning]

def deposit_money(amount,uid):
    if shop.check_quantity(amount):
        result = messagebox.askyesno("Confirm Deposit", "Deposit amount: "+str((amount)))
        if result:
            temp = pandas.read_csv("data/users.csv")
            temp.loc[temp["uid"]==uid, "balance"] += int(amount)
            temp.to_csv("data/users.csv", index=False)

def get_edit_menu(uid):
    menu_file = pandas.read_csv("data/menu.csv")
    did = menu_file.loc[menu_file["uid"]==uid]["did"].values
    dish_file = pandas.read_csv("data/dish.csv")
    dish_list = dish_file["did"].values
    available_list = match(dish_list,did)
    added_list = match(did,available_list)
    return (available_list,added_list)

def match(a,b):
    return [x for x in a if x not in b]

def save_edit_menu(dish, uid):
    current_menu = pandas.read_csv("data/menu.csv")
    current_menu = current_menu[current_menu.uid != uid]
    check_table = pandas.read_csv("data/dish.csv")
    current_menu_uid_list = current_menu["uid"].values.tolist()
    current_menu_did_list = current_menu["did"].values.tolist()
    current_menu_time_list = current_menu["time"].values.tolist()
    current_menu_dish_list = current_menu["dish"].values.tolist()
    current_menu_price_list = current_menu["price"].values.tolist()
    current_menu_path_list = current_menu["path"].values.tolist()
    for e in dish:
        if e != -1:
            current_menu_uid_list.append(uid)
            current_menu_did_list.append(e)
            current_menu_time_list.append(int(check_table.loc[check_table["did"]==e]["time"]))
            current_menu_dish_list.append(str(check_table.loc[check_table["did"]==e]["dish"].values[0]))
            current_menu_price_list.append(int(check_table.loc[check_table["did"]==e]["price"]))
            current_menu_path_list.append(str(check_table.loc[check_table["did"]==e]["path"].values[0]))
    current_menu_uid_list.append(uid)
    current_menu_did_list.append(-1)
    current_menu_time_list.append(0)
    current_menu_dish_list.append("etc")
    current_menu_price_list.append(0)
    current_menu_path_list.append("images/etc/gif")
    write = pandas.DataFrame({"uid": current_menu_uid_list,
                            "did": current_menu_did_list,
                            "time": current_menu_time_list,
                            "dish": current_menu_dish_list,
                            "price": current_menu_price_list,
                            "path": current_menu_path_list})
    write = write[["uid",
                    "did",
                    "time",
                    "dish",
                    "price",
                    "path"]]
    write.to_csv("data/menu.csv", index=False)

def get_ddid_list(uid):
    ddid_list = pandas.read_csv("data/order.csv")
    ddid_list = ddid_list.loc[(ddid_list["uid"]==uid) & (ddid_list["rated"]==0)]["ddid"].values
    return ddid_list

def get_did_list(ddid):
    ddid_file = pandas.read_csv("data/order.csv")
    ddid_list = (ddid_file.loc[ddid_file["ddid"]==int(ddid)]["order"].values[0]).split(",")
    ddid_list = set([int(x) for x in ddid_list])
    return ddid_list

def save_comment(delivery_rating, food_rating, uid, did_list, comment):
    if int((delivery_rating+food_rating)/2) < 3:
        complaints = pandas.read_csv("data/complaints.csv")
        if comment != "":
            complaints_uid_list = complaints["uid"].values.tolist()
            complaints_comment_list = complaints["comment"].values.tolist()
            complaints_cnid_list = complaints["cnid"].values.tolist()
            complaints_did_list = complaints["did"].values.tolist()
            complaints_approval_list = complaints["approval"].values.tolist()
            for e in did_list:
                complaints_uid_list.append(uid)
                complaints_comment_list.append(str(comment))
                complaints_cnid_list.append(complaints_cnid_list[-1]+1)
                complaints_did_list.append(int(e))
                complaints_approval_list.append(0)
            write = pandas.DataFrame({"uid": complaints_uid_list,
                                    "comment": complaints_comment_list,
                                    "cnid": complaints_cnid_list,
                                    "did": complaints_did_list,
                                    "approval": complaints_approval_list})
            write = write[["uid",
                            "comment",
                            "cnid",
                            "did",
                            "approval"]]
            write.to_csv("data/complaints.csv", index=False)
    else:
        compliments = pandas.read_csv("data/compliments.csv")
        if comment != "":
            compliments_uid_list = compliments["uid"].values.tolist()
            compliments_comment_list = compliments["comment"].values.tolist()
            compliments_cpid_list = compliments["cpid"].values.tolist()
            compliments_did_list = compliments["did"].values.tolist()
            compliments_approval_list = compliments["approval"].values.tolist()
            for e in did_list:
                compliments_uid_list.append(uid)
                compliments_comment_list.append(str(comment))
                compliments_cpid_list.append(compliments_cpid_list[-1]+1)
                compliments_did_list.append(int(e))
                compliments_approval_list.append(0)
            write = pandas.DataFrame({"uid": compliments_uid_list,
                                    "comment": compliments_comment_list,
                                    "cpid": compliments_cpid_list,
                                    "did": compliments_did_list,
                                    "approval": compliments_approval_list})
            write = write[["uid",
                            "comment",
                            "cpid",
                            "did",
                            "approval"]]
            write.to_csv("data/compliments.csv", index=False)

def delivery_rating(rate, ddid):
    order = pandas.read_csv("data/order.csv")
    order.set_value(int(ddid), "rate", rate)
    order.set_value(int(ddid), "rated", 1)
    order.to_csv("data/order.csv", index=False)

def save_rating(food_rate, did_list, level):
    star = pandas.read_csv("data/star.csv")
    for e in did_list:
        star.loc[star["did"]==e, "star"]+=(food_rate*level)
        star.loc[star["did"]==e, "number"]+=level
    star.to_csv("data/star.csv", index=False)

def comment_op(did):
    compliments_read = pandas.read_csv("data/compliments.csv")
    complaints_read = pandas.read_csv("data/complaints.csv")
    compliments_read = compliments_read.loc[compliments_read["approval"]==1]
    compliments_read = compliments_read.loc[compliments_read["did"]==did]
    complaints_read = complaints_read.loc[complaints_read["approval"]==1]
    complaints_read = complaints_read.loc[complaints_read["did"]==did]
    return_list = compliments_read["comment"].values.tolist()
    for e in complaints_read["comment"].values:
        return_list.append(e)    
    delivery_read = pandas.read_csv("data/order.csv")
    delivery_read = delivery_read.loc[delivery_read["rated"]==1]["rate"].values.tolist()
    total_delivery = 0
    for e in delivery_read:
        total_delivery+=e
    total_delivery = total_delivery/len(delivery_read)
    food_read = pandas.read_csv("data/star.csv")
    food_read = food_read.loc[food_read["did"]==did]
    if food_read["number"].values.tolist()[0] != 0:
        total_food = food_read["star"].values.tolist()[0]/food_read["number"].values.tolist()[0]
    else:
        total_food = 0
    return (return_list, round(total_food), round(total_delivery))
    