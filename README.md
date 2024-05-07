# Crowdfunding Web App for Egypt

Crowdfunding is the practice of raising small amounts of money from a large number of people, typically via the Internet, to fund a project or venture. It has become a popular form of crowdsourcing and alternative finance, with over US$34 billion raised worldwide in 2015.

## Project Aim
Create a web platform for starting fundraising projects in Egypt. The web app should include the following features:

## 1. Authentication System
- **Registration**:
  - First name
  - Last name
  - Email
  - Password
  - Confirm password
  - Mobile phone (validated against Egyptian phone numbers)
  - Profile Picture
  - Activation Email after registration with a link that expires in 24 hours
- **Login**:
  - Login after activation using email and password
  -  Allow login with Facebook account
- **Forgot Password **
  - Option to reset password via a link sent to email
- **User Profile**:
  - View and edit profile (except email)
  - View projects and donations
  - Add optional info (e.g., Birthdate, Facebook profile, Country)
  - Delete account (with confirmation)
  - Require password to delete account

## 2. Projects
- **Project Creation**:
  - Title
  - Details
  - Category (from a predefined list by admins)
  - Multiple pictures
  - Total target (e.g., 250,000 EGP)
  - Multiple tags
  - Start/end time for the campaign
- **Project Viewing and Interaction**:
  - Users can view any project and donate to the total target
  - Users can add comments (with possible replies) and report inappropriate projects or comments
  - Users can rate projects
  - Project creator can cancel if donations are less than 25% of the target
  - Project page displays:
    - Average rating
    - Project pictures in a slider
    - 4 other similar projects based on tags

## 3. Homepage
- A slider to showcase the top 5 highest-rated running projects
- A list of the latest 5 projects
- A list of the latest 5 featured projects (selected by admin)
- A list of project categories with an option to view all projects in a category
- Search bar to search projects by title or tag
