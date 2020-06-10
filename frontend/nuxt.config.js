import colors from 'vuetify/es5/util/colors'

const DEV = process.env.NODE_ENV !== 'production'

export default {
  mode: 'spa',
  dev: DEV,
  /*
   ** Headers of the page
   */
  head: {
    titleTemplate: '%s',
    title: 'Area de clientes Gestion Group',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || '',
      },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },
  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#fff' },
  /*
   ** Global CSS
   */
  css: [],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: [{ src: '~/plugins/vue-swal', mode: 'client' }],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: ['@nuxtjs/vuetify', '@nuxtjs/date-fns'],
  /*
   ** Nuxt.js modules
   */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/auth',
  ],
  /*
   ** Axios module configuration
   ** See https://axios.nuxtjs.org/options
   */
  axios: {
    browserBaseURL: !DEV
      ? 'https://areaclientes.gestiongroup.es/api'
      : 'http://localhost:8000/api',
    proxy: true,
  },
  proxy: {
    '/api/': !DEV
      ? 'https://areaclientes.gestiongroup.es/'
      : 'http://localhost:8000/',
  },
  auth: {
    redirect: {
      login: '/offers',
      logout: '/login',
      home: '/offers',
    },
    resetOnError: true,
    cookie: false,
    fetchUserOnLogin: true,
    strategies: {
      local: {
        endpoints: {
          login: {
            url: 'users/login',
            method: 'post',
            propertyName: 'access',
          },
          user: { url: 'users/me', propertyName: false },
          logout: false,
        },
        tokenType: 'Bearer',
        tokenName: 'Authorization',
      },
    },
  },
  router: {
    middleware: ['auth', 'authenticated'],
  },
  /*
   ** vuetify module configuration
   ** https://github.com/nuxt-community/vuetify-module
   */
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },
  /*
   ** Build configuration
   */
  build: {
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {},
  },
}
