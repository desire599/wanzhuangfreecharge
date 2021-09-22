<template>
    <div>
        <van-dialog v-model="dialogShow" title="充电时间" show-cancel-button :before-close="beforeClose" width="300px">
          <van-row type="flex" justify="center">
            <van-col span="12" style="padding-left:65px">
              <van-stepper v-model="hours" min="1" max="10" step="1" integer disable-input  button-size="22" />
            </van-col>
            <van-col span="12" style="padding-left:30px">
              小时
            </van-col>
          </van-row>
            <!-- {{dialogShow}} -->
        </van-dialog>
      <!-- <van-button type="primary" @click="handlerButton">主要按钮</van-button> -->
      <!-- {{this.portIdx}}:{{this.equipmentNo}} -->
    </div>
</template>
<script>
import axios from 'axios'
// import qs from 'qs'
import { Loading } from 'element-ui'
import { eventBus } from '@/main.js'
import { Toast } from 'vant'

export default ({
  data () {
    return {
      show: true,
      hours: 1,
      deviceInfo: {}
    }
  },
  props: {
    dialogShow: {
      type: Boolean,
      default: false
    },
    portIdx: {
      type: String,
      default: ''
    },
    equipmentNo: {
      type: String,
      default: ''
    },
    authorizationValue: {
      type: String,
      default: ''
    }
  },
  watch: {
    authorizationValue () {
      console.log('authorizationValue 变化了')
    }
  },
  created () {
    eventBus.$on('getDeviceInfoForIsFreeCharge', (deviceInfo) => {
      // alert(deviceInfo)
      this.deviceInfo = deviceInfo
    })
  },
  methods: {
    async beforeClose (action, done) {
      // alert(action)
      // alert(this.deviceInfo.data.isFreeCharge)
      console.log(action)
      await this.$emit('event', action)
      console.log('执行了beforeClose')
      if (action === 'confirm') {
        if (this.deviceInfo.data.isFreeCharge) {
          // 发送ajax请求
          let timestamp = ''
          // 同步等待获取timestamp
          const loadingInstance = Loading.service({ text: '等待开始充电...', lock: true, spinner: '' })
          await this.payCharge(this.equipmentNo, this.portIdx, this.authorizationValue).then(res => { timestamp = res })
          setTimeout(function () {
            loadingInstance.close()
          }, 3000)
          // console.log(timestamp, 'tes2')
          // setTimeout(() => {
          //   console.log('执行了axios', this.hours, this.portIdx, this.equipmentNo, timestamp)
          // }, 1000)
          console.log('执行了axios', this.hours, this.portIdx, this.equipmentNo, timestamp, this.authorizationValue)
          // 请求上面数据到数据库
          this.authorization = this.authorizationValue
          this.companyId = '2'
          // this.hours, timestamp || String(Number.parseInt((new Date()).valueOf() / 1000)) 如果时间戳为空 则用js计算的的时间戳上传到数据库
          this.uploadInfo(this.equipmentNo, this.companyId, this.portIdx, this.authorization, this.hours, timestamp || String(Number.parseInt((new Date()).valueOf() / 1000)))
        } else {
          Toast.fail('该设备不支持免费充电')
        }
        done()
      } else {
        done()
      }
    },
    async payCharge (deviceNum, devicePort, authorization) {
      var timestamp = ''
      await axios({
        method: 'post',
        url: '/pay/request',
        data: {
          operation: 'pay_for_charge',
          pay_type: 'wxpay',
          total_fee: '100',
          device_num: deviceNum,
          device_port: devicePort,
          isFreeCharge: '1'
        },
        headers: {
          authorization: authorization
        },
        timeout: 1000

      })
        .then(function (response) {
          console.log(JSON.parse(response.request.response))
          if (JSON.parse(response.request.response).code === 1) {
            timestamp = JSON.parse(response.request.response).timestamp
          }
        })
        .catch(function (error) {
          console.log(error)
        })
      // console.log(timestamp, 'test')
      return timestamp
    },
    async uploadInfo (deviceNum, companyId, devicePort, authorization, hours, timestamp) {
      console.log('upload', {
        device_num: deviceNum,
        company_id: companyId,
        device_port: devicePort,
        authorization: authorization,
        hours: hours,
        timestamp: timestamp
      })
      await axios({
        url: '/uploadInfo',
        method: 'post',
        data: {
          device_num: deviceNum,
          company_id: companyId,
          device_port: devicePort,
          authorization: authorization,
          hours: hours,
          timestamp: timestamp
        },
        // params: {
        //   device_num: '1234567'
        // },
        headers: {
          'content-type': 'application/json'
          // authorization: ''
        },
        timeout: 1000
      })
        .then(function (response) {
          console.log(response)
        })
        .catch(function (error) {
          console.log(error)
        })
      // await axios.get('http://localhost:5000/uploadInfo?device_num=123456')
      //   .then(res => { console.log(res.data.data); this.datalist = res.data.data })
    },
    handlerButton () {
      // this.uploadInfo(this.deviceNum, this.companyId, this.device_port, this.authorization, this.hours)
      const loadingInstance = Loading.service()
      setTimeout(function () {
        // this.$nextTick(() => { // 以服务的方式调用的 Loading 需要异步关闭
        loadingInstance.close()
      // }
      }, 3000)
    }
  }
  //   mounted: {
  //       show=this.dialogShow
  //   }

})
</script>
