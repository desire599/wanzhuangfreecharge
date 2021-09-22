<template>
    <div>
        <!-- <van-notice-bar
            :scrollable="false"
            :text="'当前设备编号：' + equipmentNo"
            /> -->
        <van-cell-group>
            <van-field v-model="equipmentNoValue" label="设备编号" placeholder="请输入设备编号">
                <template #button>
                    <van-button size="small" type="primary" @click="eventConfirm">确认</van-button>
                </template>
            </van-field>
        </van-cell-group>
    </div>
</template>
<script>
// import { Loading } from 'element-ui'
import Vue from 'vue'
import { Toast } from 'vant'
import { eventBus } from '@/main.js'

Vue.use(Toast)
export default {
  data () {
    return {
      equipmentNoValue: '',
      defaultValue: '18201954'
    }
  },
  props: {
    equipmentNo: {
      type: String,
      default: ''
    }
  },
  methods: {
    handlerButton () {
      // 获取装置端口状态信息数据
      this.$emit('event', this.defaultValue)
    },
    eventConfirm () {
      // console.log(this.equipmentNoValue.length)
      if (this.equipmentNoValue && this.equipmentNoValue.length === 8) {
        // this.defaultValue = this.equipmentNoValue
        // 获取装置地址信息
        this.$emit('eventDeviceInfo', this.equipmentNoValue)
        eventBus.$on('isCorrectDeviceEvent', (deviceInfo) => {
          if (deviceInfo.code === 1) {
            // Toast.success(deviceInfo.message === 'success' ? '成功' : '')
            this.defaultValue = this.equipmentNoValue
          } else {
            Toast.fail(deviceInfo.message)
          }
        })
        Toast.loading({
          message: '加载中...',
          forbidClick: true,
          duration: 2000
        })
      } else {
        Toast.fail('设备编号有误')
        // this.$emit('eventDeviceInfo', this.defaultValue)
      }
    },
    eventEmit () {
      // 获取装置地址信息
      this.$emit('eventDeviceInfo', this.defaultValue)
    }

  }
}
</script>
