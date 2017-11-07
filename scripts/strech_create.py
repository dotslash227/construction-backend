import pymongo
from pymongo import MongoClient


def main():
    client = MongoClient(host='db', port=27027)
    db = client.construction

    count = 0
    present_tcs = ''
    strech_id = 1
    for chain in db.Chainages.find().sort('lenght', 1):
        if not present_tcs:
            present_tcs = chain['TCS']
            startChain = chain
        if (count >= 100) or present_tcs != chain['TCS']:
            count = 1
            strech = {
                'id': 'strech_' + str(strech_id),
                'name': '%s | %s to %s' % (startChain['road'], startChain['name'], lastchain['name']),
                'tcs': lastchain['TCS'],
                'startChainage': startChain['name'],
                'endChainage': lastchain['name']
            }
            strech_id += 1
            db.Streches.insert(strech)
            present_tcs = chain['TCS']
            startChain = chain
        else:
            count += 1

        lastchain = chain


if __name__ == '__main__':
    main()
