export default function ({ $auth, redirect, route }) {
  if (!$auth.loggedIn && route.name !== 'login') {
    return redirect('/login')
  }
  if (route.name && route.name.startsWith('admin') && $auth.user.role !== 'admin') {
    return redirect('/login')
  }
  if (route.name && route.name.startsWith('support')) {
    if (!['admin', 'support'].includes($auth.user.role)) {
      return redirect('/login')
    }
  }
}
