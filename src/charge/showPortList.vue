<template>
    <div>
      <el-empty v-if="emptyIsShow" description="没有属于本网页的端口在充电...">
        <!-- {{emptyIsShow}} -->
      </el-empty>
      <div v-if="listShow">
        充电列表：
        <br/>
        <!-- {{portListData.data.portList}} -->
        <slot></slot>
        <van-list
            v-model="loading"
            :finished="finished"
            finished-text="没有更多了"
            >
            <van-cell v-for="(item,index) in list" :key="item.id" :title="computeText(item)" >
              <!-- {{item}} -->
              <!-- {{index}} -->
                <van-button @click="stopCharge(index,item.id,item.deviceNum,item.devicePort)" type="warning"  icon="icon-power" size="mini" style="">
                    <span class="iconfont icon-power" style="font-size:10px"> 停止充电</span>
                </van-button>
            </van-cell>
        </van-list>
    </div>
    </div>

</template>
<script>
import '@/icon/iconfont.css'
import axios from 'axios'
import { Loading } from 'element-ui'
import Vue from 'vue'
import { Dialog } from 'vant'

// 全局注册
Vue.use(Dialog)
export default {
  data () {
    return {
      list: [],
      loading: false,
      finished: false,
      emptyIsShow: false,
      listShow: true
    }
  },
  props: {
    portListData: {
      type: Object
      // default: function () {
      //   return {

      //   }
      // }
    },
    authorizationValue: {
      type: String,
      default: ''
    }
  },
  watch: {
    portListData () {
      // alert(this.portListData.data.portList.length)
      if (this.portListData.data.portList.length === 0) {
        // 加载状态结束
        // this.loading = false
        this.emptyIsShow = true
        this.listShow = false
      } else {
        this.emptyIsShow = false
        this.listShow = true
        this.list = []
        for (let i = 0; i < this.portListData.data.portList.length; i++) {
        // this.list.push(this.portListData.data.portList[i].deviceNum + '---' + this.portListData.data.portList[i].devicePort + '号端口正在充电')
          this.list.push(this.portListData.data.portList[i])
          // 加载状态结束
          this.loading = false
          // 数据全部加载完成
          if (this.list.length >= this.portListData.data.portList.length) {
            this.finished = true
          }
        }
      // 加载状态结束
      // this.loading = false
      }
    },
    authorizationValue () {
      // console.log('authorizationValue 变化了')
    }
  },
  computed: {
    computeText () {
      return (portData) => {
        return portData.deviceNum + '--' + portData.devicePort + '号端口正在充电'
      }
    }
  },
  methods: {
    beforeClose (action, done) {
      if (action === 'confirm') {
        this.sendStopChargeRequest()
        // setTimeout(done, 1000)
        done()
      } else {
        done()
      }
    },
    async stopCharge (index, chargeId, deviceNum, devicePort) {
      // alert(index)
      Dialog.confirm({
        title: '提示',
        message: '是否结束充电？',
        theme: 'round-button',
        // beforeClose: this.beforeClose()
        beforeClose: (action, done) => {
          if (action === 'confirm') {
            done()
            this.sendStopChargeRequest(chargeId, deviceNum, devicePort)
            this.list.splice(index, 1) // 移除数组指定元素
            if (this.list.length === 0) {
              this.emptyIsShow = true
              this.listShow = false
            }
          } else {
            done()
          }
        }
      }).then(() => {
        // on confirm
      }).catch(() => {
        // on cancel
      })
      // // 移除数组指定元素
      // this.list.splice(index, 1)
    },
    async sendStopChargeRequest (chargeId, deviceNum, devicePort) {
      const loadingInstance = Loading.service({ text: '正在停止充电...', lock: true, spinner: '' })
      // alert(this.authorizationValue)
      await axios({
        method: 'post',
        url: '/device/stop_charge',
        headers: {
          // authorization: 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MzE5NjA5NjksIm5iZiI6MTYzMTk2MDk2OCwiZXhwIjoxNjMyNTY1NzY5LCJ1X2lkIjozMDYzMzM0LCJ1X3R5cGUiOjEsImNvbXBhbnlfaWQiOjIsImlzcyI6ImRpZGlfd3oifQ.LXGHp6c1osHOOXIyo-P4-G-_IjITO1aB43FwcjPM3dY'
          authorization: this.authorizationValue
        },
        data: {
          charge_id: chargeId,
          device_num: deviceNum,
          device_port: devicePort
        }
        // timeout: 1000
      })
        .then(function (response) {
          console.log(response.request.response)
          // alert(response.request.response)
        })
        .catch(function (error) {
          console.log(error)
        })

      setTimeout(function () {
        loadingInstance.close()
      }, 500)
    }
  }
}
</script>
