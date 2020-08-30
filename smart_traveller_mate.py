from tkinter import *
import requests
import googlemaps
from datetime import datetime

address=[]  #list of addresses.
latitude=[] #list of latitude.
longitude=[]    #list of longitude.
manhattan={}    #dictionay with key as address and value as hf value.
matrix={}   #dictionay of dictionary with contains key as an address and value as another dictionary.
open={}
closed={}
timed={}
travel=0
way=[]
last=""
num=0

top = Tk()
top.title("SMART TRAVELLER MATE")
top.geometry("925x530")
frame1 = Frame(top)
frame1.pack()

def fetch(url):
    global num
    api_key = "Insert your key of geocoding api here"
    address.append(url)
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address[num], api_key))
    api_response_dict = api_response.json()
    if api_response_dict['status'] == 'OK':
        lati= api_response_dict['results'][0]['geometry']['location']['lat']
        longi= api_response_dict['results'][0]['geometry']['location']['lng']
        manhattan[address[num]]= abs(lati-longi)
        latitude.append(lati)
        longitude.append(longi)
    print('Latitude:', latitude)
    print('Longitude:', longitude)
    print('HF Value:', manhattan)

def distance(j):
    global num
    temp={}
    temp1={}
    l=list(zip(latitude,longitude))
    gmaps = googlemaps.Client(key='Insert your key of google maps api here')
    for i in range(num):
        now=datetime.now()
        directions_result = gmaps.directions(l[j],l[i],mode="driving",departure_time=now)
        print(address[j],"to",address[i])
        a=directions_result[0]['legs'][0]['distance']['text']
        driving_time=directions_result[0]['legs'][0]['duration']['text']
        b=a.split(" ")
        z=driving_time.split(" ")
        if b[1] == 'm':
            b[0] = float(b[0])/1000.0
        '''if "km" in b[1] and len(b[0])>=4:
            b[0] = b[0][0:1] + b[0][2:5]
            b[0]=float(b[0])'''
        print(b[0],"Km")
        print(z[0],z[1])
        if z[1] == 'h' or z[1] == 'hours':
            z[0] = float(z[0])*60.0
        if z[1] == 'day' or z[1] == 'days':
            z[0] = float(z[0])*24.0*60.0
        temp[address[i]]=float(b[0])
        temp1[address[i]]=float(z[0])
    matrix[address[j]]=temp
    timed[address[j]]=temp1

def a_star(travel,last):
    global num
    for l in range(num):
        for j in open:
            open[j] = manhattan[j] + matrix[last][j]
        if len(open) > 0:
            small = minimum()
            way.append(small)
            closed[small] = open[small]
            travel = travel + matrix[last][small]
            del open[small]
            last = small
    return travel

def minimum():
    global num
    least= min(open.keys(), key=lambda k: open[k])
    return least

def get_value():
    global num
    url = url_input.get()
    url_input.delete(0, 'end')
    fetch(url)
    num = num + 1
    print(address)

def get_schedule():
    global num
    global travel
    for i in range(num):
        distance(i)

    closed[address[0]] = manhattan[address[0]]
    last = address[0]
    way.append(address[0])

    for i in range(1, num, 1):
        open[address[i]] = manhattan[address[i]]

    travel = a_star(travel, last)
    url_textbox.insert(INSERT, address)
    url_textbox.insert(INSERT, '\n')
    print("Travel Distance:", travel, "Km")
    url_textbox.insert(INSERT , 'Travel Distance: ')
    url_textbox.insert(INSERT, travel)
    url_textbox.insert(INSERT, ' Kms')
    url_textbox.insert(INSERT, '\n')
    print("\nYour Schedule IS:")
    url_textbox.insert(INSERT, '\n')
    url_textbox.insert(INSERT, 'Your Schedule IS:')
    url_textbox.insert(INSERT, '\n')
    for i in range(num - 1):
        print(way[i], "to", way[i + 1], "(", timed[way[i]][way[i + 1]], "mins )")
        url_textbox.insert(INSERT,way[i])
        url_textbox.insert(INSERT, " to ")
        url_textbox.insert(INSERT, way[i+1])
        url_textbox.insert(INSERT, " ( ")
        url_textbox.insert(INSERT, timed[way[i]][way[i+1]])
        url_textbox.insert(INSERT, " mins ) ")
        url_textbox.insert(INSERT, '\n')

url_label=Label(frame1, text="INPUT:")
url_label.grid(row=0, column=0, pady="10", padx="5")
url_input = Entry(frame1, bg="white", width="140")
url_input.grid(row=0, column=1, columnspan="2", padx="5")
url_add = Button(frame1, text="ADD", bg="#3971cc", fg="white", command=get_value)
url_add.grid(row=1, column=2, padx="5", pady="10")
url_submit = Button(frame1, text="SUBMIT !!", bg="#3971cc", fg="white", command=get_schedule)
url_submit.grid(row=1, column=1, padx="5", pady="10")
url_label1 = Label(frame1, text="OUTPUT:")
url_label1.grid(row=2, column=0, pady="10", padx="5")
url_textbox = Text(frame1, bg="#adb2ba", height="22", width="105")
url_textbox.grid(row=2, column=1, columnspan="2",pady="10", padx="5" )

top.mainloop()