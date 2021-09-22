import requests
import smtplib  # smtp服务器
from email.mime.text import MIMEText  # 邮件文本
import pymysql
import time, json, datetime

config = {
    "host": "localhost",
    "user": "test2",
    "passwd": "123456",
    "dbName": "test2"
}

headers = {
    'authorization': 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MzE0MzM4NTYsIm5iZiI6MTYzMTQzMzg1NSwiZXhwIjoxNjMyMDM4NjU2LCJ1X2lkIjozMDYzMzM0LCJ1X3R5cGUiOjEsImNvbXBhbnlfaWQiOjIsImlzcyI6ImRpZGlfd3oifQ.l42Zv6A16_onNUPHrBncEUeBLntUuC1NKYWWRfUCZyg',
}


# 获取到装置中各个端口的信息 deviceNum：装置号
def get_device_info(device_num):
    text = requests.get("https://websocket.wanzhuangkj.com/query?device_num=" + device_num + "&company_id=2").json()
    info = text['data']['port']
    # print(info)
    return info


# 获取到装置的端口的数据 deviceNum：装置号 portIdx：端口号 从1开始
def get_port_data(device_num, port_idx):
    port_data = get_device_info(device_num)
    # print(port_data[port_idx])
    return port_data[int(port_idx) - 1]


# 支付开始充电 deviceNum：装置号 portIdx：端口号 从1开始
def pay_for_charge(device_num, port_idx):
    data2 = {
        'operation': 'pay_for_charge',
        'pay_type': 'wxpay',  # 支付类型wxpay：微信支付
        'total_fee': '100',  # 总消费
        # 'device_num': '18201954',
        'device_num': device_num,
        # 'device_port': '3',
        'device_port': port_idx,
        'isFreeCharge': '1'
    }
    response = requests.post('https://webapi.wanzhuangkj.com/pay/request', headers=headers, data=data2).json()
    # print(response)
    return response


# 获取装置各个端口的状态信息数据
def get_all_ports_data():
    device_num = '18201954'
    company_id = '2'
    response = requests.get(
        'https://websocket.wanzhuangkj.com/query?device_num=' + device_num + '&company_id=' + company_id).json()
    # print(response)
    return response


# 停止端口充电
def stop_charge(charge_id):
    data = {
        'charge_id': str(charge_id),
    }
    response = requests.post('https://webapi.wanzhuangkj.com/device/deviceChargeOver', headers=headers,
                             data=data).json()
    # print("stop_charge()",response)
    return response


# 从数据库中获取数据
def get_data_from_db():
    # 打开数据库连接
    db = pymysql.connect(host=config['host'], user=config['user'], password=config['passwd'], database=config['dbName'])
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from info"
    infoArr = []
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results)
        for row in results:
            info_dict = {'id': row[0], 'deviceNum': row[1], 'companyId': row[2], 'devicePort': row[3],
                         'authorization': row[4], 'hour': row[5], 'timestamp': row[6], 'total_hours': row[7]}
            infoArr.append(info_dict)
            # print(row)
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()
    return infoArr


def auto_charge(device_num, port_idx, hour, timestamp, total_hours):
    # 判断距离开始充电是否过去一小时 有误差 相隔时间越大误差越小
    if int(time.time()) > (int(timestamp) + 60*60 + 60*60 * (int(total_hours) - int(hour))):
        print("过去了1一小时", {'port_idx': port_idx, 'timestamp': timestamp})
        if hour > 0:
            # 获取charge_id
            charge_id = get_port_data(device_num=device_num, port_idx=int(port_idx))['chargeId']
            # 停止充电
            response = stop_charge(charge_id)
            # print(response)
            if response['code'] == 1:
                print('装置：' + str(device_num) + ',端口：' + str(port_idx) + ",charge_id:" + str(
                    charge_id) + ',已停止充电', response)
            else:
                print('装置：' + str(device_num) + ',端口：' + str(port_idx) + ",charge_id:" + str(
                    charge_id) + ',停止充电失败', response)

            time.sleep(3)  # 延迟3秒，否则太快可能还没停止

            # 支付充电
            response = pay_for_charge(device_num=device_num, port_idx=port_idx)
            if response['code'] == 1:
                print('装置：' + str(device_num) + ',端口：' + str(port_idx) + ',已开始充电', response)
            else:
                print('装置：' + str(device_num) + ',端口：' + str(port_idx) + ',开始充电失败', response)
        return {'code': 1, 'message': 'auto_charge() success'}
    else:
        return {'code': -1, 'message': 'auto_charge() fail,Less than an hour'}


def hour_decreace(id_d, hour, step):
    # 打开数据库连接
    # db = pymysql.connect(config['host'], config['user'], config['passwd'], config['dbName'])
    db = pymysql.connect(host=config['host'], user=config['user'], password=config['passwd'],
                         database=config['dbName'])

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    hour_dec = hour - step
    if hour_dec > 0:

        # SQL 查询语句
        sql = "UPDATE info SET hour = '%s'" % (hour_dec) + " where id = '%s'" % id_d
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 执行update操作时需要写这个，否则就会更新不成功！！！
            db.commit()
        except:
            print("Error: unable to fetch data")
    else:
        # SQL 查询语句
        sql = "delete from info where id = '%s'" % id_d
        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
        except:
            print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    # 返回当前剩余的hour
    print(hour_dec)
    return hour_dec


def main():
    # 循环执行10分钟
    count = 0
    while 1:
        print("检测中...", count, "***", str(int(time.time())),
              time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        # 执行任务代码
        test3()
        time.sleep(3)
        count = count + 1
        if count > 200:
            break


def test3():
    # 获取数据库中的数据
    infoArr = get_data_from_db()
    # print(infoArr)
    # 遍历每个元组的数据
    for item in infoArr:
        res = auto_charge(device_num=item['deviceNum'], port_idx=item['devicePort'], hour=item['hour'],
                          timestamp=item['timestamp'], total_hours=item['total_hours'])
        if res['code'] == 1:  # auto_charge 成功执行了
            # 将数据库中的hour减1
            current_hour = hour_decreace(id_d=item['id'], hour=item['hour'], step=1)
            # 如果当前剩余时间为0，则停止充电
            if current_hour == 0:
                # 获取charge_id
                charge_id = get_port_data(device_num=item['deviceNum'], port_idx=item['devicePort'])['chargeId']
                # 停止充电
                stop_charge(charge_id)
                print("停止充电", charge_id)


if __name__ == '__main__':
    main()
