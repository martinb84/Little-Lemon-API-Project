The Django app called LittleLemonAPI is a fully functioning API project for the Little Lemon restaurant so that the client application developers can use the APIs to develop web and mobile applications. People with
different roles are able to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders. 
The endpoints have an authorization level. Both function and class-based views are used in this project. There are three user groups: manager, delivery crew, and users not assigned to a group which are considered 
customers. Error messages with appropriate HTTP status codes for specific errors are displayed. These include when someone requests a non-existing item, makes unauthorized API requests, or sends invalid data in a 
POST, PUT or PATCH request. Proper filtering, pagination and sorting capabilities for /api/menu-items and /api/orders endpoints are implemented. 
Finally, some throttling for the authenticated users and anonymous or unauthenticated users is applied.
