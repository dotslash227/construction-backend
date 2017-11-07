

if __name__ == '__main__':
    from pymongo import MongoClient
    from copy import deepcopy
    client = MongoClient(host='db', port=27027)
    db = client.construction
    x = open('tcs.txt')
    mpr = {}
    for i in x:
        i = i.replace(' ', '').replace('\n', '')
        i = i.split('\t')
        if i[3] in mpr:
            mpr[i[3]].append({
                'to': float(i[1]),
                'toDisplay': i[1].replace('.', '+'),
                'from': float(i[0]),
                'fromDisplay': i[0].replace('.', '+')
            })
        else:
            mpr[i[3]] = [{
                'to': float(i[1]),
                'toDisplay': i[1].replace('.', '+'),
                'from': float(i[0]),
                'fromDisplay':i[0].replace('.', '+')
            }]

    for k in mpr:
        r = db.TCS.update({'id': k}, {'$set': {'chainages': mpr[k]}})
