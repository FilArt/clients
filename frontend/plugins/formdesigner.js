const fb = {
  formId: 132177,
  text: 'Soporte',
  background: '#ff0000',
  color: '#ffffff',
  fontSize: '16px',
  borderRadius: 5,
  buttonSide: 'right',
  buttonAlign: 'center',
  popup: {
    hideCloseBtn: false,
    host: 'formdesigner.ru',
    overlay: {
      background: '#000000',
      opacity: 0.1,
    },
  },
}

global._FDFeedBack = fb
window._FDFeedBack = fb
document._FDFeedBack = fb

const fd = document.createElement('script')
fd.type = 'text/javascript'
fd.async = true
fd.src = (document.location.protocol === 'https:' ? 'https:' : 'http:') + '//formdesigner.ru/js/widgets/feedback.js'
const s = document.getElementsByTagName('script')[0]
s.parentNode.insertBefore(fd, s)
