
# ***<center><font color="red"> LovinEscapades-API</font>***: The Ultimate Trip Tracking Tool!</center>
## <center> A Django web app </center>

### **Table of content:**
- [Overview](#overview)
- [Application Development](#application-development)
- [Main Features](#main-features)
- [Project Structure](#project-structure)
- [API Endponts](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Accessibility and Design](#accessibility-and-design)
- [Usage and Screenshots](#usage-and-screenshots)
- [Database Schema](#database-schema)
- [Online Validators](#online-validators)
- [Unit Testing](#unit-testing)
- [Manual Testing](#manual-testing)
- [Heroku Deployment](#heroku-deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Documentation version](#documentation-version)

## Overview
![alt text](image.png)

### **Project Description**
LovinEscapades-API is a backend solution designed to facilitate seamless trip management and social interaction for travel enthusiasts. Built with Django Rest Framework, this API provides robust user authentication, trip creation and management, image handling, and social features like following users and liking trips. It supports full CRUD (Create, Read, Update, Delete) operations for trips and images, allowing users to manage their travel experiences efficiently. The API is well-documented and adheres to RESTful principles, ensuring ease of use for developers. Future enhancements include a React frontend for an interactive user experience and potential integration with mapping libraries for enhanced trip visualization.

### **Project Inspiration**
This backend API project builds upon the knowledge and skills acquired during the development of "LovinEscapades" Django web application completed as part of Milestone Project 4 at Code Institute ([more here](https://github.com/eneliviu/LovinEscapades.git)).

### **Public Access**:
* Trip Exploration: Unregistered users might be able to view public trip locations on a map.
* Content Discovery: Access to shared trip details and images (depending on privacy settings).

### **Future Considerations**:
* User-friendly frontent React app for a interactive user experience.
* Integration with mapping libraries.
* Potential social features for user interaction and community building.

### **Disclaimer**:
This API serves as a backend foundation for a potential application.
The envisioned features and functionalities are subject to change and refinement based on further development and user feedback.


## Application development
This application was developed using an iterative approach, following Agile principles.

**User Stories & Epics**
I employed a user-centric approach, defining key epics and user stories to guide project development.

**Example Epic**:
Epic: As an API developer,
I want to implement robust and secure user authentication,
so that API consumers can securely access and interact with protected resources.

**Example User Story**:
As an API consumer,
I can authenticate with the API using JWT (JSON Web Tokens),
So that I can access protected resources and perform authorized actions.

**Key Epics**:
* User Authentication: Implement secure and reliable user authentication.
* Trip Management: Enable users to create, manage, and share trip plans.
* Social Interaction: Allow users to interact with other users and their content (e.g., liking posts, following users).
* API Documentation: Provide comprehensive and user-friendly API documentation.


All critical user stories identified as "must-have" were successfully implemented within the project timeline.

![Main menu](static/docs/Kanban.webp#center)
*<center><font color="red">LovinEscapades</font>: Github Kanban baord with project User stories*.</center><br>

![Main menu](static/docs/Kanban_detail.webp#center)
*<center><font color="red">LovinEscapades</font>: Custom template for User Stories*.</center><br>

This project builds upon the "LovinEscapades" project from Milestone Project 4 at Code Institute. It provides an opportunity to apply API development concepts and enhance my understanding of backend development principles. During development, I focused on code quality and maintainability, adhering to the DRY principle and utilizing frequent Git commits for effective version control.


[*Back to top*](#)


## Main Features

### **Robust User Registration and Authentication:**
* Utilizes JSON Web Tokens (JWT) for secure and stateless user authentication.
* Eliminates the need for server-side session management, improving security and scalability.
* The API provides token refresh endpoints for maintaining continuous user sessions without requiring frequent re-authentication.
* Implement robust user registration, login, logout, and password management functionalities.

### **Comprehensive Trip Management:**
* Enable users to create, retrieve, update, and delete their travel itineraries.
* Facilitate the upload, storage, and association of images with specific trips.
* Allow users to filter and search for trips based on various criteria, such as destination, travel dates, and user preferences.

### **Support for Location Mapping:**
* Provide trip locations as coordinates (Lat, Lon) for potentially mapping the trip itineraries

### **Engaging Social Features:**
* Empower users to connect with other travelers by following other users.
* Enable users to express their interest in trips by liking posts.

### **Well-Defined API:**
* The API adheres to RESTful principles and provides clear and concise documentation for developers.
* Includes comprehensive API documentation generated using tools like Swagger-UI and Redoc
* Provides a smooth user experience by handling errors gracefully and delivering helpful messages.

More details about the API are provided in the [Usage and Screenshots](#usage-and-screenshots) section.

[*Back to top*](#)

## Project structure

### ***Lovingescapades-API*** project consists of four apps:

### 1. `profiles`
The user profile app offers two primary sections:
- Profile update section for editing basic user information such as username, first and last name, and email address.
- Functionality for posting and deleting testimonials, which are subject to admin approval before appearing on the landing page.

### 2. `trips`
This app features the `Dashboard` page, allowing users to:
- View updated counts of trips, uploaded photos, and testimonials awaiting approval.
- Decide if new trip information will be shared publicly or kept private. Public trips are mapped on the landing page, while private trips are visible only to the authenticated user.
- Quickly access trip details through trip card elements, which provide basic trip information (destination, start and end dates, creation date) along with options to edit/delete trips and upload/delete photos.
- Display approved user testimonials on the landing page and map the locations of shared trips.

### 3. `likes`
This app provides essential functionality for site visitors to send inquiries to the site admin via a dedicated form.

### 4. `followers`
- Hosts the photo gallery where all publicly shared photos by registered users can be viewed by any visitor.
- Users can publish photos even if they choose not to make the associated trip information public.
- Each photo in the gallery includes a like icon and basic trip details, though the feature for sending and receiving likes has not been implemented yet.


[*Back to top*](#)

## API Endpoints
The following table provides an overview of the available API endpoints for the LovinEscapades-API:

| Endpoint | Method | Description | Permission |
|---|---|---|---|
| `/dj-rest-auth/registration/` | POST | Register a new user | Public |
| `/dj-rest-auth/user/` | GET | Retrieve user data | IsAuthenticated |
| `/api-auth/login/` | POST | Login a user and obtain a JWT token | Public |
| `/api-auth/logout/` | POST | Logout a user and invalidate the JWT token | IsAuthenticated |
| `/api-auth/token/refresh/` | POST | Refresh the JWT token | IsAuthenticated |
| `/profiles/` | GET | Retrieve the list of user profiles | IsAuthenticatedOrReadOnly |
| `/profiles/<id>/` | GET | Retrieve a specific user profile | IsAuthenticated (IsOwner for updating own profile) |
| `/profiles/<id>/` | PUT | Update a specific user profile | IsAuthenticated (IsOwner) |
| `/profiles/<id>/` | DELETE | Delete a specific user profile | IsAuthenticated (IsOwner) |
| `/trips/` | GET | List all shared trips | IsAuthenticatedOrReadOnly |
| `/trips/` | POST | Create a new trip | IsAuthenticated |
| `/trips/<id>/` | GET | Retrieve a specific trip | IsAuthenticatedOrReadOnly |
| `/trips/<id>/` | PUT | Update a specific trip | IsAuthenticated (IsOwner) |
| `/trips/<id>/` | DELETE | Delete a specific trip | IsAuthenticated (IsOwner) |
| `/trips/<id>/images/` | GET | List all images for a specific trip | IsAuthenticatedOrReadOnly |
| `/trips/<id>/images/` | POST | Upload a new image | IsAuthenticated (IsOwner of the trip) |
| `/trips/<trip_id>/images/<image_id>` | GET | Retrieve a specific image for a specific trip | IsAuthenticatedOrReadOnly |
| `/trips/<trip_id>/images/<image_id>` | PUT | Update a specific image for a specific trip | IsAuthenticated (IsOwner of the image) |
| `/trips/<trip_id>/images/<image_id>` | DELETE | Delete a specific image for a specific trip | IsAuthenticated (IsOwner of the image) |
| `/images/` | GET | Retrieve all shared images | IsAuthenticatedOrReadOnly |
| `/images/<id>/` | GET | Retrieve a specific image | IsAuthenticatedOrReadOnly |
| `/followers/` | GET | List all followers or follow a new user | IsAuthenticated |
| `/followers/<id>/` | GET | Retrieve a specific user | IsAuthenticatedOrReadOnly |
| `/followers/<id>/` | DELETE | Unfollow a specific user | IsAuthenticated |
| `/likes/` | GET | List all likes or like a new trip | IsAuthenticated |
| `/likes/<id>/` | GET | Retrieve a specific trip | IsAuthenticatedOrReadOnly |
| `/likes/<id>/` | DELETE | Unlike a specific trip | IsAuthenticated |


A comprehensive overview of the API endpoints, including detailed documentation, is available through [Swagger-UI](https://drf-backend-api-70211104c0c7.herokuapp.com/schema/swagger-ui/), [Redoc](https://drf-backend-api-70211104c0c7.herokuapp.com/schema/redoc/) or directly in [yaml](https://drf-backend-api-70211104c0c7.herokuapp.com/schema/) format.


![alt text](images_doc\SwaggerUI.png)
![alt text](images_doc\Redoc.png)


[*Back to top*](#)

## Technologies Used

### **Django Rest Framework:**
- A web framework made with Python that helps build web apps quickly and efficiently. It's great for managing databases and organizing code, making it easier to create complex features.

### **Geopy Python Module:**
- A library that helps find geographic coordinates, like latitude and longitude, from place names. It’s used to show trip locations accurately on the map.

### **Django graph models:**
- [Django Extensions](https://shorturl.at/GxkSs) is a collection of custom extensions for the Django Framework that can be used for creating ER (Entity-Relationship) diagrams for the project database. These diagrams make it easier to visualize, understand, and manage the database structure. You can view these database model relationships using the online [GraphViz generator](https://shorturl.at/AAuhy).

### **Python modules**
The following Python modules were installed using the `pip install` command in the terminal and were listed in the [`requirements.txt`](requirements.txt) file.

### **Markdown**
* The Markdown formatting for README.md and HELP.md files was done according to the documentation provided at
[www.markdownguide.org](https://www.markdownguide.org/basic-syntax/).

### Cloudinary serving
This project utilizes Cloudinary for efficient and secure image storage and delivery.

### Cloud deployment
* The app is currently deployed on [Heroku Cloud Application Platform](https://www.heroku.com)
* For cloud deployment, the [dependency requirements file](requirements.txt) was compiled using the following command:
```
pip freeze --local > requirements.txt
```

* The processes to run on the Heroku platform are specified in the `Procfile` file.
* Sensitive information is stored in the `env.py` file, which is listed in the `.gitignore` to prevent it from being uploaded to GitHub.
* The app can be accessed at [***LovinEscapades-api***](https://github.com/eneliviu/drf-backend-api.git).

### Local deployment
* For development or deployment on a local development, the web server can be started using the terminal command:

```
python manage.py runserver
```

[*Back to top*](#)


## Usage and Screenshots


![alt text](images_doc\image-3.png) ![alt text](images_doc\image-2.png)

**Image List View (Public)



## Entity Relationship Diagram (EDR)

The EDR for the full project database shcema was produced using the
[Graph models extention](https://shorturl.at/psHzX) and visualized using the online [GraphViz generator](https://shorturl.at/AAuhy). 

![alt text](images_doc/ERD.png)
<p align="center"><strong>EDR project database diagram</strong></p>

The database models in more detail are presented below:

<p align="center"><img src="images_doc/ProfileDB.png" alt="ProfileDB"></p>
<p align="center"><img src="images_doc/TripDB.png" alt="TripDB"></p>
<p align="center"><img src="images_doc/ImageDB.png" alt="ImageDB"></p>
<p align="center"><img src="images_doc/FollowerDB.png" alt="FollowerDB"></p>
<p align="center"><img src="images_doc/LikeDB.png" alt="LikeDB"></p>

## Online Validators

### **PEP8**
The [Pep8 CI](https://pep8ci.herokuapp.com/) Python Linter returned no errors:
| App            | File         | CI Linter Result           |  Status |
| --- | --- | --- | --- |
| `trips`        | `models.py`  |All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `serializers.py`  | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `utils.py`   | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `urls.py`    | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `views.py`   | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `profiles`     | `models.py`  | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `serializers.py`  | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `urls.py`    | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `views.py`   | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `followers`    | `models.py`   | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `serializers.py`  | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `urls.py`    | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `views.py`   | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `likes` | `models.py`   | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `serializers.py`  | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `urls.py`    | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
|                | `views.py`   | All clear, no errors found | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
---


## Unit testing
The project includes a comprehensive test suite for the Trip and Image API endpoints.
The tests are located in the `trips/tests.py` file and cover the following views:
- **TripListView**: Tests for listing trips, including handling shared and non-shared trips.
- **TripDetailView**: Tests for retrieving a specific trip using valid and invalid IDs.
- **ImageListView**: Tests for listing images associated with trips, including handling shared and non-shared images.
- **ImageDetailView**: Tests for retrieving a specific image associated with a trip using valid and invalid IDs.

The test suite includes setup methods to initialize test data and individual test methods to verify the functionality of the respective endpoints.

### Test Classes
1. **TripListViewTests**:
    * Verifies the functionality of listing trips through the `TripListView` endpoint.
    * Tests include:
        * Listing trips that are shared.
        * Handling trips that are not shared.
2. **PostDetailViewTests**:
    * Verifies the functionality of retrieving a trip through the `TripDetailView` endpoint.
    * Tests include:
        * Retrieving a trip using a valid ID.
        * Handling retrieval of a trip using an invalid ID.
3. **TripImageListViewTests**:
    * Verifies the functionality of listing images through the `ImageListView` endpoint.
    * Tests include:
        * Listing images that are shared.
        * Handling images that are not shared.
4. **TripImageDetailViewTests**:
    * Verifies the functionality of retrieving an image through the `ImageDetailView` endpoint.
    * Tests include:
        * Retrieving an image using a valid ID.
        * Handling retrieval of an image using an invalid ID.

### Running Tests
To run the tests, use the following command:
```bash
python manage.py test
```
This command will execute the test suite and display the results in the terminal.

The tests cover various scenarios to ensure the correctness and robustness of the API endpoints.

<p align="center"><strong>Table: Overview of Test Classes and Methods for the Trip and Image API Endpoints</strong></p>

| Type    | Name                                         | Description                                                                                                    | Expected Status |Result                     |
|---------|----------------------------------------------|-------------------------------------------------------------------------------------------|-------------------------------------|--------------------------|
| Class   | `TripListViewTests`                          | Test suite for the TripListView. Checks listing of trips including shared and non-shared.          | -            |
| Method  | `test_can_list_trips`                        | Verifies that trips can be listed through the TripListView endpoint.                  | Status code: 200 OK       |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| Method  | `test_can_handle_list_trips_not_shared`      | Verifies handling of trips that are not shared.                                       | Status code: 200 OK       |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| Class   | `PostDetailViewTests`                        | Test suite for the TripDetailView. Tests retrieving trips using valid and invalid IDs.| -                         |
| Method  | `test_can_retrieve_post_using_valid_id`      | Ensures a trip can be retrieved by a valid ID.                                        | Status code: 200 OK        |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| Method  | `test_can_retrieve_post_using_invalid_id`    | Ensures appropriate handling of requests with an invalid trip ID.                     | Status code: 404 Not Found |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| Class   | `TripImageListViewTests`                     | Test suite for the ImageListView. Checks listing of images including shared and non-shared. | -                    |
| Method  | `test_can_list_trip_images`                  | Verifies that images can be listed through the ImageListView endpoint.                | Status code: 200 OK        |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| Method  | `test_can_handle_list_trip_images_not_shared`| Verifies handling of images that are not shared.                                      | Status code: 200 OK        |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| Class   | `TripImageDetailViewTests`                   | Test suite for the ImageDetailView. Tests retrieving images using valid and invalid IDs.| -                        |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| Method  | `test_can_retrieve_trip_image_using_valid_id`| Ensures an image can be retrieved by a valid ID.                                        | Status code: 200 OK      |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| Method  | `test_can_retrieve_trip_image_using_invalid_id`| Ensures appropriate handling of requests with an invalid image ID.   | Status code: 404 Not Found |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|


[*Back to top*](#)

## Manual Testing

| Feature | Expected behaviour | Test | Status |
| --- | --- | --- | --- |
| `User registration` | **New user can register**
| &nbsp;&nbsp;- *Username validation* | Accept a valid username | Non-empty string | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Username validation* | Accept a valid password | Strong password |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Redirect to dashboard* | Innloged user redirected to user dashboard | Successful navigation (200 status code) |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Success message* | Returns Django messsage for successful login | Green message box on screen |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `User login` | **User information retrieved, user can login**
| &nbsp;&nbsp;- *Username validation* | Valid username | Can login with corrent user name | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Password validation* | Valid password | Can login with correct password | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Redirect to home address* | Redirect | User redirected to home after registration |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Success message* | Returns messsage for successful login/registration | Green message box on screen |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Welcome message* | Dispalys username and welcome message | Green message box on screen |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Create new trip` | **Authenticated users can create a new trip**
| &nbsp;&nbsp;- *Select time intervals* | Start date less or equal to end date | Type wrong dates combinations | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Select time intervals* | Completed trips cannot be in the future | Type wrong dates combintations | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Select time intervals* | Planned trips cannot be in the past | Type wrong dates combintations | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Select time intervals* | Ongoing trips must contain the current date | Type wrong dates combintations | ![alert](https://via.placeholder.com/10/E54151?text=+) `alert`|
| &nbsp;&nbsp;- *Success messages* | Create/delete trips must return a message to the user | Create and delete trips | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Edit trip` | **Modify an existing trip**
| &nbsp;&nbsp;- *Select time intervals* | Start date less or equal to end date | Type wrong dates combinations | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Select time intervals* | Completed trips cannot be in the future | Type wrong dates combintations | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Select time intervals* | Planned trips cannot be in the past | Type wrong dates combintations | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Select time intervals* | Ongoing trips must contain the current date | Type wrong dates combintations | ![alert](https://via.placeholder.com/10/E54151?text=+) `alert`|
| &nbsp;&nbsp;- *Success messages* | Create/delete trips must return a message to the user | Create and delete trips | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Change title* |  Title non-empty, min 100 char | Enter title with different  lengths | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Change place* | Place non-empty, min 2 char | Enter place names with different lengths | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Change country* | Country non-empty, 2-56 chars | Enter country names with different lengths | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Success messages* | Edit trips must return a message to the user | Edit trips | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Map the shared trips * | Shared trips must be mapped | Create trips with/without sharing rights | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Delete trip` | **Modify an existing trip**
| &nbsp;&nbsp;- *Remove trip and associated phots* | Deleting a trip must remove all associated photos | Create/delete trips | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Remove trip and map markers* | Deleting a trip must remove all associated map markers | Create/delete trips | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Success messages* | Removing trips must return a message to the user | Remove trips | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Upload/Delete photos` | **An image can be uploaded to the site**
| &nbsp;&nbsp;- *File type* | Only valid image files can be uploaded | Upload wrong file types | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Title length* | Title between 2-50 chars | Enter photo titles with different lengths  | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Description length* | Photo description 2-500 chars | Enter photos descriptions with different lengths | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Upload shared photos ti gallery* | Shared photos must be uploaded to Gallery | Upload photos with/withoud sharing rights | ![alert](https://via.placeholder.com/10/E54151?text=+) `alert`|
| &nbsp;&nbsp;- *Delete photo* | Upload/delete photos must return a message to the user | Uploade/delete photos | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Success messages* | Upload/delete photos must return a message to the user | Uploade/delete photos | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Post testimonials` | **An authenticated user can be post a testimonial**
| &nbsp;&nbsp;- *Create testimonial* | A post should contain vaild text 2-50 chars | Enter posts with different lengths | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Testimonial on the landing page* | Approved testimonials should be posted on the lading page | Create and approve posts | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Delete testimonial* | Users can delete their own testimonials | Add and delete testimonials | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Success messages* | Add/delete testimonials must return a message to the user | Uploade/delete testimonials | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Send inquiries` | **A site visitor can send an email to site admin**
| &nbsp;&nbsp;- *Valid sender name* | Sender name of 2-100 chars | Enter sender names with different lengths | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Valid message* | A message text of 50-500 chars | Enter messages with different lengths | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Admin can receive message* | The messages are visible on the admin page | Send inquiries | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Admin can approve message* | The admin can approve a message on admin page | Send inquiries | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Success messages* | Sent inquries must return a message to the user | Send inquiries | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Create user profile` | **A profile table shoukd be created when a user registers to the site**
| &nbsp;&nbsp;- *User Profile in the admin page* | Profile can be accessed by the admin | Create new users and check the admin page | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *User Profile can be deleted* | Deleting users removes the profile from admin | Delete User from the admin | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *A users can follow other users* | Can select one or mores users to follow from the admin page| Follow/unfollow users | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Edite user profile` | **A user can edit his profile data**
| &nbsp;&nbsp;- *User can change/remove name* | User can chose what personal data to display | Add and remove user names | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *User can modify email address* | User can change email address, but a valid email is mandatory have | Edit email address | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Success messages* | User receives a meaasge after editing the profile | Edit profile items | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Leaflet map` | **A user map shared trips and; the map has basic filtering options**
| &nbsp;&nbsp;- *Shared trip location is mapped correctly* | User can find the correct trip destination on the map | Add many destinations | ![alert](https://via.placeholder.com/10/E54151?text=+) `alert`|
| &nbsp;&nbsp;- *Filter trips* | User and site visitors can filter trips | Use different entries for place, country, category and trip status  | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Filter success* | The filter retrieves the correct trips | The right trips are mapped | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Error messages* | User receives an error messasge if no match is found | Use different entries for place, country, category and trip status | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|

---

Despite these measures, certain errors might still occur, such as:
* Selecting inappropriate trip dates that don't align with the trip status, like planning a trip with past dates.
* Overlapping dates when creating a new trip that conflict with previously created trips.

[*Back to top*](#)


## Heroku Deployment
This project uses Cloudinary for image storage, which allows for efficient and scalable management of images.
To configure Cloudinary,  obtain your cloud name, API key, and API secret. Cloudinary credentials were accessed via
the `CLOUDINARY_URL` environmental variable. Additionally, the project uses CodeInstitute's PostgreSQL database,
accessed via the `DATABASE_URL` environment variable.

### React Client
A React client has been configured to consume the API endpoints provided by the LovinEscapades-API.
This client is also deployed on Heroku, ensuring seamless integration and interaction with the backend API.
The React client handles the frontend functionalities, providing users with an intuitive and responsive interface
to interact with the trip tracking tool.

[*Back to top*](#)

## API documentation


[*Back to top*](#)


## Contributing

### To contribute to the ***LovinEscapades-API*** project:
- Fork the repository on GitHub to create your own copy.
- Clone the forked repository to your local machine.
- To fork the project:
    - Click the "Fork" button on the top-right corner of the repository page
    - Clone Your Fork by running the following command in the terminal or command prompt:
        `git clone https://github.com/your-username/repository-name.git`
- Make your desired changes, whether it's fixing a bug, adding a feature, or updating documentation.
- Commit your changes with clear messages.
- Push your commits to your forked repository on GitHub.
- Submit a pull request detailing your changes and their benefits.

[*Back to top*](#)

## License
### Open Source
As an open-source project, ***LovinEscapades-API*** promotes transparency and community involvement.
The code is accessible on GitHub, allowing developers to view, fork, and contribute to the project as they desire.

[*Back to top*](#)

## Acknowledgements
* [`BugBytes` Youtube channel](https://www.youtube.com/watch?v=qzrE7cfc_3Q) for using Django Graphs and great short examples of using extensions
* `ChatGPT` was utilized to generate sensible input for text content, assist in crafting the README file, and perform language proof-checking.

### Use of GenAI
Generative AI tools, such as ChatGPT, were leveraged in various aspects of this project.
They were utilized to assist in:
* Generating initial drafts of documentation and code comments.
* Ensuring the accuracy and clarity of technical descriptions.
* Identifying and upgrading deprecated libraries within the walkthrough CodeInstitute projects.

[*Back to top*](#)

## Documentation version

Last updated: Jan 9, 2025

[*Back to top*](#)