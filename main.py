import os
import pandas as pd
import tkinter
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
                   'Website': ['Meesho'], 'Date': pd.Timestamp.now()}

        inventory_df = pd.DataFrame(data)   
        dispatch_df = pd.DataFrame(row)   
        
        if not os.path.exists('data'):
            os.makedirs('data')
            inventory_df.to_csv(INVENTORY_DATA_PATH, index=False)
            dispatch_df.to_csv(DISPATCH_DATA_PATH, index=False)

def changeInventoryQuantity(productCode, actionStr):

    report = ""

    inventory_df = pd.read_csv(INVENTORY_DATA_PATH)
    product_codes = list(inventory_df['ProductCode'])

    if productCode in product_codes:
        quantity = inventory_df[inventory_df['ProductCode']
                                == productCode]['Quantity']
        quantity = int(quantity)

        if(actionStr == 'return'):
            quantity += 1
        else:
            quantity -= 1
        
        inventory_df.loc[inventory_df['ProductCode']
                            == productCode, 'Quantity'] = quantity

        report = f'{productCode} updated. Current Quantity {quantity}'
        inventory_df.to_csv(INVENTORY_DATA_PATH, index=False)
    else:
        report = 'Invalid Product Code'

    return report

def returnFunc(product_var, message):
    productCode = product_var.get()

    report = ""
    if(productCode == ""):
        report = "Enter Product Code"
    else:
        report = changeInventoryQuantity(productCode, 'return')
        
    message['text'] = report
    product_var.set("")

def dispatchFunc(product_var, website_var, message):
    productCode = product_var.get()
    website = website_var.get()
    
    report = ""

    if(productCode == "" or website == ""):
        report = "Enter Both Fields"
    else:
        r1 = changeInventoryQuantity(productCode, 'dispatch')
        if(r1 != 'Invalid Product Code'):
            # ADD TO DISPATCH DATA
            df = pd.read_csv(DISPATCH_DATA_PATH)
            row = {'ProductCode': productCode,
                   'Website': website, 'Date': pd.Timestamp.now()}
            df = df.append(row, ignore_index=True)
            df.to_csv(DISPATCH_DATA_PATH, index=False)
            report = r1

        else:
            report = 'Invalid Product Code'
    
    message['text'] = report
    product_var.set("")

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
            row = {'ProductCode': productCode, 'Quantity': quantity}
            inventory_df = inventory_df.append(row, ignore_index=True)
            report = f'{productCode} added. Current Quantity {quantity}'
            inventory_df.to_csv(INVENTORY_DATA_PATH, index=False)

    message2['text'] = report
    new_product_var.set("")
    new_product_quantity.set("")

def createGUI():
    
    # ROOT and Variables
    root = tkinter.Tk()

    product_var = tkinter.StringVar()
    new_product_var = tkinter.StringVar()
    new_product_quantity = tkinter.StringVar()
    website_var = tkinter.StringVar()
    
    #Canvas/Background
    canvas = tkinter.Canvas(root, height=600, width=600, bg="white")
    canvas.pack()

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

    message = tkinter.Label(frame, width=40, text="Message",  font=(
    'calibre', 15, 'normal'), bg="white")
    message.place(relx=0.08, rely=0.3)

    dispatchButton = tkinter.Button(
    frame, text="Dispatched", command= lambda : dispatchFunc(product_var, website_var, message)).place(relx=0.58, rely=0.2)

    returnButton = tkinter.Button(
    frame, text="Returned", command=lambda : returnFunc(product_var, message)).place(relx=0.8, rely=0.2)

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

    root.mainloop()


def EasyIMS():
    checkDB()
    createGUI()

if __name__ == '__main__':
    EasyIMS()
