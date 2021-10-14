<template>
  <div>
    <deviceInfo ref="deviceInfo" @eventPortList="getPortList"></deviceInfo>
    <deviceSelect ref="deviceSelect" @event="getEquipmentNo" @eventDeviceInfo="getDeviceInfo" :equipment-no="equipmentNo"></deviceSelect>
    <van-divider></van-divider>
    <devicePortStatus ref="devicePortStatus" @event="handlerDialogShow" @event1="getDevicePortStatus2" :equipment-no="equipmentNo"></devicePortStatus>
    <portTimeSelect :dialog-show="dialogIsShow" :port-idx="portIdx" :equipment-no="equipmentNo" :authorization-value="authorizationValue" @event="handlerBeforeClose"></portTimeSelect>
    <authorizationText @event="handlerGetAuth" ref="authorizationText"></authorizationText>
    <portList :port-list-data="portListData" :authorization-value="authorizationValue">
      <!-- {{portListData}} -->
    </portList>
    <van-tabbar v-model="active" >
      <van-tabbar-item @click="notClickMe" name="home" icon="home-o">不</van-tabbar-item>
      <van-tabbar-item @click="notClickMe" name="search" icon="search">要</van-tabbar-item>
      <van-tabbar-item @click="notClickMe" name="friends" icon="friends-o">点</van-tabbar-item>
      <van-tabbar-item @click="notClickMe" name="setting" icon="setting-o">我</van-tabbar-item>
      <van-popup v-model="show" round position="bottom" :closeable="true" :style="{ height: '30%' }" >
        <img src="@/static/1.jpeg" height="80%" style="margin:5% 0 0 28%" alt="" srcset="">
      </van-popup>
    </van-tabbar>
    <!-- <qrReader></qrReader> -->
  </div>

</template>
<script>
import devicePortStatus from '@/charge/devicePortStatus.vue'
import portTimeSelect from '@/charge/portTimeSelect.vue'
import deviceSelect from '@/charge/deviceSelect.vue'
import authorizationText from '@/charge/authorizationText.vue'
import deviceInfo from '@/charge/showDeviceInfo.vue'
import portList from '@/charge/showPortList.vue'
// import qrReader from '@/components/QrReader.vue'
// import Vue from 'vue'

// import Vue from 'vue'
// Vue.component(devicePortStatus,'dv')
import Vue from 'vue'
import { Toast } from 'vant'
Vue.use(Toast)

export default ({
  data () {
    return {
      dialogIsShow: false,
      portIdx: '',
      equipmentNo: '18201954', // 这里设置默认值,
      authorizationValue: '',
      active: '',
      show: false,
      portListData: {}
    }
  },
  components: {
    devicePortStatus,
    portTimeSelect,
    deviceSelect,
    authorizationText,
    deviceInfo,
    portList
    // qrReader
  },
  mounted () {
    // this.$refs.deviceSelect.eventEmit()
    // alert(this.authorizationValue)
    // console.log(this.authorizationValue)
  },
  beforeUpdate () {
    // alert(this.authorizationValue)
    // this.$refs.deviceSelect.eventEmit()
  },
  watch: {
    authorizationValue () {
      // alert(this.authorizationValue)
      this.$refs.deviceSelect.eventEmit()
    }
  },
  methods: {
    handlerDialogShow (index, dataList) {
      // if (dataList.port[index].errMsg === '设备已离线') {
      if (dataList.port[index].errMsg) {
        Toast.fail(dataList.port[index].errMsg)
      } else {
        console.log('执行了handlerDialogShow', index)
        this.portIdx = String(index + 1)
        this.dialogIsShow = !this.dialogIsShow
      }
    },
    handlerBeforeClose (action) {
      // alert(action)
      console.log('执行了handlerBeforeClose')
      this.dialogIsShow = !this.dialogIsShow
      this.$refs.authorizationText.handlerAuth()
      // if(action === 'cancel')
      if (action === 'confirm') {
        // 通过获取更新充电列表
        // 延时4s左右 等待充电请求完成 否则将无法正常更新数据
        setTimeout(() => {
          this.$refs.deviceSelect.eventEmit()
        }, 4500)
      } else {
        // 点击cancel返回键 则没有进行发送充电请求 不用等待 直接请求更新
        this.$refs.deviceSelect.eventEmit()
      }
    },
    getEquipmentNo (equipmentNo) {
      this.equipmentNo = equipmentNo
      this.$refs.devicePortStatus.getDevicePortStatus(equipmentNo)
      console.log('执行了getEquipmentNo', equipmentNo, this.equipmentNo)
    },
    handlerGetAuth (authorization) {
      console.log('执行了handlerGetAuth', authorization)
      this.authorizationValue = authorization
    },
    refreshTimer () {
      // this.$refs.headerChild.restart(630)
    },
    getDevicePortStatus2 () {
      console.log('tes')
      this.$refs.deviceSelect.handlerButton()
    },
    getDeviceInfo (deviceNum) {
      this.$refs.authorizationText.handlerAuth()
      console.log('getDeviceInfo ', 'App.vue 75行')
      this.$refs.deviceInfo.getDeviceInfo(deviceNum, this.authorizationValue)
    },
    getPortList (res) {
      this.portListData = res
      // console.log('###########', this.portListData)
      // alert(res)
    },
    notClickMe (event) {
      this.show = !this.show
      console.log(event.target)
      switch (event.target.innerHTML) {
        case '不' : this.show = !this.show
      }
    }
  }

})
</script>
