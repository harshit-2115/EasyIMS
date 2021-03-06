import os
import requests
import base64
import tkinter

import pandas as pd
from tkinter import ttk

INVENTORY_DATA_PATH = './data/inventory_data.csv'
DISPATCH_DATA_PATH = './data/dispatch_data.csv'

def checkDB():
    
    try:
        inventory_df = pd.read_csv(INVENTORY_DATA_PATH)
        df = pd.read_csv(DISPATCH_DATA_PATH)

    except Exception as e:
        print(e)

        #Temp_Data
        data = {'ProductCode' : ['PD123'], 'Quantity' : [5], 'Created_Date' : pd.Timestamp.now()}
        row = {'ProductCode': ['PD123'],
                   'Website': ['Meesho'], 'Quantity':[5] ,'Date': pd.Timestamp.now()}

        inventory_df = pd.DataFrame(data)   
        dispatch_df = pd.DataFrame(row)   
        
        if not os.path.exists('data'):
            os.makedirs('data')
            inventory_df.to_csv(INVENTORY_DATA_PATH, index=False)
            dispatch_df.to_csv(DISPATCH_DATA_PATH, index=False)

def changeInventoryQuantity(productCode, drquantity, actionStr):

    report = ""

    inventory_df = pd.read_csv(INVENTORY_DATA_PATH)
    product_codes = list(inventory_df['ProductCode'])

    if productCode in product_codes:
        quantity = inventory_df[inventory_df['ProductCode']
                                == productCode]['Quantity']
        quantity = int(quantity)

        if(actionStr == 'return'):
            quantity += drquantity
        else:
            quantity -= drquantity
            if(quantity < 0): return 'Error : Dispatch Order > Item Stock'
        
        inventory_df.loc[inventory_df['ProductCode']
                            == productCode, 'Quantity'] = quantity

        report = f'{productCode} updated. Current Quantity {quantity}'
        inventory_df.to_csv(INVENTORY_DATA_PATH, index=False)
    else:
        report = 'Invalid Product Code'

    return report

def returnFunc(product_var, dr_quantity, message):
    productCode = product_var.get()
    drquantity = int(dr_quantity.get())

    report = ""
    if(productCode == ""):
        report = "Enter Product Code"
    else:
        report = changeInventoryQuantity(productCode, drquantity, 'return')
        
    message['text'] = report
    product_var.set("")
    dr_quantity.set("")


def dispatchFunc(product_var, website_var, dr_quantity, message):
    productCode = product_var.get()
    website = website_var.get()
    drquantity = int(dr_quantity.get())

    report = ""

    if(productCode == "" or website == "" or drquantity == " "):
        report = "Enter All Fields"
    else:
        r1 = changeInventoryQuantity(productCode, drquantity, 'dispatch')
        if(r1 != 'Invalid Product Code' and r1 != 'Error : Dispatch Order > Item Stock'):
            # ADD TO DISPATCH DATA
            df = pd.read_csv(DISPATCH_DATA_PATH)
            row = {'ProductCode': productCode,
                   'Website': website, 'Quantity':drquantity, 'Date': pd.Timestamp.now()}
            df = df.append(row, ignore_index=True)
            df.to_csv(DISPATCH_DATA_PATH, index=False)
            report = r1
        else:
            report = r1
    
    message['text'] = report
    product_var.set("")
    dr_quantity.set("")

def newProductFunc(new_product_var, new_product_quantity, message2):
    report = ""
    productCode = new_product_var.get()
    quantity = new_product_quantity.get()

    if(productCode == "" or quantity == ""):
        report = "Enter both fields"
    else:
        inventory_df = pd.read_csv(INVENTORY_DATA_PATH)
        product_codes = list(inventory_df['ProductCode'])
        if productCode in product_codes:
            report = f"{productCode} product already exists."
        else:
            row = {'ProductCode': productCode, 'Quantity': quantity, 'Created_Date' : pd.Timestamp.now()}
            inventory_df = inventory_df.append(row, ignore_index=True)
            report = f'{productCode} added. Current Quantity {quantity}'
            inventory_df.to_csv(INVENTORY_DATA_PATH, index=False)

    message2['text'] = report
    new_product_var.set("")
    new_product_quantity.set("")

def getAccessCode():
    url = "https://api.flipkart.net/oauth-service/oauth/token"

    querystring = {"grant_type": "client_credentials", "scope": "Seller_Api"}

    sample_string = ""
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    headers = {
        'Authorization': "Basic " + base64_string 
    }

    response_json = requests.request("GET", url, headers=headers, params=querystring).json()
    print(response_json)
    access_token = response_json["access_token"]
    print("Your access token is : " + access_token)
    return access_token


