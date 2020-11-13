export default function ({ $auth, redirect, route }) {
  if (
    !$auth.loggedIn &&
    !route.name.includes('login') &&
    !route.name.includes('calc') &&
    !route.name.includes('pyme') &&
    !route.name.includes('hogar')
  ) {
    return redirect('/login')
  }
  if (route.name && route.name.startsWith('admin') && !['admin', 'support'].includes($auth.user.role)) {
    return redirect('/login')
  }
}
