<template>
    <div class="deviceInfo">
      <!-- 两端对齐 -->
      <van-row type="flex" justify="space-between">
        <van-col style="" class="title">{{deviceName}}</van-col>
        <van-col style="text-align: right;background:">
          <span v-if="deviceStatus" class="iconfont icon-signal-a" style="color:green;">{{deviceConnectionType}}</span>
          <span v-else class="iconfont icon-wuxinhao-a" style="color:red;">{{deviceConnectionType}}</span>
        </van-col>
      </van-row>
      <van-row type="flex" class="addr">
        <van-col style="">地址：</van-col>
        <van-col style="text-align: left;">{{address}}</van-col>
      </van-row>
      <van-row type="flex" class="deviceNum">
        <van-col style="">设备编号：</van-col>
        <van-col style="text-align: left;">{{deviceNum}}</van-col>
      </van-row>
      <!-- {{deviceInfo}} -->
    </div>
</template>
<script>
import axios from 'axios'
import { eventBus } from '@/main.js'
// import { Toast } from 'vant'

export default {
  data () {
    return {
      deviceInfo: '',
      deviceName: '',
      address: '',
      deviceNum: '',
      deviceSign: '',
      deviceStatus: false,
      deviceConnectionType: ''
    }
  },
  methods: {
    async getDeviceInfo (deviceNum, authorization) {
      await this.requestGetDeviceInfo(deviceNum, authorization).then(res => {
        this.deviceInfo = res
        // alert(res)
        // this.deviceName = res.data.device.deviceName
        // this.address = res.data.device.address
        // this.deviceNum = res.data.device.deviceNum
      })
      if (this.deviceInfo.code === 1) {
        // 显示正在充电的端口 把数据传给App.vue父组件组件
        this.$emit('eventPortList', this.deviceInfo)
        // 将数据传给portTimeSelece.vue 判断是否是支持免费充电
        eventBus.$emit('getDeviceInfoForIsFreeCharge', this.deviceInfo)
        // console.log('**********************', this.deviceInfo)
        this.deviceName = this.deviceInfo.data.device.deviceName
        this.address = this.deviceInfo.data.device.address
        this.deviceNum = this.deviceInfo.data.device.deviceNum

        await axios.get('/query?device_num=' + (this.deviceNum) + '&company_id=2')
          .then(res => {
            // console.log('********************', res.data.data)
            this.deviceSign = res.data.data.sign
            this.deviceStatus = res.data.data.status
            this.deviceConnectionType = res.data.data.connectionType
          })
      }
      //  else {
      //   Toast.fail(this.dataInfo.message)
      // }
      eventBus.$emit('isCorrectDeviceEvent', this.deviceInfo)
    },
    async requestGetDeviceInfo (deviceNum, authorization) {
      // alert(authorization)
      var dataInfo = ''
      await axios({
        method: 'post',
        url: '/device/getChargeInfo',
        data: {
          device_num: deviceNum,
          authorization: authorization
        },
        // headers: {
        //   authorization: authorization
        // },
        timeout: 1000
      })
        .then(function (response) {
          console.log(JSON.parse(response.request.response))
          dataInfo = JSON.parse(response.request.response)
        })
        .catch(function (error) {
          console.log(error)
        })
      return dataInfo
    }
  }
}
</script>
<style lang="scss" scoped>
.deviceInfo{
  margin: 16px;
}
.title {
  font-size: 16px;
  // color: green;
}
.addr {
  font-size: 12px;
  // color: green;
}
.deviceNum {
  font-size: 12px;
  // color: green;
}
</style>
