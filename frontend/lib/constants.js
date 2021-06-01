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

const statuses = {
  LEED,
  KO,
  KO_PAPELLERA,
  PENDIENTE_TRAMITACION,
  TRAMITACION_EN_PROCESO,
  PENDIENTE_PAGO,
  PAGADO,
  tramitacion: {
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
export default Object.freeze({
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
    category: {
      text: 'Tipo de cliente',
      value: 'category',
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
    is_name_changed: {
      type: 'switch',
      text: 'Cambio de nombre',
      value: 'is_name_changed',
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
      onlyAdmin: true,
      group: {
        text: 'Luz',
        value: 'luz',
      },
    },
    tarif_luz: {
      text: 'Tarif luz',
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
      onlyAdmin: true,
      group: {
        text: 'Gas',
        value: 'gas',
      },
    },
    tarif_gas: {
      text: 'Tarif gas',
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
  tarifs: ['2.0A', '2.1A', '2.0DHA', '2.0DHS', '2.0TD', '2.1DHA', '2.1DHS', '3.0A', '3.0TD', '3.1A', '6.1TD'],
  tarifsGas: ['3.1', '3.2', '3.3', '3.4'],
  showInput: (letter, number, tarif) => {
    if (!letter || !number || !tarif) return false
    letter = letter.toLowerCase()
    number = parseInt(number)
    tarif = tarif.toUpperCase()
    return (
      number === 1 ||
      ['3.0A', '3.1A'].includes(tarif) ||
      (letter + number === 'c3' && ['2.1DHA', '2.0DHA'].includes(tarif)) ||
      (tarif.includes('S') && letter === 'c')
    )
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
    OLDMAN: 'Persona major',
    RECALL: 'Volver a llamar',
    NOT_RESPOND: 'El numero no responde',
    PROCESSING: 'En proceso',
    SUCCESS: 'Firmado',
    AGENT_FAIL: 'No firmado',
    OPERATOR_FAIL: 'No le interesa',
    NOT_LOCATED: 'No localizado',
    INVALID_NUMBER: 'Número inválido',
    OPEN: 'Pendiente',
    PERMANENT_BUSY: 'Permanentemente empleado',
    MEETING: 'Reunion',
    RESCHEDULE_MEETING: 'Aplazada con fecha',
    RENEW: 'Renovaciones',
    BAD_CONTACT: 'Mal contacto',
    ACEPT: 'Proceso aceptacion',
    FIDELIZACION: 'Fidelizacion',
  },
})
