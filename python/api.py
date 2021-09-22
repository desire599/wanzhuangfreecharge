from flask import Flask, request
import pymysql, requests, time, json

app = Flask(__name__)

config = {
    "host": "localhost",
    "user": "test2",
    "passwd": "123456",
    "dbName": "test2"
}


def insert(data):
    # 打开数据库连接
    db = pymysql.connect(host=config['host'], user=config['user'], password=config['passwd'], database=config['dbName'])
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from info"
    # sql2 = "insert into info hour = '%s'" % (hour_dec) + " where id = '%s'" % id_d
    sql1 = "INSERT INTO info (deviceNum,companyId,devicePort,authorization,hour,timestamp,total_hours) VALUES (%s,%s," \
           "%s,%s,%s,%s,%s) "
    infoArr = []
    try:
        # 执行SQL语句
        cursor.execute(sql1, (
            data['device_num'], data['company_id'], data['device_port'], data['authorization'], data['hours'],
            data['timestamp'], data['hours']))
        # 执行update操作时需要写这个，否则就会更新不成功！！！
        db.commit()
        # 获取所有记录列表
        # results = cursor.fetchall()
        # print(results)
        # for row in results:
        #     info_dict = {'id': row[0], 'deviceNum': row[1], 'companyId': row[2], 'devicePort': row[3],
        #                  'authorization': row[4], 'hour': row[5]}
        #     infoArr.append(info_dict)
        # print(row)
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()
    return infoArr


def delete(data):
    # 打开数据库连接
    db = pymysql.connect(host=config['host'], user=config['user'], password=config['passwd'], database=config['dbName'])
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    print(data)
    # SQL 查询语句
    sql = "delete from info where deviceNum = %s and devicePort=%s"
    try:
        # 执行SQL语句
        cursor.execute(sql, (
            data['device_num'], data['device_port']))
        # 执行update操作时需要写这个，否则就会更新不成功！！！
        db.commit()
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()


@app.route("/uploadInfo", methods=['GET', 'POST'])
def uploadInfo():
    if request.method == 'GET':
        # q = request.args['device_num']
        q = request.args.get('device_num')
        print(q)
        return "Hello, World!GET"
    else:
        data = request.get_json()
        print(data)
        insert(data)
        return data


@app.route("/getAuth", methods=['GET', 'POST'])
def getAuth():
    if request.method == 'GET':
        # 打开数据库连接
        db = pymysql.connect(host=config['host'], user=config['user'], password=config['passwd'],
                             database=config['dbName'])
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语句
        sql = "select * from user where user_id=" + "1"
        # sql2 = "insert into info hour = '%s'" % (hour_dec) + " where id = '%s'" % id_d
        # infoArr = []
        info_dict = {}
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 执行update操作时需要写这个，否则就会更新不成功！！！
            db.commit()
            # 获取所有记录列表
            results = cursor.fetchall()
            print(results)
            for row in results:
                info_dict = {'authorization': row[1]}
                # infoArr.append(info_dict)
            # print(row)
        except:
            print("Error: unable to fetch data")
        # 关闭数据库连接
        db.close()
        print(info_dict)
        return info_dict['authorization']
    else:
        return "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MzE5NjA5NjksIm5iZiI6MTYzMTk2MDk2OCwiZXhwIjoxNjMyNTY1NzY5LCJ1X2lkIjozMDYzMzM0LCJ1X3R5cGUiOjEsImNvbXBhbnlfaWQiOjIsImlzcyI6ImRpZGlfd3oifQ.LXGHp6c1osHOOXIyo-P4-G-_IjITO1aB43FwcjPM3dY"


@app.route("/device/getChargeInfo", methods=['POST'])
def getChargeInfo():
    # device_num = request.args.get('device_num')
    # authorization = request.args.get('authorization')
    data = request.get_json()
    headers = {'authorization': data['authorization']}
    r = requests.get('https://webapi.wanzhuangkj.com/device/getChargeInfo?device_num=' + data['device_num'],
                     headers=headers).json()
    print(data)
    # time.sleep(2)
    return r


# 停止端口充电
@app.route("/device/stop_charge", methods=['POST'])
def stop_charge():
    data_r = request.get_json()
    data = {
        'charge_id': data_r['charge_id'],
    }
    headers = {
        'authorization': request.headers['authorization']
    }
    print(request.headers['authorization'])
    response = requests.post('https://webapi.wanzhuangkj.com/device/deviceChargeOver', headers=headers,
                             data=data).json()
    print("stop_charge()", response)
    delete(data_r)
    return response


# 支付开始充电 deviceNum：装置号 portIdx：端口号 从1开始
@app.route("/pay/request", methods=['POST'])
def pay_for_charge():
    data_r = request.get_json()
    data2 = {
        'operation': 'pay_for_charge',
        'pay_type': 'wxpay',  # 支付类型wxpay：微信支付
        'total_fee': '100',  # 总消费
        # 'device_num': '18201954',
        'device_num': data_r['device_num'],
        # 'device_port': '3',
        'device_port': data_r['device_port'],
        'isFreeCharge': '1'
    }
    headers = {
        'authorization': request.headers['authorization']
    }
    response = requests.post('https://webapi.wanzhuangkj.com/pay/request', headers=headers, data=data2).json()
    print(response)
    return response


@app.route("/query", methods=['GET'])
def query():
    response = requests.get('https://websocket.wanzhuangkj.com/query?device_num='+request.args.get('device_num')+'&company_id='+request.args.get('company_id')).json()
    # print(response)
    return response


if __name__ == '__main__':
    # app.debug(true)
    app.run()
