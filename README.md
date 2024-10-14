<h1 allign="center" id="title"> For Home Cooks </h1>

![for Home Cooks]()

[Live Project can be viewed here.]()
![Logo]()

For Home Cooks is a recipe application for homecooks who are looking to widen their recipe catelogue.

## Table of Contents

### User Experience (UX)

- [Project Goals](#project-goals)
- [User Goals](#user-experience-ux)
- [Developer Goals](#developers-goals)
- [User Stories](#user-stories)
- [Design Choices](#design-choices)
- [Wireframes](#wireframes)

### Features

- [Future Features](#future-feautres)

### Testing

- [Manual Testing](#manual-testing)
- [Bugs](#bugs)

### Deployment

- [How to Deploy Site](#deployments)

### Credits

- [Credits](#credits)
- [Code](#code)
- [Acknowledgments](#acknowledgments)

## User Experience (UX)

### Project Goals

This project's goal is to build a full-stack site that allows your users to manage a common dataset about a particular domain. That is appealing to the users of this site. As well as improve my own developer skills and move out my comfort zone.

#### Recruiters Goals

The main audience for this site is anyone aged 8+ with parental guidance.

#### User Goals:

- Find and share recipes
- Enjoy cooked goods.

#### Developers goals:

- Create an appealing, functional site.
- Demonstrate the use of full-stack development.
- Make site that allows users to find and share recipes.

#### User Stories

As a user I want:

- Search for recipes.
- To understand the instructions given.
- Share recipes.
- Consistent functionalities.

As the site owner I want:

- A site that provides search and share functions.
- A structured and PEP8 compliant.
- Demonstrate what I have learnt with Python and external libiraries such as Flask and Materialise.
- A site that functions and is consistent with handling data.

## Design Choices

### Languages Used

- HTML
- CSS
- JavaScript
- Python+Flask
- PostgreSQL

### Fonts

-
-

### Icons

-
-

### Colours

-
-

### Images

### Video Files

-

### Wireframes

Wireframes were created using [Balsamiq](https://balsamiq.com/).

- [Home](/readme/wireframes/homepage.png)
- [Recipe Page](/readme/wireframes/recipe-page.png)
- [Recipe Genre Display](/wireframes/recipe-genre-display%20.png)
- [How To Make..](/readme/wireframes/how-to-page.png)
- [Gallery](/readme/wireframes/gallery.png)
- [Sign In](/readme/wireframes/sign-in.png)
- [Your Recipes](/readme/wireframes/your-recipes.png)
- [CRUD - Functionality](/readme/wireframes/crud-creating-update-selete-section.png)

## Features

- Navigation bar that alllows users to access different parts of the sites.
-
-
-

### Loaded page:

When you first load on the page you are met with the homepage.

<details>
<summary>User Interface</summary>
<IMG src="assets/images/"  alt="User Interface"/>
</details>

### Navigation:

<details>
<summary>Navigation</summary>
<IMG src="assets/images/"  alt="Navigation"/>
</details>

### Recipe Page:

<details>
<summary>Recipe Page</summary>
<IMG src="assets/images/"  alt=""/>
</details>

### Gallery Page:

### CRUD Functionality:

If you match the sequence correctly an alert will display before the next round.

<details>
<summary>Create</summary>
<IMG src="assets/images/"  alt="Create functionality"/>
</details>

<details>
<summary>Read</summary>
<IMG src="assets/images/"  alt="Read functionality"/>
</details>

<details>
<summary>Update</summary>
<IMG src="assets/images/"  alt="Update functionality"/>
</details>

<details>
<summary>Delete</summary>
<IMG src="assets/images/"  alt="Delete functionality"/>
</details>

## Future Features

## Accessibility

-
-

## Testing

### Manual Testing

| What to test       | Expected Results                          | Passed |
| ------------------ | ----------------------------------------- | ------ |
| Navigation Menu    | Navigate site and send to correct pages   |        |
| Search for recipe  | Display recipe when searched for          |        |
| Add recipe to site | User can add recipe to the site           |        |
| Sign Up Form       | Allow user to sign up to recipe site.     |        |
| Login Form         | Allow user to login to recipe site.       |        |
| Comments           | Allow user input within the recipe page.  |        |
| Edit and Delete    | Edit or Delte recipes that users created. |        |

### For this project I have had friends and family, test amongst various devices. Such as;

-
-
-
-
-

### Lighthouse - Developer Chrome Tools

<details>
<summary>Lighthouse Overview</summary>
<IMG src="assets/images/lighthouse/"  alt="Lighthouse Overview Score"/>
</details>
<br>

<details>
<summary>Lighthouse Acessibility</summary>
<IMG src="assets/images/lighthouse/"  alt="Lighthouse Accessibility Score"/>
</details>
<br>

<details>
<summary>Lighthouse Diagnostics</summary>
<IMG src="assets/images/lighthouse/"  alt="Lighthouse Accessibility Score"/>
</details>
<br>

<details>
<summary>Lighthouse Overview - After changes</summary>
<IMG src="assets/images/lighthouse/"  alt="Lighthouse Overview Score - After changes"/>
</details>

## Validators

W3c was used to validate HTML, CSS and JavaScript code.

### HTML Validator:

<details>
<summary>HTML Validator Overview Part 1</summary>
<IMG src="assets/images/validators/"  alt="HTML Validator Overview Part 1"/>
</details>
<br>
<details>
<summary>HTML Validator </summary>
<IMG src="assets/images/validators/"  alt="HTML Validator"/>
</details>

<br>

### CSS Validator:

<br>
<details>
<summary>CSS Validator </summary>
<IMG src="assets/images/validators/"  alt="CSS Validator "/>
</details>

### JavaScript Validator:

<details>
<summary>JavaScript Validator</summary>
<IMG src="assets/images/validators/"  alt="JavaScript Validator Results"/>
</details>

## Bugs

### Current Bugs

- Sign in/up form gave back an error - due to column name change. 
- Sign in/up form not redirecting to pages.

<br>
  <details>
  <summary>Console Message</summary>
  <IMG src="assets/images/console/"  alt="Console message"/>

</details>
<br>
<details>
<summary>Console Message - After Change</summary>
<IMG src="assets/images/console/"  alt="Console message - after changes"/>

</details>

### Fixed Bugs

- Materialise mobile navbar wouldn't initialise, switched over to Bootstrap for functionality for navbar and footer functions.
-
-
-

## Deployments

This project was deployed to GitHub Pages using the steps below;

### How to Deploy to GitHub Pages.

1. Open the browser, search GitHub and log in. If you do not have an account, sign up [here](https://github.com/login).
2. Locate and select the [For Home Cooks]().
3. Once the repository is open, select settings.
4. Select 'Pages', which is found on the left-hand side under the Code and Automation category.
5. Underneath build and deployment, there are two sub-heading 'Source' and 'Branch'. Select the 'None' dropdown below the branch sub-heading.
6. Change the 'None' option to 'Main', then press "Save".
7. Wait a few moments whilst the pages refresh. (This could take up to 5 minutes.)
8. You may need to refresh the page, to see the saved changes. You should have seen that the site and the link to the live site. An orange icon will display which will indicate that the save changes are still loading.
9. You can also check your deployment by selecting 'Code'. On the right-hand side, you should see 'Deployments'. Select 'Deployments' to view the status of your deployments.

### How to run this project locally.

To clone this project to Gitpod use the following steps;

1. Open the browser, search GitHub and log in. If you do not have an account, sign up [here](https://github.com/login).
2. Open a new tab, search Gitpod and log in. If you don't have an account, you can sign in with GitHub.
3. Open a new workspace.
4. Go back to the GitHub tab and locate [For Home Cooks]().
5. Click the green "<> Code" button.
6. Under the HTTPS tab, copy the URL for the repository.
7. Go back to your Gitpod Workspace and open the terminal.
8. Change the location of your current working directory to where you want the cloned directory.
9. Type "git clone", then paste the URL that you had copied earlier from GitHub.
10. Press Enter to create your local clone.

### How to Fork this project.

To fork this project from Gitpod, please follow the steps below;

1. Open the browser, search GitHub and log in. If you do not have an account, sign up [here](https://github.com/login).
2. Locate the GitHub tab and locate the project you want to fork. [For Home Cooks]()
3. At the top right-hand side of the page, you will see a "Fork" button. Click on the button and wait a few moments. You should see the new forked repository under your own GitHub account.
4. By default the folk is named as their upstream repositories, you can rename the repositories by typing a name in the "Repository name" field.
5. You can also add a description to your fork and/or copy the default branch only.
6. To also access the files in the repository. Head over to your forked repository. Click the green "<> Code" button.
7. Under the HTTPS tab, copy the URL for the repository.
8. Go to the workspace you have created earlier.
9. To change the current directory to the location where you want the cloned directory.
10. Type "git clone" and paste the URL you copied from GitHub. Press "Enter" and your local clone will be created.

## Credits

### Frameworks, Libraries and Programs Used

- [Balsamiq](https://balsamiq.com/) - For creating wireframes.
- [GitHub](https://github.com/) - To store my repository and deploy site.
- [Gitpod](https://www.gitpod.io/) - Used to write code for this project.
- [HTML Validation](https://validator.w3.org/) - To validate my HTML Code.
- [CSS Validation](https://jigsaw.w3.org/css-validator/) - To validate my CSS code.

### Code

- [Coding2go](https://www.youtube.com/watch?v=bVl5_UdcAy0&t=201s) - Used this walkthrough for form validation.

### Acknowledgments

- []() -
- []() -
- []() -
- []() -
-

[Back to top](#title)
