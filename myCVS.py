# myCVS - Thomas Nguyen 2021

from ttkthemes import themed_tk as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import requests
import json
from bs4 import BeautifulSoup
import re
import webbrowser


# Globals class to keep track of variables we might need elsewhere
class Globals:
    i = 0
    checkForGoodStates = "https://www.cvs.com/immunizations/covid-19-vaccine"  # Grab from this URL
    checkRequest = requests.get(checkForGoodStates)
    stateCheck = BeautifulSoup(checkRequest.text, 'html.parser')
    myString = str(stateCheck.find_all('a', class_='type__link__alpha'))
    # Find string that contains the state that doesn't have vaccines available at CVS
    pattern = '<span class="link__alpha">(.*?)</span>'  # Separate state from html
    substring = re.search(pattern, myString).group(1)
    # Use re to split using pattern, substring is now the bad state
    # Dictionary with all 50 states and abbreviations
    stateDict = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
                 'Colorado': 'CO', 'Connecticut': 'CT',
                 'Delaware': 'DE', 'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU',
                 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
                 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
                 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
                 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
                 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
                 'Northern Mariana Islands': 'MP',
                 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR',
                 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
                 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI', 'Virginia': 'VA', 'Washington': 'WA',
                 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}

    # Placeholder variable to grab the correct abbreviation
    state = None


def about():  # About message
    messagebox.showinfo("About", "Created by Thomas Nguyen. Find out which cities in your state have Covid-19 vaccines at CVS!")


def search():  # Search button is pressed > Perform scraping

    entry = searchInput.get()  # Input from the entry
    for key, value in Globals.stateDict.items():  # Look through state dictionary
        if (entry.lower() == key.lower()) or (entry.lower() == value.lower()):  # Compare input with either abbreviation or full state name
            Globals.state = value  # Set state to the correct abbreviation
        if key == Globals.substring:
            Globals.substring = value  # Set substring to abbreviation for bad state

    finalCheck = entry.title()  # To combat having an invalid input after a valid input
    # If the entry didn't match any of the states OR
    # If the input isn't in the state dictionary
    if (Globals.state is None) or (finalCheck not in Globals.stateDict and finalCheck.upper() not in Globals.stateDict.values()):
        messagebox.showwarning("ERROR","Please enter valid input!")  # Invalid!
    else:  # Valid input!
        if Globals.state == Globals.substring:  # State with no CVS vaccines :(
            messagebox.showwarning("Disclaimer","Sorry, " + Globals.state + " doesn't have vaccines at CVS yet.")
        else:  # Vaccine!
            myListbox.delete(0,'end')  # Clear listbox every time
            url = "https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status." + Globals.state + ".json?vaccineinfo"
            # Time to scrape the cities and their availability!
            request = requests.get(url)
            soup = BeautifulSoup(request.text, 'html.parser')
            myString = soup.text
            myDict = json.loads(myString)  # Convert the text into a dictionary
            info = myDict['responsePayloadData']['data'][Globals.state]  # Find the cities for specific state
            for item in info:  # Iterate the cities and insert information into listbox!
                myListbox.insert(Globals.i,item['city']+" = "+item['status'])
                Globals.i+=1   # Iterate index that we are inserting into listbox


def openUrl(websiteUrl):
    webbrowser.open_new(websiteUrl)


root = tk.ThemedTk()  # Set window & theme
root.get_themes()
root.set_theme("yaru")  # Ubuntu because pretty
root.configure(background="white smoke")  # Match background for Windows users
root.title("myCVS")  # Title of application
root.geometry("310x260")  # Nice size

myMenu = Menu(root)  # Create about menu
myMenu.add_command(label='About', command=about)
root.config(menu=myMenu)

fillerFrame = ttk.Frame(root, height=10)  # Filler frame to create space between top and next widgets
fillerFrame.pack(side=TOP)


searchFrame = ttk.Frame(root)  # Frame under fillerFrame
searchFrame.pack()

searchLabel = ttk.Label(searchFrame, text="ENTER STATE: ")  # Enter label
searchLabel.pack(side=LEFT)


searchInput = ttk.Entry(searchFrame)  # Entry label
searchInput.pack(side=LEFT)


anotherFiller = ttk.Frame(root,height=10)  # Another spacing frame!
anotherFiller.pack()


searchButton = ttk.Button(searchFrame, text="SEARCH",command=search)  # Good ole search button
searchButton.pack()


resultFrame = ttk.Frame(root)  # Frame for results
resultFrame.pack()


spacingFrame = ttk.Frame(root,width=15)  # Another spacing frame
spacingFrame.pack(side=LEFT)

# Hyperlink to schedule with matching text and nice blue color + matching background since non-theme label
scheduleLink=Label(root, text="SCHEDULE APPOINTMENT!", font="Terminus 9 underline", fg='SlateBlue2', bg='white smoke')
scheduleLink.pack(side=BOTTOM)
scheduleLink.bind("<Button-1>", lambda e: openUrl("https://www.cvs.com/vaccine/intake/store/covid-screener/covid-qns"))


myListbox=Listbox(root, width=45)  # Listbox for all cities and availability
myListbox.pack(side=LEFT)

myScrollbar=ttk.Scrollbar(root)  # Scrollbar for listbox
myScrollbar.pack(fill=BOTH, side=RIGHT)

# Attach scrollbar to listbox and configure both for vertical scrolling
myListbox.config(yscrollcommand=myScrollbar.set)
myScrollbar.config(command=myListbox.yview)


root.mainloop()  # Keep GUI up!




