## Manual Testing

| Feature | Purpose | Test | Status |
| --- | --- | --- | --- |
| `Functional Testing` | **Verify that the API endpoints work as expected under normal conditions**
| &nbsp;&nbsp;- *Test each endpoint* | Accept a valid username | Non-empty string | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
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


Functional Testing
Authentication and Authorization Testing
Edge Case Testing (large images)
Data Integrity Testing(update trip info)
Third-Party Service Testing (Cloudinary)