def getUpdatedInventory(access_token):

    returnDict = {}

    inventory_df = pd.read_csv(INVENTORY_DATA_PATH)
    product_codes = list(inventory_df['ProductCode'])
    product_codes = ','.join(product_codes)
    
    headers = {
    'Authorization': 'Bearer' + access_token
    }

    url1 = f'https://api.flipkart.net/sellers/listings/v3/{product_codes}'

    response_json = requests.get(url1, headers=headers).json()
    
    if('available' in response_json):
        proddict = response_json['available']
        products = list(proddict.keys())
        for i in products:
            PID = proddict[i]['product_id']
            LID = proddict[i]['locations'][0]['id']
            up_quantity = int(inventory_df.loc[inventory_df['ProductCode'] == i, 'Quantity'])
            loc_dict = [{
                'id' : LID,
                'inventory' : up_quantity
            }]

            p_dict = {
                'product_id' : PID,
                'locations' : loc_dict
            }

            returnDict[i] = p_dict
    else:
        return 'None'
    print('/n', returnDict)
    return returnDict


    




def updateFlipkart(message2):
    report = ""
    accessCode = getAccessCode()
    data = getUpdatedInventory(accessCode)
    if(data == 'None'):
        report = 'No Matching Product Found'
    else :
        headers = {
        'Authorization': 'Bearer' + accessCode,
        'Content-Type': 'application/json'
            }
        url1 = 'https://api.flipkart.net/sellers/listings/v3/update/inventory'
        response_json = requests.request("POST", url1, headers=headers, json=data).json()
        print(response_json)
        report = 'Successfully Updated'

    message2['text'] = report 

def createGUI():
    
    # ROOT and Variables
    root = tkinter.Tk()
    root.title("EasyIMS")

    product_var = tkinter.StringVar()
    new_product_var = tkinter.StringVar()
    new_product_quantity = tkinter.StringVar()
    website_var = tkinter.StringVar()
    dr_quantity = tkinter.StringVar()
    
    #Canvas/Background
    canvas = tkinter.Canvas(root, height=600, width=600,bg="white")
    canvas.grid(column=3)

    # Form Frame
    frame = tkinter.Frame(root, bg="#263D42")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    # Upper Form
    productCode = tkinter.Label(
        frame, text="Product Code", bg="white", padx=5, pady=5, justify="left").place(x=10, y=10)

    website = tkinter.Label(
        frame, text="Website", bg="white", padx=10, pady=5, justify="left").place(x=10, rely=0.1)

    codeEntry = tkinter.Entry(frame, width=30,  font=(
        'calibre', 15, 'normal'), textvariable=product_var).place(x=125, y=10)

    websiteDD = tkinter.ttk.Combobox(
        frame, width=29, font=(
            'calibre', 15, 'normal'), textvariable=website_var, state="readonly")
    websiteDD['values'] = ('Flipkart', 'Meesho', 'Amazon')
    websiteDD.place(x=125, rely=0.1)
    websiteDD.current()

    dispatchQuantity = tkinter.Label(
        frame, text="Quantity", bg="white", padx=5, pady=5, justify="left").place(x=10, rely=0.18)
    dispatchQuantity = tkinter.Entry(frame, width=30,  font=(
        'calibre', 15, 'normal'), textvariable=dr_quantity).place(x=125, rely=0.18)


    message = tkinter.Label(frame, width=40, text="Message",  font=(
    'calibre', 15, 'normal'), bg="white")
    message.place(relx=0.08, rely=0.35)

    dispatchButton = tkinter.Button(
    frame, text="Dispatched", command= lambda : dispatchFunc(product_var, website_var, dr_quantity, message)).place(relx=0.58, rely=0.27)

    returnButton = tkinter.Button(
    frame, text="Returned", command=lambda : returnFunc(product_var, dr_quantity, message)).place(relx=0.8, rely=0.27)

    # Lower Form
    newProductCode = tkinter.Label(
    frame, text="New Product Code", bg="white", padx=5, pady=5, justify="left").place(x=10, rely=0.5)

    newCodeEntry = tkinter.Entry(frame, width=30,  font=(
        'calibre', 15, 'normal'), textvariable=new_product_var).place(x=145, rely=0.5)

    newProductQuantity = tkinter.Label(
        frame, text="Quantity", bg="white", padx=5, pady=5, justify="left").place(x=10, rely=0.57)

    newCodeQuantity = tkinter.Entry(frame, width=30,  font=(
        'calibre', 15, 'normal'), textvariable=new_product_quantity).place(x=145, rely=0.57)

    message2 = tkinter.Label(frame, width=40, text="Message",  font=(
        'calibre', 15, 'normal'), bg="white")
    message2.place(relx=0.08, rely=0.8)

    newProductButton = tkinter.Button(
        frame, text="Add Product", command=lambda : newProductFunc(new_product_var, new_product_quantity, message2)).place(relx=0.75, rely=0.65)


    updateFlipkartBtn = tkinter.Button(
        frame, text="Update on Flipkart", command=lambda :updateFlipkart(message2)).place(relx=0.33, rely=0.9)

    root.mainloop()


def EasyIMS():
    checkDB()
    createGUI()

if __name__ == '__main__':
    EasyIMS()
