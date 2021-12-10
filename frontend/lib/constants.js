const cleanEmpty = (obj) => {
  if (Array.isArray(obj)) {
    return obj.length
      ? obj.map((v) => (v && typeof v === 'object' ? cleanEmpty(v) : v)).filter((v) => !(v == null))
      : null
  } else {
    return Object.entries(obj)
      .map(([k, v]) => [k, v && typeof v === 'object' ? cleanEmpty(v) : v])
      .reduce((a, [k, v]) => (v == null ? a : ((a[k] = v), a)), {})
  }
}
const LEED = 'Leed'
const KO = 'KO'
const KO_PAPELLERA = 'KO (papellera)'
const PENDIENTE_TRAMITACION = 'Pendiente tramitación'
const TRAMITACION_EN_PROCESO = 'Tramitación en proceso'
const PENDIENTE_PAGO = 'Pendiente Pago'
const PAGADO = 'Pagado'

const DEBUG = process.env.NODE_ENV === 'development'

const CV_URL = DEBUG ? 'http://localhost:8000' : 'https://call-visit.gestiongroup.es'

const statuses = {
  LEED,
  KO_PAPELLERA,
  PENDIENTE_TRAMITACION,
  TRAMITACION_EN_PROCESO,
  PENDIENTE_PAGO,
  PAGADO,
  tramitacion: {
    KO,
    PENDIENTE_TRAMITACION,
    TRAMITACION_EN_PROCESO,
  },
  facturacion: {
    PENDIENTE_PAGO,
  },
  client: {
    PENDIENTE_PAGO,
    PAGADO,
  },
}

const userStatuses = [
  {
    text: 'Firmado',
    value: '0',
    color: 'success',
  },
  {
    text: 'Renovacion',
    value: '1',
    color: 'blue',
  },
  {
    text: 'Fidelizacion',
    value: '2',
    color: 'purple',
  },
  {
    text: 'No cliente',
    value: '3',
    color: 'error',
  },
  {
    text: 'Tramitacion',
    value: '4',
    color: 'orange',
  },
]
export default Object.freeze({
  DEBUG,
  CV_URL,
  userStatuses,
  statuses,
  cleanEmpty,
  userRoles: {
    admins: {
      text: 'Admins',
      value: 'admin',
    },
    agents: {
      text: 'Agentes',
      value: 'agent',
    },
    tramitacion: {
      text: 'Tramitacion',
      value: 'support',
    },
  },
  puntoFields: {
    client_type: {
      text: 'Tipo de cliente',
      value: 'client_type',
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
    is_name_changed: {
      type: 'switch',
      text: 'Cambio de nombre',
      value: 'is_name_changed',
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
    name: {
      text: 'Nuevo nombre',
      value: 'name',
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
    province: {
      text: 'Provincia',
      value: 'province',
      group: {
        text: 'Direccion',
        value: 'direccion',
      },
    },
    locality: {
      text: 'Localidad',
      value: 'locality',
      group: {
        text: 'Direccion',
        value: 'direccion',
      },
    },
    address: {
      text: 'Direccion',
      value: 'address',
      icon: 'mdi-map-marker',
      group: {
        text: 'Direccion',
        value: 'direccion',
      },
    },
    postalcode: {
      text: 'Codigo postal',
      value: 'postalcode',
      group: {
        text: 'Direccion',
        value: 'direccion',
      },
    },
    company_luz: {
      text: 'Comercializadora luz',
      value: 'company_luz',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    cups_luz: {
      text: 'CUPS luz',
      value: 'cups_luz',
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    tarif_luz: {
      text: 'Tarifa',
      value: 'tarif_luz',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    consumo_annual_luz: {
      text: 'Consumo anual luz',
      value: 'consumo_annual_luz',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    last_time_company_luz_changed: {
      text: 'Ultima cambio',
      value: 'last_time_company_luz_changed',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    p1: {
      text: 'P1',
      value: 'p1',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    p2: {
      text: 'P2',
      value: 'p2',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    p3: {
      text: 'P3',
      value: 'p3',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    p4: {
      text: 'P4',
      value: 'p4',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    p5: {
      text: 'P5',
      value: 'p5',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    p6: {
      text: 'P6',
      value: 'p6',
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    company_gas: {
      text: 'Comercializadora gas',
      value: 'company_gas',
      onlyAdmin: true,
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    cups_gas: {
      text: 'CUPS gas',
      value: 'cups_gas',
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    tarif_gas: {
      text: 'Tarifa',
      value: 'tarif_gas',
      onlyAdmin: true,
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    consumo_annual_gas: {
      text: 'Consumo anual gas',
      value: 'consumo_annual_gas',
      onlyAdmin: true,
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    last_time_company_gas_changed: {
      text: 'Ultima cambio gas',
      value: 'last_time_company_gas_changed',
      onlyAdmin: true,
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    legal_representative: {
      text: 'Representante legal',
      value: 'legal_representative',
      onlyAdmin: true,
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
    dni: {
      text: 'DNI',
      value: 'dni',
      onlyAdmin: true,
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
    cif: {
      text: 'CIF/DNI',
      value: 'cif',
      onlyAdmin: true,
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
    iban: {
      text: 'IBAN',
      value: 'iban',
      icon: 'mdi-bank',
      group: {
        text: 'Documentacion',
        value: 'doc',
      },
    },
  },
  onlyUnique: (value, index, self) => self.indexOf(value) === index,
  ourColor: '#004680',
  tarifs: ['2.0TD', '3.0TD', '6.1TD'],
  tarifsGas: ['3.1', '3.2', '3.3', '3.4'],
  showInput: (letter, number, tarif) => {
    if (!letter || !number || !tarif) return false
    letter = letter.toLowerCase()
    number = parseInt(number)
    tarif = tarif.toUpperCase()
    if (tarif === '2.0TD') return letter === 'p' ? [1, 2].includes(number) : [1, 2, 3].includes(number)
    return true
  },
  clientTypes: {
    0: 'Físico',
    1: 'Jurídico',
    2: 'Autónomo',
  },
  trans: {
    Attachment: 'Archivos',
  },
  cvStatuses: {
    MEETING: 'Reunion',
    RENEW: 'Renovaciones',
    RECALL: 'Volver a llamar',
    SUCCESS: 'Firmado',
    ACEPT: 'Proceso aceptacion',
    GESTIONES_DE_AGENTES: 'Gestiones de agentes',
    FIDELIZACION: 'Fidelizacion',
    RESCHEDULE_MEETING: 'Aplazada con fecha',
    PENDIENTE_FACTURA: 'Pendiente factura',
    FACTURA_RECIBIDA: 'Factura recibida',
    ESTUDIO_REALIZADO: 'Estudio realizado',
    ESTUDIO_ENVIADO: 'Estudio enviado',
    INVALID_NUMBER: 'Número inválido',
    NOT_RESPOND: 'El numero no responde',
    PERMANENT_BUSY: 'Permanentemente empleado',
    BAD_CONTACT: 'Mal contacto',
    OLDMAN: 'Persona major',
    NOT_LOCATED: 'No localizado',
    OPERATOR_FAIL: 'No le interesa',
    AGENT_FAIL: 'No firmado',
    PROCESSING: 'En proceso',
    OPEN: 'Pendiente',
  },
})
