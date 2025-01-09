
# ***<center><font color="red"> LovinEscapades-API</font>***: The Ultimate Trip Tracking Tool!</center>
## <center> A Django web app </center>

### **Table of content:**
- [Overview](#overview)
- [Application Development](#application-development)
- [Main Features](#main-features)
- [Application Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Accessibility and Design](#accessibility-and-design)
- [Usage and Screenshots](#usage-and-screenshots)
- [Online Validators](#online-validators)
- [Manual Testing](#manual-testing)
- [Unit Testing](#unit-testing)
- [Known bugs and issues](#known-bugs-and-issues)
- [Further improvements](#further-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Documentation version](#documentation-version)


## Overview

**Project Inspiration**
This backend API project builds upon the knowledge and skills acquired during the development of "LovinEscapades" Django web application completed as part of Milestone Project 4 at Code Institute ([more here](https://github.com/eneliviu/LovinEscapades.git)).

The application envisioned utilizes a full-stack development approach, leveraging:

* Backend: Python with the Django framework
* Frontend: Technologies like Javascript and CSS (specific libraries to be determined)

LovinEscapades aims to empower users to manage their travel experiences through features like:

* User Authentication: Secure login and user management.
* Trip Management: Create, update, and manage trip details.
* Image Management: Upload, store, and associate images with trips.
* Trip Sharing: Share trip information and images with others (public or private).
* Social Features: Potential future functionalities like user interaction and testimonials.

**Public Access**:

* Trip Exploration: Unregistered users might be able to view public trip locations on a map.
* Content Discovery: Access to shared trip details and images (depending on privacy settings).

**Future Considerations**:

* User-friendly interface for a seamless user experience.
* Integration with mapping libraries for interactive trip visualization.
* Potential social features for user interaction and community building.

**Disclaimer**:

This API serves as a backend foundation for a potential application. The envisioned features and functionalities are subject to change and refinement based on further development and user feedback.


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

TODO


### User Registration

- The site visitor must fill in a standard registration form:

![Main menu](static/clips/User_registration_form.webp#center)
*<font color="red">LovinEscapades</font>: Responsive design: tablet and mobile phone*.<br>

- The user instroduces username, email and a strong password
![Main menu](static/clips/User_registration_form_fill.webp#center)
*<font color="red">LovinEscapades</font>: Responsive design: tablet and mobile phone*.<br>

- If the registration is successful, the user is redirect to the home page and a success message is posted.
- For logged-in users, the Registration navbar menu is not visible anymore, and the 'My profile'- page with a user icon appears on the right side of the navbar.
- Authenticated users can navigate to the Dashboard page

![Main menu](static/clips/User_registration_logged.webp#center)
*<font color="red">LovinEscapades</font>: Responsive design: tablet and mobile phone*.<br>


### User Dashboard
- The Dashboard offers CRUD fuctionality for managing trips and images

![Main menu](static/clips/Dashboard_clean.webp#center)
*<font color="red">LovinEscapades</font>: Dashboard page*.<br>

#### **Create new trip**
- On the Dashboard, the stats are null and the user can create a new trip record by clicking on the 'Add new trip' button to open an empty form in a Bootstrap modal.
- By design, all form fields are required

![Main menu](static/clips/Add_new_trip_start.webp#center)
*<font color="red">LovinEscapades</font>:Add new trip form*.<br>

- Using Javascript, the date picker entries are corroborated in real-time to the Trip status category (Completed, On-going and Planned) to avoid erroneous choices and to increase the UX. The eventual error are shown in browser alerrs, and the user can chose other entries accordingly. 
- On the backend, the date entries are checked against those form other planned trips to eliminate possible collusions. There errors are hadled by Python logic in `trip.views.py`, and a Django error message is sent if necessary.



![Main menu](static/clips/Add_trip_Completed_error.webp#center)

*<font color="red">LovinEscapades</font>: Add new trip form: date choice missmatch for COMPLETED trips*.<br>



![Main menu](static/clips/Add_trip_Planned_error.webp#center)

*<font color="red">LovinEscapades</font>: Add new trip form: date choice missmatch for PLANNED trips*.<br>

- After a new trip is created and posted as a trip card containg basic trip info  
- Django success message is sent to the user.
- The Dasboard is paginated such that it can handle a large number of trip instances 



![Main menu](static/clips/Add_new_trip_success.webp#center)

*<font color="red">LovinEscapades</font>: Add new trip form: correct date choice for ON-GOING trips*.<br>

- The created trip, if the shared choice is `YES`, it will be sent to the Leaflet map on the landing page. By clicking on the marker, trip information and a redirecting link appear in a tooltip while the map zooms in at the marker location
- The coordinates are calculated using the `geopy` Python module that uses the trip destination (Place and Country) to localize and retrieve the Longitude and the Latitude for mapping the location.
- Although the form does not show the coordinates fields when creating a new trip, these fields exist and are populated when the coordinates are saved.  
- If the location cannot be geolocated, a Django error message is sent to the user.  


![Main menu](static/clips/Add_new_trip_on_map.webp#center)

*<font color="red">LovinEscapades</font>: Add new trip form: correct date choice for ON-GOING trips*.</center><br>


![Main menu](static/clips/Add_new_trip_on_map_tooltip.webp#center)

*<font color="red">LovinEscapades</font>: Add new trip form: correct date choice for ON-GOING trips*.<br>

#### **Managing trips**
- After a  new trip is created, the dashboard stats are updated accordigly



![Main menu](static/clips/Dashboard_update_stats.webp#center)

*<font color="red">LovinEscapades</font>: Trip card with CRUD functionalitys*.<br>

- The trip cards have CRUD functionality for editing trip data and uploading photos.


![Main menu](static/clips/Trip_card.webp#center)

*<font color="red">LovinEscapades</font>: Trip card with CRUD functionalitys*.<br>

- By clicking on the `Update` button, the user is directed to a page containing two choices: 
    - `Update trip` for changing the trip info.
    - `Upload photo` for uploading trip photos.



![Main menu](static/clips/Update_trip_page.webp#center)

*<font color="red">LovinEscapades</font>: Trip card with CRUD functionalitys*.<br>

- Selecting `Update trip` opens the create trip form with all fields filled in, such that the user can modify and save the new trip information.


![Main menu](static/clips/Edit_trip_form.webp#center)

*<font color="red">LovinEscapades</font>: Edit trip page*.<br>

- Selecting `Update photo` option opens a form for loading photos.
- All form fields are mandatory and must be non-empty.
- Constraints on min and max text length are in place using Django Validators.
- After upload, a success message is sent to the user.
- If the user chooses to share it, then the photo is also sent to the `Gallery`-page.



![Main menu](static/clips/Upload_photos_form.webp#center)

*<font color="red">LovinEscapades</font>: Upload photo form*.<br>



![Main menu](static/clips/Upload_photo_success.webp#center)

*<font color="red">LovinEscapades</font>: Upload photo success*.<br>

- After image upload, the stats on the dashboard are updated accordingly


![Main menu](static/clips/Dasboard_stats_1_photo_1_trip.webp#center)

*<font color="red">LovinEscapades</font>: Updated dashboard with trip and photo added*.<br>

- The user can access the uploaded photo using the `Photos` button on the trip card to navigate to a `details<image_id>` URL that opens a masonry gallery of image cards. 



![Main menu](static/clips/User_trip_photo.webp#center)

*<font color="red">LovinEscapades</font>: Gallery page with shared photo*.<br>

- Shared photos can be seen by any site visitor on the `Gallery`-page.


![Main menu](static/clips/Gallery_shared_photo.webp#center)

*<font color="red">LovinEscapades</font>: Gallery page with shared photo*.<br>

- Each photo can be individually deleted form the  `details<image_id>`



![Main menu](static/clips/Delete_photo.webp#center)

*<font color="red">LovinEscapades</font>: Delete photo modal confirmation*.<br>

- After the photo is being deleted, the user is redirected to Dashboard and a Django success message is sent to the user.
- The stats on the Dashboard are updated accordingly



![Main menu](static/clips/Delete_photo_success.webp#center)

*<font color="red">LovinEscapades</font>: Delete photo success message and updated dashboard stats*.<br>

### Manage the user profile
- Initially, the user profile contains only the username and email address that are required 
    by the registration process, but the fields for first and last name are empty.


![Main menu](static/clips/User_profile_clean.webp#center)

*<font color="red">LovinEscapades</font>: User profile page*.<br>

- The `Update` button opens a form for updating the user information



![Main menu](static/clips/Update_user_profile.webp#center)

*<font color="red">LovinEscapades</font>: Update user profile form*.<br>

- After submitting the form, the user is redirected back to `My Profile`-page where the personalia has been updated



![Main menu](static/clips/Update_user_profile_success.webp#center)

*<font color="red">LovinEscapades</font>: Update user profile form*.<br>

- The user can post testimonials to the landing page using the 'New testimonial' button



 ![Main menu](static/clips/Testimonials_form.webp#center)

*<font color="red">LovinEscapades</font>: Post testimonial form*.<br>

- After submitting the testimonial, the user is redirected to `My Profile`-page where the post is loaded and pending approval. 



 ![Main menu](static/clips/Testimonials_success.webp#center)

*<font color="red">LovinEscapades</font>: Posted testimonial*.<br>



 ![Main menu](static/clips/Testimonial_admin.webp#center)

*<font color="red">LovinEscapades</font>: Testimonial pending approval on admin page*.<br>



 ![Main menu](static/clips/Testimonial_approved.webp#center)

*<font color="red">LovinEscapades</font>: Approved testimonial on admin page*.<br>



 ![Main menu](static/clips/Testimonial_approved_user_profile.webp#center)

*<font color="red">LovinEscapades</font>: Approved testimonial on admin page*.<br>

- The `Dashboard`-page has also been udated with a new testimonial post


 ![Main menu](static/clips/Dashboard_trip_testimonial_approved.webp#center)

*<font color="red">LovinEscapades</font>: Updated dashboard page with trip and approved testimonial*.<br>

- After approval, the testimonial is posted on the landing page


 ![Main menu](static/clips/Landing_page_with_testimonial.webp#center)

*<font color="red">LovinEscapades</font>: Updated dashboard page with trip and approved testimonial*.<br>



- Deleteing a trip will remove all the linked trip photos as well
- The dasboard stats and the landing page map are also updated

 ![Main menu](static/clips/Example_two_trips_two_photos.webp#center)

*<font color="red">LovinEscapades</font>: Updated dashboard page with trip and approved testimonial*.<br>

 ![Main menu](static/clips/Map_two_trips.webp#center)

*<font color="red">LovinEscapades</font>: Updated map with new trip marker added*.<br>

 ![Main menu](static/clips/Delete_trip.webp#center)

*<font color="red">LovinEscapades</font>: Delete trip and associated photo*.<br>


 ![Main menu](static/clips/Delete_trip_success.webp#center)

*<font color="red">LovinEscapades</font>: Delete trip and associated photo*.<br>

 ![Main menu](static/clips/Map_one_trip_after_delete.webp#center)

*<font color="red">LovinEscapades</font>: Delete trip marker from map after trip deletion*.<br>


[*Back to top*](#)


#### **Managing site admin inquiries**

 ![Main menu](static/clips/Contact_us_form.webp#center)

*<font color="red">LovinEscapades</font>: Form for sending inquiries to site admin*.<br>


 ![Main menu](static/clips/Contact_success.webp#center)

*<font color="red">LovinEscapades</font>: Inquiry successfully sent to site admin*.<br>


 ![Main menu](static/clips/Inquiry_to_site_admin.webp#center)

*<font color="red">LovinEscapades</font>: Inquiry successfully sent to site admin*.<br>


 ![Main menu](static/clips/Inquiry_to_site_admin_read.webp#center)

*<font color="red">LovinEscapades</font>: Inquiry successfully sent to site admin*.<br>


[*Back to top*](#)

#### **Managing photo gallery page**

- The `Gallery`-page contains all the photos sahred by the user.
- A user can choose to share a photo, but not to make the entire trip public.
- Deleting a trip will delete also the associated photos from the `Gallery`-page



 ![Main menu](static/clips/Shared_gallery.webp#center)

*<font color="red">LovinEscapades</font>: Inquiry successfully sent to site admin*.<br>


[*Back to top*](#)


## Database schema

The Entity Relationship Diagram (EDR) for the full project database shcema was produced using the
[Graph models extention](https://shorturl.at/psHzX) and visualized using the online [GraphViz generator](https://shorturl.at/AAuhy). 



![Main menu](static/docs/graphviz_all_models.webp#center)

*<font color="red">LovinEscapades</font>: EDR project database diagram*.<br>


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

### **Lighthouse**
The Lighthouse validator showed very good results, with an warning related to a Leaflet internal issue.


![Main menu](static/docs/Lighthouse_navtest.webp#center)

*<font color="red">LovinEscapades</font>: Lighthouse navigation test*.<br>


![Main menu](static/docs/Lighthouse_snapshot_test.webp#center)

*<font color="red">LovinEscapades</font>: Lighthouse snapshot test*.<br>


# Unit testing
The project includes a comprehensive test suite for the Trip and Image API endpoints.
The tests are located in the `trips/tests.py` file and cover the following views:
- **TripListView**: Tests for listing trips, including handling shared and non-shared trips.
- **TripDetailView**: Tests for retrieving a specific trip using valid and invalid IDs.
- **ImageListView**: Tests for listing images associated with trips, including handling shared and non-shared images.
- **ImageDetailView**: Tests for retrieving a specific image associated with a trip using valid and invalid IDs.

The test suite includes setup methods to initialize test data and individual test methods to verify the functionality of the respective endpoints.

## Test Classes
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

## Running Tests
To run the tests, use the following command:
```bash
python manage.py test
```
This command will execute the test suite and display the results in the terminal. The tests cover various scenarios to ensure the correctness and robustness of the API endpoints.

## Test Cases

Here are some sample test cases from the test suite:
1. **TripListViewTests**:
    * Test to verify that the `TripListView` can list trips.
    * Test to verify that the `TripListView` can handle trips that are not shared.
2. **PostDetailViewTests**:
    * Test to verify that the `TripDetailView` can retrieve a trip using a valid ID.
    * Test to verify that the `TripDetailView` can handle retrieval of a trip using an invalid ID.
3. **TripImageListViewTests**:
    * Test to verify that the `ImageListView` can list images.
    * Test to verify that the `ImageListView` can handle images that are not shared.
4. **TripImageDetailViewTests**:
    * Test to verify that the `ImageDetailView` can retrieve an image using a valid ID.
    * Test to verify that the `ImageDetailView` can handle retrieval of an image using an invalid ID.
These test cases cover a range of scenarios to ensure that the API endpoints function correctly and handle various edge cases. The tests help maintain the quality and reliability of the application by verifying the expected behavior of the endpoints.


[*Back to top*](#)

<p align="center"><strong>Table: Overview of Test Classes and Methods for the Trip and Image API Endpoints</strong></p>

| Type    | Name                                         | Description                                                                                                    | Expected Result                     |
|---------|----------------------------------------------|----------------------------------------------------------------------------------------------------------------|-------------------------------------|
| Class   | `TripListViewTests`                          | Test suite for the TripListView. Checks listing of trips including shared and non-shared.                       | -                                   |
| Method  | `test_can_list_trips`                        | Verifies that trips can be listed through the TripListView endpoint.                                           | Status code: 200 OK                 |
| Method  | `test_can_handle_list_trips_not_shared`      | Verifies handling of trips that are not shared.                                                                | Status code: 200 OK                 |
| Class   | `PostDetailViewTests`                        | Test suite for the TripDetailView. Tests retrieving trips using valid and invalid IDs.                          | -                                   |
| Method  | `test_can_retrieve_post_using_valid_id`      | Ensures a trip can be retrieved by a valid ID.                                                                 | Status code: 200 OK                 |
| Method  | `test_can_retrieve_post_using_invalid_id`    | Ensures appropriate handling of requests with an invalid trip ID.                                              | Status code: 404 Not Found          |
| Class   | `TripImageListViewTests`                     | Test suite for the ImageListView. Checks listing of images including shared and non-shared.                     | -                                   |
| Method  | `test_can_list_trip_images`                  | Verifies that images can be listed through the ImageListView endpoint.                                         | Status code: 200 OK                 |
| Method  | `test_can_handle_list_trip_images_not_shared`| Verifies handling of images that are not shared.                                                               | Status code: 200 OK                 |
| Class   | `TripImageDetailViewTests`                   | Test suite for the ImageDetailView. Tests retrieving images using valid and invalid IDs.                        | -                                   |
| Method  | `test_can_retrieve_trip_image_using_valid_id`| Ensures an image can be retrieved by a valid ID.                                                               | Status code: 200 OK                 |
| Method  | `test_can_retrieve_trip_image_using_invalid_id`| Ensures appropriate handling of requests with an invalid image ID.                                            | Status code: 404 Not Found          |

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


## Heroku Deployment
This project uses Cloudinary for image storage, which allows for efficient and scalable management of images.
To configure Cloudinary, you need to set up an account on Cloudinary's website and obtain your cloud name, API key, and API secret.
These credentials should be added to your project's environment variables.

Additionally, the project uses CodeInstitute's PostgreSQL database, accessed via the `DATABASE_URL` environment variable.

### React Client
A React client has been configured to consume the API endpoints provided by the LovinEscapades-API.
This client is also deployed on Heroku, ensuring seamless integration and interaction with the backend API.
The React client handles the frontend functionalities, providing users with an intuitive and responsive interface
to interact with the trip tracking tool.

[*Back to top*](#)


[*Back to top*](#)


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
- [`BugBytes` Youtube channel](https://www.youtube.com/watch?v=qzrE7cfc_3Q) for using Django Graphs and great short examples of using extensions
- `ChatGPT` was utilized to generate sensible input for text content, assist in crafting the README file, and perform language proof-checking.


[*Back to top*](#)


## Documentation version

Last updated: Jan 9, 2025

[*Back to top*](#)