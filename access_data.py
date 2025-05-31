import requests

class Data():
    
    def __init__(self):
        self.date = ''
        self.countries = ['zloty (Polska)']
        self.short = ['PLN']
        self.conv_rate = [1.0]

        if self.get_data() == False:
            self.load_last()

    def get_data(self):
        url = "https://api.nbp.pl/api/exchangerates/tables/A/"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: {response.status_code}")
            return False
        rates = data[0]['rates']
        
        time = data[0]['effectiveDate']
        self.date = time

        for rate in rates:
            self.countries.append(rate['currency'])
            self.short.append(rate['code'])
            self.conv_rate.append(rate['mid'])
        
        with open('data.txt', 'w') as f:
            f.write(str(time) + '\n')
            f.write(str(self.countries) + '\n')
            f.write(str(self.short) + '\n')
            f.write(str(self.conv_rate) + '\n')
        return True
    
    def load_last(self):
        with open('data.txt', 'r') as f:
           content = f.read()
        text = content.strip().split('\n')
        self.date = text[0]
        self.countires = text[1]
        self.short = text[2]
        self.conv_rate = text[3]

