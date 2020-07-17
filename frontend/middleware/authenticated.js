export default function ({ $auth, redirect, route }) {
  if (!$auth.loggedIn && route.name !== 'login') {
    return redirect('/login')
  }
  if (
    (route.name.startsWith('admin') || route.name.startsWith('support')) &&
    (!$auth.user.role !== 'admin' ||
      !$auth.user.permissions.includes('support'))
  ) {
    return redirect('/profile')
  }
}
