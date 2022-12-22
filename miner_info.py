import urllib.request, json

# https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
# https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
# https://stackoverflow.com/questions/4435169/how-do-i-append-one-string-to-another-in-python

def get_miner_info(pkt_addresses):
    
    result = "<b>Miner statistics</b>\n"
    
    for pkt_address in pkt_addresses:

        pkt_address = str(pkt_address[0]).lower()
        
        result += "\nAddress: " + pkt_address + "\n"

        with urllib.request.urlopen("https://explorer.pkt.cash/api/v1/PKT/pkt/address/" + pkt_address) as url:
            data = json.load(url)

            balance = int(data["balance"]) / (2**30)
            mined24 = int(data["mined24"]) / (2**30)
            unconsolidated_txns = int(data["balanceCount"])

            result += "Address balance: " + f"{balance:,.2f}" + " PKT\n"
            result += "Unconsolidated Txns: " + str(unconsolidated_txns) + "\n"

            if (unconsolidated_txns > 1200):
                result += "You should fold your coins again!\n"

            result += "\n"
            result += "Mined last 24 hours: " + f"{mined24:,.2f}" + " PKT\n"

        with urllib.request.urlopen("https://explorer.pkt.cash/api/v1/PKT/pkt/address/" + pkt_address + "/income/30") as url:
            data = json.load(url)

            received_yesterday = int(data["results"][0]["received"]) / (2**30)
            received_7daysago = int(data["results"][7]["received"]) / (2**30)
            received_30daysago = int(data["results"][30]["received"]) / (2**30)

            result += "Mined yesterday: " + f"{received_yesterday:,.2f}" + " PKT\n"
            result += "Mined 7 days ago: " + f"{received_7daysago:,.2f}" + " PKT\n"
            result += "Mined 30 days ago: " + f"{received_30daysago:,.2f}" + " PKT\n"

    return result