## Inspiration

Nowadays, most retailers and wholesalers are moving to E-Commerce websites to expand their business and increase sales. The process of selling products online is easy as you only need to pack the product, the delivery executive of the E-Commerce company will pick it from your shop/godown and it'll be delivered. But there is one major issue, that is managing your inventory across all the E-Commerce websites that you use as a seller. Most E-Commerce websites provide their own Inventory-Management-System(IMS) and it is updated when you sell a product, but it won't update your inventory on other E-Commerce platforms. So, most sellers have to manually update the inventory on all E-Commerce websites they are using, this is a time consuming task and might result in errors. 

Another inspiration is that the IMS softwares that are available in the market are very complex for 30-40 year old sellers who are moving to E-Commerce websites. Most IMS systems comes with many features and thus makes it difficult for a middle-ages person to understand. 

## What it does

EasyIMS can tackle the above two difficulties faced by the sellers. It is very basic and easy to understand. A seller just need to enter products in their inventory and update it when a product is dispatched or returned. And it'll take only one click to update the inventory across E-Commerce Platforms. 

P.S : Only Flipkart is integrated right now.

## How we built it

It is a Python desktop app. GUI is built using tkinter library, Pandas is used for CRUD operations and data is saved in CSV files.

## What's next for EasyIMS

Next tasks are :

1. I'm also storing product Dispatch Data in a CSV. But it is not used anywhere. I thought I'll create a system to predict future sales using ML but other things took a lot of time. Using ML is next.
2. Integrating with other E-Commerce websites. Currently, it is only integrated with Flipkart. 

## Instructions

1. Download the repository.

2. If you have Python, Pandas installed directly run the main.py file. Else, Install Miniconda then run :
    ```
    conda env create -n EasyIMS python
    pip install -r requirements.txt
    python main.py
    ```
    
