<template>
  <v-container>
    <v-checkbox
      v-model="privacyAccepted"
      :success="privacyAccepted"
      :error="!privacyAccepted"
      :hint="privacyHint + ' política de privacidad.'"
      label="Estoy de acuerdo"
      persistent-hint
    >
      <template v-slot:message>
        <span>
          {{ privacyHint }}
        </span>
        <a target="_blank" href="https://gestiongroup.es/privacy_policy"> política de privacidad. </a>
      </template>
    </v-checkbox>
  </v-container>
</template>

<script>
export default {
  name: 'Privacy',
  data() {
    return {
      privacyHint:
        'Sus datos personales se utilizarán para simplificar su trabajo con el sitio, controlar el acceso a su cuenta y para otros fines descritos en nuestra',
    }
  },
  computed: {
    privacyAccepted: {
      set(val) {
        this.$store.commit('privacyAccepted', val)
      },
      get() {
        return this.$store.state.privacyAccepted
      },
    },
  },
}
</script>
