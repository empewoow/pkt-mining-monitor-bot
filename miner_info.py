import urllib.request, json
#import constants

# https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
# https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
# https://stackoverflow.com/questions/4435169/how-do-i-append-one-string-to-another-in-python

def get_miner_info(pkt_address):

    address = str(pkt_address).lower()
    result = "<b>Miner statistics</b>\n\n"
    result += "Address: " + pkt_address + "\n"

    with urllib.request.urlopen("https://explorer.pkt.cash/api/v1/PKT/pkt/address/" + address) as url:
        data = json.load(url)

        balance = int(data["balance"]) / (2**30)
        mined24 = int(data["mined24"]) / (2**30)
        unconsolidated_txns = int(data["balanceCount"])

        result += "Address balance: " + "%.2f" % balance + " PKT\n"
        result += "Unconsolidated Txns: " + str(unconsolidated_txns) + "\n"

        if (unconsolidated_txns > 1200):
            result += "You should fold your coins again!\n"

        result += "\n"
        result += "Mined last 24 hours: " + "%.2f" % mined24 + " PKT\n"

    with urllib.request.urlopen("https://explorer.pkt.cash/api/v1/PKT/pkt/address/" + address + "/income/30") as url:
        data = json.load(url)

        received_yesterday = int(data["results"][0]["received"]) / (2**30)
        received_7daysago = int(data["results"][7]["received"]) / (2**30)
        received_30daysago = int(data["results"][30]["received"]) / (2**30)

        result += "Mined yesterday: " + "%.2f" % received_yesterday + " PKT\n"
        result += "Mined 7 days ago: " + "%.2f" % received_7daysago + " PKT\n"
        result += "Mined 30 days ago: " + "%.2f" % received_30daysago + " PKT"

    return result

#print(get_miner_info(constants.PKT_ADDRESS))