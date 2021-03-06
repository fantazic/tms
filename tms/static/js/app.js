application = new Vue({
  el: '#app',

  ready: function () {
    this.$http.get(
      '/tms/api/me/',
      function (data) {
        console.log(data.message)
        if (data.message == 'Login') {
          this.isLogin = true
          this.user = data.user
          this.date = data.date
          this.tasks = data.tasks
          this.dates = data.dates
          this.preferredHour = data.preferredHour
        }
        this.showBody = true
      }
    ).error(function (data, status, request) {
      console.log(data)
    })

    $.fn.datepicker.defaults.format = "yyyy-mm-dd"
    $.fn.datepicker.defaults.autoclose = true
    $.fn.datepicker.defaults.todayHighlight = true
  },

  data: function () {
    return {
      user: {
        username: null,
        password: null
      },
      message: null,
      isLogin: false,
      isSignup: false,
      showBody: false,
      newTask: {
        task_id: null,
        date: null,
        hour: '1',
        note: null,
        action: null
      },
      date: null,
      dates: [],
      tasks: [],
      taskMessage: null,
      preferredHour: 0,
      hourOptions: new Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
      csrf: this.getCookie('csrftoken')
    }
  },

  computed: {
    formButton: function () {
      return this.isSignup ? 'Register' : 'Login'
    },
    navButton: function () {
      return this.isSignup ? 'Login' : 'Register'
    },
    userErrors: function () {
      for (key in this.user) {
        if (! this.user[key]) return true
      }

      return false
    },
    taskErrors: function () {
      return (! this.newTask.date || this.newTask.date == ''
      || ! this.newTask.note || this.newTask.note == '')
    }
  },

  methods: {
    showSignup: function (e) {
      this.isSignup = !this.isSignup
    },

    signup: function (e) {
      e.preventDefault()

      that = this

      this.$http.post(
        that.isSignup ? '/tms/api/signup/' : '/tms/api/login/',
        that.user,
        function (data) {
          console.log(data.message)
          if (data.message == 'Success') {
            that.message = {type: 'success', message: data.message}
            that.isLogin = true

            that.date = data.date
            that.tasks = data.tasks
            that.dates = data.dates
            that.preferredHour = data.preferredHour
          } else {
            that.message = {type: 'warning', message: data.message}
          }
        },
        {
          headers: {
            "X-CSRFToken": that.csrf
          },
          emulateJSON: true
        }
      ).error(function (data, status, request) {
        console.log(data)
      })
    },

    logout: function (e) {
      that = this

      this.$http.get(
        '/tms/api/logout/',
        function (data) {
          console.log(data.message)
          if (data.message == "Success") {
            that.isLogin = false
            this.user = {'username': '', 'password': ''}
          }
        })
    },

    addTask: function () {
      that = this

      that.taskMessage = null
      that.newTask = {
        task_id: null,
        date: that.date,
        hour: '1',
        note: null,
        action: 'Create'
      }
    },

    updateTask: function (task) {
      that = this

      that.taskMessage = null
      that.newTask = Vue.util.extend({}, task)
      that.newTask.action = 'Edit'
    },

    deleteTask: function (task) {
      that = this

      that.taskMessage = null
      that.newTask = Vue.util.extend({}, task)
      that.newTask.action = 'Delete'
    },

    submitTask: function (e) {
      e.preventDefault()
      that = this

      this.$http.post(
        '/tms/api/crud_task/',
        that.newTask,
        function (data) {
          console.log(data)
          if (data.message == "Success") {
            that.taskMessage = {type: 'success', message: 'Completed ' + that.newTask.action}
            that.newTask = {'date': '', 'hour': '', 'note': ''}
            that.date = data.date
            that.tasks = data.tasks
            that.dates = data.dates

            $('#taskModal').modal('toggle')
          } else {
            that.taskMessage = {type: 'warning', message: data.message}
          }
        },
        {
          headers: {
            "X-CSRFToken": that.csrf
          },
          emulateJSON: true
        }
      ).error(function (data, status, request) {
        console.log(data)
      })
    },

    getDatesAndTasks: function (e) {
      that = this

      this.$http.get(
        '/tms/api/get_dates_and_tasks/',
        {'date': that.date},
        function (data) {
          console.log(data)
          if (data.message == "Success") {
            that.dates = data.dates
            that.tasks = data.tasks
            that.date = data.date
          }
        }
      ).error(function (data, status, request) {
        console.log(data)
      })
    },

    datePrevious: function () {
      this.date = this.dates[0].date
      this.getDatesAndTasks()
    },

    dateNext: function () {
      this.date = this.dates[this.dates.length - 1].date
      this.getDatesAndTasks()
    },

    datePick: function (dd) {
      this.date = dd.date
      this.getDatesAndTasks()
    },

    isToday: function (dd) {
      return this.date == dd.date
    },

    setHour: function () {
      that = this

      this.$http.post(
        '/tms/api/set_hour/',
        { 'hour': that.preferredHour, 'date': that.date },
        function (data) {
          console.log(data)
          if (data.message == "Success") {
            that.dates = data.dates
          }
        },
        {
          headers: {
            "X-CSRFToken": that.csrf
          },
          emulateJSON: true
        }
      ).error(function (data, status, request) {
        console.log(data)
      })
    },

    getCookie: function (name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    }
  }
})
