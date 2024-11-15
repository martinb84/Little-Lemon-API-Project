The Django app called LittleLemonAPI is a fully functioning API project for the Little Lemon restaurant so that the client application developers can use the APIs to develop web and mobile applications. People with
different roles are able to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders. 
The endpoints have an authorization level. Both function and class-based views are used in this project. There are three user groups: manager, delivery crew, and users not assigned to a group which are considered 
customers. Error messages with appropriate HTTP status codes for specific errors are displayed. These include when someone requests a non-existing item, makes unauthorized API requests, or sends invalid data in a 
POST, PUT or PATCH request. Proper filtering, pagination and sorting capabilities for /api/menu-items and /api/orders endpoints are implemented. 
Finally, some throttling for the authenticated users and anonymous or unauthenticated users is applied.

In this project, the APIs make it possible for the end-users to perform certain tasks and have the following functionalities:

1.	The admin can assign users to the manager group

2.	You can access the manager group with an admin token

3.	The admin can add menu items 

4.	The admin can add categories

5.	Managers can log in 

6.	Managers can update the item of the day

7.	Managers can assign users to the delivery crew

8.	Managers can assign orders to the delivery crew

9.	The delivery crew can access orders assigned to them

10.	The delivery crew can update an order as delivered

11.	Customers can register

12.	Customers can log in using their username and password and get access tokens

13.	Customers can browse all categories 

14.	Customers can browse all the menu items at once

15.	Customers can browse menu items by category

16.	Customers can paginate menu items

17.	Customers can sort menu items by price

18.	Customers can add menu items to the cart

19.	Customers can access previously added items in the cart

20.	Customers can place orders

21.	Customers can browse their own orders
