<template>
  <v-dialog v-model="dialog" max-width="650" scrollable>
    <template v-slot:activator="{ on }">
      <v-btn v-on="on">Cambiar valores</v-btn>
    </template>

    <v-card class="pa-1">
      <v-card-text>
        <v-card flat class="d-flex align-center justify-space-between pa-1">
          <v-card flat class="d-flex" style="max-width: 50%">
            <img width="100%" src="/gg_logo_blue.png" />
          </v-card>

          <v-card flat class="d-flex flex-column" style="font-style: italic">
            <v-card flat style="text-align: right"> № {{ values.id }} </v-card>
            <v-card flat style="text-align: right"> Fecha de la propuesta: {{ values.date }} </v-card>
            <v-card flat style="text-align: right"> Periodo de validez: 7 Días </v-card>
          </v-card>
        </v-card>

        <hr />

        <br />

        <v-card flat class="d-flex justify-center text-h5 font-weight-bold">
          <v-card-title>PROPUESTA DE FACTURACIÓN</v-card-title>
        </v-card>
        <br />

        <div class="centered-list">
          <p>
            NOMBRE DEL CLIENTE: {{ values.client_name }}
            <edit-field @click="editValue('client_name', 'nombre del cliente')" />
          </p>
          <p>TARIFA: {{ values.tarif }}</p>
          <p>
            CUPS: {{ values.cups }}
            <edit-field @click="editValue('cups', 'CUPS')" />
          </p>
          <p>
            EMAIL DE CLIENTE: {{ values.client_email }}
            <edit-field @click="editValue('client_email', 'email de cliente')" />
          </p>
          <p>COMERCIALIZADORA: {{ values.company_name }}</p>
          <p>OFERTA: {{ values.name }}</p>
        </div>

        <v-card flat class="d-flex flex-column font-italic font-weight-black">
          <v-card flat> POTENCIA: </v-card>
        </v-card>

        <v-card flat class="d-flex flex-column offset font-weight-light caption">
          <v-card flat>
            <span class="first-word">P1:</span> {{ values.up1 }} kW/h × {{ values.period }} dias × {{ values.p1 }} € =
            {{ values.p1_subtotal }} €
            <edit-field @click="editValue('p1', 'Precio de potencia P1')" />
          </v-card>
          <v-card v-if="values.up2" flat>
            <span class="first-word">P2:</span> {{ values.up2 }} kW/h × {{ values.period }} dias × {{ values.p2 }} € =
            {{ values.p2_subtotal }} €
            <edit-field @click="editValue('p2', 'Precio de potencia P2')" />
          </v-card>
          <v-card v-if="values.up3" flat>
            <span class="first-word">P3:</span> {{ values.up3 }} kW/h × {{ values.period }} dias × {{ values.p3 }} € =
            {{ values.p3_subtotal }} €
            <edit-field @click="editValue('p3', 'Precio de potencia P3')" />
          </v-card>
          <v-card v-if="values.up4" flat>
            <span class="first-word">P4:</span> {{ values.up4 }} kW/h × {{ values.period }} dias × {{ values.p4 }} € =
            {{ values.p4_subtotal }} €
            <edit-field @click="editValue('p4', 'Precio de potencia P4')" />
          </v-card>
          <v-card v-if="values.up5" flat>
            <span class="first-word">P5:</span> {{ values.up5 }} kW/h × {{ values.period }} dias × {{ values.p5 }} € =
            {{ values.p5_subtotal }} €
            <edit-field @click="editValue('p5', 'Precio de potencia P5')" />
          </v-card>
          <v-card v-if="values.up6" flat>
            <span class="first-word">P6:</span> {{ values.up6 }} kW/h × {{ values.period }} dias × {{ values.p6 }} € =
            {{ values.p6_subtotal }} €
            <edit-field @click="editValue('p6', 'Precio de potencia P6')" />
          </v-card>
        </v-card>

        <br />

        <v-card flat class="d-flex flex-column font-italic font-weight-black">
          <v-card>CONSUMO:</v-card>
        </v-card>

        <v-card flat class="d-flex flex-column offset font-weight-light caption">
          <v-card v-if="values.uc1">
            <span class="first-word">P1: </span>{{ values.uc1 }} X {{ values.c1 }} (€/kWh) = {{ values.c1_subtotal }} €
            <edit-field @click="editValue('c1', 'Precio de consumo P1')" />
          </v-card>
          <v-card v-if="values.uc2" flat>
            <span class="first-word">P2: </span>{{ values.uc2 }} X {{ values.c2 }} (€/kWh) = {{ values.c2_subtotal }} €
            <edit-field @click="editValue('c2', 'Precio de consumo P2')" />
          </v-card>
          <v-card v-if="values.uc3" flat>
            <span class="first-word">P3: </span>{{ values.uc3 }} X {{ values.c3 }} (€/kWh) = {{ values.c3_subtotal }} €
            <edit-field @click="editValue('c3', 'Precio de consumo P3')" />
          </v-card>
          <v-card v-if="values.uc4" flat>
            <span class="first-word">P4: </span>{{ values.uc4 }} X {{ values.c4 }} (€/kWh) = {{ values.c4_subtotal }} €
            <edit-field @click="editValue('c4', 'Precio de consumo P4')" />
          </v-card>
          <v-card v-if="values.uc5" flat>
            <span class="first-word">P5: </span>{{ values.uc5 }} X {{ values.c5 }} (€/kWh) = {{ values.c5_subtotal }} €
            <edit-field @click="editValue('c5', 'Precio de consumo P5')" />
          </v-card>
          <v-card v-if="values.uc6" flat>
            <span class="first-word">P6: </span>{{ values.uc6 }} X {{ values.c6 }} (€/kWh) = {{ values.c6_subtotal }} €
            <edit-field @click="editValue('c6', 'Precio de consumo P6')" />
          </v-card>
        </v-card>

        <br />

        <v-card flat class="d-flex flex-column font-italic font-weight-black">
          <v-card>OTROS CONCEPTOS:</v-card>
        </v-card>

        <v-card flat class="d-flex flex-column offset">
          <v-card v-if="values.reactive">
            <span class="first-word">Energía reactiva:</span> {{ values.reactive }} €
          </v-card>
          <v-card flat>
            <span class="first-word">Alquiler de equipos:</span> {{ values.rental }} €
            <edit-field @click="editValue('rental', `Alquiler de equipos`)" />
          </v-card>
          <v-card flat>
            <span class="first-word">
              <span v-if="values.kind === 'luz'"> IMP. ELECTRICIDAD: </span>
              <span v-else>IMP. HIDROCARBUROS</span>
              <span> ({{ values.tax_percent }}%): </span>
            </span>
            {{ values.tax }} €
          </v-card>
          <v-card flat>
            <span v-if="values.kind === 'gas'">
              <span class="first-word"> IGIC ({{ values.igic_percent }}%): </span> {{ values.igic }} €
              <edit-field @click="editValue('igic_percent', `IGIC (%)`)" />
            </span>
            <span v-else>
              <span class="first-word"> IVA ({{ values.iva_percent }}%): </span> {{ values.iva }} €
              <edit-field @click="editValue('iva_percent', `IVA (%)`)" />
            </span>
          </v-card>
        </v-card>

        <br />

        <v-card flat class="d-flex flex-row">
          <v-card flat>
            <img height="60" src="/person.svg" />
          </v-card>
          <v-card flat class="d-flex flex-column" style="text-indent: 10px">
            <v-card flat>
              Nombre del asesor/a: {{ values.agent }}
              <edit-field v-if="$auth.user.role === 'admin'" @click="editValue('agent', `nombre del asesor/a`)" />
            </v-card>
            <v-card flat>
              Teléfono: {{ values.agent_phone }}
              <edit-field v-if="$auth.user.role === 'admin'" @click="editValue('agent_phone', `teléfono`)" />
            </v-card>
            <v-card flat>
              Email: {{ values.agent_email }}
              <edit-field v-if="$auth.user.role === 'admin'" @click="editValue('agent_email', `email`)" />
            </v-card>
            <v-card flat> Web: <a href="https://gestiongroup.es" target="_blank">gestiongroup.es</a> </v-card>
          </v-card>
        </v-card>
      </v-card-text>

      <v-card-actions>
        <v-btn block color="success" @click="dialog = false">Listo</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import EditField from '@/components/buttons/EditField'
export default {
  name: 'Propuesta',
  components: { EditField },
  props: {
    value: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      dialog: false,
      values: this.value,
    }
  },
  methods: {
    editValue(name, field) {
      const newValue = prompt(`Cambiar ${field} a...`)
      this.values = { ...this.values, [name]: newValue }
      this.$emit('update', { key: name, value: newValue })
    },
  },
}
</script>

<style>
#offer-app {
  padding: 1em;
}

.our-color {
  color: #004680;
}

.offset {
  text-indent: 6em;
}

.first-word {
  font-weight: bolder;
}

.border {
  border: 3px solid #004680;
  border-radius: 1cm;
  padding: 3px;
  text-align: center;
}

.centered-list {
  display: flex;
  flex-direction: column;
}

.centered-list > p {
  text-indent: 100px;
  line-height: 4px;
}
</style>
