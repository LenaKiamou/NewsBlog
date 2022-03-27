# Final Project
Web Programming with Python and JavaScript

## Introduction
A web application that simulates a news blog platform. In this platform, readers can search and view all the articles. The 'authors' group is able to compose new articles and last the 'editors' group is responsible for the final check and publish.


### Distinctiveness and Complexity
- Register/Login/Logout with error checking
- Django groups implementation
- CRUD operations for articles 
- Models for Category,Author,Reader and Article
- Search field for articles
- Different users for 'editors', 'authors' and 'readers' with different authorities and restrictions
- Decorator for access denial to unauthorized users
- JavaScript for better user interface
- Mobile responsiveness
- Bootstrap and CSS beautification

## Project Structure
### Static
##### images 
The background image and the authors' pictures
##### news
article.js: JavaScript code for edit function
style.css: CSS for the website

### Forms
NewArticle: form for creating a new unpublished article

### Views
The common views of the website for all the groups:
- index: Displays the latest 9 articles
- login_view
- logout_view
- news_view: Displays all the published articles
- article_view: The whole view of a specific article
- profile_view: Displays all the published articles by a specific author
- search: Using POST method get the given query and check through all the published articles if the query contained in the title or in the content
- category_view: For every category displays all the published articles
- authors_view: Display all the details about the authors(image-name-mini biografy)

Additional views for the 'Readers':
- register
- follow: Allow the Reader-user to follow an Author-user
- favorites: Displays all the published articles by following Author-users

Additional views for the 'Authors':
- create: Using POST method is able to create a new article
- edit: Via json is able to edit an unpublished article

Additional views for the 'Editors':
- edit: Via json is able to edit an unpublished article
- publish: Allow an 'editor' to publish an article
- delete: Allow an 'editor' to delete a published article
- unpublished: Displays all the unpublished articles


### Models
- Category: Model for caterogies
- Author: Model for authors with bio, picture and foreign key to User 
- Reader: Model for readers with ManyToMany key to authors for following and foreign key to User
- Article: Model for articles with title, content, created day, category, published flag and foreign key to Author

### Decorators
allowed_users: a decorator to restrict access to website functions based on the user's group 

### Templates
- article.html: displays the whole article with title, date, content, author and 3 buttons depend on the request user. An author can 'edit' his own article only if it is not published yet. Otherwise the button is not available. An editor can 'edit' every unpublished article. Also the 'editors' group is responsible to 'publish' them and after that is able to 'delete' them.
- articles.html: the common template for every page that displays articles.
- authors.html: the template for the authors list with the name, the image and a mini biografy. Also only for the 'readers' is available a 'follow' button.
- create.html: the template for the form (only available to the authors).
- index.html: the home page with the latest news(9).
- layout.html
- login.html
- pagination.html
- profile.html: displays all the published articles by a specific author.
- register.html

### How to run the application
- You can register as a reader user. 
- Browse through our categories and read our articles.
- Search for related to the given query articles.
- Visit the 'Authors' link on the footer to view all the staff members and follow them to have all the articles appear in 'My favorites'.
- Create an author user through the admin page and login.
- Create/Edit your articles
- Create an editor user through the admin page and login.
- Visit 'Unpublished articles' link in the navbar.
- Read through the unpublished article, correct it and publish it.
- You have the option to delete any published article.
