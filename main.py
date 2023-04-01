'''
    TODO : duplicate entries not allowed in sheet
    TODO : Upload it in a cloud to check every hour or so..
    TODO : use twilio to notify the customer
    TODO : set up the date_from , date_to {add it like 60 days from entered day } --> refer https://tequila.kiwi.com/portal/docs/tequila_api/search_api
    TODO : set up nights_in_dst_from, and nights_in_dst_to and calculate round trip
    TODO : calculate round_trip and alert the user with the flight details
    TODO : write more meaningful indentifier names
    TODO : make the UI better and adaptable
    TODO : incoperate modularity
    TODO : delete from the sheet when date expired
    TODO : exception handling if something goes wrong
    TODO : send mail to the customer instead of me

'''
import requests
from flight_data import FlightData
import tkinter as tk
from PIL import ImageTk, Image
import notification_manager

class FlightNotifi:
    '''
        class initiates the GUI interface
    '''
    def __init__(self):
        # create the window
        self.window = tk.Tk()
        self.window.title("Travel Data Form")
        self.window.geometry("700x500")

        bg_image = ImageTk.PhotoImage(Image.open("flight_back.jpg").resize((700, 500)))
        bg_label = tk.Label(self.window, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # create the labels
        self.title_label = tk.Label(self.window, text="Notifi travel", font=("Arial", 16))
        self.title_label.pack()

        self.name_label = tk.Label(self.window, text="boarding pt :")
        self.name_label.pack()
        self.frompoint = tk.Entry(self.window)
        self.frompoint.pack()

        self.email_label = tk.Label(self.window, text="destination pt :")
        self.email_label.pack()
        self.topoint = tk.Entry(self.window)
        self.topoint.pack()

        self.phone_label = tk.Label(self.window, text="start date (leave if not specefic) ")
        self.phone_label.pack()
        self.fromdate = tk.Entry(self.window)
        self.fromdate.pack()

        self.destination_label = tk.Label(self.window, text="till date (leave if not specific ):")
        self.destination_label.pack()
        self.todate = tk.Entry(self.window)
        self.todate.pack()

        self.departure_label = tk.Label(self.window, text="min days stay :")
        self.departure_label.pack()
        self.departure_entry = tk.Entry(self.window)
        self.departure_entry.pack()

        self.return_label = tk.Label(self.window, text="max day stay :")
        self.return_label.pack()
        self.return_entry = tk.Entry(self.window)
        self.return_entry.pack()

        self.price_label = tk.Label(self.window, text="max payable :")
        self.price_label.pack()
        self.price_entry = tk.Entry(self.window)
        self.price_entry.pack()

        self.button = tk.Button(self.window, text="Post to moniter", command=self.post_new_click)
        self.button.pack()

        self.see_button = tk.Button(self.window, text='see previously updated', command=self.check_flights)
        self.see_button.pack()

        self.display_lab = tk.Label(self.window, text="")
        self.display_lab.pack(pady=20)


        # run the window
        self.window.mainloop()


        # create the button
    def post_new_click(self):
        '''
            on click of button:
            upload data to the excel sheet
            display the current least price

        :return:
        '''
        self.bcode = self.frompoint.get().upper()
        self.dcode = self.topoint.get().upper()
        self.from_date = self.fromdate.get()
        self.to_date = self.todate.get()
        self.min_stay = self.departure_entry.get()
        self.max_stay = self.return_entry.get()
        self.price = int(self.price_entry.get())

        # placing into the sheets
        self.add_new_city()



    def check_flights(self):
        getsheet_url = 'https://script.google.com/.. [google sheet code toGet]' # TODO : add the endpoint
        response = requests.get(url=getsheet_url)
        data = response.json()
        res = ''

        for plan in data:
            self.bcode = plan['bcode']
            self.dcode = plan['dcode']
            self.price = int(plan['price'])

            headers = {"apikey": 'uIXOXQtw -- [get your api key from TEQUILA]'} # TODO : add the api key
            query = {
                "fly_from": self.bcode,
                "fly_to": self.dcode,
                'limit': 10,
                "curr": "INR"
            }

            response = requests.get(
                url=f"https://api.tequila.kiwi.com/v2/search",
                headers=headers,
                params=query,
            )
            try:
                data = response.json()["data"][0]
                print('data found successful')

            except IndexError:
                print(f"No flights found for {self.dcode}.")
                return None

            flight_data = FlightData()
            flight_data.price = int(data["price"]),
            flight_data.origin_city = data["route"][0]["cityFrom"],
            flight_data.origin_airport = data["route"][0]["flyFrom"],
            flight_data.destination_city = data["route"][0]["cityTo"],
            flight_data.destination_airport = data["route"][0]["flyTo"],

            if self.price > flight_data.price[0]:
                # cheap flight found , setting up email notification!
                print(f"{flight_data.destination_city}: INR{flight_data.price}")

                self.sendnotifi = notification_manager.NotificationManager(flight_data.origin_city, flight_data.destination_city,flight_data.price[0])
                self.sendnotifi.sendmail()

                # display in app
                res += f"{flight_data.origin_city} to {flight_data.destination_city} at price : INR{flight_data.price[0]}\n"

            else:
                print(f"{flight_data.origin_city} to {flight_data.destination_city} price overflow")

        self.display_lab.config(text=res)

    def add_new_city(self):
        # TODO: add the endpoint
        insert_place_api = 'https://script.google.com/... [place here the api created in google sheets to doPost]'
        response = requests.post(insert_place_api, json={'bcode': self.bcode, 'dcode': self.dcode, 'price': self.price})
        print(response)


f1 = FlightNotifi()
f1.check_flights() # is this required here ?? see
print('ended')

