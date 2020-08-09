import colors from 'vuetify/es5/util/colors'
import es from 'vuetify/es5/locale/es'

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
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1',
      },
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
  // loading: { color: '#fff' },
  /*
   ** Global CSS
   */
  css: [],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: [
    { src: '~/plugins/vue-swal', mode: 'client' },
    { src: '~/plugins/vue-mask', mode: 'client' },
    { src: '~/plugins/vue-beautiful-chat', mode: 'client' },
  ],
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
    '@nuxtjs/auth-next',
    [
      '@nuxtjs/yandex-metrika',
      {
        id: '52936624',
        webvisor: true,
        clickmap: true,
        // useCDN:false,
        trackLinks: true,
        accurateTrackBounce: true,
      },
    ],
    '@nuxtjs/sentry',
  ],
  /*
   ** Axios module configuration
   ** See https://axios.nuxtjs.org/options
   */
  axios: {
    browserBaseURL: !DEV ? 'https://areaclientes.gestiongroup.es/api' : 'http://localhost:8000/api',
    proxy: true,
  },
  proxy: {
    '/api/': !DEV ? 'https://areaclientes.gestiongroup.es/' : 'http://localhost:8000/',
    '/media/': !DEV ? 'https://areaclientes.gestiongroup.es/' : 'http://localhost:8000/',
  },
  auth: {
    redirect: {
      logout: '/login',
    },
    resetOnError: true,
    cookie: false,
    fetchUserOnLogin: true,
    strategies: {
      local: {
        scheme: 'refresh',
        token: {
          property: 'access',
          maxAge: 60 * 5, // 5 minutes
        },
        refreshToken: {
          property: 'refresh',
          data: 'refresh',
          maxAge: 60 * 60 * 24, // 1 day
        },
        user: {
          property: false,
        },
        endpoints: {
          login: { url: 'users/login' },
          refresh: { url: 'users/refresh' },
          user: { url: 'users/me' },
          logout: false,
        },
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
    lang: {
      locales: { es },
      current: 'es',
    },
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: '#004680',
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent4,
        },
      },
    },
  },
  sentry: {
    dsn: 'https://320295fbbb5d437a83399c65dedc1163@o228899.ingest.sentry.io/1443546',
    disableServerSide: true,
    config: {
      clientIntegrations: {
        Vue: { attachProps: true }, //, logErrors: this.options.dev },
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
    extend(config, ctx) {
      // Run ESLint on save
      if (ctx.isDev && ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/,
        })
      }
    },
  },
}
