import urllib.request, json
import re

# https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
# https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
# https://stackoverflow.com/questions/4435169/how-do-i-append-one-string-to-another-in-python

req_headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }

def get_pkt_usd_price():

    price = -1.0

    try:
        req = urllib.request.Request(
            "https://api-cloud.bitmart.com/spot/v1/ticker_detail?symbol=PKT_USDT",
            data = None, 
            headers = req_headers
        )
        with urllib.request.urlopen(req) as res:

            data = json.load(res)
            price = float(data["data"]["last_price"])

    except EnvironmentError:
            print("Bitmart API error!")

    return price


def get_mining_data(addresses):

    if len(addresses) == 0:

        return "You first have to add at least one PKT address. Use /add_address to add one."

    else:

        result = "<b>Mining statistics</b>\n"
        number = 0

        pkt_usd_price = get_pkt_usd_price()

        if (pkt_usd_price != -1.0):
            result += "\nCurrent price PKT (on <a href=\"https://www.bitmart.com/trade/en-US?symbol=PKT_USDT\">BitMart</a>):\n   $ " + str(pkt_usd_price) + "\n"

        for address in addresses:

            address = str(address[0])

            if re.match(r'^pkt1q.*', address):
                nice_address = address[:13] + "..." + address[-8:] # New PKT address
            else:
                nice_address = address[:9] + "..." + address[-8:] # Legacy PKT address

            link_nice_address = "<a href=\"https://explorer.pkt.cash/address/" + address + "\">" + nice_address + "</a>"
            number += 1

            result += "\nAddress " + str(number) + "/" + str(len(addresses)) + ":\n   " + link_nice_address + "\n"
            failed = 0

            try:
                req = urllib.request.Request(
                    "https://explorer.pkt.cash/api/v1/PKT/pkt/address/" + address,
                    data = None, 
                    headers = req_headers
                )
                with urllib.request.urlopen(req) as res:
                    data = json.load(res)

                    # Balance:
                    balance = int(data["balance"]) / (2**30)
                    result += "Balance:\n   " + f"{balance:,.2f}" + " PKT"
                    if (pkt_usd_price != -1.0):
                        balance_usd = float(balance) * pkt_usd_price
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
                    if (pkt_usd_price != -1.0):
                        mined24_usd = float(mined24) * pkt_usd_price
                        result += " ($ " + f"{mined24_usd:,.2f}" + ")\n"
                    else:
                        result += "\n"
            
            except EnvironmentError:
                failed = 1
                result += "Cannot retrieve information from the block explorer. Either http://explorer.pkt.cash is down or this is not a valid PKT address."

            if failed == 0:
                try:
                    req = urllib.request.Request(
                        "https://explorer.pkt.cash/api/v1/PKT/pkt/address/" + address + "/income/30",
                        data = None, 
                        headers = req_headers
                    )
                    with urllib.request.urlopen(req) as res:
                        data = json.load(res)

                        # Mined yesterday:
                        received_yesterday = int(data["results"][0]["received"]) / (2**30)
                        result += "Mined yesterday:\n   " + f"{received_yesterday:,.2f}" + " PKT"
                        if (pkt_usd_price != -1.0):
                            received_yesterday_usd = float(received_yesterday) * pkt_usd_price
                            result += " ($ " + f"{received_yesterday_usd:,.2f}" + ")\n"
                        else:
                            result += "\n"
                        
                        # Mined 7 days ago:
                        received_7daysago = int(data["results"][7]["received"]) / (2**30)
                        result += "Mined 7 days ago:\n   " + f"{received_7daysago:,.2f}" + " PKT"
                        if (pkt_usd_price != -1.0):
                            received_7daysago_usd = float(received_7daysago) * pkt_usd_price
                            result += " ($ " + f"{received_7daysago_usd:,.2f}" + ")\n"
                        else:
                            result += "\n"
                        
                        # Mined 30 days ago:
                        received_30daysago = int(data["results"][30]["received"]) / (2**30)
                        result += "Mined 30 days ago:\n   " + f"{received_30daysago:,.2f}" + " PKT"
                        if (pkt_usd_price != -1.0):
                            received_30daysago_usd = float(received_30daysago) * pkt_usd_price
                            result += " ($ " + f"{received_30daysago_usd:,.2f}" + ")\n"
                        else:
                            result += "\n"
                
                except EnvironmentError:
                    result += ""

        return result