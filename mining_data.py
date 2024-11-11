import urllib.request
import json
import math
import re

# https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
# https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
# https://stackoverflow.com/questions/4435169/how-do-i-append-one-string-to-another-in-python

pkt_usd_price_api_url = "https://api.mexc.com/api/v3/ticker/price?symbol=PKTCUSDT"
pkt_explorer_api_url = "https://explorer-api.pkt.ai"
pkt_explorer_url = "https://packetscan.io"

req_headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }

def get_pkt_usd_price():

    price_str = ""
    price_float = -1.0

    try:
        req = urllib.request.Request(
            pkt_usd_price_api_url,
            data = None, 
            headers = req_headers
        )
        with urllib.request.urlopen(req) as res:

            data = json.load(res)
            price_str = data["price"]
            price_float = float(price_str)

    except EnvironmentError:
            print("MEXC API error!")

    return price_str, price_float 


def get_mining_data(addresses):

    if len(addresses) == 0:

        return "You first have to add at least one PKT address. Use /add_address to add one."

    else:

        result = "<b>Mining statistics</b>\n"
        number = 0

        pkt_usd_price_str, pkt_usd_price_float = get_pkt_usd_price()

        if (pkt_usd_price_float != -1.0):

            result += "\nCurrent price PKT (on <a href=\"" + pkt_usd_price_api_url + "\">MEXC</a>):\n   $ " + pkt_usd_price_str + "\n"

        for address in addresses:

            address = str(address[0])

            if re.match(r'^pkt1q.*', address):
                nice_address = address[:13] + "..." + address[-8:] # New PKT address
            else:
                nice_address = address[:9] + "..." + address[-8:] # Legacy PKT address

            link_nice_address = "<a href=\"" + pkt_explorer_url + "/address/" + address + "\">" + nice_address + "</a>"
            number += 1

            result += "\nAddress " + str(number) + "/" + str(len(addresses)) + ":\n   " + link_nice_address + "\n"
            failed = 0

            try:
                req = urllib.request.Request(
                    pkt_explorer_api_url + "/api/v1/PKT/pkt/address/" + address,
                    data = None, 
                    headers = req_headers
                )
                with urllib.request.urlopen(req) as res:
                    data = json.load(res)

                    # Balance:
                    balance = int(data["balance"]) / (2**30)
                    result += "Balance:\n   " + f"{balance:,.2f}" + " PKT"
                    if (pkt_usd_price_float != -1.0):
                        balance_usd = float(balance) * pkt_usd_price_float
                        result += " ($ " + f"{balance_usd:,.2f}" + ")\n"
                    else:
                        result += "\n"

                    # Unconsolidated Txns:
                    unconsolidated_txns = int(data["balanceCount"])
                    result += "Unconsolidated Txns:\n   " + str(unconsolidated_txns)
                    if (unconsolidated_txns > 1200):
                        result += " ⚠️ <i>Fold coins!</i>"
                    result += "\n"

                    # Mined last 24 hours:
                    mined24 = int(data["mined24"]) / (2**30)
                    result += "Mined last 24 hours:\n   " + f"{mined24:,.2f}" + " PKT"
                    if (pkt_usd_price_float != -1.0):
                        mined24_usd = float(mined24) * pkt_usd_price_float
                        result += " ($ " + f"{mined24_usd:,.2f}" + ")\n"
                    else:
                        result += "\n"
            
            except EnvironmentError:
                failed = 1
                result += "Cannot retrieve information from the block explorer. Either the explorer API is down or this is not a valid PKT address."

            if failed == 0:
                try:
                    req = urllib.request.Request(
                        pkt_explorer_api_url + "/api/v1/PKT/pkt/address/" + address + "/income/30",
                        data = None, 
                        headers = req_headers
                    )
                    with urllib.request.urlopen(req) as res:
                        data = json.load(res)

                        # Mined yesterday:
                        received_yesterday = int(data["results"][0]["received"]) / (2**30)
                        result += "Mined yesterday:\n   " + f"{received_yesterday:,.2f}" + " PKT"
                        if (pkt_usd_price_float != -1.0):
                            received_yesterday_usd = float(received_yesterday) * pkt_usd_price_float
                            result += " ($ " + f"{received_yesterday_usd:,.2f}" + ")\n"
                        else:
                            result += "\n"
                        
                        # Mined 7 days ago:
                        received_7daysago = int(data["results"][7]["received"]) / (2**30)
                        result += "Mined 7 days ago:\n   " + f"{received_7daysago:,.2f}" + " PKT"
                        if (pkt_usd_price_float != -1.0):
                            received_7daysago_usd = float(received_7daysago) * pkt_usd_price_float
                            result += " ($ " + f"{received_7daysago_usd:,.2f}" + ")\n"
                        else:
                            result += "\n"
                        
                        # Mined 30 days ago:
                        received_30daysago = int(data["results"][30]["received"]) / (2**30)
                        result += "Mined 30 days ago:\n   " + f"{received_30daysago:,.2f}" + " PKT"
                        if (pkt_usd_price_float != -1.0):
                            received_30daysago_usd = float(received_30daysago) * pkt_usd_price_float
                            result += " ($ " + f"{received_30daysago_usd:,.2f}" + ")\n"
                        else:
                            result += "\n"
                
                except EnvironmentError:
                    result += ""

        return result