# Overview

This application was written as I was learning how to integrate the use of cloud databases into my programming.

With this Address Book application, all of the contact data is written to a Firestore database.  The functionality includes adding new contacts to the addressbook, displaying all contacts, updating a contact, and deleting a contact.  As part of my work, I also incorporated a function that displays a notification to the console when data in cloud database is added, changed, or deleted.

***Note you will need to create your cloud database project in Google Firebase and download a security .json file to make this application work.  You DO NOT need to create a collection as it will be created the first time you run this application.***

[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

For this application I am using Google Firebase to store my information.

This application uses the collection "my_address_booK" where each contact in the address book uses the email address as the document name since email addresses have a high liklyhood of being unique.  Within that document each field (first name, last name, phone number, and notes) of the contact information is stored in a collection.

# Development Environment

Viusal Studio Code
Python 3.10.1 64-bit
Git / GitHub
Google Firebase / Firestore
Firebase Tools module 11.23.1
Firebase-Admin module 0.4.8

# Useful Websites

- [Intro to Cloud Databases](https://learning.oreilly.com/library/view/an-introduction-to/9781492044857/ch01.html)
- [Firebase Tutorial](https://firebase.google.com/docs/firestore)
- [Cloud Workshop by Brother Macbeth](https://video.byui.edu/media/t/1_al5oz4pq)

# Future Work

Future enhancements and features:

- Web Frontend
- Search by name
- Timestamp each record for date last modified

