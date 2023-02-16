# Christopher Infante
# CSE 310 - Winter 2023

# This program is an Adress Book where you can add, delete, and display contacts that are stored in Google Firebase.

import firebase_admin   # import the firebase_admin module
from firebase_admin import credentials # import the credentials module from firebase_admin
from firebase_admin import firestore # import the firestore module from firebase_admin
import os # import the os module
import time # import the time module
from colors import style # import the style class from the colors.py file

# create a credentials object and initialize the firebase admin sdk
# The patch to your security .json file goes here!
cred = credentials.Certificate("cloud-addressbook-firebase-adminsdk-zvy9u-b74a9b7fef.json") 
firebase_admin.initialize_app(cred)

# connect to firestore
db = firestore.client() 

# create collection and insert document
collection = db.collection('my_address_book')  # create collection

# create a class Contact
class Contact:
    def __init__(self, first_name, last_name, phone_number, email, notes): 
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.notes = notes

    # method to create a new contact
    def create_new_contact(self): 
        self.first_name = input("Enter the first name: ")
        self.last_name = input("Enter the last name: ")
        self.phone_number = input("Enter the phone number: ")
        self.email = input("Enter the email: ")
        self.notes = input("Enter the notes: ")

    # method to print the contact
    def print_contact(self): 
        print("First Name:", self.first_name)
        print("Last Name:", self.last_name)
        print("Phone Number:", self.phone_number)
        print("Email:", self.email)
        print("Notes:", self.notes)
        
    def get_phone(self): # method to return the phone number
        return self.phone_number
    
    def get_name(self): # method to return the name
        return self.first_name
    
    def get_email(self): # method to return the email
        return self.email
    
    def get_notes(self):    # method to return the notes
        return self.notes

# function to save the contact to the firestore database
def save_contact(contact):
    record = collection.document(contact.email).set({ # insert document
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'phone_number': contact.phone_number,
        'email': contact.email,
        'notes': contact.notes
    })
    print(style.YELLOW + "\nContact has been added to the Addressbook\n" + style.RESET)
            
# function to display all the contacts
def display_all(): # function to display all the contacts
    record = collection.get() # returns a list
    
    print(style.CYAN + "\nDisplaying All Contacts\n" + style.RESET)
    
    for i in record: # loop through the list
        data = i.to_dict()
        # read the fields from each record and store them in variables
        field_email = data["email"] 
        field_firstname = data["first_name"] 
        field_lastname = data["last_name"]
        field_notes = data["notes"] 
        field_phonenumber = data["phone_number"] 
        # print the contact from the fields read above
        print(f"First Name: {field_firstname}")
        print(f"Last Name:  {field_lastname}")
        print(f"Phone #:    {field_phonenumber}")
        print(f"Email:      {field_email}")
        print(f"Notes:      {field_notes}")
        print(style.BLUE + "--------------------------------" + style.RESET)
    print ("\n")  

# function to edit a contact            
def edit_contact(): 
    name = input("Enter the email address of the contact you want to edit: ") # string to store the email of the contact
    
    # check if the contact exists
    if collection.document(name).get().exists: 
        record =  collection.document(name).get() # get the record
        data = record.to_dict() # convert the record to a dictionary
        # read the fields from this record and store them in variables
        field_email = data["email"] 
        field_firstname = data["first_name"] 
        field_lastname = data["last_name"]
        field_notes = data["notes"] 
        field_phonenumber = data["phone_number"] 
        
        # print the contact from the fields read above
        print(f"First Name: {field_firstname}")
        print(f"Last Name:  {field_lastname}")
        print(f"Phone #:    {field_phonenumber}")
        print(f"Email:      {field_email}")
        print(f"Notes:      {field_notes}")
        print("--------------------------------")
        
        # ask the user to update the contact information
        first_name = input(style.YELLOW + "Enter new first name: " + style.RESET)
        last_name = input(style.YELLOW + "Enter new last name: " + style.RESET)
        phone_number = input(style.YELLOW + "Enter new phone number: " + style.RESET)
        email = input(style.YELLOW + "Enter new email: " + style.RESET)
        notes = input(style.YELLOW + "Enter new notes: " + style.RESET)
        
        # update the document
        record = collection.document(name).update({ 
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'email': email,
            'notes': notes
        })
        
        print(style.YELLOW + "\nContact has been updated\n" + style.RESET)

    # if the contact does not exist        
    else:
        print(style.RED + "\nContact does not exist\n" + style.RESET) 

# function to delete a contact
def delete_contact(): 
    name = input("Enter the email address of the contact you want to delete: ")
        
    # check if the contact exists
    if collection.document(name).get().exists:
        collection.document(name).delete() # delete the contact
        print(style.YELLOW + "Contact deleted from Addressbook!" + style.RESET)
        print("\n")
    # if the contact does not exist
    else:
        print(style.RED + "\nContact does not exist in the Addressbook\n" + style.RESET)
        
# function to log and display the recent transactions
def notify_transaction(results, changes, read_time):
    current_time = time.time()
    for change in changes:
        change_ref = change.document
        change_time = change_ref.create_time.timestamp()
        
        if (current_time - change_time) <= 30: # only show the recent transactions (last 10 seconds)
            if change.type.name == 'ADDED':
                print(f'New data added to the document: {change.document.id} -> {change.document.to_dict()}')
        elif change.type.name == 'MODIFIED':
            print(f'Data in the document was modified: {change.document.id} -> {change.document.to_dict()}')
        elif change.type.name == 'REMOVED':
            print(f'Data was deleted from the document: {change.document.id} -> {change.document.to_dict()}')
              
# main function
def main(): 
    
    while True:
        collection.on_snapshot(notify_transaction) # call the notify_transaction function
        time.sleep(2) # this allows the notify_transaction function to display before the menu is displayed
        # display the menu
        choice = input(style.CYAN +  "      " + style.UNDERLINE + "Main Menu\n" + style.RESET + style.GREEN + "1. Add a new contact\n2. Display all contacts\n3. Edit a contact\n4. Delete a contact\n5. Quit\n" + style.RESET + "Enter your choice: ")
        if choice == "1":
            cont = Contact("", "", "", "", "")
            cont.create_new_contact()
            save_contact(cont)
        elif choice == "2":
            display_all()
        elif choice =="3":
            edit_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            print(style.YELLOW + "\nThank you for using Chris' Addressbook, Goodbye!\n" + style.RESET)
            break 

if __name__ == "__main__":
    main()
