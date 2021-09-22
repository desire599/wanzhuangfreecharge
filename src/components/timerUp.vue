<template>
    <div class="timer">
        <div ref="startTimer" v-html="timeValue">00:00:00</div>
    </div>
</template>

<script>
export default {
  name: 'Timer',
  props: {
    time: {
      type: Number
    }
  },
  data () {
    return {
      timer: '',
      oldTimer: '',
      seconds: 0,
      timeValue: ''
    }
  },
  created () {
    // this.timer = setInterval(this.startTimer, 1000)
    if (this.time) {
      this.seconds = this.time
    }
    this.timeValue = '00:00:00'
    this.restart(this.seconds)
  },
  // 在created中 进行了 this.seconds = this.time 所以去掉了watch
  // watch: {
  //   time () {
  //     this.seconds = this.time
  //     // 经过考虑 其实不用做到实时更新 首次创建 created() 的时候开始一个定时器就行
  //     // this.restart(this.seconds)
  //     // console.log('time变化了')
  //   }
  // },
  methods: {
    startTimer () {
    //   this.seconds = this.time
      this.timeValue = this.computeTime(this.seconds++)
    },
    computeTime (second) {
      let hours = 0; let minutes = 0; let seconds = 0
      hours = Math.floor((second % 86400) / 3600)
      minutes = Math.floor(((second % 86400) % 3600) / 60)
      seconds = Math.floor(((second % 86400) % 3600) % 60)
      if (hours < 10) {
        hours = '0' + hours
      }
      if (minutes < 10) {
        minutes = '0' + minutes
      }
      if (seconds < 10) {
        seconds = '0' + seconds
      }
      return hours + ':' + minutes + ':' + seconds
      // return hours + ':' + minutes
    },
    stop () {
    //   if (this.timer) {
    //     clearInterval(this.timer)
    //   }
      if (this.oldTimer) {
        clearInterval(this.oldTimer)
      }
    },
    start (seconds) {
      this.seconds = seconds
      this.timer = setInterval(this.startTimer, 1000)
    },
    restart (seconds) {
      this.oldTimer = this.timer
      this.start(seconds)
      this.stop()
    }
  }
}
</script>
